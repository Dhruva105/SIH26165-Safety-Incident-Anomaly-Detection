"""Streamlit entry point for the Workplace Incident Review application."""
from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

st.set_page_config(
    page_title="Worksite | Incident Review",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded",
)

STYLE_PATH = ROOT / "app" / "theme.css"
if STYLE_PATH.exists():
    st.markdown(f"<style>{STYLE_PATH.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

pages = {
    "WORKSPACE": [
        st.Page("pages/incident_review.py", title="Incident intake & review", icon=":material/fact_check:", default=True),
    ],
    "PROJECT EVIDENCE": [
        st.Page("pages/overview.py", title="Project brief", icon=":material/article:"),
        st.Page("pages/dataset.py", title="Data & coverage", icon=":material/database:"),
        st.Page("pages/methodology.py", title="Methods", icon=":material/science:"),
        st.Page("pages/results.py", title="Experiments", icon=":material/monitoring:"),
        st.Page("pages/explorer.py", title="Pattern explorer", icon=":material/search:"),
    ],
    "GOVERNANCE": [
        st.Page("pages/ethics.py", title="Use & limitations", icon=":material/shield:"),
        st.Page("pages/references.py", title="Sources", icon=":material/menu_book:"),
    ],
}

nav = st.navigation(pages, position="sidebar")
with st.sidebar:
    st.markdown(
        """
        <div class="brand-lockup">
          <div class="brand-mark">W</div>
          <div><div class="brand-name">WORKSITE</div><div class="brand-sub">INCIDENT INTELLIGENCE</div></div>
        </div>
        <div class="sidebar-project">
          <div class="sidebar-kicker">UNIVERSITY PROJECT · INT396</div>
          <div class="sidebar-id">SIH26165</div>
          <div class="sidebar-note">A human-led review workflow for finding unusual patterns in reported workplace injuries.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='sidebar-bottom'>RESEARCH PROTOTYPE<br/>SCREENING SIGNALS ARE NOT SAFETY DECISIONS.</div>", unsafe_allow_html=True)

nav.run()
