import { type RouteConfig, index, route } from "@react-router/dev/routes"

export default [
  index("routes/home.tsx"),
  route("/player", "routes/player.tsx"),
  route("/ds", "routes/ds.tsx"),
  route("/tts", "routes/tts.tsx"),
] satisfies RouteConfig
