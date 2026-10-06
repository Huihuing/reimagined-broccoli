import Link from "next/link";

export default function Home() {
  return (
    <main className="shell">
      <section className="card hero">
        <p className="eyebrow">REIMAGINED BROCCOLI</p>
        <h1>작은 개발 블로그</h1>
        <p className="description">
          회원가입 기능 구현 과제를 위한 Next.js 프론트엔드입니다.
        </p>
        <Link className="button" href="/signup">
          회원가입
        </Link>
      </section>
    </main>
  );
}
