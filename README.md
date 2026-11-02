# Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF

**Course:** INT396 – Unsupervised Learning  
**Project ID:** SIH26165  
**Student:** Dhruv Pal  
**Methods:** Isolation Forest, Local Outlier Factor (LOF), TF-IDF, TruncatedSVD and PCA

## 1. Project overview

This project develops a reproducible exploratory pipeline for identifying unusual patterns in occupational severe-injury incident reports. It compares an isolation-based method (Isolation Forest) with a local-density method (LOF), examines feature representations and parameter sensitivity, and presents aggregate results through a Streamlit dashboard.

**Important:** an anomaly score is not a prediction of an accident or a validated safety-risk score. A flagged record is a candidate for review, not proof of unsafe conduct, negligence or preventability.

## 2. Dataset

The supplied CSV is the OSHA Severe Injury Reports extract named `January2015toNovember2025.csv`. The initially inspected copy has 105,996 rows, 28 columns, 105,996 unique UPA values, five repeated distinct `ID` values affecting ten rows, no exact duplicate rows, and event dates from 2015-01-01 to 2025-11-30. Re-run the audit on the copy you use for submission.

Official source and current documentation: https://www.osha.gov/severeinjury

The dataset captures reported severe injuries within the source's collection scope. It is not a representative census of all workplace injuries, near-misses or unsafe acts.

## 3. Repository structure

```text
Safety-Incident-Anomaly-Detection/
├── app/                    # Streamlit website
├── artifacts/              # Generated experiment outputs
├── configs/                # YAML settings
├── data/                   # Local raw dataset (excluded from Git)
├── docs/                   # Project plan, methodology and logs
├── notebooks/              # Executable academic workflow notebooks
├── reports/                # Audit tables and figures
├── scripts/                # Convenience scripts
├── src/safety_anomaly/     # Reusable Python package
└── tests/                  # Automated tests
```

## 4. Setup

Recommended: Python 3.11 (Python 3.10+ is supported).

### Windows PowerShell

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

If the local CSV is not already present, copy it to:

```text
data/raw/January2015toNovember2025.csv
```

## 5. Run the dataset audit

```powershell
python -m safety_anomaly.cli audit
```

Audit outputs are written to `reports/data_audit/`.

## 6. Run the experiments

Start with a quick smoke experiment:

```powershell
python -m safety_anomaly.cli run --quick --sample-size 1000
```

Recommended initial experiment:

```powershell
python -m safety_anomaly.cli run --quick --sample-size 5000
```

Run the larger configured grids only after checking runtime and memory:

```powershell
python -m safety_anomaly.cli run --sample-size 5000
```

Available feature representations:

```powershell
python -m safety_anomaly.cli run --quick --sample-size 5000 --representation structured
python -m safety_anomaly.cli run --quick --sample-size 5000 --representation structured_injury
python -m safety_anomaly.cli run --quick --sample-size 5000 --representation structured_text
```

LOF is limited by `experiments.lof_max_rows` in `configs/default.yaml` (default 10,000). Do not raise it without benchmarking memory and runtime. IF/LOF are compared on the same deterministic sample.

## 7. Run the notebooks

```powershell
jupyter lab
```

Open notebooks in this order:

1. `01_dataset_audit.ipynb`
2. `02_exploratory_data_analysis.ipynb`
3. `03_preprocessing_and_features.ipynb`
4. `04_anomaly_detection_models.ipynb`
5. `05_pca_and_evaluation.ipynb`

Select the `.venv` Python kernel. The notebooks call the same reusable package functions used by the CLI.

## 8. Run the Streamlit website

```powershell
streamlit run app/streamlit_app.py
```

Open the local URL printed by Streamlit, normally http://localhost:8501. Run the audit and experiment pipeline first to populate the dashboard.

## 9. Test and validate

```powershell
pytest -q
```

Run an end-to-end quick smoke test:

```powershell
python -m safety_anomaly.cli audit
python -m safety_anomaly.cli run --quick --sample-size 1000
pytest -q
```

Then launch Streamlit and check all navigation pages. The automated tests cover data audit behavior, preprocessing, both detectors, agreement metrics, and privacy-safe exports. Streamlit page rendering is additionally checked through a local manual smoke test.

## 10. Package the project as a ZIP archive

From the project root, create a self-contained ZIP (including the local raw CSV):

```powershell
python scripts/package_project.py
```

The default archive is created one directory above the project folder as `Safety-Incident-Anomaly-Detection.zip`. To create an archive without the raw dataset:

```powershell
python scripts/package_project.py --without-dataset
```

Alternatively, from the parent directory in Windows PowerShell:

```powershell
Compress-Archive -Path .\Safety-Incident-Anomaly-Detection -DestinationPath .\Safety-Incident-Anomaly-Detection.zip -Force
```

The packaging script excludes virtual environments, Git internals, caches and private manual-review artifacts. It includes the supplied dataset by default so the recipient can run the pipeline locally. Do not commit that CSV to a public Git repository.

## 11. Outputs

- `reports/data_audit/`: data-quality summaries.
- `artifacts/public/`: aggregated summaries, experiment tables, PCA coordinates/figures and a public-safe anomaly explorer export.
- `artifacts/private/`: blinded manual-review worksheet. Do not commit it.
- `artifacts/models/`: reserved for serialized models if later required.

The public-safe export does not include UPA, employer, street address, ZIP, exact coordinates or raw narrative text.

## 12. Manual review

The pipeline generates `artifacts/private/blinded_manual_review.csv`. Reviewers should use a predefined rubric such as unusual incident pattern, plausible ordinary incident, data-quality anomaly, or indeterminate. The sheet intentionally omits model membership. Do not present reviewer opinions as ground truth; report reviewer count and agreement where available.

## 13. Research interpretation

Jaccard similarity, Adjusted Rand Index and Spearman score correlation describe agreement between unsupervised models, not anomaly accuracy. Injury outcome indicators are not anomaly labels. Claims about false positives require manual or independently verified review.

## 14. Reproducibility

- Fixed random seed in YAML configuration.
- Exact sample size and parameter settings saved in experiment outputs.
- Reusable source modules and notebooks.
- Raw source file preserved unchanged.
- Runtime and model configuration included in experiment summary.

## 15. Citation

See `CITATION.cff` and `docs/METHODOLOGY.md`. Verify source and method references before formal academic submission.

## 16. Limitations

The data are subject to reporting and selection bias. Coverage and completeness vary by industry, location, reporting practices and source scope. Statistical outliers are not necessarily harmful or preventable. Model outputs must not be used to rank employers or make employment decisions.
