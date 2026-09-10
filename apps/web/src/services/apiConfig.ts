/** Public endpoint configuration and operator access, held only in memory. */
let accessKey = "";

export function setApiAccessKey(value: string): void {
  accessKey = value.trim();
}

export function apiHeaders(): Record<string, string> {
  return accessKey ? { Authorization: `Bearer ${accessKey}` } : {};
}

export function resolveApiBaseUrl(explicit?: string): string {
  const value = (explicit ?? process.env.NEXT_PUBLIC_API_URL ?? "").trim();
  if (!value) return process.env.NODE_ENV === "development" ? "http://localhost:8000" : "";
  try {
    const url = new URL(value);
    const local = ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
    if (url.username || url.password || url.search || url.hash) return "";
    if (url.protocol !== "https:" && !(url.protocol === "http:" && local)) return "";
    if (typeof window !== "undefined" && window.location.protocol === "https:" && url.protocol !== "https:") return "";
    return value.replace(/\/+$/, "");
  } catch {
    return "";
  }
}
