"""Style application-owned elements only; native layout and theme handle the rest."""

import streamlit as st


def apply_styles() -> None:
    # Read the accent from the theme rather than maintaining a second palette.
    accent = st.get_option("theme.primaryColor")
    st.markdown(
        f"""
        <style>
        .research-eyebrow {{
            color: {accent}; font-size: 1rem; font-weight: 600;
            margin-bottom: .25rem; overflow-wrap: anywhere;
        }}
        .research-footer {{ font-size: .9rem; overflow-wrap: anywhere; }}
        </style>
        """,
        unsafe_allow_html=True,
    )
