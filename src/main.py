import sys
from pathlib import Path

import streamlit as st

# Ensure repository root is on sys.path so src package imports resolve
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.ui.app import run_app

def main():
    st.set_page_config(page_title="Local File Mover", layout="centered")
    run_app()

if __name__ == "__main__":
    main()
