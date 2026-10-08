import Link from "next/link";
import "./globals.css";

export const metadata = {
  title: "Little Notes | Next.js 메모 실습",
  description: "Next.js App Router와 React state로 완성한 메모 앱",
};

export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <body>
        <div className="site-shell">
          <header className="site-header">
            <div className="brand">
              <span className="brand-icon" aria-hidden="true">✦</span>
              <span>little notes<span className="brand-period">.</span></span>
            </div>
            <nav className="site-nav" aria-label="주요 메뉴">
              <Link href="/">홈</Link>
              <Link href="/notes">메모</Link>
            </nav>
            <span className="header-label">NEXT.JS LAB · 01</span>
          </header>
          <main id="main-content">{children}</main>
          <footer className="site-footer">
            <span>Next.js × React</span>
            <span>작은 기록이 모여 하루를 만듭니다.</span>
          </footer>
        </div>
      </body>
    </html>
  );
}
