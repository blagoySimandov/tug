#!/usr/bin/env python3
"""
Soccer action detection pipeline for TUG AI narrator.

Extracts ResNet-152 features from an MP4, then processes them in sliding
120s windows (60s stride) using the CALF model. Detected events are emitted
as NDJSON to stdout immediately after each window, and saved to
narrator_events.json at the end.

Usage:
    python analyze.py --video /path/to/match.mp4 --output ./output
"""

import os
import sys
import json
import argparse

import numpy as np
import torch

# Absolute path to the CALF model root inside the SoccerNetv2-DevKit clone.
# All DevKit relative paths (PCA files, model weights) are anchored here.
CALF_ROOT = "/Users/merti/Desktop/SoccerNetv2-DevKit/Task1-ActionSpotting/CALF"

def get_device(override: str = None) -> torch.device:
    """Auto-detect best available device, or use override if provided."""
    if override:
        return torch.device(override)
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")

# Inlined from inference/config/classes.py to avoid that file calling .cuda()
# at import time (which crashes on non-CUDA machines).
INVERSE_EVENT_DICTIONARY_V2 = {
    0: "Penalty", 1: "Kick-off", 2: "Goal", 3: "Substitution",
    4: "Offside", 5: "Shots on target", 6: "Shots off target",
    7: "Clearance", 8: "Ball out of play", 9: "Throw-in", 10: "Foul",
    11: "Indirect free-kick", 12: "Direct free-kick", 13: "Corner",
    14: "Yellow card", 15: "Red card", 16: "Yellow->red card",
}

# Feature framerate used by the pre-trained model (2 frames per second).
FRAMERATE = 2

# The model architecture is fixed to chunk_size=240 frames (120s at 2FPS).
# Changing this would break the trained weights (conv_conf in_channels depends on it).
MODEL_CHUNK = 240

# Temporal receptive field of the CALF model in frames (40s at 2FPS).
MODEL_RF = 80

# Stride between consecutive windows in frames.
# 120 frames = 60s — new events emitted every minute of video.
STRIDE = 120

# Human-readable description template per event class.
DESCRIPTIONS = {
    "Penalty":            "Penalty awarded at {time}",
    "Kick-off":           "Kick-off at {time}",
    "Goal":               "Goal scored at {time}",
    "Substitution":       "Substitution made at {time}",
    "Offside":            "Offside call at {time}",
    "Shots on target":    "Shot on target at {time}",
    "Shots off target":   "Shot off target at {time}",
    "Clearance":          "Clearance at {time}",
    "Ball out of play":   "Ball out of play at {time}",
    "Throw-in":           "Throw-in at {time}",
    "Foul":               "Foul committed at {time}",
    "Indirect free-kick": "Indirect free kick at {time}",
    "Direct free-kick":   "Direct free kick at {time}",
    "Corner":             "Corner kick at {time}",
    "Yellow card":        "Yellow card shown at {time}",
    "Red card":           "Red card shown at {time}",
    "Yellow->red card":   "Second yellow, red card shown at {time}",
}


def fmt_time(ms: int) -> str:
    s = ms // 1000
    return f"{s // 60}:{s % 60:02d}"


def extract_features(video_path: str, output_dir: str) -> np.ndarray:
    """
    Run ResNet-152 feature extraction + PCA on the full video.
    Returns a float32 array of shape (N, 512).
    CWD must be CALF_ROOT and inference/ must be on sys.path before calling.
    """
    from Features.VideoFeatureExtractor import VideoFeatureExtractor, PCAReducer

    raw_path = os.path.join(output_dir, "features_raw.npy")
    pca_path = os.path.join(output_dir, "features_pca.npy")

    print("[1/4] Extracting ResNet-152 features (2 FPS)...", flush=True)
    extractor = VideoFeatureExtractor(
        feature="ResNET",
        back_end="TF2",
        transform="crop",
        grabber="opencv",
        FPS=FRAMERATE,
    )
    extractor.extractFeatures(
        path_video_input=video_path,
        path_features_output=raw_path,
        overwrite=True,
    )

    print("[2/4] Applying PCA reduction to 512D...", flush=True)
    reducer = PCAReducer(
        pca_file="inference/Features/pca_512_TF2.pkl",
        scaler_file="inference/Features/average_512_TF2.pkl",
    )
    reducer.reduceFeatures(
        input_features=raw_path,
        output_features=pca_path,
        overwrite=True,
    )

    return np.load(pca_path).astype(np.float32)


def load_model(device: torch.device) -> torch.nn.Module:
    """
    Load the pre-trained CALF model from models/CALF_benchmark/model.pth.tar.
    CWD must be CALF_ROOT and inference/ must be on sys.path before calling.
    """
    from model import ContextAwareModel

    print(f"[3/4] Loading CALF model weights on {device}...", flush=True)
    model = ContextAwareModel(
        input_size=512,
        num_classes=17,
        chunk_size=MODEL_CHUNK,
        dim_capsule=16,
        receptive_field=MODEL_RF,
        num_detections=15,
        framerate=FRAMERATE,
    ).to(device)

    ckpt = torch.load("models/CALF_benchmark/model.pth.tar", map_location=device)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()
    return model


def run_window(
    model: torch.nn.Module,
    window: np.ndarray,
    win_start_frame: int,
    confidence_threshold: float,
    label_map: dict,
    first_window: bool,
    device: torch.device,
) -> list:
    """
    Run model inference on a single 240-frame window.
    Returns sorted list of event dicts for the non-overlapping portion.

    To avoid emitting duplicate events from overlapping windows, only the
    second half (rel_pos >= 0.5) is reported after the first window.
    The first window reports all events since there is no prior overlap.
    """
    feat = torch.from_numpy(window).float().unsqueeze(0).unsqueeze(0).to(device)

    with torch.no_grad():
        _, output_spotting = model(feat)  # (1, num_detections, 2+num_classes)

    spots = output_spotting.cpu().numpy()[0]  # (15, 19)
    events = []

    for i in range(spots.shape[0]):
        conf = float(spots[i, 0])
        if conf < confidence_threshold:
            continue

        rel_pos = float(spots[i, 1])

        # Skip the overlap portion (first half) on all windows except the first,
        # so each event is only streamed once.
        if not first_window and rel_pos < 0.5:
            continue

        class_idx = int(np.argmax(spots[i, 2:]))
        label = label_map[class_idx]

        abs_frame = win_start_frame + rel_pos * (MODEL_CHUNK - 1)
        timestamp_ms = int(abs_frame / FRAMERATE * 1000)

        time_str = fmt_time(timestamp_ms)
        desc = DESCRIPTIONS.get(label, f"{label} at {time_str}").format(time=time_str)

        events.append({
            "timestamp_ms": timestamp_ms,
            "label": label,
            "confidence": round(conf, 4),
            "description": desc,
        })

    return sorted(events, key=lambda e: e["timestamp_ms"])


def dedup(events: list, window_ms: int = 2000) -> list:
    """
    Remove duplicate events: same label within window_ms of each other.
    Keeps the detection with the highest confidence score.
    """
    seen = []
    for ev in sorted(events, key=lambda e: e["timestamp_ms"]):
        matched = False
        for prev in seen:
            if (
                prev["label"] == ev["label"]
                and abs(prev["timestamp_ms"] - ev["timestamp_ms"]) <= window_ms
            ):
                if ev["confidence"] > prev["confidence"]:
                    prev.update(ev)
                matched = True
                break
        if not matched:
            seen.append(dict(ev))
    return seen


def main():
    parser = argparse.ArgumentParser(
        description="Soccer AI event detector for TUG narrator"
    )
    parser.add_argument("--video", required=True, help="Path to input MP4 video")
    parser.add_argument("--output", default="./output", help="Output directory")
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.3,
        help="Minimum confidence threshold 0-1 (default: 0.3)",
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="Force device: cuda, mps, or cpu (default: auto-detect)",
    )
    args = parser.parse_args()

    # Resolve paths to absolute BEFORE os.chdir changes the working directory.
    video_path = os.path.abspath(args.video)
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    # Change CWD to CALF_ROOT so all DevKit relative paths work:
    #   inference/Features/pca_512_TF2.pkl
    #   models/CALF_benchmark/model.pth.tar
    device = get_device(args.device)

    os.chdir(CALF_ROOT)
    sys.path.insert(0, os.path.join(CALF_ROOT, "inference"))

    print(f"Device: {device}", flush=True)

    # Phase 1 & 2: feature extraction
    features = extract_features(video_path, output_dir)
    total_frames = features.shape[0]
    duration_s = total_frames / FRAMERATE
    print(
        f"Video: {total_frames} frames @ {FRAMERATE} FPS = {duration_s:.0f}s "
        f"({duration_s / 60:.1f} min)",
        flush=True,
    )

    # Pad to guarantee at least one full model window.
    if total_frames < MODEL_CHUNK:
        pad_len = MODEL_CHUNK - total_frames
        features = np.concatenate(
            [features, np.zeros((pad_len, 512), dtype=np.float32)]
        )

    # Phase 3: load model
    model = load_model(device)

    # Phase 4: streaming sliding window inference
    win_starts = list(range(0, total_frames, STRIDE))
    print(
        f"\n[4/4] Processing {len(win_starts)} windows "
        f"({MODEL_CHUNK / FRAMERATE:.0f}s window, {STRIDE / FRAMERATE:.0f}s stride)...\n",
        flush=True,
    )

    all_events = []

    for idx, win_start in enumerate(win_starts):
        window = features[win_start: win_start + MODEL_CHUNK]

        # Pad final window if shorter than MODEL_CHUNK.
        if window.shape[0] < MODEL_CHUNK:
            pad_len = MODEL_CHUNK - window.shape[0]
            window = np.concatenate(
                [window, np.zeros((pad_len, 512), dtype=np.float32)]
            )

        chunk_events = run_window(
            model,
            window,
            win_start_frame=win_start,
            confidence_threshold=args.confidence,
            label_map=INVERSE_EVENT_DICTIONARY_V2,
            first_window=(idx == 0),
            device=device,
        )

        for ev in chunk_events:
            print(json.dumps(ev), flush=True)

        all_events.extend(chunk_events)

    # Phase 5: deduplicate and write final narrator JSON
    final = dedup(all_events)
    final.sort(key=lambda e: e["timestamp_ms"])

    out_path = os.path.join(output_dir, "narrator_events.json")
    with open(out_path, "w") as f:
        json.dump(final, f, indent=2)

    print(f"\nDone. {len(final)} unique events saved to {out_path}", flush=True)


if __name__ == "__main__":
    main()
