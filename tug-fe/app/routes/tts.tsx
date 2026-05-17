import { useState } from "react";
import { api } from "~/api";
import { Button } from "~/components/ui/button";

const VOICES = [
  "Puck", "Achernar", "Alnilam", "Autonoe", "Enceladus", "Rasalgethi",
  "Sadachbia", "Schedar", "Umbriel", "Zubenelgenubi",
  "Achird", "Algenib", "Callirrhoe", "Despina", "Pulcherrima",
  "Sulafat", "Vindemiatrix", "Zephyr",
];

export default function TtsTest() {
  const [text, setText] = useState("Goal! 23rd minute. What a strike from the edge of the box!");
  const [voice, setVoice] = useState("Puck");
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate() {
    setLoading(true);
    setError(null);
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    try {
      const blob = await api.generateSpeech(text, voice);
      setAudioUrl(URL.createObjectURL(blob));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-background min-h-screen p-10">
      <h1 className="text-foreground mb-8 text-2xl font-bold tracking-tight">TTS Test</h1>
      <div className="max-w-lg space-y-4">
        <div className="space-y-1.5">
          <label className="text-muted-foreground text-xs font-semibold uppercase tracking-widest">
            Text
          </label>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={4}
            className="bg-muted text-foreground w-full rounded-md border p-3 text-sm focus:outline-none"
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-muted-foreground text-xs font-semibold uppercase tracking-widest">
            Voice
          </label>
          <select
            value={voice}
            onChange={(e) => setVoice(e.target.value)}
            className="bg-muted text-foreground w-full rounded-md border p-2 text-sm focus:outline-none"
          >
            {VOICES.map((v) => (
              <option key={v} value={v}>{v}</option>
            ))}
          </select>
        </div>
        <Button onClick={handleGenerate} disabled={loading || !text.trim()}>
          {loading ? "Generating…" : "Generate Speech"}
        </Button>
        {error && <p className="text-destructive text-sm">{error}</p>}
        {audioUrl && (
          <audio controls src={audioUrl} className="w-full" autoPlay />
        )}
      </div>
    </div>
  );
}
