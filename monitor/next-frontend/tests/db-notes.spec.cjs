const { test, expect } = require("@playwright/test");

async function login(page) {
  await page.goto("/");
  await expect(page.getByLabel("아이디")).toBeVisible();
  await page.getByLabel("아이디").fill("admin");
  await page.getByLabel("비밀번호").fill("test-password");
  await page.getByRole("button", { name: "로그인 →" }).click();
  await expect(page.getByText("운영자 계정 연결됨")).toBeVisible();
}

async function create(page, title, body) {
  await page.getByRole("button", { name: "+ 새 메모" }).click();
  await page.getByLabel("제목").fill(title);
  await page.getByLabel("내용").fill(body);
  await page.getByRole("button", { name: "DB에 등록" }).click();
  await expect(page.getByText("등록 후 DB의 상세 조회를 완료했습니다.")).toBeVisible();
  return Number((await page.locator(".detail-meta").innerText()).match(/#(\d+)/)[1]);
}

test("Flask + PostgreSQL 로그인/목록/상세/등록/수정/삭제와 새로고침 영구 저장", async ({ page }) => {
  await page.goto("/");
  const unauthorized = await page.request.get("/api/notes");
  expect(unauthorized.status()).toBe(401);

  await login(page);
  const title = "DB 통합 저장 확인";
  const id = await create(page, title, "첫 내용");
  await page.reload();
  await expect(page.getByText("운영자 계정 연결됨")).toBeVisible();
  await expect(page.locator(".note").filter({ hasText: title })).toHaveCount(1);

  await page.locator(".note").filter({ hasText: title }).click();
  await expect(page.locator(".detail-body")).toHaveText("첫 내용");
  const fetched = await page.request.get(`/api/notes/${id}`);
  expect(fetched.status()).toBe(200);
  expect((await fetched.json()).note.body).toBe("첫 내용");

  await page.getByRole("button", { name: "수정", exact: true }).click();
  await page.getByLabel("내용").fill("취소하는 문장");
  await page.getByRole("button", { name: "수정 취소" }).click();
  expect((await (await page.request.get(`/api/notes/${id}`)).json()).note.body).toBe("첫 내용");

  await page.getByRole("button", { name: "수정", exact: true }).click();
  await page.getByLabel("내용").fill("영구 수정된 내용");
  await page.getByLabel("처리 상태").selectOption("완료");
  await page.getByRole("button", { name: "수정 저장" }).click();
  await expect(page.locator(".detail-body")).toHaveText("영구 수정된 내용");
  await page.reload();
  await page.locator(".note").filter({ hasText: title }).click();
  await expect(page.locator(".detail-body")).toHaveText("영구 수정된 내용");
  await expect(page.locator(".detail-meta")).toContainText("완료");

  let sentDeletes = 0;
  page.on("request", r => { if (r.method() === "DELETE" && r.url().includes("/api/notes/")) sentDeletes++; });
  await page.getByRole("button", { name: "삭제", exact: true }).click();
  await page.getByRole("button", { name: "삭제 취소" }).click();
  expect(sentDeletes).toBe(0);
  expect((await page.request.get(`/api/notes/${id}`)).status()).toBe(200);
  await page.getByRole("button", { name: "삭제", exact: true }).click();
  await page.getByRole("button", { name: "삭제 확정" }).click();
  await expect(page.getByText("삭제 후 DB 목록을 다시 조회했습니다.")).toBeVisible();
  expect(sentDeletes).toBe(1);
  await page.reload();
  await expect(page.locator(".note").filter({ hasText: title })).toHaveCount(0);
  expect((await page.request.get(`/api/notes/${id}`)).status()).toBe(404);
});

test("Flask 400/404 거절을 실패로 보여 주며 원본 메모를 보존", async ({ page }) => {
  await login(page);
  const id = await create(page, "공백과 오류 검사", "기존 본문");
  await page.getByRole("button", { name: "수정", exact: true }).click();
  await page.getByLabel("내용").fill("    ");
  await page.getByRole("button", { name: "수정 저장" }).click();
  await expect(page.locator(".global-error")).toContainText("공백");
  const preserved = await page.request.get(`/api/notes/${id}`);
  expect((await preserved.json()).note.body).toBe("기존 본문");

  const invalid = await page.request.put(`/api/notes/${id}`, {
    data: { title: "테스트", body: "  ", status: "완료" },
  });
  expect(invalid.status()).toBe(400);
  expect((await (await page.request.get(`/api/notes/${id}`)).json()).note.body).toBe("기존 본문");

  await page.getByLabel("내용").fill("서버 삭제 후 수정");
  expect((await page.request.delete(`/api/notes/${id}`)).status()).toBe(200);
  await page.getByRole("button", { name: "수정 저장" }).click();
  await expect(page.locator(".global-error")).toContainText("HTTP 404");
  await expect(page.getByText("수정 결과를 DB에서 다시 조회했습니다.")).toHaveCount(0);

  await page.getByRole("button", { name: "목록 새로고침" }).click();
  const secondId = await create(page, "없는 DELETE 검사", "삭제 취소와 실패 확인");
  await page.getByRole("button", { name: "삭제", exact: true }).click();
  expect((await page.request.delete(`/api/notes/${secondId}`)).status()).toBe(200);
  await page.getByRole("button", { name: "삭제 확정" }).click();
  await expect(page.locator(".dialog .error")).toContainText("HTTP 404");
  await expect(page.getByText("삭제 후 DB 목록을 다시 조회했습니다.")).toHaveCount(0);
  await page.getByRole("button", { name: "삭제 취소" }).click();
  await page.getByRole("button", { name: "목록 새로고침" }).click();

  const missing = await page.request.get("/api/notes/999999999");
  expect(missing.status()).toBe(404);
  const missingUpdate = await page.request.put("/api/notes/999999999", { data: { title: "x", body: "y" } });
  expect(missingUpdate.status()).toBe(404);
  const missingDelete = await page.request.delete("/api/notes/999999999");
  expect(missingDelete.status()).toBe(404);
});
