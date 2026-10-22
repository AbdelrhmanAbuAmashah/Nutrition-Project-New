import { NextRequest } from "next/server";
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

async function forward(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> },
) {
  const ar = request.headers.get("accept-language")?.startsWith("ar");
  const fail = (status: number, code: string, message: string) =>
    Response.json(
      { error: { code, message } },
      { status, headers: { "Cache-Control": "no-store" } },
    );
  const headers = new Headers();
  for (const key of [
    "content-type",
    "cookie",
    "origin",
    "x-csrf-token",
    "idempotency-key",
    "accept-language",
  ]) {
    const value = request.headers.get(key);
    if (value) headers.set(key, value);
  }
  let body: Uint8Array | undefined;
  if (!["GET", "HEAD"].includes(request.method) && request.body) {
    const reader = request.body.getReader();
    const chunks: Uint8Array[] = [];
    let length = 0;
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      length += value.length;
      if (length > 131072) {
        await reader.cancel();
        return fail(
          413,
          "validation",
          ar ? "حجم الطلب أكبر من المسموح." : "The request is too large.",
        );
      }
      chunks.push(value);
    }
    body = new Uint8Array(length);
    let offset = 0;
    for (const chunk of chunks) {
      body.set(chunk, offset);
      offset += chunk.length;
    }
  }
  try {
    const path = (await params).path.map(encodeURIComponent).join("/");
    const base = (
      process.env.API_INTERNAL_URL || "http://127.0.0.1:8000"
    ).replace(/\/$/, "");
    const response = await fetch(
      `${base}/api/v1/${path}${request.nextUrl.search}`,
      {
        method: request.method,
        headers,
        body: body as BodyInit | undefined,
        redirect: "manual",
        cache: "no-store",
        signal: AbortSignal.timeout(15000),
      },
    );
    const output = new Headers({
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
    });
    for (const key of [
      "content-type",
      "content-disposition",
      "x-request-id",
      "retry-after",
    ]) {
      const value = response.headers.get(key);
      if (value) output.set(key, value);
    }
    for (const cookie of response.headers.getSetCookie())
      output.append("set-cookie", cookie);
    return new Response(response.body, {
      status: response.status,
      headers: output,
    });
  } catch {
    return fail(
      503,
      "service_unavailable",
      ar
        ? "الخدمة غير متاحة مؤقتاً. يرجى المحاولة بعد قليل."
        : "The service is temporarily unavailable. Please try again shortly.",
    );
  }
}
export { forward as GET, forward as POST, forward as PATCH, forward as DELETE };
