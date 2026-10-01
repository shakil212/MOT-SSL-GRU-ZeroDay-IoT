"""Reusable interface pieces and bounded, non-model file inspection."""

import codecs

import streamlit as st

from src.inference.contracts import SubmittedInput
from src.ui.session import cancel_replacement, clear_file, receive_upload, replace_file

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
PREVIEW_BYTES = 8 * 1024


def text_preview(content: bytes) -> tuple[str, bool]:
    """Inspect a UTF-8 prefix without interpreting columns or model features."""
    if not content:
        raise ValueError("The file is empty. Choose a non-empty file to inspect.")
    if len(content) > MAX_UPLOAD_BYTES:
        raise ValueError("This demonstration accepts files up to 10 MiB.")
    truncated = len(content) > PREVIEW_BYTES
    decoder = codecs.getincrementaldecoder("utf-8-sig")()
    try:
        preview = decoder.decode(content[:PREVIEW_BYTES], final=not truncated)
    except UnicodeDecodeError as exc:
        raise ValueError(
            "A text preview is unavailable: this file is not readable as UTF-8 text. "
            "This does not determine model compatibility."
        ) from exc
    if any(ord(char) < 32 and char not in "\t\r\n" for char in preview):
        raise ValueError(
            "A text preview is unavailable: the file contains binary control characters. "
            "Model compatibility has not been assessed."
        )
    return preview, truncated


def page_heading(eyebrow: str, title: str, description: str) -> None:
    # Only application-owned static text belongs in the HTML eyebrow.
    with st.container(gap=None):
        st.markdown(f'<div class="research-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
        st.title(title)
        st.write(description)


def submission_controls() -> None:
    st.write("Text preview supports UTF-8 files.")
    st.caption("Model input requirements are not yet available.")
    st.caption("Up to 10 MiB · Kept only for this session; not saved to disk.")
    selected = st.session_state.selected_file
    replacing = st.session_state.replacing_file
    if selected is not None:
        st.write("File selected. It remains available when you navigate between pages.")
        if not replacing:
            replace_column, clear_column = st.columns(2, gap="small", wrap=True)
            replace_column.button("Replace file", on_click=replace_file, width="stretch")
            clear_column.button("Clear file", on_click=clear_file, width="stretch")
        else:
            st.write("Choose a replacement below. Your current file stays selected until another is received.")
            st.button("Cancel replacement", on_click=cancel_replacement)
    if selected is None or replacing:
        widget_key = f"inspection_upload_{st.session_state.upload_generation}"
        st.file_uploader(
            "Choose a replacement file" if replacing else "Choose a file for inspection",
            key=widget_key,
            on_change=receive_upload,
            args=(widget_key,),
            help="Selecting a file does not validate it for the model.",
        )


def inspect_upload(submitted: SubmittedInput) -> None:
    st.write("**Selected file**")
    st.text(submitted.filename, width="stretch", wrap=True)
    st.caption(f"File size: {len(submitted.content):,} bytes")
    st.caption("File inspection only; model compatibility has not been assessed.")
    try:
        preview, truncated = text_preview(submitted.content)
    except ValueError as exc:
        st.warning(str(exc))
        return
    if not preview.strip():
        st.info("No visible text in this preview.")
    else:
        st.write("**Text preview available**")
        st.code(preview, language=None, height=280, wrap_lines=True)
    if truncated:
        st.write("Showing the first 8 KiB only. The remainder has not been inspected.")
