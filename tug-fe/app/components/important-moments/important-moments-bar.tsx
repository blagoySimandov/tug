import { GoalChip, RedCardChip } from "./impnt-chips";
export const ImportantMomentsBar = () => {
  return (
    <div className="flex gap-2 items-center">
      <GoalChip matchMinute={10} />
      <RedCardChip matchMinute={10} />
    </div>
  );
};
