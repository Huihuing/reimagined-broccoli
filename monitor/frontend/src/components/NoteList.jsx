export default function NoteList({
  notes,
  selectedId,
  onSelect,
  onCreate,
  onRefresh,
}) {
  return (
    <section className="panel notes-list-panel">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">OBSERVATION NOTES</p>
          <h2>관찰 메모</h2>
        </div>
        <div className="button-row">
          <button className="button" type="button" onClick={onRefresh}>
            메모 새로고침
          </button>
          <button className="button primary" type="button" onClick={onCreate}>
            새 메모
          </button>
        </div>
      </div>

      {notes.length === 0 ? (
        <p className="empty-state">저장된 관찰 메모가 없습니다.</p>
      ) : (
        <div className="note-list">
          {notes.map((note) => (
            <button
              className={note.id === selectedId ? "note-item selected" : "note-item"}
              key={note.id}
              type="button"
              onClick={() => onSelect(note.id)}
            >
              <span className="note-number">#{note.id}</span>
              <span className="note-title">{note.title}</span>
              <span className="note-status">{note.status}</span>
            </button>
          ))}
        </div>
      )}
    </section>
  );
}
