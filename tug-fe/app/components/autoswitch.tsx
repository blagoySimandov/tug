import { useVideoStore } from "~/store/video";
import { Switch } from "./ui/switch";

export const AutoSwitch = () => {
  const { autoswitchEnabled, setAutoswitchEnabled } = useVideoStore();
  return (
    <label className="flex items-center gap-2 cursor-pointer">
      <Switch
        id="autoswitch"
        checked={autoswitchEnabled}
        onCheckedChange={setAutoswitchEnabled}
      />
      Enable AutoSwitch
    </label>
  );
};
