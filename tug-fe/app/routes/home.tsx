import { useState } from "react"
import { VideoLayout, type LayoutMode } from "~/components/video-layout"

const MODES: { label: string; value: LayoutMode }[] = [
  { label: "Full", value: "fullscreen" },
  { label: "Split", value: "split" },
  { label: "PiP", value: "pip" },
]

const PRIMARY_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
const SECONDARY_URL = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"

export default function Home() {
  const [mode, setMode] = useState<LayoutMode>("fullscreen")

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="flex items-center justify-between border-b border-border px-6 py-3">
        <span className="text-sm font-semibold tracking-wide text-primary">TUG</span>
        <div className="flex gap-1">
          {MODES.map(({ label, value }) => (
            <button
              key={value}
              onClick={() => setMode(value)}
              className={`rounded px-3 py-1 text-xs font-medium transition-colors ${
                mode === value
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </header>

      <main className="flex-1 overflow-hidden p-4">
        <VideoLayout mode={mode} primaryUrl={PRIMARY_URL} secondaryUrl={SECONDARY_URL} />
      </main>
    </div>
  )
}
