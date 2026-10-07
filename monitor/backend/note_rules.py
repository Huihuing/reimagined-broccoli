NOTE_STATUSES = ("확인 전", "확인 중", "완료")


def validate_note_input(
    title: str,
    body: str,
    status: str = "확인 전",
) -> tuple[str, str, str, str | None]:
    cleaned_title = title.strip()
    cleaned_body = body.strip()
    cleaned_status = status.strip() or "확인 전"

    if not cleaned_title:
        return cleaned_title, cleaned_body, cleaned_status, "제목을 입력해 주세요."
    if not cleaned_body:
        return cleaned_title, cleaned_body, cleaned_status, "내용을 입력해 주세요."
    if cleaned_status not in NOTE_STATUSES:
        return cleaned_title, cleaned_body, cleaned_status, "올바른 처리 상태를 선택해 주세요."

    return cleaned_title, cleaned_body, cleaned_status, None
