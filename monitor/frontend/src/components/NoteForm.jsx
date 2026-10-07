import { useEffect, useState } from "react";

const STATUSES = ["확인 전", "확인 중", "완료"];

export default function NoteForm({ note, onSave, onCancel, error }) {
  const [title, setTitle] = useState(note?.title ?? "");
  const [body, setBody] = useState(note?.body ?? "");
  const [status, setStatus] = useState(note?.status ?? "확인 전");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setTitle(note?.title ?? "");
    setBody(note?.body ?? "");
    setStatus(note?.status ?? "확인 전");
  }, [note]);

  async function handleSubmit(event) {
    event.preventDefault();
    setSaving(true);
    try {
      await onSave({ title, body, status });
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="panel detail-panel">
      <p className="eyebrow">{note ? `EDIT NOTE #${note.id}` : "NEW NOTE"}</p>
      <h2>{note ? "관찰 메모 수정" : "새 관찰 메모"}</h2>

      <form className="stack-form" onSubmit={handleSubmit}>
        <label>
          제목
          <input value={title} onChange={(event) => setTitle(event.target.value)} />
        </label>

        <label>
          내용
          <textarea
            rows="8"
            value={body}
            onChange={(event) => setBody(event.target.value)}
          />
        </label>

        <label>
          처리 상태
          <select value={status} onChange={(event) => setStatus(event.target.value)}>
            {STATUSES.map((item) => (
              <option key={item} value={item}>{item}</option>
            ))}
          </select>
        </label>

        {error && <p className="error-banner">{error}</p>}

        <div className="button-row">
          <button className="button" type="button" onClick={onCancel}>취소</button>
          <button className="button primary" disabled={saving}>
            {saving ? "저장 중..." : "저장"}
          </button>
        </div>
      </form>
    </section>
  );
}
