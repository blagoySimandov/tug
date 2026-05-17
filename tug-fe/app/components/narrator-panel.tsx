import { useEffect, useRef, useState } from "react";
import { useApi } from "~/api/context";
import { NARRATOR_VIBES, type NarratorStyle, type NarratorVibe, type NarratorVoice } from "~/api/types";

interface NarratorPanelProps {
  eventId: number;
  videoUrl: string;
  windowStart: number;
  windowEnd: number;
}

function DotsAnimation() {
  const [frame, setFrame] = useState(0);
  const frames = [". ", ".. ", "..."];

  useEffect(() => {
    const id = setInterval(() => setFrame((f) => (f + 1) % frames.length), 500);
    return () => clearInterval(id);
  }, []);

  return <span>Generating{frames[frame]}</span>;
}

export function NarratorPanel({ eventId, videoUrl, windowStart, windowEnd }: NarratorPanelProps) {
  const api = useApi();
  const voice: NarratorVoice = "Schedar";
  const [vibe, setVibe] = useState<NarratorVibe>("electrifying");
  const [customInstruction, setCustomInstruction] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const prevAudioUrl = useRef<string | null>(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    if (prevAudioUrl.current) {
      URL.revokeObjectURL(prevAudioUrl.current);
      prevAudioUrl.current = null;
    }
    setAudioUrl(null);

    const style: NarratorStyle = { voice, persona: vibe, custom_instruction: customInstruction };

    try {
      const blob = await api.generateNarrationAudio(eventId, videoUrl, style, windowStart, windowEnd);
      const url = URL.createObjectURL(blob);
      prevAudioUrl.current = url;
      setAudioUrl(url);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to generate narration");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="border-t border-primary-foreground/10 bg-primary/95 px-5 py-3">
      <div className="flex flex-wrap items-start gap-4">
        {/* Vibe */}
        <div className="flex flex-col gap-1">
          <span className="text-[10px] font-semibold uppercase tracking-widest text-primary-foreground/40">
            Vibe
          </span>
          <select
            value={vibe}
            onChange={(e) => setVibe(e.target.value as NarratorVibe)}
            className="rounded border border-primary-foreground/15 bg-primary-foreground/10 px-2 py-1 text-xs text-primary-foreground focus:outline-none"
          >
            {NARRATOR_VIBES.map(({ label, value }) => (
              <option key={value} value={value} className="bg-neutral-900">
                {label}
              </option>
            ))}
          </select>
        </div>

        {/* Custom instruction */}
        <div className="flex min-w-48 flex-1 flex-col gap-1">
          <span className="text-[10px] font-semibold uppercase tracking-widest text-primary-foreground/40">
            Custom instruction
          </span>
          <input
            type="text"
            value={customInstruction}
            onChange={(e) => setCustomInstruction(e.target.value)}
            placeholder="e.g. focus more on Bayern pressing style"
            className="w-full rounded border border-primary-foreground/15 bg-primary-foreground/10 px-2 py-1 text-xs text-primary-foreground placeholder:text-primary-foreground/30 focus:outline-none"
          />
        </div>

        {/* Generate */}
        <div className="flex flex-col gap-1">
          <span className="text-[10px] font-semibold uppercase tracking-widest text-primary-foreground/40">
            &nbsp;
          </span>
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="rounded bg-accent px-3 py-1 text-xs font-semibold text-accent-foreground transition-opacity disabled:opacity-50"
          >
            {loading ? <DotsAnimation /> : "Generate"}
          </button>
        </div>
      </div>

      {error && <p className="mt-2 text-xs text-red-400">{error}</p>}

      {audioUrl && (
        <audio
          key={audioUrl}
          controls
          src={audioUrl}
          autoPlay
          className="mt-2 h-8 w-full"
        />
      )}
    </div>
  );
}
