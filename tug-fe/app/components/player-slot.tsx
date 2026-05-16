import ReactPlayer from "react-player"

interface PlayerSlotProps {
  url: string
  className?: string
}

export function PlayerSlot({ url, className = "" }: PlayerSlotProps) {
  return (
    <div className={`overflow-hidden rounded-lg bg-foreground ${className}`}>
      <ReactPlayer
        url={url}
        width="100%"
        height="100%"
        controls
        playing={false}
      />
    </div>
  )
}
