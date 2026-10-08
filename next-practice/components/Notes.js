"use client";

import { useRef, useState } from "react";

const initialNotes = [
  { id: 1, content: "오늘 배운 Next.js 내용을 정리하기" },
  { id: 2, content: "작은 아이디어도 메모로 남겨 보기" },
];

export default function Notes() {
  const [notes, setNotes] = useState(initialNotes);
  const [text, setText] = useState("");
  const [editingId, setEditingId] = useState(null);
  const [deleteId, setDeleteId] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const nextId = useRef(3);
  const noteToDelete = notes.find((note) => note.id === deleteId);

  function resetForm() {
    setEditingId(null);
    setText("");
    setError("");
  }

  function submitNote(event) {
    event.preventDefault();
    const value = text.trim();
    if (!value) {
      setError("메모 내용을 입력해 주세요. 공백만 입력할 수 없습니다.");
      setNotice("");
      return;
    }

    if (editingId !== null) {
      if (!notes.some((note) => note.id === editingId)) {
        resetForm();
        setNotice("수정하려는 메모를 찾을 수 없습니다.");
        return;
      }
      setNotes((previous) =>
        previous.map((note) => (note.id === editingId ? { ...note, content: value } : note))
      );
      setNotice("메모를 수정했어요.");
    } else {
      const id = nextId.current++;
      setNotes((previous) => [...previous, { id, content: value }]);
      setNotice("새 메모를 추가했어요.");
    }
    resetForm();
  }

  function beginEdit(note) {
    setEditingId(note.id);
    setText(note.content);
    setError("");
    setNotice("");
  }

  function confirmDelete() {
    if (deleteId === null) return;
    setNotes((previous) => previous.filter((note) => note.id !== deleteId));
    if (editingId === deleteId) resetForm();
    setDeleteId(null);
    setNotice("메모를 삭제했어요.");
  }

  return (
    <div className="notes-grid">
      <section className="editor-panel" aria-label="메모 입력">
        <div className="panel-index"><span>01 / WRITE</span><span aria-hidden="true">✳</span></div>
        <h2>{editingId === null ? "새 메모 작성" : "메모 수정하기"}</h2>
        <p className="panel-help">{editingId === null ? "오늘의 생각을 한 줄씩 쌓아 보세요." : "기존 내용을 수정해도 다른 메모는 그대로 유지됩니다."}</p>
        <form onSubmit={submitNote} noValidate>
          <label className="field-label" htmlFor="note-content">메모 내용</label>
          <textarea
            id="note-content"
            placeholder="지금 생각나는 것을 적어 보세요..."
            rows={6}
            value={text}
            onChange={(event) => { setText(event.target.value); if (error) setError(""); }}
            aria-invalid={Boolean(error)}
            aria-describedby={error ? "note-error" : undefined}
          />
          {error && <p className="field-error" id="note-error" role="alert">{error}</p>}
          <div className="editor-actions">
            <button className="button button-primary" type="submit">
              {editingId === null ? "메모 추가하기 ↗" : "수정 내용 저장 ↗"}
            </button>
            {editingId !== null && <button className="button button-subtle" type="button" onClick={() => { resetForm(); setNotice("수정을 취소했어요. 기존 메모는 그대로예요."); }}>수정 취소</button>}
          </div>
        </form>
        <div className="panel-footnote"><span aria-hidden="true">ⓘ</span> 새로고침하면 처음 메모로 돌아옵니다. 서버 DB에는 저장되지 않아요.</div>
      </section>

      <section className="list-panel" aria-label="메모 목록">
        <div className="list-heading">
          <div><span className="eyebrow">02 / YOUR COLLECTION</span><h2>저장한 생각 <span className="note-count">{notes.length.toString().padStart(2, "0")}</span></h2></div>
          <span className="list-decor" aria-hidden="true">✺</span>
        </div>
        {notice && <p className="notice" role="status">{notice}</p>}
        {notes.length === 0 ? (
          <div className="empty-notes"><span aria-hidden="true">✎</span><h3>아직 메모가 없어요.</h3><p>왼쪽 입력칸에서 첫 번째 메모를 작성해 보세요.</p></div>
        ) : (
          <ul className="note-list">
            {notes.map((note, index) => (
              <li className="note-item" key={note.id}>
                <div className="note-number">{String(index + 1).padStart(2, "0")}</div>
                <div className="note-body">
                  <p>{note.content}</p>
                  <div className="note-actions">
                    <button className="text-button" type="button" onClick={() => beginEdit(note)}>수정</button>
                    <button className="text-button danger" type="button" onClick={() => { setDeleteId(note.id); setNotice(""); }}>삭제</button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      {noteToDelete && (
        <div className="dialog-backdrop">
          <div className="dialog" role="alertdialog" aria-modal="true" aria-labelledby="delete-title" aria-describedby="delete-description">
            <span className="dialog-symbol" aria-hidden="true">!</span>
            <h2 id="delete-title">이 메모를 삭제할까요?</h2>
            <p id="delete-description">삭제하면 목록에서 해당 메모만 사라져요. 취소하면 원래 내용이 유지됩니다.</p>
            <div className="dialog-preview">{noteToDelete.content}</div>
            <div className="dialog-actions">
              <button className="button button-subtle" type="button" onClick={() => setDeleteId(null)}>취소</button>
              <button className="button button-danger" type="button" onClick={confirmDelete}>삭제 확인</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
