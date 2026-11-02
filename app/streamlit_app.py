"""Streamlit entry point for the project showcase."""
from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

st.set_page_config(page_title="Safety Incident Anomaly Analysis", page_icon="🦺", layout="wide")

pages = [
    st.Page("pages/overview.py", title="Overview", icon="🏠", default=True),
    st.Page("pages/dataset.py", title="Dataset", icon="🗂️"),
    st.Page("pages/methodology.py", title="Methodology", icon="🧪"),
    st.Page("pages/results.py", title="Results", icon="📊"),
    st.Page("pages/explorer.py", title="Anomaly Explorer", icon="🔎"),
    st.Page("pages/ethics.py", title="Ethics & Limitations", icon="⚖️"),
    st.Page("pages/references.py", title="References", icon="📚"),
]
nav = st.navigation(pages, position="sidebar")
with st.sidebar:
    st.markdown("### INT396 · SIH26165")
    st.caption("Unsupervised occupational safety incident analysis")
    st.divider()
    st.caption("Research prototype. Anomaly scores are exploratory signals, not safety-risk predictions.")
nav.run()
