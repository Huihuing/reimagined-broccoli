"use client";
import { useState } from "react";
import { apiRequest } from "../lib/api";

export default function EventList() {
  const [events, setEvents] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  async function reload() {
    setLoading(true); setError("");
    try {
      const payload = await apiRequest("/events");
      setEvents(payload.events);
    } catch (err) { setError(err.message); }
    finally { setLoading(false); }
  }
  return (
    <section className="panel" aria-label="일반 서비스 요청 기록">
      <h2>일반 서비스 요청 기록</h2>
      <button type="button" onClick={reload} disabled={loading}>기록 불러오기 / 다시 시도</button>
      {error && <p role="alert">{error}</p>}
      {events === null ? <p>기록 불러오기를 눌러 요청을 확인하세요.</p> : events.length === 0 ? <p>아직 요청 기록이 없습니다.</p> : (
        <div style={{overflowX: "auto"}}>
          <table><thead><tr><th>유형</th><th>방법</th><th>경로</th><th>상태 코드</th></tr></thead>
          <tbody>{events.map(event => <tr key={event.id}><td>{event.event_type}</td><td>{event.method}</td><td>{event.path}</td><td>{event.status}</td></tr>)}</tbody></table>
        </div>
      )}
    </section>
  );
}
