export default function EventList({
  events,
  summary,
  filters,
  onFilterChange,
  onRefresh,
  loading,
  error,
}) {
  function handleSubmit(event) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    onFilterChange({
      path: String(form.get("path") ?? ""),
      status: String(form.get("status") ?? ""),
    });
  }

  return (
    <section className="panel events-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">REQUEST EVENTS</p>
          <h2>요청 기록</h2>
        </div>
        <button className="button" type="button" onClick={onRefresh}>
          기록 새로고침
        </button>
      </div>

      <div className="summary-grid">
        <div className="summary-card">
          <span>조회 요청</span>
          <strong>{summary.total}</strong>
        </div>
        <div className="summary-card">
          <span>오류 요청</span>
          <strong>{summary.errors}</strong>
        </div>
      </div>

      <form className="filter-form" onSubmit={handleSubmit}>
        <input
          name="path"
          defaultValue={filters.path}
          placeholder="경로 검색 예: /board"
        />
        <input
          name="status"
          defaultValue={filters.status}
          inputMode="numeric"
          placeholder="상태 코드 예: 404"
        />
        <button className="button primary" type="submit">필터 적용</button>
        <button
          className="button"
          type="button"
          onClick={() => onFilterChange({ path: "", status: "" })}
        >
          조건 해제
        </button>
      </form>

      {error && <p className="error-banner">{error}</p>}
      {loading ? (
        <p className="empty-state">요청 기록을 불러오는 중입니다.</p>
      ) : events.length === 0 ? (
        <p className="empty-state">조건에 맞는 요청 기록이 없습니다.</p>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>번호</th>
                <th>메서드</th>
                <th>경로</th>
                <th>상태</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event) => (
                <tr key={event.id}>
                  <td>#{event.id}</td>
                  <td><span className="method-badge">{event.method}</span></td>
                  <td className="path-cell">{event.path}</td>
                  <td>
                    <span className={event.status >= 400 ? "status-code error" : "status-code"}>
                      {event.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
