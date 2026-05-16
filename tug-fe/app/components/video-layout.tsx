import { useCallback } from "react";
import { useVideoStore, type LayoutMode } from "~/store/video";
import { PlayerSlot } from "./player-slot";

export type { LayoutMode };

interface VideoLayoutProps {
  primaryUrl: string;
  secondaryUrl?: string;
}

const primaryClasses: Record<LayoutMode, string> = {
  split: "absolute inset-y-0 left-0 right-[calc(50%+1px)]",
  pip: "absolute inset-0",
};

const secondaryClasses: Record<LayoutMode, string> = {
  split: "absolute inset-y-0 left-[calc(50%+1px)] right-0",
  pip: "absolute bottom-4 right-4 z-10 w-64 aspect-video shadow-xl ring-1 ring-border rounded-lg overflow-hidden",
};

function FlashOverlay() {
  return <div className="pointer-events-none absolute inset-0 rounded-lg flash-ring" />;
}

function computeLayout(
  primaryPriorityUntil: number,
  secondaryPriorityUntil: number,
  manualLayoutMode: LayoutMode,
): { mode: LayoutMode; isSwapped: boolean } {
  const now = Date.now();
  const primaryActive = primaryPriorityUntil > now;
  const secondaryActive = secondaryPriorityUntil > now;

  if (primaryActive && secondaryActive) return { mode: "split", isSwapped: false };
  if (secondaryActive) return { mode: "pip", isSwapped: true };
  if (primaryActive) return { mode: "pip", isSwapped: false };
  return { mode: manualLayoutMode, isSwapped: false };
}

function DualVideoLayout({ primaryUrl, secondaryUrl }: { primaryUrl: string; secondaryUrl: string }) {
  const primaryVideoId = useVideoStore((s) => s.primaryVideoId);
  const secondaryVideoId = useVideoStore((s) => s.secondaryVideoId);
  const setPrimaryTimestamp = useVideoStore((s) => s.setPrimaryTimestamp);
  const setSecondaryTimestamp = useVideoStore((s) => s.setSecondaryTimestamp);
  const flashingVideoId = useVideoStore((s) => s.flashingVideoId);
  const flashCount = useVideoStore((s) => s.flashCount);
  const primaryPriorityUntil = useVideoStore((s) => s.primaryPriorityUntil);
  const secondaryPriorityUntil = useVideoStore((s) => s.secondaryPriorityUntil);
  const manualLayoutMode = useVideoStore((s) => s.manualLayoutMode);
  const setPrimarySeeker = useVideoStore((s) => s.setPrimarySeeker);
  const setSecondarySeeker = useVideoStore((s) => s.setSecondarySeeker);

  const primaryRef = useCallback((el: HTMLVideoElement | null) => {
    if (el) setPrimarySeeker((s) => { el.currentTime = s; el.play(); });
  }, [setPrimarySeeker]);

  const secondaryRef = useCallback((el: HTMLVideoElement | null) => {
    if (el) setSecondarySeeker((s) => { el.currentTime = s; el.play(); });
  }, [setSecondarySeeker]);

  const { mode, isSwapped } = computeLayout(primaryPriorityUntil, secondaryPriorityUntil, manualLayoutMode);
  const transition = "transition-all duration-500 ease-in-out";
  const primaryZ = flashingVideoId === primaryVideoId ? "z-10" : "z-0";
  const secondaryZ = flashingVideoId === secondaryVideoId ? "z-10" : "z-0";
  const primaryContainerClass = `${isSwapped ? secondaryClasses[mode] : primaryClasses[mode]} ${transition} ${primaryZ}`;
  const secondaryContainerClass = `${isSwapped ? primaryClasses[mode] : secondaryClasses[mode]} ${transition} ${secondaryZ}`;

  function handlePrimaryProgress(seconds: number) {
    setPrimaryTimestamp(seconds);
    if (Math.floor(seconds) % 5 === 0) {
      console.log("[store] primaryTimestamp", seconds.toFixed(2));
    }
  }

  return (
    <div className="relative h-full w-full">
      <div className={primaryContainerClass}>
        <PlayerSlot
          ref={primaryRef}
          url={primaryUrl}
          className="h-full w-full"
          onProgress={handlePrimaryProgress}
        />
        {flashingVideoId === primaryVideoId && <FlashOverlay key={flashCount} />}
      </div>
      <div className={secondaryContainerClass}>
        <PlayerSlot
          ref={secondaryRef}
          url={secondaryUrl}
          className="h-full w-full"
          onProgress={setSecondaryTimestamp}
        />
        {flashingVideoId === secondaryVideoId && <FlashOverlay key={flashCount} />}
      </div>
    </div>
  );
}

export function VideoLayout({ primaryUrl, secondaryUrl }: VideoLayoutProps) {
  if (!secondaryUrl) {
    return (
      <div className="relative h-full w-full">
        <PlayerSlot url={primaryUrl} className="h-full w-full" />
      </div>
    );
  }
  return <DualVideoLayout primaryUrl={primaryUrl} secondaryUrl={secondaryUrl} />;
}
