import Link from "next/link";
import Counter from "../components/Counter";

export default function HomePage() {
  return (
    <div className="page-stack">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">THE SIMPLE NOTE EXPERIENCE</span>
          <h1>생각을 기록하는<br /><em>가장 가벼운 공간.</em></h1>
          <p>복잡한 설정 없이, 오늘 떠오른 생각을 자유롭게 적어 보세요. 작은 React 상태 변화부터 Next.js 메모 앱까지 직접 경험합니다.</p>
          <div className="hero-actions">
            <Link className="button button-primary" href="/notes">메모 쓰러 가기 <span aria-hidden="true">↗</span></Link>
            <a className="button button-ghost" href="#counter">카운터 실습 보기 ↓</a>
          </div>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="hero-paper"><span>YOUR SPACE TO THINK</span><strong>Make room<br />for ideas<span>.</span></strong><i>✳</i></div>
          <span className="spark spark-one">✧</span><span className="spark spark-two">✦</span>
        </div>
      </section>

      <section className="section-heading">
        <div><span className="eyebrow">PRACTICE 01</span><h2>작은 변화부터 시작해요</h2></div>
        <p>숫자를 올리고 초기화하면서 <code>useState</code>가 화면을 어떻게 바꾸는지 확인하세요.</p>
      </section>

      <Counter />

      <section className="bottom-cta">
        <div><span className="eyebrow">PRACTICE 02</span><h2>이제 생각을 남길 차례.</h2><p>메모를 등록하고, 수정하고, 삭제하는 모든 과정을 경험해 보세요.</p></div>
        <Link href="/notes" className="button button-outline">메모 페이지 열기 →</Link>
      </section>
    </div>
  );
}
