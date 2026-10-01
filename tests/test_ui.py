from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from src.ui.components import PREVIEW_BYTES, MAX_UPLOAD_BYTES, text_preview

APP = Path(__file__).resolve().parents[1] / "app.py"


@pytest.mark.parametrize("content, message", [
    (b"", "empty"),
    (b"\xff", "UTF-8"),
    (b"a\x00b", "binary"),
    (b"a" * (MAX_UPLOAD_BYTES + 1), "10 MiB"),
], ids=["empty", "invalid-utf8", "binary", "oversized"])
def test_unreadable_or_oversized_input_has_a_clear_message(content, message):
    with pytest.raises(ValueError, match=message):
        text_preview(content)


def test_preview_is_bounded_and_handles_split_unicode():
    content = b"a" * (PREVIEW_BYTES - 1) + "€".encode()
    preview, truncated = text_preview(content)
    assert truncated
    assert preview == "a" * (PREVIEW_BYTES - 1)
    assert text_preview(b"\xef\xbb\xbfhello") == ("hello", False)


def test_app_launches_and_navigation_keeps_inference_disabled():
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    app.sidebar.radio[0].set_value("Data submission").run()
    assert not app.exception
    assert any("No file selected" in item.value for item in app.info)
    assert app.button[0].disabled
    assert any("Model not connected" in item.value for item in app.info)
    assert not app.warning
    app.sidebar.radio[0].set_value("Research notes").run()
    assert not app.exception
    assert not app.metric


def test_upload_inspect_replace_and_clear_never_produces_predictions():
    app = AppTest.from_file(str(APP)).run()
    app.sidebar.radio[0].set_value("Data submission").run()
    app.file_uploader[0].upload("inspection.txt", b"inspection only", "text/plain").run()
    assert not app.exception
    assert app.code[0].value == "inspection only"
    assert button(app, "Run prediction").disabled
    button(app, "Replace file").click().run()
    app.file_uploader[0].set_value(("binary.dat", b"\xff", "application/octet-stream")).run()
    assert not app.exception
    assert not app.code
    assert any("UTF-8" in item.value for item in app.warning)
    assert button(app, "Run prediction").disabled
    button(app, "Clear file").click().run()
    assert not app.exception
    assert any("No file selected" in item.value for item in app.info)
    assert not app.metric


def button(app, label):
    return next(item for item in app.button if item.label == label)


def test_overview_action_and_upload_survive_navigation():
    app = AppTest.from_file(str(APP)).run()
    button(app, "Open data submission").click().run()
    assert app.sidebar.radio[0].value == "Data submission"
    app.file_uploader[0].upload("retained.txt", b"retained preview").run()
    for page in ["Research notes", "Overview"]:
        app.sidebar.radio[0].set_value(page).run()
        app.sidebar.radio[0].set_value("Data submission").run()
        assert not app.exception
        assert app.code[0].value == "retained preview"
        assert app.session_state["selected_file"].filename == "retained.txt"
        assert button(app, "Run prediction").disabled
    button(app, "Clear file").click().run()
    app.sidebar.radio[0].set_value("Overview").run()
    button(app, "Open data submission").click().run()
    assert app.session_state["selected_file"] is None
    assert app.file_uploader[0].value is None
    assert not app.code


def test_replacement_can_be_cancelled_then_replace_same_filename():
    app = AppTest.from_file(str(APP)).run()
    button(app, "Open data submission").click().run()
    app.file_uploader[0].upload("same.txt", b"original").run()
    button(app, "Replace file").click().run()
    assert app.code[0].value == "original"
    button(app, "Cancel replacement").click().run()
    assert app.code[0].value == "original"
    button(app, "Replace file").click().run()
    app.sidebar.radio[0].set_value("Research notes").run()
    app.sidebar.radio[0].set_value("Data submission").run()
    assert app.code[0].value == "original"
    app.file_uploader[0].upload("same.txt", b"replacement").run()
    assert not app.exception
    assert app.code[0].value == "replacement"
    button(app, "Clear file").click().run()
    app.file_uploader[0].upload("same.txt", b"original").run()
    assert app.code[0].value == "original"


@pytest.mark.parametrize("content, message", [
    (b" \n\t", "No visible text"),
    (b"", "empty"),
    (b"\xff", "UTF-8"),
], ids=["whitespace", "empty", "unreadable"])
def test_preview_states_remain_non_predictive(content, message):
    app = AppTest.from_file(str(APP)).run()
    button(app, "Open data submission").click().run()
    app.file_uploader[0].upload("preview.txt", content).run()
    assert not app.exception
    assert not app.code
    assert any(message in item.value for item in [*app.info, *app.warning])
    assert button(app, "Run prediction").disabled
    assert not app.metric


def test_uploads_are_isolated_between_sessions():
    first = AppTest.from_file(str(APP)).run()
    button(first, "Open data submission").click().run()
    first.file_uploader[0].upload("private.txt", b"session one").run()
    second = AppTest.from_file(str(APP)).run()
    button(second, "Open data submission").click().run()
    assert second.session_state["selected_file"] is None
    assert not second.code
    assert first.session_state["selected_file"].content == b"session one"


def test_long_filename_and_many_lines_keep_a_bounded_preview():
    app = AppTest.from_file(str(APP)).run()
    button(app, "Open data submission").click().run()
    filename = "long-name-" * 20 + ".txt"
    app.file_uploader[0].upload(filename, b"line\n" * 2000).run()
    assert not app.exception
    assert app.text[0].value == filename
    assert len(app.code[0].value.encode()) <= PREVIEW_BYTES
    assert any("first 8 KiB" in item.value for item in app.markdown)
    assert button(app, "Run prediction").disabled
