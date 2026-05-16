import { useSearchParams } from "react-router";
import { useMatches } from "~/api/hooks";
import { AutoSwitch } from "~/components/autoswitch";
import { ImportantMomentsBar } from "~/components/important-moments";
import { VideoLayout, type LayoutMode } from "~/components/video-layout";
import { useVideoStore } from "~/store/video";

const MODES: { label: string; value: LayoutMode }[] = [
  { label: "Split", value: "split" },
  { label: "PiP", value: "pip" },
];

export default function Player() {
  const [searchParams] = useSearchParams();
  const mode = useVideoStore((s) => s.manualLayoutMode);
  const setMode = useVideoStore((s) => s.setManualLayoutMode);
  const { data: matches = [], isLoading } = useMatches();

  const primaryId = searchParams.get("primary") ?? "";
  const secondaryId = searchParams.get("secondary") ?? "";
  const primaryMatch = matches.find((m) => m.id === primaryId);
  const secondaryMatch = matches.find((m) => m.id === secondaryId);

  const storePrimaryId = useVideoStore((s) => s.primaryVideoId);
  const storeSecondaryId = useVideoStore((s) => s.secondaryVideoId);
  const setPrimaryVideoId = useVideoStore((s) => s.setPrimaryVideoId);
  const setSecondaryVideoId = useVideoStore((s) => s.setSecondaryVideoId);
  if (primaryId && storePrimaryId !== primaryId) setPrimaryVideoId(primaryId);
  if (secondaryId && storeSecondaryId !== secondaryId) setSecondaryVideoId(secondaryId);

  if (isLoading) {
    return (
      <div className="flex h-svh items-center justify-center text-muted-foreground">
        Loading...
      </div>
    );
  }

  if (!primaryMatch) {
    return (
      <div className="flex h-svh items-center justify-center text-muted-foreground">
        Match not found
      </div>
    );
  }

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
        <VideoLayout primaryUrl={primaryMatch.url} secondaryUrl={secondaryMatch?.url} />
      </main>
    </div>
  );
}
