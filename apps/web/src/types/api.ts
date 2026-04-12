export type ReadyStatus = {
  kind: "success" | "degraded" | "offline";
  label: string;
  message: string;
  baseUrl: string;
};