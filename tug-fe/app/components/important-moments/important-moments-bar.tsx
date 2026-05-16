import { useLiveImportantMoments } from "~/api/hooks";
import { useVideoStore } from "~/store/video";
import { GoalChip, RedCardChip } from "./impnt-chips";

const CHIP_MAP = {
  goal: GoalChip,
  red_card: RedCardChip,
} as const;

export const ImportantMomentsBar = () => {
  const currentTimestamp = useVideoStore((s) => s.currentTimestamp);
  const { data } = useLiveImportantMoments("arg_fr", 0, 999999);

  const visible = data?.filter((m) => m.videoTimestamp <= currentTimestamp) ?? [];

  return (
    <div className="flex gap-2 items-center">
      {visible.map((m) => {
        const Chip = CHIP_MAP[m.type];
        return <Chip key={m.videoTimestamp} videoTimestamp={m.videoTimestamp} />;
      })}
    </div>
  );
};
