export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiRequest(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    credentials: "include",
    ...options,
    headers: {
      ...(options.body ? { "Content-Type": "application/json" } : {}),
      ...(options.headers ?? {}),
    },
  });

  const payload = await response
    .json()
    .catch(() => ({ error: "서버 응답을 읽을 수 없습니다." }));

  if (!response.ok) {
    throw new ApiError(
      payload.error ?? "요청을 처리하지 못했습니다.",
      response.status,
    );
  }

  return payload;
}
