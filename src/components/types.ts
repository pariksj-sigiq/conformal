export type ChatRole = "user" | "assistant" | "system";

export type TraceEvent = {
  id: string;
  type: string;
  label: string;
  status?: "pending" | "running" | "complete" | "error";
  detail?: string;
  payload?: unknown;
  timestamp: number;
};

export type ChartBundle = {
  id: string;
  title: string;
  sql: string;
  description?: string;
  spec?: Record<string, unknown>;
  generatedAt?: number;
};

export type ChatMessage = {
  id: string;
  role: ChatRole;
  content: string;
  trace?: TraceEvent[];
  charts?: ChartBundle[];
  createdAt: number;
};
