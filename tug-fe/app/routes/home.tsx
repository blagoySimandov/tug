import { AutoSwitch } from "~/components/autoswitch";
import { ImportantMomentsBar } from "~/components/important-moments";
import { VideoLayout, type LayoutMode } from "~/components/video-layout";
import { useVideoStore } from "~/store/video";

const MODES: { label: string; value: LayoutMode }[] = [
  { label: "Split", value: "split" },
  { label: "PiP", value: "pip" },
];

const PRIMARY_URL =
  "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342";
const SECONDARY_URL =
  "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8";

export default function Home() {
  const mode = useVideoStore((s) => s.manualLayoutMode);
  const setMode = useVideoStore((s) => s.setManualLayoutMode);

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="flex h-11 items-center gap-4 bg-primary px-5">
        <span className="text-sm font-black tracking-tight text-accent">TUG</span>
        <div className="h-5 w-px bg-primary-foreground/15" />
        <div className="flex flex-1 justify-center">
          <ImportantMomentsBar />
        </div>
        <AutoSwitch />
        <div className="h-5 w-px bg-primary-foreground/15" />
        <div className="flex overflow-hidden rounded border border-primary-foreground/15">
          {MODES.map(({ label, value }) => (
            <button
              key={value}
              onClick={() => setMode(value)}
              className={`px-3 py-1 text-xs font-medium transition-colors ${
                mode === value
                  ? "bg-accent text-accent-foreground"
                  : "text-primary-foreground/55 hover:bg-primary-foreground/10 hover:text-primary-foreground"
              }`}
            >
              {label}
            </button>
          ))}
        </div>
      </header>

      <main className="flex-1 overflow-hidden p-2">
        <VideoLayout
          primaryUrl={PRIMARY_URL}
          secondaryUrl={SECONDARY_URL}
        />
      </main>
    </div>
  );
}
