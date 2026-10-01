"""Launch with: python -m streamlit run app.py."""

import streamlit as st

from src.inference.service import UnavailableInferenceService
from src.ui.components import inspect_upload, page_heading, submission_controls
from src.ui.session import initialize_session, open_submission
from src.ui.styles import apply_styles

st.set_page_config(
    page_title="Zero-day IoT | Research demonstrator",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state=260,
)
apply_styles()
initialize_session()
service = UnavailableInferenceService()
status = service.status()

with st.sidebar:
    st.markdown("**IoT Research Lab**")
    st.caption("MOT-SSL-GRU-ZeroDay-IoT")
    page = st.radio("Navigation", ["Overview", "Data submission", "Research notes"], key="workspace_page")
    st.divider()
    with st.container(gap=None):
        st.caption("PROJECT STAGE")
        st.write("Interface demonstration")
        st.caption(status.message)

with st.container(horizontal_alignment="center"):
    with st.container(width=1120, gap="small"):
        if page == "Overview":
            page_heading(
                "University Machine Learning research",
                "Zero-day IoT intrusion detection",
                "Exploring temporal and self-supervised GRU-based learning for zero-day intrusion detection in IoT networks.",
            )
            st.button("Open data submission", type="primary", on_click=open_submission)
            st.header("Explore the demonstration", anchor=False)
            for column, title, description in zip(
                st.columns(3, gap="small", wrap=True),
                ["1. Submit file", "2. Inspect file", "3. Prediction"],
                [
                    "Choose a file to inspect.",
                    "Review file details and readable text.",
                    "Available after model integration.",
                ],
            ):
                with column, st.container(border=True, gap=None):
                    st.subheader(title, anchor=False)
                    st.write(description)
            with st.container(border=True, gap="small"):
                st.header("Research direction", anchor=False)
                st.write("Evaluation plan: strict Leave-One-Attack-Family-Out (LOAFO).")
                st.caption("Explore the approach and current stage in Research notes.")

        elif page == "Data submission":
            page_heading(
                "Interactive demonstration",
                "Submit and inspect data",
                "Choose a file, review its contents, and explore the planned prediction workflow.",
            )
            left, right = st.columns([3, 2], gap="medium", wrap=True)
            with left, st.container(border=True):
                st.header("1. Submit file", anchor=False)
                submission_controls()
                st.header("2. Inspect file", anchor=False)
                submitted = st.session_state.selected_file
                if submitted is None:
                    st.info("No file selected. Choose a file above to see its details and text preview here.")
                else:
                    inspect_upload(submitted)
            with right, st.container(border=True):
                st.header("3. Prediction", anchor=False)
                st.info(f"No prediction available — {status.message}.")
                st.write("The model is being trained separately in Google Colab. Prediction will become available after integration.")
                st.button("Run prediction", disabled=True, type="primary", width="stretch")
                st.subheader("Results", anchor=False)
                st.caption("Results will appear here after model integration and a prediction run.")
                with st.expander("About future results"):
                    st.write("Confidence or probability will be shown only if supported by the trained model.")

        else:
            page_heading(
                "Research context",
                "Research notes",
                "The project objective, proposed approach, and evaluation plan.",
            )
            objective, approach = st.columns(2, gap="small", wrap=True)
            with objective, st.container(border=True):
                st.header("Research objective", anchor=False)
                st.write("Investigate zero-day IoT intrusion detection using Machine Learning.")
            with approach, st.container(border=True):
                st.header("Learning approach", anchor=False)
                st.write("Temporal and self-supervised GRU-based learning form the project's stated research approach.")
            with st.container(border=True):
                st.header("Evaluation plan", anchor=False)
                st.write("Strict Leave-One-Attack-Family-Out (LOAFO) evaluation.")
                st.write("This is the planned evaluation protocol. Verified research results are not yet available in this demonstration.")
            st.header("Current stage", anchor=False)
            st.write("The model is being trained separately in Google Colab. The application currently demonstrates file submission and inspection.")
            st.caption("Model-specific details remain pending notebook and trained-model verification.")

        st.divider()
        st.markdown('<div class="research-footer">MOT-SSL-GRU-ZeroDay-IoT · University research demonstration</div>', unsafe_allow_html=True)
