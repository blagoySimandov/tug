import { useState } from "react";
import { useNavigate } from "react-router";
import { useMatches } from "~/api/hooks";
import type { Match } from "~/api/types";
import { VideoThumbnail } from "~/components/video-thumbnail";
import { useVideoStore } from "~/store/video";

function TeamRow({ team }: { team: { name: string; flag: string } }) {
  return (
    <div className="flex items-center gap-2">
      <span className="text-2xl">{team.flag}</span>
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
      className={`flex w-64 flex-col overflow-hidden rounded-xl border-2 bg-card transition-all ${
        selected
          ? "border-accent shadow-lg shadow-accent/20"
          : "border-border hover:border-primary/30"
      }`}
    >
      <div className="aspect-video w-full bg-muted">
        <VideoThumbnail url={match.url} className="h-full w-full" />
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
  const navigate = useNavigate();
  const { data: matches = [], isLoading } = useMatches();
  const setPrimaryVideoId = useVideoStore((s) => s.setPrimaryVideoId);
  const setSecondaryVideoId = useVideoStore((s) => s.setSecondaryVideoId);

  function toggle(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
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
    navigate(`/player?${params.toString()}`);
  }

  return (
    <div className="flex h-svh flex-col bg-background">
      <header className="flex h-11 items-center gap-4 bg-primary px-5">
        <span className="text-sm font-black tracking-tight text-accent">TUG</span>
      </header>
      <main className="flex flex-1 flex-col items-center justify-center gap-10 p-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Select matches to watch</h1>
          <p className="mt-1 text-sm text-muted-foreground">Pick one or two</p>
        </div>
        {isLoading ? (
          <p className="text-sm text-muted-foreground">Loading...</p>
        ) : (
          <div className="grid grid-cols-2 gap-6">
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
        <button
          disabled={selected.size === 0}
          onClick={handleWatch}
          className="rounded-lg bg-accent px-10 py-3 font-semibold text-accent-foreground transition-opacity disabled:cursor-not-allowed disabled:opacity-40"
        >
          Watch{selected.size > 0 ? ` (${selected.size})` : ""}
        </button>
      </main>
    </div>
  );
}
