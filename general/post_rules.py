def validate_post_input(title: str, body: str) -> tuple[str, str, str | None]:
    cleaned_title = title.strip()
    cleaned_body = body.strip()

    if not cleaned_title and not cleaned_body:
        return cleaned_title, cleaned_body, "제목과 내용을 입력해 주세요."
    if not cleaned_title:
        return cleaned_title, cleaned_body, "제목을 입력해 주세요."
    if not cleaned_body:
        return cleaned_title, cleaned_body, "내용을 입력해 주세요."

    return cleaned_title, cleaned_body, None
