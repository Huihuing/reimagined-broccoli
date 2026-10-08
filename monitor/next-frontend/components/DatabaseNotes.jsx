"use client";

import { useEffect, useState } from "react";
import { apiRequest } from "../lib/api";

const emptyForm = { title: "", body: "", status: "확인 전" };
const statuses = ["확인 전", "확인 중", "완료"];

export default function DatabaseNotes() {
  const [checking, setChecking] = useState(true);
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [notes, setNotes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [mode, setMode] = useState("create");
  const [form, setForm] = useState({ ...emptyForm });
  const [confirming, setConfirming] = useState(null);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);

  async function refreshNotes() {
    const data = await apiRequest("/notes");
    setNotes(data.notes);
    return data.notes;
  }

  useEffect(() => {
    let active = true;
    async function restore() {
      try {
        const session = await apiRequest("/auth/session");
        if (!active) return;
        if (session.authenticated) {
          setUser(session.user);
          const data = await apiRequest("/notes");
          if (active) setNotes(data.notes);
        }
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setChecking(false);
      }
    }
    restore();
    return () => { active = false; };
  }, []);

  function clearMessages() {
    setError("");
    setNotice("");
  }

  function beginCreate() {
    setSelected(null);
    setForm({ ...emptyForm });
    setMode("create");
    clearMessages();
  }

  async function signIn(event) {
    event.preventDefault();
    clearMessages();
    setBusy(true);
    try {
      const data = await apiRequest("/auth/login", {
        method: "POST", body: JSON.stringify({ username, password }),
      });
      setUser(data.user);
      setPassword("");
      await refreshNotes();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function signOut() {
    setBusy(true);
    clearMessages();
    try {
      await apiRequest("/auth/logout", { method: "POST" });
      setUser(null);
      setNotes([]);
      setConfirming(null);
      beginCreate();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function openNote(id) {
    clearMessages();
    setBusy(true);
    try {
      const { note } = await apiRequest(`/notes/${id}`);
      setSelected(note);
      setMode("view");
    } catch (err) {
      setError(err.message);
      if (err.status === 404) {
        setSelected(null);
        setMode("create");
        try { await refreshNotes(); } catch { /* original error remains visible */ }
      }
    } finally {
      setBusy(false);
    }
  }

  function beginEdit() {
    if (!selected) return;
    setForm({
      title: selected.title,
      body: selected.body,
      status: selected.status,
    });
    setMode("edit");
    clearMessages();
  }

  function cancelEdit() {
    // Intentionally no PUT request: PostgreSQL retains the original note.
    setForm({ ...emptyForm });
    setMode("view");
    setError("");
    setNotice("수정을 취소했습니다. DB의 원본은 그대로입니다.");
  }

  async function submitNote(event) {
    event.preventDefault();
    clearMessages();
    if (!form.title.trim() || !form.body.trim()) {
      setError("제목과 내용은 공백만 입력할 수 없습니다. 저장하지 않았습니다.");
      return;
    }
    setBusy(true);
    const isEdit = mode === "edit";
    const path = isEdit ? `/notes/${selected.id}` : "/notes";
    try {
      const { note } = await apiRequest(path, {
        method: isEdit ? "PUT" : "POST",
        body: JSON.stringify({
          title: form.title.trim(),
          body: form.body.trim(),
          status: form.status,
        }),
      });
      await refreshNotes();
      // Force an actual Flask GET detail after the write rather than trusting POST/PUT alone.
      const detail = await apiRequest(`/notes/${note.id}`);
      setSelected(detail.note);
      setMode("view");
      setForm({ ...emptyForm });
      setNotice(isEdit ? "수정 결과를 DB에서 다시 조회했습니다." : "등록 후 DB의 상세 조회를 완료했습니다.");
    } catch (err) {
      setError(`저장 실패 (HTTP ${err.status}): ${err.message}`);
      // Do not show a success notice or discard pending edits on failure.
    } finally {
      setBusy(false);
    }
  }

  async function confirmDelete() {
    if (!confirming) return;
    clearMessages();
    setBusy(true);
    try {
      await apiRequest(`/notes/${confirming.id}`, { method: "DELETE" });
      await refreshNotes();
      if (selected?.id === confirming.id) {
        setSelected(null);
        setForm({ ...emptyForm });
        setMode("create");
      }
      setConfirming(null);
      setNotice("삭제 후 DB 목록을 다시 조회했습니다.");
    } catch (err) {
      setError(`삭제 실패 (HTTP ${err.status}): ${err.message}`);
      // Keep the dialog visible on failure. Nothing is reported as deleted.
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark">✳</span> mini watch <span className="brand-separator">/</span> notes db</div>
        <span className="topbar-label">NEXT.JS + FLASK + POSTGRESQL</span>
      </header>
      <div className="intro"><p className="eyebrow">ADVANCED ASSIGNMENT 03 + 04</p><h1>관찰 기록을 <em>안전하게 저장.</em></h1><p>Flask API를 통해 PostgreSQL에 실제 저장합니다. 새로고침해도 기록은 유지됩니다.</p></div>
      {checking ? (
        <section className="panel"><p role="status">로그인 세션을 확인하고 있습니다...</p></section>
      ) : !user ? (
        <section className="panel login-panel">
          <div className="panel-heading"><span className="tag">01 / AUTHENTICATION</span><h2>운영자 로그인</h2><p>기존 Flask 계정으로 로그인하세요. 로그인 후 메모 API를 사용할 수 있습니다.</p></div>
          <form onSubmit={signIn} className="form">
            <label htmlFor="username">아이디</label><input id="username" value={username} onChange={e => setUsername(e.target.value)} autoComplete="username" />
            <label htmlFor="password">비밀번호</label><input id="password" type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" />
            {error && <p role="alert" className="error">{error}</p>}
            <button className="primary" type="submit" disabled={busy}>로그인 →</button>
          </form>
        </section>
      ) : (
        <>
          <div className="accountbar"><span>● <strong>{user.name}</strong> 운영자 계정 연결됨</span><div><button onClick={() => { clearMessages(); refreshNotes().catch(err => setError(err.message)); }} disabled={busy}>목록 새로고침</button><button onClick={signOut} disabled={busy}>로그아웃</button></div></div>
          {error && <p role="alert" className="error global-error">{error}</p>}
          {notice && <p role="status" className="notice">{notice}</p>}
          <div className="columns">
            <section className="panel list-panel">
              <div className="panel-heading"><span className="tag">02 / DATABASE LIST</span><div className="heading-row"><h2>저장된 메모</h2><span className="count">{notes.length}</span></div></div>
              <button className="primary new-note" type="button" onClick={beginCreate}>+ 새 메모</button>
              {notes.length === 0 ? <p className="empty">DB에 메모가 없습니다. 새 메모를 등록해 보세요.</p> :
                <ul className="note-list">{notes.map(note => (
                  <li key={note.id}>
                    <button type="button" disabled={busy} className={selected?.id === note.id ? "note selected" : "note"} onClick={() => openNote(note.id)}>
                      <span className="note-top"><span>#{note.id}</span><span className="status">{note.status}</span></span>
                      <strong>{note.title}</strong><span className="preview">{note.body}</span>
                    </button>
                  </li>
                ))}</ul>}
            </section>
            <section className="panel detail-panel">
              <div className="panel-heading"><span className="tag">03 / DETAILS & ACTIONS</span><h2>{mode === "create" ? "새 메모 등록" : mode === "edit" ? "기존 메모 수정" : "메모 상세"}</h2></div>
              {mode === "view" && selected ? (
                <div className="detail">
                  <div className="detail-meta">ID #{selected.id} · {selected.status}</div>
                  <h3>{selected.title}</h3><p className="detail-body">{selected.body}</p>
                  <div className="actions">
                    <button className="primary" onClick={beginEdit} disabled={busy}>수정</button>
                    <button className="danger-button" onClick={() => { clearMessages(); setConfirming(selected); }} disabled={busy}>삭제</button>
                  </div>
                </div>
              ) : (
                <form className="form" onSubmit={submitNote} noValidate>
                  <label htmlFor="note-title">제목</label>
                  <input id="note-title" placeholder="기록 제목" value={form.title} onChange={e => { setForm({ ...form, title: e.target.value }); setError(""); }} />
                  <label htmlFor="note-body">내용</label>
                  <textarea id="note-body" rows={7} placeholder="관찰한 내용을 작성하세요..." value={form.body} onChange={e => { setForm({ ...form, body: e.target.value }); setError(""); }} />
                  <label htmlFor="note-status">처리 상태</label>
                  <select id="note-status" value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>{statuses.map(s => <option key={s} value={s}>{s}</option>)}</select>
                  <div className="actions"><button className="primary" disabled={busy} type="submit">{mode === "edit" ? "수정 저장" : "DB에 등록"}</button>{mode === "edit" && <button type="button" className="secondary" disabled={busy} onClick={cancelEdit}>수정 취소</button>}</div>
                </form>
              )}
            </section>
          </div>
          {confirming && (
            <div className="backdrop"><div className="dialog" role="alertdialog" aria-modal="true" aria-labelledby="delete-heading" aria-describedby="delete-description">
              <h2 id="delete-heading">메모를 삭제할까요?</h2><p id="delete-description">#{confirming.id} {confirming.title} — 취소하면 DELETE 요청을 보내지 않습니다.</p>
              {error && <p role="alert" className="error">{error}</p>}
              <div className="actions"><button className="secondary" disabled={busy} onClick={() => { setConfirming(null); clearMessages(); }}>삭제 취소</button><button className="danger-button" disabled={busy} onClick={confirmDelete}>삭제 확정</button></div>
            </div></div>
          )}
        </>
      )}
      <footer className="footer">Flask session · PostgreSQL observation_notes · 브라우저와 DB는 API로만 통신</footer>
    </main>
  );
}
