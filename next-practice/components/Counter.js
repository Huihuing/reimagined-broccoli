"use client";

import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <section className="counter-card" id="counter" aria-label="숫자 카운터 실습">
      <div className="counter-description">
        <div className="decorative-square" aria-hidden="true">↗</div>
        <div><h3>숫자 카운터</h3><p>버튼을 누르면 React state가 즉시 바뀝니다.</p></div>
      </div>
      <div className="counter-controls">
        <output className="counter-value" aria-live="polite">{count}</output>
        <button className="button button-primary" type="button" onClick={() => setCount((value) => value + 1)}>+1 증가</button>
        <button className="button button-subtle" type="button" onClick={() => setCount(0)}>초기화</button>
      </div>
    </section>
  );
}
