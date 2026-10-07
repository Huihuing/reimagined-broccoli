export default function DeleteConfirm({ note, onConfirm, onCancel, error }) {
  return (
    <section className="panel detail-panel">
      <p className="eyebrow">DELETE NOTE #{note.id}</p>
      <h2>메모 삭제 확인</h2>
      <p><strong>{note.title}</strong> 메모를 삭제하시겠습니까?</p>
      <p className="muted">이 화면을 여는 것만으로는 삭제되지 않습니다.</p>

      {error && <p className="error-banner">{error}</p>}

      <div className="button-row">
        <button className="button" type="button" onClick={onCancel}>취소</button>
        <button className="button danger" type="button" onClick={onConfirm}>삭제 확정</button>
      </div>
    </section>
  );
}
