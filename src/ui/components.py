import streamlit as st
from typing import Optional

def render_header():
    st.title("Local File Mover")
    st.markdown("Move all files from a source folder to a destination folder using a simple UI.")

def render_input_section(source_value: Optional[str], dest_value: Optional[str]):
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("Source Folder Path", value=source_value or "")
    with col2:
        dest = st.text_input("Destination Folder Path", value=dest_value or "")
    return source.strip(), dest.strip()

def render_move_button(enabled: bool):
    return st.button("Move Files", disabled=not enabled)

def render_progress_container(current_file: str, moved: int, total: int):
    st.info(f"Moving files: {moved} / {total}")
    if current_file:
        st.write(f"Current: {current_file}")

def render_results_section(result: dict):
    if result is None:
        return
    moved_count = result.get("moved_count", 0)
    failed_count = result.get("failed_count", 0)
    duration_seconds = result.get("duration_seconds")
    moved_files = result.get("moved", [])
    failed_files = result.get("failed", [])

    st.subheader("Operation Results")
    st.write(f"Moved files: {moved_count}")
    st.write(f"Failed files: {failed_count}")
    if duration_seconds is not None:
        st.write(f"Duration: {duration_seconds:.2f} seconds")

    if moved_files:
        st.markdown("**Moved files**")
        st.table([{"filename": filename} for filename in moved_files])

    if failed_files:
        st.markdown("**Failed files**")
        st.table(failed_files)
