import { Switch } from "./ui/switch";
//TODO: Make it better looking
export const AutoSwitch = () => {
  return (
    <label className="flex items-center gap-2 cursor-pointer">
      <Switch id="autoswitch" />
      Enable AutoSwitch
    </label>
  );
};
