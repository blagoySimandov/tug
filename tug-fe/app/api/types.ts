// Run `bun run gen:types` (with backend running) to regenerate from the OpenAPI spec.
// Source of truth: tug-be/models.py
export type { components } from "./generated";

import type { components } from "./generated";

export type MomentType = components["schemas"]["MomentType"];
export type ImportantMoment = components["schemas"]["ImportantMoment"];
export type ImportantMomentsResponse = ImportantMoment[];
