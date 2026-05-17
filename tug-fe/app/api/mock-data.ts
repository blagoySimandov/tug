import type { MatchesResponse } from "./types";

export const MOCK_MATCHES: MatchesResponse = [
  {
    id: "arg_fr",
    homeTeam: { name: "Argentina", flag: "🇦🇷" },
    awayTeam: { name: "France", flag: "🇫🇷" },
    homeScore: 3,
    awayScore: 3,
    leagueName: "FIFA World Cup",
    url: "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/arg_fr.mp4?alt=media&token=5ee16507-af66-4409-b9f1-2de014937342",
  },
  {
    id: "cr_bra",
    homeTeam: { name: "Croatia", flag: "🇭🇷" },
    awayTeam: { name: "Brazil", flag: "🇧🇷" },
    homeScore: 1,
    awayScore: 1,
    leagueName: "FIFA World Cup",
    url: "https://firebasestorage.googleapis.com/v0/b/tug-splitball.firebasestorage.app/o/cr_bra.mp4?alt=media&token=c648c419-949b-4048-b880-1613227fdaf8",
  },
];
