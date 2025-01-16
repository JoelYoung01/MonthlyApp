import type { Requirement } from "./Requirement";

export type AppDefinition = {
  id: number;
  name: string;
  start_date: string;
  due_date: string;
  description: string;
  requirements: Requirement[];
};
