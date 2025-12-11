import streamlit as st
from app.visualization.pages.page_config import render_config_page
from app.visualization.pages.page_results import render_results_page


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "config"

    if st.session_state["page"] == "config":
        render_config_page()
    elif st.session_state["page"] == "results":
        render_results_page()
    else:
        st.session_state["page"] = "config"
        render_config_page()


if __name__ == "__main__":
    main()
