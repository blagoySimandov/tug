import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router";
import { useMatches } from "~/api/hooks";
const logo = "/logo.png";
import type { Match } from "~/api/types";
import { AutoSwitch } from "~/components/autoswitch";
import { ImportantMomentsBar } from "~/components/important-moments";
import { NarratorPanel } from "~/components/narrator-panel";
import { VideoLayout, type LayoutMode } from "~/components/video-layout";
import { useVideoStore } from "~/store/video";

const BASE_URL = "http://localhost:8000";
const CHUNK = 120;

const abbr = (name: string) => name.slice(0, 3).toUpperCase();
const matchLabel = (match: Match | undefined) =>
  match ? `${abbr(match.homeTeam.name)} vs ${abbr(match.awayTeam.name)}` : undefined;

const MODES: { label: string; value: LayoutMode }[] = [
  { label: "Split", value: "split" },
  { label: "PiP", value: "pip" },
];

export default function Player() {
  const [searchParams] = useSearchParams();
  const [narratorOpen, setNarratorOpen] = useState(false);
  const navigate = useNavigate();
  const mode = useVideoStore((s) => s.manualLayoutMode);
  const setMode = useVideoStore((s) => s.setManualLayoutMode);
  const { data: matches = [], isLoading } = useMatches();

  const primaryId = searchParams.get("primary") ?? "";
  const secondaryId = searchParams.get("secondary") ?? "";
  const narratorOn = searchParams.get("narrator") === "1";

  const primaryMatch = matches.find((m) => m.id === primaryId);
  const secondaryMatch = matches.find((m) => m.id === secondaryId);

  const primaryTimestamp = useVideoStore((s) => s.primaryTimestamp);
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

  const primaryUrl = narratorOn
    ? `${BASE_URL}/events/${primaryMatch.id}/narrated-stream.m3u8`
    : primaryMatch.url;

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="flex min-h-11 items-center gap-4 bg-primary px-5 py-1.5">
        <button onClick={() => navigate("/")} className="flex items-center gap-2 transition-opacity hover:opacity-80">
          <img src={logo} alt="TUG logo" className="h-9 object-contain" />
          <span style={{ fontFamily: "'Bebas Neue', sans-serif" }} className="text-xl tracking-widest text-accent">TUG</span>
        </button>
        <div className="h-5 w-px bg-primary-foreground/15" />
        <div className="flex flex-1 justify-center">
          <ImportantMomentsBar
            primaryLabel={matchLabel(primaryMatch)}
            secondaryLabel={matchLabel(secondaryMatch)}
            primaryHomeLogo={primaryMatch.homeTeam.logo}
            primaryAwayLogo={primaryMatch.awayTeam.logo}
            secondaryHomeLogo={secondaryMatch?.homeTeam.logo}
            secondaryAwayLogo={secondaryMatch?.awayTeam.logo}
          />
        </div>
        {narratorOn && (
          <span className="rounded border border-accent/40 bg-accent/10 px-2 py-0.5 text-xs font-medium text-accent">
            Narrator
          </span>
        )}
        <AutoSwitch />
        <div className="h-5 w-px bg-primary-foreground/15" />
        <button
          onClick={() => setNarratorOpen((o) => !o)}
          className={`rounded px-3 py-1 text-xs font-medium transition-colors ${
            narratorOpen
              ? "bg-accent text-accent-foreground"
              : "text-primary-foreground/55 hover:bg-primary-foreground/10 hover:text-primary-foreground"
          }`}
        >
          Narrator
        </button>
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
      {narratorOpen && (
        <NarratorPanel
          eventId={parseInt(primaryId, 10)}
          videoUrl={primaryMatch.url}
          windowStart={Math.max(0, primaryTimestamp - 150)}
          windowEnd={primaryTimestamp + 150}
        />
      )}
      <main className="flex-1 overflow-hidden p-2">
        <VideoLayout primaryUrl={primaryUrl} secondaryUrl={secondaryMatch?.url} />
      </main>
    </div>
  );
}
