import { ArrowRightLeft, Circle, Crosshair, Flame, ShieldAlert, Square, Star, Target, Video } from "lucide-react";
import { Badge } from "~/components/ui/badge";
import { cn } from "~/lib/utils";

interface BaseChipProps {
  icon: React.ReactNode;
  label: string;
  videoTimestamp: number;
  className?: string;
}

export const BaseChip = ({
  icon,
  label,
  videoTimestamp,
  className,
}: BaseChipProps) => (
  <Badge
    variant="outline"
    className={cn(
      "h-auto animate-fade-in gap-2 px-3 py-1.5 text-xs font-semibold uppercase tracking-widest backdrop-blur-sm",
      className,
    )}
  >
    {icon}
    <span>{label}</span>
    <span className="font-mono tabular-nums opacity-50">
      {Math.floor(videoTimestamp / 60)}&apos;
    </span>
  </Badge>
);

export const GoalChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Crosshair strokeWidth={2.5} />}
    label="Goal"
    videoTimestamp={videoTimestamp}
    className="border-amber-400/25 bg-amber-950/80 text-amber-100 shadow-[0_0_16px_rgba(251,191,36,0.12)]"
  />
);

export const RedCardChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Square fill="currentColor" strokeWidth={0} />}
    label="Red Card"
    videoTimestamp={videoTimestamp}
    className="border-red-500/25 bg-red-950/80 text-red-100 shadow-[0_0_16px_rgba(239,68,68,0.12)]"
  />
);

export const YellowCardChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Square fill="currentColor" strokeWidth={0} />}
    label="Yellow"
    videoTimestamp={videoTimestamp}
    className="border-yellow-400/25 bg-yellow-950/80 text-yellow-100 shadow-[0_0_16px_rgba(234,179,8,0.12)]"
  />
);

export const VarDecisionChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Video strokeWidth={2.5} />}
    label="VAR"
    videoTimestamp={videoTimestamp}
    className="border-blue-400/25 bg-blue-950/80 text-blue-100 shadow-[0_0_16px_rgba(96,165,250,0.12)]"
  />
);

export const AttackChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Flame strokeWidth={2.5} />}
    label="Attack"
    videoTimestamp={videoTimestamp}
    className="animate-pulse border-orange-400/25 bg-orange-950/80 text-orange-100 shadow-[0_0_16px_rgba(251,146,60,0.18)]"
  />
);

export const SubstitutionChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<ArrowRightLeft strokeWidth={2.5} />}
    label="Sub"
    videoTimestamp={videoTimestamp}
    className="border-green-400/25 bg-green-950/80 text-green-100"
  />
);

export const PenaltyChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Target strokeWidth={2.5} />}
    label="Penalty"
    videoTimestamp={videoTimestamp}
    className="border-red-400/25 bg-red-950/80 text-red-100 shadow-[0_0_16px_rgba(239,68,68,0.15)]"
  />
);

export const NearMissChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<ShieldAlert strokeWidth={2.5} />}
    label="Near Miss"
    videoTimestamp={videoTimestamp}
    className="border-orange-400/25 bg-orange-950/80 text-orange-100"
  />
);

export const FreeKickChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Circle strokeWidth={2.5} />}
    label="Free Kick"
    videoTimestamp={videoTimestamp}
    className="border-slate-400/25 bg-slate-950/80 text-slate-100"
  />
);

export const CornerChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Circle strokeWidth={2.5} />}
    label="Corner"
    videoTimestamp={videoTimestamp}
    className="border-slate-400/25 bg-slate-900/80 text-slate-200"
  />
);

export const HighlightChip = ({ videoTimestamp }: { videoTimestamp: number }) => (
  <BaseChip
    icon={<Star strokeWidth={2.5} />}
    label="Highlight"
    videoTimestamp={videoTimestamp}
    className="border-purple-400/25 bg-purple-950/80 text-purple-100 shadow-[0_0_16px_rgba(192,132,252,0.15)]"
  />
);
