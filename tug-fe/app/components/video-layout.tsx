import { PlayerSlot } from "./player-slot"

export type LayoutMode = "fullscreen" | "split" | "pip"

interface VideoLayoutProps {
  mode: LayoutMode
  primaryUrl: string
  secondaryUrl: string
}

function FullscreenLayout({ primaryUrl }: { primaryUrl: string }) {
  return <PlayerSlot url={primaryUrl} className="h-full w-full" />
}

function SplitLayout({ primaryUrl, secondaryUrl }: { primaryUrl: string; secondaryUrl: string }) {
  return (
    <div className="grid h-full w-full grid-cols-2 gap-2">
      <PlayerSlot url={primaryUrl} className="h-full" />
      <PlayerSlot url={secondaryUrl} className="h-full" />
    </div>
  )
}

function PipLayout({ primaryUrl, secondaryUrl }: { primaryUrl: string; secondaryUrl: string }) {
  return (
    <div className="relative h-full w-full">
      <PlayerSlot url={primaryUrl} className="h-full w-full" />
      <div className="absolute bottom-4 right-4 w-64 shadow-xl ring-1 ring-border">
        <PlayerSlot url={secondaryUrl} className="aspect-video w-full rounded-md" />
      </div>
    </div>
  )
}

export function VideoLayout({ mode, primaryUrl, secondaryUrl }: VideoLayoutProps) {
  if (mode === "split") return <SplitLayout primaryUrl={primaryUrl} secondaryUrl={secondaryUrl} />
  if (mode === "pip") return <PipLayout primaryUrl={primaryUrl} secondaryUrl={secondaryUrl} />
  return <FullscreenLayout primaryUrl={primaryUrl} />
}
