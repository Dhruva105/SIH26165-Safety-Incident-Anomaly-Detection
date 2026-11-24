"""Worksite incident intake, historical pattern screening and human review."""
from __future__ import annotations

from datetime import date, datetime, timezone
import html
import json
from pathlib import Path
import uuid

import pandas as pd
import streamlit as st

from safety_anomaly.operational_review import IncidentReviewEngine, build_review_prompts

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "artifacts" / "models" / "incident_review_engine.joblib"

st.markdown(
    """
    <section class="worksite-hero">
      <div class="worksite-hero-copy">
        <div class="hero-kicker"><span class="hero-kicker-dot"></span> SIH26165 &nbsp; / &nbsp; FIELD REVIEW WORKSPACE</div>
        <h1 class="worksite-hero-title">Incident <em>review.</em></h1>
        <p class="worksite-hero-deck">Move from a factual report to a structured review. Screen unusual patterns, compare historical cases and make the next investigation step clear.</p>
        <div class="hero-tags">
          <span>ISOLATION FOREST</span>
          <span>K-MEANS GROUPING</span>
          <span>HISTORICAL CONTEXT</span>
        </div>
      </div>
      <div class="worksite-hero-art" aria-hidden="true">
        <div class="hero-orbit hero-orbit-outer"></div>
        <div class="hero-orbit hero-orbit-middle"></div>
        <div class="hero-orbit hero-orbit-inner"></div>
        <div class="hero-core"><span>W</span></div>
        <div class="hero-signal hero-signal-one"><b>01</b><small>REPORT</small></div>
        <div class="hero-signal hero-signal-two"><b>02</b><small>SCREEN</small></div>
        <div class="hero-signal hero-signal-three"><b>03</b><small>REVIEW</small></div>
        <div class="hero-art-caption">PATTERN → EVIDENCE → ACTION</div>
      </div>
      <div class="hero-bottom-line"><span>WORKSITE / INCIDENT INTELLIGENCE</span><span>RESEARCH PROTOTYPE · HUMAN REVIEW REQUIRED</span></div>
    </section>
    <section class="workflow-strip">
      <div class="workflow-step"><span class="workflow-number">01</span><div><strong>Capture</strong><small>Record the event</small></div></div>
      <div class="workflow-connector"></div>
      <div class="workflow-step"><span class="workflow-number">02</span><div><strong>Screen</strong><small>Find unusual patterns</small></div></div>
      <div class="workflow-connector"></div>
      <div class="workflow-step"><span class="workflow-number">03</span><div><strong>Compare</strong><small>Review similar cases</small></div></div>
      <div class="workflow-connector"></div>
      <div class="workflow-step"><span class="workflow-number">04</span><div><strong>Follow up</strong><small>Record human review</small></div></div>
    </section>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="notice-band"><strong>Scope of use.</strong> This prototype supports initial review only. It does not predict accidents, measure injury probability, determine legal compliance or replace emergency response and qualified safety judgement. Do not enter names, contact details, exact addresses, medical identifiers or confidential information.</div>',
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner="Loading the fitted review model…")
def load_engine(path: str, modified: float) -> IncidentReviewEngine:
    del modified
    return IncidentReviewEngine.load(path)


if not MODEL_PATH.exists():
    st.error("The fitted review model is missing. The incident screening workflow cannot run.")
    st.code("python scripts/build_review_model.py --sample-size 5000", language="bash")
    st.stop()

try:
    engine = load_engine(str(MODEL_PATH), MODEL_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"The fitted review model could not be loaded: {exc}")
    st.stop()

for key, default in {
    "review_cases": [],
    "active_assessment": None,
    "active_incident": None,
    "active_review_token": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

reference = engine.reference_rows


def options_for(column: str, limit: int = 80) -> list[str]:
    if column not in reference.columns:
        return []
    return reference[column].dropna().astype(str).value_counts().head(limit).index.tolist()


def safe_json_bytes(payload: dict) -> bytes:
    return json.dumps(payload, indent=2, ensure_ascii=False, default=str).encode("utf-8")


def new_case_payload(
    incident: dict,
    assessment: dict,
    checks: dict[str, bool],
    notes: str,
    owner: str,
    due_date: date | None,
) -> dict:
    return {
        "case_id": f"WS-{datetime.now(timezone.utc):%y%m%d}-{uuid.uuid4().hex[:5].upper()}",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "incident": incident,
        "model_screening": assessment,
        "review_checklist": checks,
        "review_notes": notes.strip(),
        "action_owner_role_or_team": owner.strip(),
        "follow_up_due_date": due_date.isoformat() if due_date else None,
        "model_version": engine.model_version,
        "reference_sample_size": len(engine.reference_rows),
        "disclaimer": "Exploratory anomaly screening only. Not a risk probability or compliance assessment.",
    }


new_tab, register_tab = st.tabs(["01  Report & review", "02  Case register"])

with new_tab:
    st.markdown('<div class="section-head"><span class="section-index">01</span><span class="section-label">Record the incident</span></div>', unsafe_allow_html=True)
    st.caption("Enter only the facts needed to understand the event. Use 'Not known' rather than guessing.")
    with st.form("incident_intake_form", clear_on_submit=False):
        left, right = st.columns(2, gap="large")
        with left:
            event_date = st.date_input("Event date", value=date.today(), max_value=date.today())
            industry_code = st.text_input("Industry NAICS code · optional", placeholder="e.g. 236220", max_chars=6)
            event_options = options_for("EventTitle")
            event_choice = st.selectbox("Event category", ["Other / not listed"] + event_options)
            event_custom = st.text_input(
                "Specify event category",
                placeholder="e.g. caught in rotating equipment",
                disabled=event_choice != "Other / not listed",
            )
            injury_nature = st.text_input("Injury nature · optional", placeholder="e.g. fracture, burn, laceration")
        with right:
            source_options = options_for("SourceTitle")
            source_choice = st.selectbox("Equipment or source", ["Other / not listed", "Not known"] + source_options)
            source_custom = st.text_input(
                "Specify source or equipment",
                placeholder="e.g. fixed ladder, conveyor",
                disabled=source_choice != "Other / not listed",
            )
            secondary_source = st.text_input("Secondary source · optional", placeholder="e.g. wet floor, moving vehicle")
            body_part = st.text_input("Body part affected · optional", placeholder="e.g. hand, lower leg")
        narrative = st.text_area(
            "What happened?",
            height=175,
            placeholder=(
                "Describe the task, what happened immediately before the event, the equipment or environment involved, "
                "and the immediate response. Keep it factual and remove identifying details."
            ),
            help="A useful narrative explains the task, sequence, exposure and immediate response. Do not include names or identifying details.",
        )
        submitted = st.form_submit_button("Screen incident  →", type="primary", use_container_width=True)

    if submitted:
        event_label = event_custom.strip() if event_choice == "Other / not listed" else event_choice
        if source_choice == "Other / not listed":
            source_label = source_custom.strip()
        elif source_choice == "Not known":
            source_label = "Unknown"
        else:
            source_label = source_choice

        if len(narrative.strip()) < 25:
            st.error("Please provide at least 25 characters of factual incident context.")
        elif not event_label:
            st.error("Select an event category or specify one.")
        elif not source_label:
            st.error("Specify the source or equipment, or choose Not known.")
        elif industry_code.strip() and not industry_code.strip().isdigit():
            st.error("The NAICS code should contain digits only.")
        else:
            incident = {
                "EventDate": event_date.isoformat(),
                "Primary NAICS": industry_code.strip() or "Unknown",
                "EventTitle": event_label,
                "SourceTitle": source_label,
                "Secondary Source Title": secondary_source.strip() or "Unknown",
                "NatureTitle": injury_nature.strip() or "Unknown",
                "Part of Body Title": body_part.strip() or "Unknown",
                "Final Narrative": narrative.strip(),
            }
            try:
                assessment_obj = engine.assess(incident)
                assessment = {
                    "anomaly_score": float(assessment_obj.anomaly_score),
                    "reference_percentile": float(assessment_obj.reference_percentile),
                    "flagged_for_review": bool(assessment_obj.flagged_for_review),
                    "signal_label": assessment_obj.signal_label,
                    "similar_cases": assessment_obj.similar_cases,
                    "limitations": assessment_obj.limitations,
                    "pattern_group": assessment_obj.pattern_group,
                    "cluster_size": assessment_obj.cluster_size,
                    "pattern_summary": assessment_obj.pattern_summary,
                }
                st.session_state.active_incident = incident
                st.session_state.active_assessment = assessment
                st.session_state.active_review_token = uuid.uuid4().hex[:8]
                st.session_state.active_checks = {}
                st.session_state.review_notes_value = ""
                st.session_state.review_owner_value = ""
                st.session_state.review_due_value = None
            except Exception as exc:
                st.error(f"The incident could not be screened: {exc}")

    if st.session_state.active_incident and st.session_state.active_assessment:
        incident = st.session_state.active_incident
        assessment = st.session_state.active_assessment
        token = st.session_state.active_review_token or "review"
        prompts = build_review_prompts(incident["EventTitle"], incident["SourceTitle"], incident["Final Narrative"])

        st.markdown('<div class="section-rule"></div><div class="section-head"><span class="section-index">02</span><span class="section-label">Review the screening result</span></div>', unsafe_allow_html=True)
        result_left, result_right = st.columns([1.35, 1], gap="large")
        with result_left:
            if assessment["flagged_for_review"]:
                st.warning("Unusual pattern · human review suggested")
            else:
                st.info("Closer to common reference patterns · human review is still required")
            st.markdown(
                f"<div style='font-family:Georgia,serif;font-size:2.8rem;color:#202a27;line-height:1.05'>{assessment['reference_percentile']:.1f}<span style='font-size:1.05rem'>th percentile</span></div>",
                unsafe_allow_html=True,
            )
            st.caption("Relative anomaly-score position within the model's fitted reference sample.")
            st.progress(max(0.0, min(1.0, assessment["reference_percentile"] / 100.0)))
        with result_right:
            st.markdown(
                "<div style='background:#fff;border:1px solid #d9ddd5;padding:1rem 1.1rem;border-radius:4px;height:100%'>"
                "<div style='font-size:.62rem;letter-spacing:.14em;color:#8f442a;font-weight:800'>REFERENCE SET</div>"
                f"<div style='font-family:Georgia,serif;font-size:1.9rem;margin:.2rem 0'>{len(engine.reference_rows):,}</div>"
                "<div style='font-size:.8rem;color:#66716b;line-height:1.5'>OSHA severe-injury reports sampled for the fitted model</div>"
                "</div>",
                unsafe_allow_html=True,
            )
        pattern = assessment.get("pattern_summary", {})
        st.markdown('<div class="section-head"><span class="section-index">03</span><span class="section-label">Place the incident in a recurring pattern group</span></div>', unsafe_allow_html=True)
        pattern_left, pattern_right = st.columns([0.8, 1.6], gap="large")
        with pattern_left:
            st.markdown(
                f"<div style='background:#20352d;color:#f2f0e9;padding:1.1rem;border-radius:4px'>"
                f"<div style='font-size:.62rem;letter-spacing:.15em;color:#c8a47f;font-weight:800'>K-MEANS GROUP</div>"
                f"<div style='font-family:Georgia,serif;font-size:2rem;margin:.25rem 0'>{html.escape(assessment.get('pattern_group','Pattern group'))}</div>"
                f"<div style='font-size:.78rem;color:#c9d3cc'>{assessment.get('cluster_size',0):,} reference records assigned</div></div>",
                unsafe_allow_html=True,
            )
        with pattern_right:
            summary_rows = [
                ("Most common event", pattern.get("dominant_event", "Not recorded")),
                ("Most common source", pattern.get("dominant_source", "Not recorded")),
                ("Most common injury", pattern.get("dominant_injury", "Not recorded")),
            ]
            for key, value in summary_rows:
                st.markdown(
                    f"<div style='border-bottom:1px solid #d9ddd5;padding:.42rem 0'>"
                    f"<span style='font-size:.65rem;color:#8f442a;font-weight:800;letter-spacing:.08em;text-transform:uppercase'>{key}</span><br/>"
                    f"<span style='font-size:.86rem;color:#202a27'>{html.escape(str(value))}</span></div>",
                    unsafe_allow_html=True,
                )
        st.caption("K-Means group descriptors summarise the most frequent categories in each cluster. A group is a statistical pattern, not a hazard severity class or causal explanation.")

        st.caption(
            "Model: Isolation Forest for unusual-pattern screening; K-Means for recurring pattern grouping; nearest neighbours for historical examples. Features combine structured categories, industry/date fields and TF-IDF narrative representation reduced with TruncatedSVD. "
            "The 3% contamination setting is a model threshold, not a claim that 3% of incidents are unsafe."
        )

        st.markdown('<div class="section-head"><span class="section-index">04</span><span class="section-label">Compare nearby historical patterns</span></div>', unsafe_allow_html=True)
        st.caption("The records below are nearest neighbours in the fitted feature space. Similarity does not establish a shared cause or identical circumstances.")
        similar = pd.DataFrame(assessment.get("similar_cases", []))
        display_cols = [
            column for column in ["EventDate", "Industry sector", "EventTitle", "SourceTitle", "NatureTitle", "Part of Body Title"]
            if column in similar.columns
        ]
        if not similar.empty and display_cols:
            similar = similar[display_cols].copy()
            similar = similar.rename(columns={
                "EventDate": "Year", "Industry sector": "Industry", "EventTitle": "Event",
                "SourceTitle": "Source", "NatureTitle": "Injury", "Part of Body Title": "Body part",
            })
            st.dataframe(similar, use_container_width=True, hide_index=True)
        else:
            st.info("No comparable historical patterns were returned for this entry.")

        st.markdown('<div class="section-head"><span class="section-index">05</span><span class="section-label">Complete the human review</span></div>', unsafe_allow_html=True)
        st.caption("These are prompts for evidence collection. Confirm each item against the site, task, equipment and applicable procedures.")
        checks: dict[str, bool] = {}
        for index, item in enumerate(prompts):
            check_label = f"{item['area']}  |  {item['prompt']}"
            checks[check_label] = st.checkbox(check_label, key=f"review_{token}_{index}")
        st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
        action_left, action_right = st.columns(2, gap="large")
        with action_left:
            owner = st.text_input("Action owner role or team", key=f"owner_{token}", placeholder="e.g. Maintenance supervisor")
            set_due = st.checkbox("Set a follow-up date", key=f"set_due_{token}")
            due_date = st.date_input("Follow-up due date", value=date.today(), key=f"due_{token}") if set_due else None
        with action_right:
            notes = st.text_area(
                "Investigation notes and corrective actions",
                key=f"notes_{token}",
                height=135,
                placeholder="Record verified findings, controls to investigate, the action required and how its effectiveness will be checked.",
            )

        assessment_export = {
            "signal_label": assessment["signal_label"],
            "reference_percentile": round(float(assessment["reference_percentile"]), 2),
            "flagged_for_review": bool(assessment["flagged_for_review"]),
            "similar_cases": assessment["similar_cases"],
            "limitations": assessment["limitations"],
            "pattern_group": assessment["pattern_group"],
            "cluster_size": assessment["cluster_size"],
            "pattern_summary": assessment["pattern_summary"],
        }
        current_case = new_case_payload(incident, assessment_export, checks, notes, owner, due_date)
        save_col, download_col = st.columns(2)
        with save_col:
            if st.button("Add to session register", type="primary", use_container_width=True, key=f"save_{token}"):
                already_saved = any(
                    item.get("incident") == incident and item.get("model_screening", {}).get("reference_percentile") == assessment_export["reference_percentile"]
                    for item in st.session_state.review_cases
                )
                if already_saved:
                    st.info("This incident is already in the current session register.")
                else:
                    st.session_state.review_cases.insert(0, current_case)
                    st.success(f"Review {current_case['case_id']} added to the session register.")
        with download_col:
            st.download_button(
                "Download review record (.json)",
                data=safe_json_bytes(current_case),
                file_name=f"{current_case['case_id']}.json",
                mime="application/json",
                use_container_width=True,
                key=f"download_current_{token}",
            )

        with st.expander("Model interpretation and limitations"):
            st.write(assessment["limitations"])
            st.write(
                "The percentile is calculated against scores from the fitted sample. The reference dataset contains severe injuries reported under federal OSHA jurisdiction; it is not a complete record of workplace incidents, near misses or State Plan reports."
            )

with register_tab:
    st.markdown('<div class="section-head"><span class="section-index">02</span><span class="section-label">Session case register</span></div>', unsafe_allow_html=True)
    st.caption("Cases stay in the active Streamlit session. Export records before leaving. This is not a secured multi-user case-management database.")
    cases = st.session_state.review_cases
    if not cases:
        st.info("No cases have been added in this session. Complete an incident review and add it to the register.")
    else:
        st.write(f"**{len(cases)} review record(s)**")
        rows = []
        for item in cases:
            rows.append({
                "Case ID": item["case_id"],
                "Created (UTC)": item["created_at_utc"],
                "Event": item["incident"]["EventTitle"],
                "Review signal": item["model_screening"]["signal_label"],
                "Reference percentile": item["model_screening"]["reference_percentile"],
                "Action owner": item["action_owner_role_or_team"],
                "Due date": item["follow_up_due_date"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.download_button(
            "Export all session records (.json)",
            data=safe_json_bytes({"exported_at_utc": datetime.now(timezone.utc).isoformat(), "cases": cases}),
            file_name="worksite-session-review-records.json",
            mime="application/json",
            use_container_width=True,
        )
        for item in cases:
            with st.expander(f"{item['case_id']}  /  {item['incident']['EventTitle']}"):
                st.write(item["model_screening"]["signal_label"])
                st.download_button(
                    f"Download {item['case_id']}",
                    data=safe_json_bytes(item),
                    file_name=f"{item['case_id']}.json",
                    mime="application/json",
                    key=f"download_{item['case_id']}",
                )

st.markdown('<div class="section-rule"></div>', unsafe_allow_html=True)
st.caption("Data source: U.S. Occupational Safety and Health Administration (OSHA), Severe Injury Reports. Coverage and scope are described in the Data & Coverage page.")
st.markdown(
    "[OSHA Severe Injury Reports](https://www.osha.gov/severeinjury) · "
    "[OSHA Severe Injury Dashboard](https://www.osha.gov/severe-injury-reports) · "
    "[OSHA machine guarding guidance](https://www.osha.gov/etools/machine-guarding/introduction/general-requirements) · "
    "[OSHA hazardous-energy control guidance](https://www.osha.gov/etools/hospitals/facilities-management/lockout-tagout)"
)
