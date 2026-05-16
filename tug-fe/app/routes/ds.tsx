import { Button } from "~/components/ui/button";
import { Badge } from "~/components/ui/badge";
import { Switch } from "~/components/ui/switch";
import {
  GoalChip,
  RedCardChip,
} from "~/components/important-moments/impnt-chips";

const Section = ({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) => (
  <section className="space-y-3">
    <h2 className="text-muted-foreground text-xs font-semibold uppercase tracking-widest">
      {title}
    </h2>
    {children}
  </section>
);

const Row = ({ children }: { children: React.ReactNode }) => (
  <div className="flex flex-wrap items-center gap-3">{children}</div>
);

const Swatch = ({ label, className }: { label: string; className: string }) => (
  <div className="flex flex-col items-center gap-1.5">
    <div className={`h-10 w-10 rounded-md border ${className}`} />
    <span className="text-muted-foreground text-[10px]">{label}</span>
  </div>
);

export default function DesignSystem() {
  return (
    <div className="bg-background min-h-screen p-10">
      <h1 className="text-foreground mb-10 text-2xl font-bold tracking-tight">
        Design System
      </h1>

      <div className="space-y-10">
        <Section title="Colors">
          <Row>
            <Swatch label="primary" className="bg-primary" />
            <Swatch label="secondary" className="bg-secondary" />
            <Swatch label="muted" className="bg-muted" />
            <Swatch label="accent" className="bg-accent" />
            <Swatch label="destructive" className="bg-destructive" />
            <Swatch label="border" className="bg-border" />
          </Row>
        </Section>

        <Section title="Typography">
          <div className="space-y-2">
            <p className="text-4xl font-bold">Heading 4xl</p>
            <p className="text-2xl font-semibold">Heading 2xl</p>
            <p className="text-xl font-medium">Heading xl</p>
            <p className="text-base">Body base — The quick brown fox</p>
            <p className="text-muted-foreground text-sm">Body sm muted</p>
            <p className="font-mono text-sm">Mono — 23&apos; 45&apos; 90&apos;</p>
          </div>
        </Section>

        <Section title="Button">
          <Row>
            <Button variant="default">Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="link">Link</Button>
          </Row>
          <Row>
            <Button size="xs">XSmall</Button>
            <Button size="sm">Small</Button>
            <Button size="default">Default</Button>
            <Button size="lg">Large</Button>
          </Row>
        </Section>

        <Section title="Badge">
          <Row>
            <Badge variant="default">Default</Badge>
            <Badge variant="secondary">Secondary</Badge>
            <Badge variant="destructive">Destructive</Badge>
            <Badge variant="outline">Outline</Badge>
            <Badge variant="ghost">Ghost</Badge>
          </Row>
        </Section>

        <Section title="Switch">
          <Row>
            <Switch />
            <Switch size="sm" />
            <Switch defaultChecked />
            <Switch defaultChecked size="sm" />
            <Switch disabled />
          </Row>
        </Section>

        <Section title="Important Moment Chips">
          <div className="flex flex-wrap items-center gap-3 rounded-lg bg-zinc-900 p-6">
            <GoalChip matchMinute={23} />
            <RedCardChip matchMinute={67} />
            <GoalChip matchMinute={90} />
          </div>
        </Section>
      </div>
    </div>
  );
}
