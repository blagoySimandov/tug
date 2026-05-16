import { useVideoStore } from "~/store/video";
import { Switch } from "./ui/switch";

export const AutoSwitch = () => {
  const { autoswitchEnabled, setAutoswitchEnabled } = useVideoStore();
  return (
    <label className="flex cursor-pointer items-center gap-2">
      <Switch
        id="autoswitch"
        checked={autoswitchEnabled}
        onCheckedChange={setAutoswitchEnabled}
        className="data-checked:bg-accent data-unchecked:bg-primary-foreground/25"
      />
      <span className="text-xs font-medium text-primary-foreground/75">Auto</span>
    </label>
  );
};
