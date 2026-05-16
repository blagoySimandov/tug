import { useEffect, useRef } from "react";
import { useLiveImportantMoments } from "~/api/hooks";
import { useVideoStore } from "~/store/video";
import { GoalChip, RedCardChip, YellowCardChip, VarDecisionChip } from "./impnt-chips";

const CHIP_MAP = {
  goal: GoalChip,
  red_card: RedCardChip,
  yellow_card: YellowCardChip,
  var_decision: VarDecisionChip,
} as const;

export const ImportantMomentsBar = () => {
  const primaryVideoId = useVideoStore((s) => s.primaryVideoId);
  const secondaryVideoId = useVideoStore((s) => s.secondaryVideoId);
  const primaryTimestamp = useVideoStore((s) => s.primaryTimestamp);
  const secondaryTimestamp = useVideoStore((s) => s.secondaryTimestamp);
  const autoswitchEnabled = useVideoStore((s) => s.autoswitchEnabled);
  const setFlashingVideoId = useVideoStore((s) => s.setFlashingVideoId);
  const setPriorityUntil = useVideoStore((s) => s.setPriorityUntil);
  const clearPriority = useVideoStore((s) => s.clearPriority);
  const seekVideo = useVideoStore((s) => s.seekVideo);

  const { data: primaryData } = useLiveImportantMoments(primaryVideoId, 0, 999999);
  const { data: secondaryData } = useLiveImportantMoments(secondaryVideoId, 0, 999999);

  const visible = [
    ...(primaryData?.filter((m) => m.videoTimestamp <= primaryTimestamp) ?? []),
    ...(secondaryData?.filter((m) => m.videoTimestamp <= secondaryTimestamp) ?? []),
  ];

  const seenRef = useRef(new Set<string>());
  const timeoutsRef = useRef<Record<string, ReturnType<typeof setTimeout>>>({});

  useEffect(() => {
    const newMoment = visible.find((m) => !seenRef.current.has(`${m.videoId}:${m.videoTimestamp}`));
    if (!newMoment) return;
    seenRef.current.add(`${newMoment.videoId}:${newMoment.videoTimestamp}`);

    clearTimeout(timeoutsRef.current[newMoment.videoId]);
    setFlashingVideoId(newMoment.videoId);
    if (autoswitchEnabled) {
      setPriorityUntil(newMoment.videoId, Date.now() + newMoment.priorityDuration * 1000);
    }
    timeoutsRef.current[newMoment.videoId] = setTimeout(() => {
      if (autoswitchEnabled) clearPriority(newMoment.videoId);
      setFlashingVideoId(null);
    }, newMoment.priorityDuration * 1000);
  }, [visible, autoswitchEnabled, setFlashingVideoId, setPriorityUntil, clearPriority]);

  return (
    <div className="flex gap-2 items-center">
      {visible.map((m) => {
        const Chip = CHIP_MAP[m.type];
        return (
          <button key={`${m.videoId}:${m.videoTimestamp}`} onClick={() => seekVideo(m.videoId, m.videoTimestamp)} className="cursor-pointer transition-opacity hover:opacity-75">
            <Chip videoTimestamp={m.videoTimestamp} />
          </button>
        );
      })}
    </div>
  );
};
