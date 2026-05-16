import { useEffect, useRef } from "react";
import { useLiveImportantMoments } from "~/api/hooks";
import { useVideoStore } from "~/store/video";
import { GoalChip, RedCardChip } from "./impnt-chips";

const CHIP_MAP = {
  goal: GoalChip,
  red_card: RedCardChip,
} as const;

export const ImportantMomentsBar = () => {
  const primaryVideoId = useVideoStore((s) => s.primaryVideoId);
  const secondaryVideoId = useVideoStore((s) => s.secondaryVideoId);
  const primaryTimestamp = useVideoStore((s) => s.primaryTimestamp);
  const secondaryTimestamp = useVideoStore((s) => s.secondaryTimestamp);
  const setFlashingVideoId = useVideoStore((s) => s.setFlashingVideoId);
  const setPriorityUntil = useVideoStore((s) => s.setPriorityUntil);
  const clearPriority = useVideoStore((s) => s.clearPriority);

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
    setPriorityUntil(newMoment.videoId, Date.now() + newMoment.priorityDuration * 1000);
    timeoutsRef.current[newMoment.videoId] = setTimeout(() => {
      clearPriority(newMoment.videoId);
      setFlashingVideoId(null);
    }, newMoment.priorityDuration * 1000);
  }, [visible, setFlashingVideoId, setPriorityUntil, clearPriority]);

  return (
    <div className="flex gap-2 items-center">
      {visible.map((m) => {
        const Chip = CHIP_MAP[m.type];
        return <Chip key={`${m.videoId}:${m.videoTimestamp}`} videoTimestamp={m.videoTimestamp} />;
      })}
    </div>
  );
};
