import { useVideoStore } from "~/store/video";
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
  const primaryPlaying = useVideoStore((s) => s.primaryPlaying);
  const secondaryPlaying = useVideoStore((s) => s.secondaryPlaying);
  const setPrimaryPlaying = useVideoStore((s) => s.setPrimaryPlaying);
  const setSecondaryPlaying = useVideoStore((s) => s.setSecondaryPlaying);
  const setCurrentTimestamp = useVideoStore((s) => s.setCurrentTimestamp);

  function handleProgress(seconds: number) {
    setCurrentTimestamp(seconds);
    if (Math.floor(seconds) % 5 === 0) {
      console.log("[store] currentTimestamp", seconds.toFixed(2));
    }
  }

  return (
    <div className="relative h-full w-full">
      <div className={primaryClasses[mode]}>
        <PlayerSlot
          url={primaryUrl}
          className="h-full w-full"
          playing={primaryPlaying}
          onPlay={() => setPrimaryPlaying(true)}
          onPause={() => setPrimaryPlaying(false)}
          onProgress={handleProgress}
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
