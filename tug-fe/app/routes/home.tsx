import { useState } from "react";
import { useNavigate } from "react-router";
import { useMatches } from "~/api/hooks";
import type { Match } from "~/api/types";
import { VideoThumbnail } from "~/components/video-thumbnail";
import { useVideoStore } from "~/store/video";
const logo = "/logo.png";

function TeamRow({ team }: { team: { name: string; flag: string; logo: string } }) {
  return (
    <div className="flex items-center gap-2">
      {team.logo
        ? <img src={team.logo} alt={team.name} className="h-7 w-7 object-contain" />
        : <span className="text-2xl">{team.flag}</span>
      }
      <span className="font-semibold">{team.name}</span>
    </div>
  );
}

function MatchCard({
  match,
  selected,
  onToggle,
}: {
  match: Match;
  selected: boolean;
  onToggle: () => void;
}) {
  return (
    <button
      onClick={onToggle}
      className={`group flex w-96 flex-col overflow-hidden rounded-xl border-2 bg-card transition-all duration-300 ${
        selected
          ? "scale-[1.03] border-accent shadow-xl shadow-accent/30"
          : "border-border hover:scale-[1.03] hover:border-primary/50 hover:shadow-xl hover:shadow-black/30"
      }`}
    >
      <div className="relative aspect-video w-full overflow-hidden bg-muted">
        <VideoThumbnail
          url={match.url}
          className="h-full w-full transition-transform duration-500 group-hover:scale-110"
        />
        <div
          className={`absolute inset-0 transition-all duration-300 ${
            selected
              ? "bg-accent/25 opacity-100"
              : "opacity-0 group-hover:bg-gradient-to-t group-hover:from-black/50 group-hover:to-transparent group-hover:opacity-100"
          }`}
        />
        {selected && (
          <div className="absolute right-2 top-2 flex h-5 w-5 items-center justify-center rounded-full bg-accent">
            <svg className="h-3 w-3 text-accent-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        )}
      </div>
      <div className="flex flex-col gap-2 p-4">
        <TeamRow team={match.homeTeam} />
        <span className="text-xs font-semibold text-muted-foreground">VS</span>
        <TeamRow team={match.awayTeam} />
      </div>
    </button>
  );
}

export default function Home() {
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [narratorEnabled, setNarratorEnabled] = useState(false);
  const navigate = useNavigate();
  const { data: matches = [], isLoading } = useMatches();
  const setPrimaryVideoId = useVideoStore((s) => s.setPrimaryVideoId);
  const setSecondaryVideoId = useVideoStore((s) => s.setSecondaryVideoId);

  function toggle(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else if (next.size < 2) {
        next.add(id);
      }
      return next;
    });
  }

  function handleWatch() {
    const ids = Array.from(selected);
    setPrimaryVideoId(ids[0]);
    if (ids[1]) setSecondaryVideoId(ids[1]);
    const params = new URLSearchParams();
    params.set("primary", ids[0]);
    if (ids[1]) params.set("secondary", ids[1]);
    if (narratorEnabled) params.set("narrator", "1");
    navigate(`/player?${params.toString()}`);
  }

  const count = selected.size;

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="relative flex h-20 items-center justify-center bg-primary px-5">
        <div className="flex items-center gap-1">
          <img src={logo} alt="TUG logo" className="h-12 object-contain" />
          <span style={{ fontFamily: "'Bebas Neue', sans-serif" }} className="text-5xl tracking-widest text-accent leading-none">TUG</span>
        </div>
      </header>

      <main className="flex flex-1 flex-col items-center justify-center gap-10 p-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Select matches to watch</h1>
          <p className="mt-1 text-sm text-muted-foreground">Pick one or two</p>
        </div>

        {isLoading ? (
          <p className="text-sm text-muted-foreground">Loading...</p>
        ) : (
          <div className="grid grid-cols-2 gap-6 lg:grid-cols-3">
            {matches.map((match) => (
              <MatchCard
                key={match.id}
                match={match}
                selected={selected.has(match.id)}
                onToggle={() => toggle(match.id)}
              />
            ))}
          </div>
        )}
      </main>

      {/* Selection tray */}
      {count > 0 && (
        <div className="fixed bottom-6 left-1/2 flex -translate-x-1/2 items-center gap-3 rounded-full bg-primary px-5 py-3 shadow-2xl shadow-black/40">
          <span className="text-sm font-bold text-primary-foreground">
            {count}/2 selected
          </span>
          {count === 1 && (
            <button
              onClick={() => setNarratorEnabled((v) => !v)}
              className={`flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                narratorEnabled
                  ? "bg-accent text-accent-foreground"
                  : "bg-primary-foreground/15 text-primary-foreground/70 hover:bg-primary-foreground/25"
              }`}
            >
              Narrator
            </button>
          )}
          <button
            onClick={handleWatch}
            className="rounded-full bg-accent px-5 py-1.5 text-sm font-semibold text-accent-foreground transition-opacity hover:opacity-90"
          >
            Watch
          </button>
        </div>
      )}
    </div>
  );
}
