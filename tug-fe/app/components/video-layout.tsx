import { useState } from "react";
import { PlayerSlot } from "./player-slot";

export type LayoutMode = "fullscreen" | "split" | "pip";

interface VideoLayoutProps {
  mode: LayoutMode;
  primaryUrl: string;
  secondaryUrl: string;
}

const primaryClasses: Record<LayoutMode, string> = {
  fullscreen: "absolute inset-0",
  split: "absolute inset-y-0 left-0 right-[calc(50%+4px)]",
  pip: "absolute inset-0",
};

const secondaryClasses: Record<LayoutMode, string> = {
  fullscreen: "absolute w-0 h-0 overflow-hidden opacity-0 pointer-events-none",
  split: "absolute inset-y-0 left-[calc(50%+4px)] right-0",
  pip: "absolute bottom-4 right-4 z-10 w-64 aspect-video shadow-xl ring-1 ring-border rounded-lg overflow-hidden",
};

export function VideoLayout({
  mode,
  primaryUrl,
  secondaryUrl,
}: VideoLayoutProps) {
  const [primaryPlaying, setPrimaryPlaying] = useState(false);
  const [secondaryPlaying, setSecondaryPlaying] = useState(false);

  return (
    <div className="relative h-full w-full">
      <div className={primaryClasses[mode]}>
        <PlayerSlot
          url={primaryUrl}
          className="h-full w-full"
          playing={primaryPlaying}
          onPlay={() => setPrimaryPlaying(true)}
          onPause={() => setPrimaryPlaying(false)}
        />
      </div>
      <div className={secondaryClasses[mode]}>
        <PlayerSlot
          url={secondaryUrl}
          className="h-full w-full"
          playing={secondaryPlaying}
          onPlay={() => setSecondaryPlaying(true)}
          onPause={() => setSecondaryPlaying(false)}
        />
      </div>
    </div>
  );
}
