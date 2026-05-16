import ReactPlayer from "react-player";

interface PlayerSlotProps {
  url: string;
  className?: string;
  playing?: boolean;
  onPlay?: () => void;
  onPause?: () => void;
  onProgress?: (seconds: number) => void;
}

export function PlayerSlot({
  url,
  className = "",
  playing = false,
  onPlay,
  onPause,
  onProgress,
}: PlayerSlotProps) {
  return (
    <div className={`overflow-hidden rounded-lg bg-foreground ${className}`}>
      <ReactPlayer
        src={url}
        width="100%"
        height="100%"
        controls
        playing={playing}
        onPlay={onPlay}
        onPause={onPause}
        onTimeUpdate={(e) => onProgress?.(e.currentTarget.currentTime)}
      />
    </div>
  );
}
