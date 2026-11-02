# Local Build Validation Report

Date: 2026-11-02

## Dataset audit
- Source CSV opened successfully.
- 105,996 rows and 28 columns.
- `UPA`: 105,996 unique, non-null values.
- `ID`: 5 distinct repeated values affecting 10 rows.
- Exact duplicate rows: 0.
- Parsed event-date range: 2015-01-01 through 2025-11-30.
- Invalid event dates: 0.

## Automated tests
- `pytest -q`: 7 passed.
- `compileall` on `src`, `app`, `scripts`, and `tests`: passed.
- All five notebooks passed nbformat validation.
- All five notebooks executed successfully in a local Python kernel.

## End-to-end pipeline smoke test
- Command: `python -m safety_anomaly.cli run --quick --sample-size 1000`
- Dataset rows read: 105,996.
- Model sample: 1,000.
- Feature representation: structured + TF-IDF narrative features.
- Reduced feature dimensions: 24.
- Experiment configurations: 6 (3 Isolation Forest, 3 LOF).
- Public outputs and PCA figures were generated.
- Private blinded manual-review worksheet was generated under `artifacts/private/`.

The smoke-run outputs are included as a demonstration of the dashboard data contract. They are not final academic results and should be replaced by a documented larger experiment before submission.

## Streamlit limitation
Streamlit is declared in the project dependencies and the application files pass Python syntax compilation. The execution container did not have Streamlit installed and outbound package installation was unavailable, so the Streamlit server could not be launched here. Install the project dependencies locally and follow the README to test the UI in a browser.
