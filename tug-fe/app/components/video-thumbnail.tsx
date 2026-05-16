import { useRef } from "react";

interface VideoThumbnailProps {
  url: string;
  seekTime?: number;
  className?: string;
}

export function VideoThumbnail({ url, seekTime = 8, className = "" }: VideoThumbnailProps) {
  const ref = useRef<HTMLVideoElement>(null);

  function handleLoadedMetadata() {
    if (ref.current) ref.current.currentTime = seekTime;
  }

  return (
    <video
      ref={ref}
      src={url}
      className={`object-cover ${className}`}
      preload="metadata"
      muted
      playsInline
      onLoadedMetadata={handleLoadedMetadata}
    />
  );
}
