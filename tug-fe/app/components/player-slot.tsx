import { forwardRef } from "react";
import ReactPlayer from "react-player";

interface PlayerSlotProps {
  url: string;
  className?: string;
  onProgress?: (seconds: number) => void;
}

export const PlayerSlot = forwardRef<HTMLVideoElement, PlayerSlotProps>(function PlayerSlot(
  { url, className = "", onProgress },
  ref,
) {
  return (
    <div className={`overflow-hidden rounded-lg bg-card ${className}`}>
      <ReactPlayer
        ref={ref}
        src={url}
        width="100%"
        height="100%"
        controls
        onTimeUpdate={(e) => onProgress?.(e.currentTarget.currentTime)}
      />
    </div>
  );
});
