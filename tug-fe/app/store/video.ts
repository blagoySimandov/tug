import { create } from "zustand";

export type LayoutMode = "split" | "pip";

interface VideoState {
  primaryVideoId: string;
  secondaryVideoId: string;
  primaryPlaying: boolean;
  secondaryPlaying: boolean;
  primaryTimestamp: number;
  secondaryTimestamp: number;
  autoswitchEnabled: boolean;
  manualLayoutMode: LayoutMode;
  primaryPriorityUntil: number;
  secondaryPriorityUntil: number;
  flashingVideoId: string | null;
  flashCount: number;
}

interface VideoActions {
  setPrimaryVideoId: (id: string) => void;
  setSecondaryVideoId: (id: string) => void;
  setPrimaryPlaying: (playing: boolean) => void;
  setSecondaryPlaying: (playing: boolean) => void;
  setPrimaryTimestamp: (timestamp: number) => void;
  setSecondaryTimestamp: (timestamp: number) => void;
  setAutoswitchEnabled: (enabled: boolean) => void;
  setManualLayoutMode: (mode: LayoutMode) => void;
  setPriorityUntil: (videoId: string, until: number) => void;
  clearPriority: (videoId: string) => void;
  setFlashingVideoId: (id: string | null) => void;
}

export const useVideoStore = create<VideoState & VideoActions>((set) => ({
  primaryVideoId: "arg_fr",
  secondaryVideoId: "cr_bra",
  primaryPlaying: false,
  secondaryPlaying: false,
  primaryTimestamp: 0,
  secondaryTimestamp: 0,
  autoswitchEnabled: true,
  manualLayoutMode: "split" as LayoutMode,
  primaryPriorityUntil: 0,
  secondaryPriorityUntil: 0,
  flashingVideoId: null,
  flashCount: 0,

  setPrimaryVideoId: (id) => set({ primaryVideoId: id }),
  setSecondaryVideoId: (id) => set({ secondaryVideoId: id }),
  setPrimaryPlaying: (playing) => set({ primaryPlaying: playing }),
  setSecondaryPlaying: (playing) => set({ secondaryPlaying: playing }),
  setPrimaryTimestamp: (timestamp) => set({ primaryTimestamp: timestamp }),
  setSecondaryTimestamp: (timestamp) => set({ secondaryTimestamp: timestamp }),
  setAutoswitchEnabled: (enabled) => set({ autoswitchEnabled: enabled }),
  setManualLayoutMode: (mode) => set({ manualLayoutMode: mode }),
  setPriorityUntil: (videoId, until) =>
    set((s) => ({
      primaryPriorityUntil: videoId === s.primaryVideoId ? until : s.primaryPriorityUntil,
      secondaryPriorityUntil: videoId === s.secondaryVideoId ? until : s.secondaryPriorityUntil,
    })),
  clearPriority: (videoId) =>
    set((s) => ({
      primaryPriorityUntil: videoId === s.primaryVideoId ? 0 : s.primaryPriorityUntil,
      secondaryPriorityUntil: videoId === s.secondaryVideoId ? 0 : s.secondaryPriorityUntil,
    })),
  setFlashingVideoId: (id) =>
    set((s) => ({
      flashingVideoId: id,
      flashCount: id !== null ? s.flashCount + 1 : s.flashCount,
    })),
}));
