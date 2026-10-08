import "./globals.css";

export const metadata = {
  title: "Mini Watch | PostgreSQL 메모",
  description: "Next.js에서 Flask와 PostgreSQL 메모 API를 연결하는 심화 실습",
};

export default function RootLayout({ children }) {
  return <html lang="ko"><body>{children}</body></html>;
}
