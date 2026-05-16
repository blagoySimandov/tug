import { useState } from "react";
import { useLiveImportantMoments } from "~/api/hooks";
import { AutoSwitch } from "~/components/autoswitch";
import { ImportantMomentsBar } from "~/components/important-moments";
import { VideoLayout, type LayoutMode } from "~/components/video-layout";

const MODES: { label: string; value: LayoutMode }[] = [
  { label: "Full", value: "fullscreen" },
  { label: "Split", value: "split" },
  { label: "PiP", value: "pip" },
];

const PRIMARY_URL =
  "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342";
const SECONDARY_URL =
  "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8";

export default function Home() {
  const [mode, setMode] = useState<LayoutMode>("fullscreen");

  const { data, isPending, error } = useLiveImportantMoments("arg_fr", 0, 10);
  console.log(data, isPending, error);

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="flex items-center justify-between border-b border-border px-6 py-3">
        <span className="text-sm font-semibold tracking-wide text-primary">
          TUG
        </span>
        <div className="flex gap-1 items-center">
          <ImportantMomentsBar />
        </div>
        <div className="flex gap-1">
          <AutoSwitch />
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
        <VideoLayout
          mode={mode}
          primaryUrl={PRIMARY_URL}
          secondaryUrl={SECONDARY_URL}
        />
      </main>
    </div>
  );
}
