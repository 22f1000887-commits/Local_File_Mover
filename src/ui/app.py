import streamlit as st

from src.services.file_mover import move_files
from src.ui.components import render_header, render_input_section, render_move_button, render_results_section
from src.ui.session_manager import init_session_state, persist_path, clear_paths
from src.utils.logging_config import get_logger
from src.utils.validators import validate_source_path, validate_destination_path


logger = get_logger(__name__)


def run_app() -> None:
    st.set_page_config(page_title="Local File Mover UI", layout="centered")
    render_header()

    init_session_state()
    source_path = st.session_state.source_path
    destination_path = st.session_state.destination_path

    source_path, destination_path = render_input_section(source_path, destination_path)
    persist_path("source_path", source_path)
    persist_path("destination_path", destination_path)

    validation_error = None
    result = None

    if render_move_button(bool(source_path and destination_path)):
        source_valid, source_message = validate_source_path(source_path)
        destination_valid, destination_message = validate_destination_path(destination_path)

        if not source_valid:
            validation_error = source_message
            logger.warning("Source validation failed: %s", source_message)
        elif not destination_valid:
            validation_error = destination_message
            logger.warning("Destination validation failed: %s", destination_message)
        else:
            try:
                with st.spinner("Moving files..."):
                    result = move_files(source_path, destination_path)
                if result["failed_count"]:
                    st.error(f"Moved {result['moved_count']} files, but {result['failed_count']} failed.")
                else:
                    st.success(f"Moved {result['moved_count']} files successfully.")
            except Exception:
                validation_error = "An unexpected error occurred while moving files."
                logger.exception("File move failed")

    if validation_error:
        st.error(validation_error)

    render_results_section(result)

    if st.button("Clear paths"):
        clear_paths()
        st.experimental_rerun()


if __name__ == "__main__":
    run_app()
