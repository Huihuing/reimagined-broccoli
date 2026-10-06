import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Broccoli Blog",
  description: "회원가입 과제용 미니 블로그",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
