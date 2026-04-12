const defaultApiBaseUrl = "http://localhost:8000";

export function getApiBaseUrl(): string {
  return process.env.MERCURIO_API_BASE_URL?.trim() || defaultApiBaseUrl;
}