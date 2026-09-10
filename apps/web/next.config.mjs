import { fileURLToPath } from "node:url";
const apiUrl = process.env.NEXT_PUBLIC_API_URL?.trim();
let apiOrigin = "";
if (apiUrl) {
  const url = new URL(apiUrl);
  const local = ["localhost", "127.0.0.1", "[::1]"].includes(url.hostname);
  if ((url.protocol !== "https:" && !(url.protocol === "http:" && local)) || url.username || url.password || url.search || url.hash) {
    throw new Error("NEXT_PUBLIC_API_URL must be an HTTPS service URL (HTTP is allowed only on localhost).");
  }
  apiOrigin = url.origin;
}
const development = process.env.NODE_ENV === "development";
const csp = [
  "default-src 'self'", "base-uri 'self'", "object-src 'none'", "frame-ancestors 'none'",
  `script-src 'self' 'unsafe-inline'${development ? " 'unsafe-eval'" : ""}`,
  "style-src 'self' 'unsafe-inline'", "img-src 'self' blob: data:", "font-src 'self'",
  `connect-src 'self' ${apiOrigin} ${development ? "http://localhost:8000 http://127.0.0.1:8000 ws://localhost:3000" : ""}`,
  "form-action 'self'",
].join("; ");
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
  outputFileTracingRoot: fileURLToPath(new URL(".", import.meta.url)),
  poweredByHeader: false,
  async headers() {
    return [{ source: "/:path*", headers: [
      { key: "Content-Security-Policy", value: csp },
      { key: "X-Content-Type-Options", value: "nosniff" },
      { key: "X-Frame-Options", value: "DENY" },
      { key: "Referrer-Policy", value: "no-referrer" },
      { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
    ] }];
  },
};

export default nextConfig;
