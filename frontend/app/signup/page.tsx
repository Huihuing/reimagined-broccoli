"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function SignupPage() {
  const [message, setMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setMessage("");
    setSubmitting(true);

    const form = new FormData(event.currentTarget);
    const password = String(form.get("password") ?? "");
    const passwordConfirm = String(form.get("passwordConfirm") ?? "");

    if (password !== passwordConfirm) {
      setMessage("비밀번호가 서로 일치하지 않습니다.");
      setSubmitting(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/signup`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: String(form.get("username") ?? ""),
          email: String(form.get("email") ?? ""),
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        const detail =
          typeof data.detail === "string"
            ? data.detail
            : "입력값을 확인해 주세요.";
        setMessage(detail);
        return;
      }

      event.currentTarget.reset();
      setMessage(`${data.username}님, 회원가입이 완료되었습니다.`);
    } catch {
      setMessage("서버에 연결할 수 없습니다.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="shell">
      <section className="card signup-card">
        <Link className="back-link" href="/">
          ← 홈으로
        </Link>
        <p className="eyebrow">SIGN UP</p>
        <h1>회원가입</h1>
        <p className="description">
          아이디, 이메일, 비밀번호를 입력해 계정을 생성하세요.
        </p>

        <form className="signup-form" onSubmit={handleSubmit}>
          <label>
            아이디
            <input
              name="username"
              minLength={3}
              maxLength={50}
              pattern="[A-Za-z0-9_]+"
              autoComplete="username"
              required
            />
          </label>

          <label>
            이메일
            <input name="email" type="email" autoComplete="email" required />
          </label>

          <label>
            비밀번호
            <input
              name="password"
              type="password"
              minLength={8}
              maxLength={72}
              autoComplete="new-password"
              required
            />
          </label>

          <label>
            비밀번호 확인
            <input
              name="passwordConfirm"
              type="password"
              minLength={8}
              maxLength={72}
              autoComplete="new-password"
              required
            />
          </label>

          <button className="button" type="submit" disabled={submitting}>
            {submitting ? "가입 중..." : "회원가입"}
          </button>
        </form>

        {message && <p className="message" role="status">{message}</p>}
      </section>
    </main>
  );
}
