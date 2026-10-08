export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export async function apiRequest(path, options = {}) {
  let response;
  try {
    response = await fetch(`/api${path}`, {
      credentials: "include",
      cache: "no-store",
      ...options,
      headers: {
        ...(options.body ? { "Content-Type": "application/json" } : {}),
        ...(options.headers ?? {}),
      },
    });
  } catch {
    throw new ApiError("Flask 서버에 연결할 수 없습니다. 백엔드 실행 상태를 확인하세요.", 0);
  }
  let data;
  try {
    data = await response.json();
  } catch {
    throw new ApiError("서버 응답을 해석하지 못했습니다.", response.status);
  }
  if (!response.ok) {
    throw new ApiError(data.error || `요청 실패 (HTTP ${response.status})`, response.status);
  }
  return data;
}
