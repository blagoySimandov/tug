import { createContext, use } from "react";
import { api, type Api } from "./index";

const ApiContext = createContext<Api>(api);

export function ApiProvider({ children }: { children: React.ReactNode }) {
  return <ApiContext value={api}>{children}</ApiContext>;
}

export function useApi(): Api {
  return use(ApiContext);
}
