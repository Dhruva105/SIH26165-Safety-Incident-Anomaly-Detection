# Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF

**Application name:** Worksite | Incident Review  
**Course:** INT396 – Unsupervised Learning  
**Project type:** Individual  
**Student:** Dhruv Pal  
**Roll No.:** RK3P24RDA26  |  **Registration ID:** 12408224  |  **Section:** K3P24RD  
**Project mapping:** SIH  |  **Mapped ID:** SIH26165  
**Course outcomes:** CO2, CO4, CO5  
**Mapped units:** Unit V & IV – Anomaly Detection (Isolation Forest / LOF) and PCA Visualisation  
**Institution:** Lovely Professional University  
**Methods:** One-hot encoding, TF-IDF, TruncatedSVD, StandardScaler, Isolation Forest, Local Outlier Factor, K-Means and PCA

## Course mapping and objectives

The official title, SIH mapping, course outcomes and three objectives are mapped to implementation evidence in [`docs/COURSE_ALIGNMENT.md`](docs/COURSE_ALIGNMENT.md). The project keeps outcome fields outside feature construction and uses them only in a clearly labelled post-hoc descriptive check. The three official objectives and their code/artifact evidence are mapped in the course-alignment document.

## 1. What the project does

Worksite is an incident review prototype built around a real workplace-safety workflow. It helps a safety reviewer move from an incident description to structured evidence collection:

1. Capture an incident using structured fields and a factual narrative.
2. Represent the incident using the same fitted structured-text feature pipeline used for the historical reference sample.
3. Assign it to one of eight exploratory K-Means pattern groups and show the group's most frequent event/source/injury descriptors.
4. Screen for unusual patterns using Isolation Forest.
5. Retrieve nearby historical reports using nearest-neighbour search.
6. Complete a rule-based human-review checklist, record follow-up ownership and export a case file.

This is a decision-support prototype. It is not an accident predictor, a calibrated safety-risk score, a compliance tool or an emergency response service. A high anomaly percentile does not mean a high probability of injury. A low percentile does not establish that a task is safe.

The research workflow remains available in the project pages and notebooks. It compares Isolation Forest and Local Outlier Factor, visualises lower-dimensional patterns with PCA and reports agreement measures. It also includes an explicit K-Means cluster-count and seed-stability evaluation.

## 2. Dataset and scope

The supplied local extract is the OSHA Severe Injury Reports dataset, named `January2015toNovember2025.csv`.

Audit of the supplied file:

- 105,996 rows and 28 columns.
- 105,996 unique, non-null UPA values.
- No exact duplicate rows.
- Five repeated distinct `ID` values affecting ten rows.
- No invalid event dates; event date range 2015-01-01 to 2025-11-30.
- No empty narratives in the inspected extract.

OSHA states that severe-injury reporting covers amputations, inpatient hospitalizations and loss of an eye. The requirement began on 1 January 2015. OSHA says the public Severe Injury Reports dataset is limited to federal OSHA jurisdiction and excludes incidents under OSHA-approved State Plans. It is not a census of all workplace injuries, near misses or unsafe acts. Review the official source for current data and scope notes: https://www.osha.gov/severeinjury

The raw CSV is deliberately excluded from this ZIP's Git-ready source package. It contains establishment/location information and free-text narratives. Download it from the official OSHA source and keep it local if you need to rerun the complete research pipeline. The included fitted model allows the website to run without the raw CSV.

## 3. Main application workflow

### Incident intake

The reviewer provides the event date, industry code (optional), event category, source/equipment, optional injury descriptors and a factual narrative. The interface warns users not to enter names, medical identifiers, exact addresses or confidential information.

### Pattern group

The incident is transformed into the fitted 24-dimensional structured-text representation and assigned to a K-Means group (k=8). The app shows the group's most frequent event, source and injury categories. Cluster IDs are statistical groups, not hazard classes or causal explanations.

### Anomaly screen

Isolation Forest (250 trees, `random_state=42`, contamination parameter 0.03) returns an anomaly score and relative percentile against the model's 5,000-record fitted reference sample. The contamination value is a model setting, not an estimate of real-world unsafe incidents.

### Similar historical records

The app retrieves five nearest records in the same fitted feature space. It displays only non-identifying fields retained in the model bundle. Similarity does not prove that two incidents share a cause or circumstances.

### Human review and export

Rule-based prompts help the reviewer check immediate response, event sequence, existing controls, contributing conditions and corrective actions. Hazard-specific prompts can be added for fall, caught-in, electrical, struck-by, fire/heat and chemical/exposure language. The reviewer can record an owner role/team, due date and notes, then export JSON.

Cases are held in Streamlit session state and can be exported. The app is not a secure multi-user records system and session records may be lost when a session ends or an app restarts. Do not use it to process confidential or identifiable incident records.

## 4. Architecture

```text
app/                         Streamlit frontend and page navigation
  pages/incident_review.py   Incident intake, screening, review and exports
  pages/                     Dataset, methodology, results, ethics and references
  theme.css                  Worksite visual design system
src/safety_anomaly/          Reusable backend and research package
  features/build.py          One-hot, date features, TF-IDF, TruncatedSVD and scaling
  operational_review.py      K-Means, Isolation Forest, nearest neighbours and review prompts
  models/                    Isolation Forest and LOF experiment functions
  evaluation/                 Agreement metrics and blinded-review utilities
  pipeline.py                Reproducible research pipeline
artifacts/models/            Fitted operational model (required for deployment)
artifacts/public/            Aggregate summaries, plots and evaluation outputs
docs/                        User guide, methodology, model card and validation notes
notebooks/                   Five ordered research notebooks
scripts/                     Model build, audit, pipeline and clustering evaluation scripts
tests/                       Automated tests
```

The frontend and backend are separate: Streamlit handles user interaction in `app/`; all model transformations and inference live in reusable Python modules in `src/safety_anomaly/`.

## 5. Setup on Windows

Recommended environment: **Python 3.13** to match the environment used to build the included model artifact.

Open PowerShell in the extracted project root (the folder containing `README.md`):

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps
```

If `py -3.13` is unavailable, install Python 3.13 from https://www.python.org/downloads/ and reopen PowerShell. The included model was built with scikit-learn 1.8.0; keep the pinned version in `requirements.txt` when deploying.

## 6. Run the website

```powershell
streamlit run app/streamlit_app.py
```

Open the local URL printed in the terminal, normally http://localhost:8501.

### Quick functional test

Try these fictional test narratives. They are only for checking the interface and are not part of the research dataset or experimental evidence.

**Scenario A – Conveyor cleaning:**

> During a planned cleaning task, material was removed from a conveyor transfer point. The belt was not fully isolated before the task began. While clearing residual material near the moving belt, a hand contacted a moving component. Work was stopped and the area was isolated for review.

**Scenario B – Ladder access:**

> A worker was accessing an elevated storage platform using a portable ladder. The ladder shifted while the worker was descending, causing a fall to the floor. The immediate work area was cleared and the ladder was taken out of use pending inspection.

**Scenario C – Forklift movement:**

> A powered forklift was reversing from a storage aisle while a pedestrian was moving through the same area. The vehicle and pedestrian paths crossed near the aisle end. The operation was stopped and the traffic route was reviewed.

**Scenario D – Heat exposure:**

> Outdoor maintenance continued during a period of high ambient temperature. The task involved sustained physical work and limited shaded recovery time. A worker reported heat-related symptoms and the task was stopped while the response and work-rest arrangements were reviewed.

For each scenario, verify that the app produces a pattern group, anomaly screen, historical matches, review checklist, action record and JSON download. Do not use the synthetic results as a paper result.

## 7. Run tests

```powershell
pytest -q
python -m compileall -q src app scripts tests
```

## 8. Reproduce the analysis (raw CSV required)

Download the source extract and place it at:

`data/raw/January2015toNovember2025.csv`

Run the data audit:

```powershell
python -m safety_anomaly.cli audit
```

Run the IF/LOF research experiment:

```powershell
python -m safety_anomaly.cli run --quick --sample-size 5000
```

Run the K-Means cluster-count and seed-stability evaluation:

```powershell
python scripts/evaluate_clusters.py --sample-size 5000
```

Rebuild the deployable operational model:

```powershell
python scripts/build_review_model.py --sample-size 5000
```

Run larger experiment grids only after checking runtime and memory. LOF is bounded by `experiments.lof_max_rows` in `configs/default.yaml`.

## 9. GitHub and Streamlit Community Cloud deployment

### Prepare GitHub

1. Create an empty repository on https://github.com/new, for example `worksite-incident-review`.
2. Do not add a README, license or `.gitignore` on GitHub; this folder already contains them.
3. In PowerShell, open the project root (the folder containing `README.md`) and initialise Git:

```powershell
git init
git branch -M main
git status --short
```

The raw OSHA CSV is not included in this package and must stay out of the public repository. The fitted model at `artifacts/models/incident_review_engine.joblib` must be included because the deployed application needs it.

4. Stage, commit and push:

```powershell
git add .
git status --short
git commit -m "Build Worksite incident review and pattern screening"
git remote add origin https://github.com/YOUR_USERNAME/worksite-incident-review.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username. Confirm the raw OSHA CSV is not staged. `artifacts/models/incident_review_engine.joblib` must be committed because the deployed app needs it.

### Deploy

1. Open https://share.streamlit.io/ and sign in with GitHub.
2. Select **Create app** and choose the repository you just pushed.
3. Choose branch `main`.
4. Set the entrypoint to `app/streamlit_app.py`.
5. In Advanced settings, choose Python 3.13 (or the same compatible Python version used for the final tested build).
6. Select **Deploy** and inspect the build logs.
7. Test the live form, pattern-group output, anomaly screen, historical matches and JSON export.
8. Copy the deployed `https://...streamlit.app` URL into the PowerPoint's Project Links slide and README.

Official deployment instructions: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 10. Verified project outputs

- `artifacts/models/incident_review_engine.joblib`: fitted model bundle for 5,000 records, 24-dimensional features, K-Means k=8 and Isolation Forest.
- `artifacts/public/experiment_summary.csv`: six IF/LOF configurations on the same deterministic 5,000-record experiment sample.
- `artifacts/public/agreement_metrics.json`: IF/LOF agreement measures for the selected configurations.
- `artifacts/public/parameter_agreement.csv`: pairwise Jaccard, ARI and score-correlation comparisons across all 15 pairs of the six IF/LOF configurations.
- `artifacts/public/outcome_proxy_comparison.csv`: descriptive flag-rate comparisons against held-out OSHA injury-outcome indicators. These are not anomaly labels or accuracy measures.
- `artifacts/public/cluster_evaluation.csv`: internal cluster indices and cross-seed ARI for k=4, 6, 8 and 10.
- `artifacts/public/cluster_profiles.csv`: aggregate dominant categories for the selected k=8 partition.
- `artifacts/public/pca_iforest.png` and `pca_lof.png`: descriptive PCA visualisations.

On the 5,000-record experiment sample, the selected IF (100 trees, 3% contamination) and LOF (k=15, 3% contamination) configurations each flag 150 records, with 19 shared flags. Their Jaccard similarity is 0.0676, adjusted Rand index is 0.0941 and Spearman score correlation is 0.1387. These values describe agreement between unsupervised methods; they do not represent anomaly detection accuracy. Across all parameter pairs, mean within-IF Jaccard is 0.4294, within-LOF Jaccard is 0.4265, and cross-method Jaccard is 0.0591.

The selected K-Means k=8 run reports a silhouette value 0.1367 (computed on a 2,000-row evaluation sample), Davies-Bouldin index 2.2188, Calinski-Harabasz index 277.90 and mean pairwise ARI 0.5291 across random seeds 13, 42 and 77. These are internal/initialization-stability diagnostics on one deterministic 5,000-row sample. They do not establish ground-truth hazard groups. See `docs/CLUSTERING_NOTE.md`.

## 11. Research-informed scope and contribution

Prior work has already applied text analytics, clustering and NLP to occupational incident narratives. A review of safety occurrence report NLP describes classification, information extraction, semantic search and topic modelling, while stressing data-quality and real-world validation issues. A 2024 highway-construction safety study also applies LLM-enabled narrative analysis and clustering. Therefore, this project does **not** claim that K-Means, Isolation Forest, LOF or TF-IDF are novel algorithms.

The applied contribution is a single reviewer-facing workflow that combines (a) recurring-pattern context from K-Means, (b) unusual-pattern screening from Isolation Forest, (c) record-level context from nearest neighbours and (d) structured human follow-up prompts and export. A later research paper should evaluate the usefulness and stability of this integrated workflow and compare its components rather than claim algorithmic novelty. Importantly, Song and Suh (2019) already applied text mining with LOF to narrative accident reports, and Smetana et al. (2024) analysed OSHA Severe Injury Reports using NLP and clustering. The work must therefore position itself as an applied, reproducible comparison and reviewer workflow, not as the first text-based anomaly detector or first OSHA narrative clustering study.

Selected related work:

- Song, B., & Suh, Y. (2019). Narrative texts-based anomaly detection using accident report documents: The case of chemical process safety. *Journal of Loss Prevention in the Process Industries, 57*, 47–54. https://doi.org/10.1016/j.jlp.2018.08.010
- Smetana, M., de Salles, L. S., Sukharev, I., & Khazanovich, L. (2024). Highway Construction Safety Analysis Using Large Language Models. *Applied Sciences, 14*(4), 1352. https://doi.org/10.3390/app14041352
- Ricketts, J., Barry, D., Guo, W., & Pelham, J. (2023). A Scoping Literature Review of Natural Language Processing Application to Safety Occurrence Reports. *Safety, 9*(2), 22. https://doi.org/10.3390/safety9020022
- Shayboun, M., Kifokeris, D., & Koch, C. (2025). A review of machine learning for analysing accident reports in the construction industry. *Journal of Information Technology in Construction, 30*, 439–460. https://doi.org/10.36680/j.itcon.2025.019
- Macêdo, J. B., Ramos, P. M. S., Maior, C. B. S., Moura, M. J. C., Lins, I. D., & Vilela, R. F. T. (2023). Identifying low-quality patterns in accident reports from textual data. *International Journal of Occupational Safety and Ergonomics, 29*(3), 1088–1100. https://doi.org/10.1080/10803548.2022.2111847

## 12. Limitations and next research stage

The dataset contains reports of selected severe injuries under federal OSHA jurisdiction; it is subject to reporting and selection bias. There are no independently adjudicated anomaly labels. Cluster boundaries have moderate/low internal separation and vary with K-Means initialization. The operational screen has not been prospectively validated with safety professionals. The current case register is session-only. Before organisational use, add authenticated access, persistent secured storage, role-based permissions, audit logging, retention controls and a formal safety/privacy review.

The subsequent IEEE-format research paper should be drafted from the verified implementation, reproducible experiments, actual reviewer assessment (if conducted) and checked references. Do not invent precision/recall, predictive accuracy, reviewer agreement or deployment outcomes.
