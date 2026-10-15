"use client";
import { useState } from "react";
import { apiRequest } from "../lib/api";

export default function AnalysisClient() {
  const [afterId, setAfterId] = useState(null);
  const [referenceTime, setReferenceTime] = useState(null);
  const [threshold, setThreshold] = useState("10");
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  async function start() {
    setBusy(true);
    setError("");
    setReport(null);
    setReferenceTime(null);
    try {
      const result = await apiRequest("/analysis/start");
      setAfterId(result.after_id);
      setNotice("새 관찰 시작: 기존 기록은 지우지 않고 마지막 원본 ID를 경계로 저장했습니다.");
    } catch (err) {
      setAfterId(null);
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function analyze() {
    if (afterId === null) {
      setError("먼저 새 관찰 시작을 누르세요.");
      return;
    }
    const number = Number(threshold);
    if (!Number.isInteger(number) || number < 1 || number > 10000) {
      setError("기준은 1~10000 사이의 정수로 입력해 주세요.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const params = new URLSearchParams({ after_id: String(afterId), threshold: String(number) });
      // IMPORTANT: threshold 10 -> 20 reuses precisely the SAME first-result time.
      if (referenceTime) params.set("reference_time", referenceTime);
      const data = await apiRequest("/analysis?" + params.toString());
      if (!referenceTime) setReferenceTime(data.reference_time);
      setReport(data);
      setNotice("동일 원본 DB 범위의 HTTP 규칙 분석 결과입니다.");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  const card = report?.card;
  return (
    <section className="panel" aria-labelledby="day3-heading" style={{marginTop: 28}}>
      <div className="panel-heading">
        <span className="tag">DAY 3 / REAL HTTP EVIDENCE</span>
        <h2 id="day3-heading">실제 요청 로그 분석</h2>
        <p>같은 관찰 구간에서 목록 조회만 계산합니다. 뒤따른 404는 근거로만 보여 줍니다.</p>
      </div>
      <div className="actions" style={{flexWrap:"wrap",alignItems:"flex-end"}}>
        <button type="button" className="secondary" onClick={start} disabled={busy}>새 관찰 시작</button>
        <label>비교 기준
          <input type="number" min="1" max="10000" step="1" value={threshold} onChange={e => setThreshold(e.target.value)} style={{maxWidth:120}} />
        </label>
        <button type="button" className="primary" onClick={analyze} disabled={busy || afterId === null}>
          결과 불러오기
        </button>
      </div>
      {afterId !== null && <p>원본 ID 경계: <strong>{afterId}</strong> · 기준시각: <code>{referenceTime || "첫 분석에서 확정"}</code></p>}
      {notice && <p role="status">{notice}</p>}
      {error && <p role="alert" className="error">{error}</p>}
      {card && <article aria-label="HTTP 규칙 카드" style={{border:"1px solid var(--border, #ddd)",padding:18,borderRadius:12,marginTop:16}}>
        <h3>{card.rule}</h3>
        <p>관찰값: <strong>{card.observed}회</strong> · 비교 기준: <strong>{card.threshold}회</strong></p>
        <p>판정: <strong>{card.verdict}</strong></p>
        <p>{card.reason}</p>
        <p>조회 근거: {card.view_count}행 · 뒤따른 404: {card.following_error_count}행 · 전체 근거: {card.records.length}행</p>
        <details open>
          <summary>근거 보기 ({card.evidence.length}행)</summary>
          <div style={{overflowX:"auto"}}>
            <table>
              <thead><tr><th>원본 ID</th><th>DB 수신시각</th><th>방법</th><th>경로</th><th>상태</th><th>종류</th></tr></thead>
              <tbody>{card.records.map(row => (
                <tr key={row.id}>
                  <td>{row.id}</td><td>{row.received_at}</td><td>{row.method}</td>
                  <td>{row.path}</td><td>{row.status_code}</td><td>{row.kind}</td>
                </tr>
              ))}</tbody>
            </table>
          </div>
        </details>
        <p style={{fontSize:13}}>같은 서비스에서 시간상 뒤따른 기록이라는 뜻일 뿐 사용자·IP·인과관계·공격 여부는 확인되지 않습니다.</p>
      </article>}
    </section>
  );
}
