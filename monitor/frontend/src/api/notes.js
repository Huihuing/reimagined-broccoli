import { apiRequest } from "./client";

export function fetchNotes() {
  return apiRequest("/notes");
}

export function fetchNote(noteId) {
  return apiRequest(`/notes/${noteId}`);
}

export function createNote(note) {
  return apiRequest("/notes", {
    method: "POST",
    body: JSON.stringify(note),
  });
}

export function updateNote(noteId, note) {
  return apiRequest(`/notes/${noteId}`, {
    method: "PUT",
    body: JSON.stringify(note),
  });
}

export function deleteNote(noteId) {
  return apiRequest(`/notes/${noteId}`, {
    method: "DELETE",
  });
}
