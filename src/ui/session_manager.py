import streamlit as st

def init_session_state():
    if "source_path" not in st.session_state:
        st.session_state.source_path = ""
    if "destination_path" not in st.session_state:
        st.session_state.destination_path = ""
    if "current_result" not in st.session_state:
        st.session_state.current_result = None

def persist_path(key: str, value: str):
    st.session_state[key] = value

def get_persisted_path(key: str) -> str:
    return st.session_state.get(key, "")

def clear_paths():
    st.session_state.source_path = ""
    st.session_state.destination_path = ""
    st.session_state.current_result = None
