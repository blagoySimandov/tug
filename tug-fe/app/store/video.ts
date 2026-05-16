import { create } from "zustand";

type ActivePlayer = "primary" | "secondary";

interface VideoState {
  primaryPlaying: boolean;
  secondaryPlaying: boolean;
  currentTimestamp: number;
  autoswitchEnabled: boolean;
  activePlayer: ActivePlayer;
}

interface VideoActions {
  setPrimaryPlaying: (playing: boolean) => void;
  setSecondaryPlaying: (playing: boolean) => void;
  setCurrentTimestamp: (timestamp: number) => void;
  setAutoswitchEnabled: (enabled: boolean) => void;
  setActivePlayer: (player: ActivePlayer) => void;
}

export const useVideoStore = create<VideoState & VideoActions>((set) => ({
  primaryPlaying: false,
  secondaryPlaying: false,
  currentTimestamp: 0,
  autoswitchEnabled: false,
  activePlayer: "primary",

  setPrimaryPlaying: (playing) => set({ primaryPlaying: playing }),
  setSecondaryPlaying: (playing) => set({ secondaryPlaying: playing }),
  setCurrentTimestamp: (timestamp) => set({ currentTimestamp: timestamp }),
  setAutoswitchEnabled: (enabled) => set({ autoswitchEnabled: enabled }),
  setActivePlayer: (player) => set({ activePlayer: player }),
}));
