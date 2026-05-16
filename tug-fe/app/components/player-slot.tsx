import ReactPlayer from "react-player";

interface PlayerSlotProps {
  url: string;
  className?: string;
  playing?: boolean;
  onPlay?: () => void;
  onPause?: () => void;
}

export function PlayerSlot({
  url,
  className = "",
  playing = false,
  onPlay,
  onPause,
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
      />
    </div>
  );
}
