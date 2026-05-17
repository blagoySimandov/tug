import { useEffect, useRef } from "react";
import { useLiveImportantMoments } from "~/api/hooks";
import { useVideoStore } from "~/store/video";
import type { ImportantMoment } from "~/api/types";
import { AttackChip, GoalChip, RedCardChip, YellowCardChip, VarDecisionChip } from "./impnt-chips";

const ATTACK_LEAD_TIME_SEC = 15;

type AnyMoment = ImportantMoment | (Omit<ImportantMoment, "type"> & { type: "attack" });

const CHIP_MAP: Record<string, React.ComponentType<{ videoTimestamp: number }>> = {
  goal: GoalChip,
  red_card: RedCardChip,
  yellow_card: YellowCardChip,
  var_decision: VarDecisionChip,
  attack: AttackChip,
};

const VARIANT_STYLES = {
  primary: "border-sky-500/40 bg-sky-500/20 text-sky-200",
  secondary: "border-violet-500/40 bg-violet-500/20 text-violet-200",
};

interface MomentsRowProps {
  label: string;
  homeLogo?: string;
  awayLogo?: string;
  variant: "primary" | "secondary";
  moments: AnyMoment[];
  onSeek: (videoId: string, timestamp: number) => void;
}

const MomentsRow = ({ label, homeLogo, awayLogo, variant, moments, onSeek }: MomentsRowProps) => {
  if (moments.length === 0) return null;
  return (
    <div className="flex items-center gap-1.5">
      <span className={`shrink-0 flex items-center gap-1 rounded border px-1.5 py-0.5 text-[11px] font-semibold ${VARIANT_STYLES[variant]}`}>
        {homeLogo && <img src={homeLogo} alt="" className="h-3.5 w-3.5 object-contain" />}
        {label}
        {awayLogo && <img src={awayLogo} alt="" className="h-3.5 w-3.5 object-contain" />}
      </span>
      <div className="flex gap-1.5">
        {moments.map((m) => {
          const Chip = CHIP_MAP[m.type];
          return (
            <button
              key={`${m.videoId}:${m.type}:${m.videoTimestamp}`}
              onClick={() => onSeek(m.videoId, m.videoTimestamp)}
              className="cursor-pointer transition-opacity hover:opacity-75"
            >
              <Chip videoTimestamp={m.videoTimestamp} />
            </button>
          );
        })}
      </div>
    </div>
  );
};

function deriveAttackMoments(goals: ImportantMoment[], currentTs: number): AnyMoment[] {
  return goals
    .filter((g) => currentTs >= g.videoTimestamp - ATTACK_LEAD_TIME_SEC && currentTs < g.videoTimestamp)
    .map((g) => ({
      ...g,
      type: "attack" as const,
      videoTimestamp: g.videoTimestamp - ATTACK_LEAD_TIME_SEC,
      priorityDuration: ATTACK_LEAD_TIME_SEC,
    }));
}

interface ImportantMomentsBarProps {
  primaryLabel?: string;
  secondaryLabel?: string;
  primaryHomeLogo?: string;
  primaryAwayLogo?: string;
  secondaryHomeLogo?: string;
  secondaryAwayLogo?: string;
}

export const ImportantMomentsBar = ({
  primaryLabel = "Cam 1",
  secondaryLabel = "Cam 2",
  primaryHomeLogo,
  primaryAwayLogo,
  secondaryHomeLogo,
  secondaryAwayLogo,
}: ImportantMomentsBarProps) => {
  const primaryVideoId = useVideoStore((s) => s.primaryVideoId);
  const secondaryVideoId = useVideoStore((s) => s.secondaryVideoId);
  const primaryTimestamp = useVideoStore((s) => s.primaryTimestamp);
  const secondaryTimestamp = useVideoStore((s) => s.secondaryTimestamp);
  const primaryPlaying = useVideoStore((s) => s.primaryPlaying);
  const secondaryPlaying = useVideoStore((s) => s.secondaryPlaying);
  const autoswitchEnabled = useVideoStore((s) => s.autoswitchEnabled);
  const setFlashingVideoId = useVideoStore((s) => s.setFlashingVideoId);
  const setPriorityUntil = useVideoStore((s) => s.setPriorityUntil);
  const clearPriority = useVideoStore((s) => s.clearPriority);
  const seekVideo = useVideoStore((s) => s.seekVideo);

  const { data: primaryData } = useLiveImportantMoments(primaryVideoId, 0, 999999);
  const { data: secondaryData } = useLiveImportantMoments(secondaryVideoId, 0, 999999);

  const primaryGoals = primaryData?.filter((m) => m.type === "goal") ?? [];
  const secondaryGoals = secondaryData?.filter((m) => m.type === "goal") ?? [];

  const primaryVisible: AnyMoment[] = [
    ...(primaryData?.filter((m) => m.videoTimestamp <= primaryTimestamp) ?? []),
    ...deriveAttackMoments(primaryGoals, primaryTimestamp),
  ];
  const secondaryVisible: AnyMoment[] = [
    ...(secondaryData?.filter((m) => m.videoTimestamp <= secondaryTimestamp) ?? []),
    ...deriveAttackMoments(secondaryGoals, secondaryTimestamp),
  ];
  const allVisible = [...primaryVisible, ...secondaryVisible];

  const prevVisibleRef = useRef(new Set<string>());
  const timeoutsRef = useRef<Record<string, ReturnType<typeof setTimeout>>>({});

  useEffect(() => {
    const currentKeys = new Set(allVisible.map((m) => `${m.videoId}:${m.type}:${m.videoTimestamp}`));
    const newMoment = allVisible.find((m) => !prevVisibleRef.current.has(`${m.videoId}:${m.type}:${m.videoTimestamp}`));
    prevVisibleRef.current = currentKeys;
    if (!newMoment) return;

    const isPlaying =
      (newMoment.videoId === primaryVideoId && primaryPlaying) ||
      (newMoment.videoId === secondaryVideoId && secondaryPlaying);
    if (!isPlaying) return;

    clearTimeout(timeoutsRef.current[newMoment.videoId]);
    setFlashingVideoId(newMoment.videoId);
    if (autoswitchEnabled) {
      setPriorityUntil(newMoment.videoId, Date.now() + newMoment.priorityDuration * 1000);
    }
    timeoutsRef.current[newMoment.videoId] = setTimeout(() => {
      if (autoswitchEnabled) clearPriority(newMoment.videoId);
      setFlashingVideoId(null);
    }, newMoment.priorityDuration * 1000);
  }, [allVisible, autoswitchEnabled, primaryPlaying, secondaryPlaying, primaryVideoId, secondaryVideoId, setFlashingVideoId, setPriorityUntil, clearPriority]);

  return (
    <div className="flex flex-col gap-0.5">
      <MomentsRow label={primaryLabel} homeLogo={primaryHomeLogo} awayLogo={primaryAwayLogo} variant="primary" moments={primaryVisible} onSeek={seekVideo} />
      <MomentsRow label={secondaryLabel} homeLogo={secondaryHomeLogo} awayLogo={secondaryAwayLogo} variant="secondary" moments={secondaryVisible} onSeek={seekVideo} />
    </div>
  );
};
