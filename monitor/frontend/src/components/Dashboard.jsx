import { useEffect, useState } from "react";

import { fetchEvents } from "../api/events";
import {
  createNote,
  deleteNote,
  fetchNote,
  fetchNotes,
  updateNote,
} from "../api/notes";
import DeleteConfirm from "./DeleteConfirm";
import EventList from "./EventList";
import NoteDetail from "./NoteDetail";
import NoteForm from "./NoteForm";
import NoteList from "./NoteList";

export default function Dashboard({ user, onLogout }) {
  const [events, setEvents] = useState([]);
  const [summary, setSummary] = useState({ total: 0, errors: 0 });
  const [filters, setFilters] = useState({ path: "", status: "" });
  const [eventError, setEventError] = useState("");
  const [eventsLoading, setEventsLoading] = useState(true);

  const [notes, setNotes] = useState([]);
  const [selectedNote, setSelectedNote] = useState(null);
  const [mode, setMode] = useState("detail");
  const [noteError, setNoteError] = useState("");
  const [message, setMessage] = useState("");

  async function loadEvents(nextFilters = filters) {
    setEventsLoading(true);
    setEventError("");
    try {
      const payload = await fetchEvents(nextFilters);
      setEvents(payload.events);
      setSummary(payload.summary);
      setFilters({
        path: payload.filters.path ?? "",
        status: payload.filters.status ?? "",
      });
    } catch (error) {
      setEventError(error.message);
    } finally {
      setEventsLoading(false);
    }
  }

  async function loadNotes() {
    setNoteError("");
    try {
      const payload = await fetchNotes();
      setNotes(payload.notes);
      if (
        selectedNote &&
        !payload.notes.some((note) => note.id === selectedNote.id)
      ) {
        setSelectedNote(null);
        setMode("detail");
      }
    } catch (error) {
      setNoteError(error.message);
    }
  }

  useEffect(() => {
    loadEvents({ path: "", status: "" });
    loadNotes();
  }, []);

  async function handleSelectNote(noteId) {
    setNoteError("");
    setMessage("");
    try {
      const payload = await fetchNote(noteId);
      setSelectedNote(payload.note);
      setMode("detail");
    } catch (error) {
      setNoteError(error.message);
    }
  }

  async function handleCreate(values) {
    setNoteError("");
    try {
      const payload = await createNote(values);
      await loadNotes();
      setSelectedNote(payload.note);
      setMode("detail");
      setMessage("메모를 저장했습니다.");
    } catch (error) {
      setNoteError(error.message);
    }
  }

  async function handleUpdate(values) {
    setNoteError("");
    try {
      const payload = await updateNote(selectedNote.id, values);
      await loadNotes();
      setSelectedNote(payload.note);
      setMode("detail");
      setMessage("메모를 수정했습니다.");
    } catch (error) {
      setNoteError(error.message);
    }
  }

  async function handleDelete() {
    setNoteError("");
    try {
      await deleteNote(selectedNote.id);
      setSelectedNote(null);
      setMode("detail");
      await loadNotes();
      setMessage("메모를 삭제했습니다.");
    } catch (error) {
      setNoteError(error.message);
    }
  }

  async function refreshAll() {
    setMessage("");
    await Promise.all([loadEvents(filters), loadNotes()]);
    setMessage("요청 기록과 메모를 다시 조회했습니다.");
  }

  function renderNoteWorkspace() {
    if (mode === "create") {
      return (
        <NoteForm
          note={null}
          onSave={handleCreate}
          onCancel={() => {
            setMode("detail");
            setNoteError("");
          }}
          error={noteError}
        />
      );
    }

    if (mode === "edit" && selectedNote) {
      return (
        <NoteForm
          note={selectedNote}
          onSave={handleUpdate}
          onCancel={() => {
            setMode("detail");
            setNoteError("");
          }}
          error={noteError}
        />
      );
    }

    if (mode === "delete" && selectedNote) {
      return (
        <DeleteConfirm
          note={selectedNote}
          onConfirm={handleDelete}
          onCancel={() => {
            setMode("detail");
            setNoteError("");
          }}
          error={noteError}
        />
      );
    }

    return (
      <NoteDetail
        note={selectedNote}
        onEdit={() => setMode("edit")}
        onDelete={() => setMode("delete")}
      />
    );
  }

  return (
    <main className="dashboard-shell">
      <header className="dashboard-header">
        <div>
          <p className="eyebrow">MINI WATCH</p>
          <h1>감시 대시보드</h1>
          <p className="muted"><strong>{user.name}</strong>님이 로그인했습니다.</p>
        </div>
        <div className="button-row">
          <button className="button primary" type="button" onClick={refreshAll}>
            전체 새로고침
          </button>
          <button className="button" type="button" onClick={onLogout}>
            로그아웃
          </button>
        </div>
      </header>

      {message && <p className="success-banner">{message}</p>}

      <EventList
        events={events}
        summary={summary}
        filters={filters}
        onFilterChange={(nextFilters) => loadEvents(nextFilters)}
        onRefresh={() => loadEvents(filters)}
        loading={eventsLoading}
        error={eventError}
      />

      <div className="notes-grid">
        <NoteList
          notes={notes}
          selectedId={selectedNote?.id}
          onSelect={handleSelectNote}
          onCreate={() => {
            setMode("create");
            setNoteError("");
            setMessage("");
          }}
          onRefresh={loadNotes}
        />
        {renderNoteWorkspace()}
      </div>
    </main>
  );
}
