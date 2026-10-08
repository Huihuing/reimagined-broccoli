const { test, expect } = require("@playwright/test");

test("홈 카운터 증가·초기화와 메모 Link 이동", async ({ page }) => {
  await page.goto("/");
  const counter = page.locator(".counter-value");
  await expect(counter).toHaveText("0");
  await page.getByRole("button", { name: "+1 증가" }).click();
  await page.getByRole("button", { name: "+1 증가" }).click();
  await expect(counter).toHaveText("2");
  await page.getByRole("button", { name: "초기화" }).click();
  await expect(counter).toHaveText("0");
  await page.getByRole("link", { name: "메모", exact: true }).click();
  await expect(page).toHaveURL(/\/notes$/);
  await expect(page.getByRole("heading", { name: "나의 메모." })).toBeVisible();
});

test("중복 내용은 서로 다른 ID이고 수정·취소·공백 검증을 거친다", async ({ page }) => {
  await page.goto("/notes");
  const input = page.getByLabel("메모 내용");
  const add = page.getByRole("button", { name: /메모 추가하기/ });
  await input.fill("중복 내용");
  await add.click();
  await input.fill("중복 내용");
  await add.click();

  const matches = page.locator(".note-item").filter({ hasText: "중복 내용" });
  await expect(matches).toHaveCount(2);
  await matches.nth(1).getByRole("button", { name: "수정" }).click();
  await expect(input).toHaveValue("중복 내용");
  await input.fill("두 번째 항목만 수정");
  await page.getByRole("button", { name: /수정 내용 저장/ }).click();
  await expect(matches).toHaveCount(1);
  await expect(page.locator(".note-item").filter({ hasText: "두 번째 항목만 수정" })).toHaveCount(1);

  await matches.first().getByRole("button", { name: "수정" }).click();
  await input.fill("취소할 변경");
  await page.getByRole("button", { name: "수정 취소" }).click();
  await expect(matches).toHaveCount(1);

  await matches.first().getByRole("button", { name: "수정" }).click();
  await input.fill("  ");
  await page.getByRole("button", { name: /수정 내용 저장/ }).click();
  await expect(page.getByRole("alert")).toContainText("공백만");
  await expect(matches).toHaveCount(1);
  await page.getByRole("button", { name: "수정 취소" }).click();
  await input.fill("   ");
  await add.click();
  await expect(page.getByRole("alert")).toContainText("공백만");
  await expect(page.locator(".note-item")).toHaveCount(4);
});

test("삭제 취소·확정, 수정 중 삭제, 빈 목록, 새로고침 복원을 확인한다", async ({ page }) => {
  await page.goto("/notes");
  await expect(page.locator(".note-item")).toHaveCount(2);
  const first = page.locator(".note-item").first();
  await first.getByRole("button", { name: "수정" }).click();
  await first.getByRole("button", { name: "삭제" }).click();
  await expect(page.getByRole("alertdialog")).toBeVisible();
  await page.getByRole("alertdialog").getByRole("button", { name: "취소" }).click();
  await expect(page.locator(".note-item")).toHaveCount(2);
  await expect(page.getByRole("button", { name: /수정 내용 저장/ })).toBeVisible();

  await page.locator(".note-item").first().getByRole("button", { name: "삭제" }).click();
  await page.getByRole("alertdialog").getByRole("button", { name: "삭제 확인" }).click();
  await expect(page.locator(".note-item")).toHaveCount(1);
  await expect(page.getByRole("button", { name: /메모 추가하기/ })).toBeVisible();
  await expect(page.getByLabel("메모 내용")).toHaveValue("");

  await page.locator(".note-item").first().getByRole("button", { name: "삭제" }).click();
  await page.getByRole("alertdialog").getByRole("button", { name: "삭제 확인" }).click();
  await expect(page.getByText("아직 메모가 없어요.")).toBeVisible();
  await page.reload();
  await expect(page.locator(".note-item")).toHaveCount(2);
});
