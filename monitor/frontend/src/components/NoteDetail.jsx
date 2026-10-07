export default function NoteDetail({ note, onEdit, onDelete }) {
  if (!note) {
    return (
      <section className="panel detail-panel">
        <p className="empty-state">목록에서 메모를 선택하거나 새 메모를 작성하세요.</p>
      </section>
    );
  }

  return (
    <section className="panel detail-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">NOTE #{note.id}</p>
          <h2>{note.title}</h2>
        </div>
        <span className="note-status large">{note.status}</span>
      </div>

      <div className="note-body">{note.body}</div>

      <div className="button-row top-gap">
        <button className="button primary" type="button" onClick={onEdit}>
          수정
        </button>
        <button className="button danger" type="button" onClick={onDelete}>
          삭제
        </button>
      </div>
    </section>
  );
}
