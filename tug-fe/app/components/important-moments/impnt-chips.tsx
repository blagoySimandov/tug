import { Crosshair, Square } from "lucide-react";
import { Badge } from "~/components/ui/badge";
import { cn } from "~/lib/utils";

interface BaseChipProps {
  icon: React.ReactNode;
  label: string;
  matchMinute: number;
  className?: string;
}

export const BaseChip = ({
  icon,
  label,
  matchMinute,
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
      {matchMinute}&apos;
    </span>
  </Badge>
);

export const GoalChip = ({ matchMinute }: { matchMinute: number }) => (
  <BaseChip
    icon={<Crosshair strokeWidth={2.5} />}
    label="Goal"
    matchMinute={matchMinute}
    className="border-amber-400/25 bg-amber-950/80 text-amber-100 shadow-[0_0_16px_rgba(251,191,36,0.12)]"
  />
);

export const RedCardChip = ({ matchMinute }: { matchMinute: number }) => (
  <BaseChip
    icon={<Square fill="currentColor" strokeWidth={0} />}
    label="Red Card"
    matchMinute={matchMinute}
    className="border-red-500/25 bg-red-950/80 text-red-100 shadow-[0_0_16px_rgba(239,68,68,0.12)]"
  />
);
