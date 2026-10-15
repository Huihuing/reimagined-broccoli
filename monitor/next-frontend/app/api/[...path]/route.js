// Same-origin Next.js -> Flask proxy. API secrets stay on the server.
export const runtime = "nodejs";
async function forward(request, context) {
  const { path } = await context.params;
  const resource = path.join("/");
  const allowed = /^(auth\/(login|logout|session)|notes(\/\d+)?|events|analysis(\/(start|raw))?|sentry-test)$/.test(resource);
  if (!allowed || ((resource === "events" || resource.startsWith("analysis")) && request.method !== "GET")) {
    return Response.json({ error: "지원하지 않는 요청입니다." }, { status: 404 });
  }
  const base = process.env.MONITOR_API_URL || process.env.FLASK_API_URL || "http://127.0.0.1:5200";
  try {
    const target = new URL("/api/" + path.map(encodeURIComponent).join("/"), base);
    if (!["http:", "https:"].includes(target.protocol)) throw new Error("Invalid URL protocol");
    target.search = new URL(request.url).search;
    const headers = new Headers();
    for (const name of ["content-type", "cookie", "x-csrf-token"]) {
      const value = request.headers.get(name);
      if (value) headers.set(name, value);
    }
    const options = { method: request.method, headers, cache: "no-store", redirect: "manual", signal: AbortSignal.timeout(15000) };
    if (!["GET", "HEAD"].includes(request.method)) options.body = await request.arrayBuffer();
    const upstream = await fetch(target, options);
    const responseHeaders = new Headers({ "Cache-Control": "no-store" });
    const type = upstream.headers.get("content-type");
    if (type) responseHeaders.set("Content-Type", type);
    for (const cookie of upstream.headers.getSetCookie()) responseHeaders.append("Set-Cookie", cookie);
    const body = [204, 205, 304].includes(upstream.status) ? null : await upstream.arrayBuffer();
    return new Response(body, { status: upstream.status, headers: responseHeaders });
  } catch {
    return Response.json({ error: "감시 API에 연결할 수 없습니다. MONITOR_API_URL과 감시 /health를 확인해 주세요." }, { status: 502 });
  }
}
export { forward as GET, forward as POST, forward as PUT, forward as DELETE };
