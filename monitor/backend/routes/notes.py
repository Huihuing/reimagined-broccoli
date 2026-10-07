from flask import Blueprint, jsonify, request

from auth_required import login_required
from note_rules import validate_note_input
from repositories.notes import (
    create_note,
    delete_note,
    find_note,
    list_notes,
    update_note,
)


notes_bp = Blueprint("notes", __name__)


def not_found(note_id: int):
    return jsonify({"error": f"{note_id}번 메모를 찾을 수 없습니다."}), 404


@notes_bp.get("/api/notes")
@login_required
def get_notes():
    return jsonify({"notes": list_notes()})


@notes_bp.get("/api/notes/<int:note_id>")
@login_required
def get_note(note_id: int):
    note = find_note(note_id)
    if note is None:
        return not_found(note_id)
    return jsonify({"note": note})


@notes_bp.post("/api/notes")
@login_required
def add_note():
    payload = request.get_json(silent=True) or {}
    title, body, status, error = validate_note_input(
        str(payload.get("title", "")),
        str(payload.get("body", "")),
        str(payload.get("status", "확인 전")),
    )
    if error:
        return jsonify({"error": error}), 400

    note = create_note(title, body, status)
    return jsonify({"note": note}), 201


@notes_bp.put("/api/notes/<int:note_id>")
@login_required
def edit_note(note_id: int):
    current = find_note(note_id)
    if current is None:
        return not_found(note_id)

    payload = request.get_json(silent=True) or {}
    title, body, status, error = validate_note_input(
        str(payload.get("title", "")),
        str(payload.get("body", "")),
        str(payload.get("status", current["status"])),
    )
    if error:
        return jsonify({"error": error}), 400

    note = update_note(note_id, title, body, status)
    if note is None:
        return not_found(note_id)

    return jsonify({"note": note})


@notes_bp.delete("/api/notes/<int:note_id>")
@login_required
def remove_note(note_id: int):
    note = delete_note(note_id)
    if note is None:
        return not_found(note_id)

    return jsonify({"deleted": note})
