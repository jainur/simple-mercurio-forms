import { getApiBaseUrl } from "@/lib/config";
import type { ReadyStatus } from "@/types/api";

type ReadyPayload = {
  status?: string;
  checks?: {
    forms_db?: boolean;
    definitions_dir?: boolean;
  };
};

export async function getReadyStatus(): Promise<ReadyStatus> {
  const baseUrl = getApiBaseUrl();

  try {
    const response = await fetch(`${baseUrl}/health/ready`, {
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      return {
        kind: "offline",
        label: "Unavailable",
        message: `API responded with HTTP ${response.status}.`,
        baseUrl,
      };
    }

    const payload = (await response.json()) as ReadyPayload;

    return {
      kind: payload.status === "ok" ? "success" : "degraded",
      label: payload.status === "ok" ? "Ready" : "Degraded",
      message:
        payload.status === "ok"
          ? "The API is reachable and its readiness checks are passing."
          : "The API is reachable, but one or more readiness checks are failing.",
      baseUrl,
    };
  } catch {
    return {
      kind: "offline",
      label: "Offline",
      message:
        "The Next.js app could not reach the FastAPI service. Start the API or update MERCURIO_API_BASE_URL.",
      baseUrl,
    };
  }
}