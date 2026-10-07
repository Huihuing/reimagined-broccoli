import { apiRequest } from "./client";

export function fetchEvents({ path = "", status = "" } = {}) {
  const params = new URLSearchParams();
  if (path.trim()) {
    params.set("path", path.trim());
  }
  if (String(status).trim()) {
    params.set("status", String(status).trim());
  }

  const query = params.toString();
  return apiRequest(`/events${query ? `?${query}` : ""}`);
}
