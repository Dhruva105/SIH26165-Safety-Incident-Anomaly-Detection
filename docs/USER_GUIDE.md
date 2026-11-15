# Incident Review Desk: User Guide

## What it does

The Incident Review Desk turns a newly documented workplace incident into a structured review workflow:

1. Enter the date, industry code if known, event category, source/equipment and a factual narrative.
2. The fitted Isolation Forest compares the incident with a 5,000-record sample from the supplied OSHA Severe Injury Reports file.
3. The app shows an exploratory anomaly percentile and nearby historical patterns.
4. A rule-based checklist highlights control areas to verify based on event/source/narrative terms.
5. The reviewer records follow-up notes, an owner role/team and an optional due date.
6. The case can be exported as JSON or retained in the current browser session.

## Local setup

Use Python 3.13 to match the runtime used to build the included model artifact.

```bash
py -3.13 -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

The deployable model bundle is included at `artifacts/models/incident_review_engine.joblib`. The raw CSV is not required to start the web app.

```bash
streamlit run app/streamlit_app.py
```

## Rebuild the fitted model

The local raw file must be placed at `data/raw/January2015toNovember2025.csv`.

```bash
python scripts/build_review_model.py --sample-size 5000
```

This replaces the model bundle. Record the source URL, download date, data coverage, sample size and random seed when rebuilding it.

## Research pipeline

The original research pages and command-line experiments remain available:

```bash
python -m safety_anomaly.cli audit
python -m safety_anomaly.cli run --quick --sample-size 1000
pytest -q
```

## Important scope and privacy notes

- The OSHA source represents severe injuries reported under federal OSHA jurisdiction; it is not a complete census of workplace injuries or near misses.
- The anomaly percentile is not a probability of injury or a validated risk score.
- Similar cases are feature-space neighbors, not confirmed causal analogues.
- Checklist items are prompts for investigation, not legal advice or a substitute for site-specific procedures.
- Do not enter personal names, medical identifiers, exact addresses or confidential employer information.
- Saved cases are session-only and should be exported before leaving. This is not a secured, multi-user case-management system.

## Deployment note

The app can be deployed as a Streamlit Community Cloud app from the GitHub repository. The fitted model artifact is committed; the raw OSHA CSV should stay out of Git because it contains establishment and location fields. For real organizational use, add authentication, role-based access, secure managed storage, retention controls, audit logging and a formal safety review process before collecting operational incident records.
