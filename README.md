# Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF

**Application:** Worksite | Incident Intelligence  
**Course:** INT396, Unsupervised Learning  
**Project mapping:** SIH / SIH26165  
**Project type:** Individual

<p align="center">
  <a href="https://sih26165-safety-incident-anomaly-detection-kmsgsezehgz7hrnwtbq.streamlit.app/"><strong>Open the live Worksite application</strong></a>
  &nbsp; · &nbsp;
  <a href="https://github.com/Dhruva105/SIH26165-Safety-Incident-Anomaly-Detection"><strong>GitHub repository</strong></a>
  &nbsp; · &nbsp;
  <a href="https://www.osha.gov/severeinjury"><strong>OSHA data source</strong></a>
</p>

---

## Student and course details

| Field | Details |
|---|---|
| Student | Dhruv Pal |
| Roll number | RK3P24RDA26 |
| Registration ID | 12408224 |
| Section | K3P24RD |
| Project type | Individual |
| Project title | Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF |
| Project mapping | SIH |
| Mapped ID | SIH26165 |
| Course outcomes | CO2, CO4, CO5 |
| Mapped units | Unit V & IV: Anomaly Detection (Isolation Forest / LOF) and PCA Visualisation |

## 1. Project overview

Worksite is a research prototype for reviewing reported workplace severe-injury incidents. It combines structured incident fields with the text of an incident narrative, screens a new report for unusual patterns, places it in an exploratory pattern group, retrieves similar historical reports and gives a reviewer a structured set of follow-up questions.

The project has two connected parts:

1. **Research pipeline:** data preparation, feature construction, Isolation Forest and Local Outlier Factor (LOF) experiments, parameter comparisons, PCA visualisation and unsupervised evaluation.
2. **Operational demonstration:** a Streamlit application for incident intake, Isolation Forest screening, K-Means grouping, historical-neighbour retrieval, human review and JSON export.

The methods are established machine-learning techniques. The project contribution is their documented comparison on this selected OSHA report sample and their connection to a reviewer-facing workflow. The project does not claim a new anomaly-detection algorithm.

### Live application

**[Launch Worksite | Incident Intelligence](https://sih26165-safety-incident-anomaly-detection-kmsgsezehgz7hrnwtbq.streamlit.app/)**

The deployed app uses the GitHub main branch and the Streamlit entry point at app/streamlit_app.py.

## 2. Problem statement and objectives

Workplace incident reports contain both structured fields (such as event category and equipment source) and unstructured narrative descriptions. Reviewing a large collection manually can make it difficult to locate less common combinations, compare detection methods and organise follow-up investigation.

The project examines whether unsupervised methods can help surface unusual report patterns and provide useful context for human review.

### Official Objective 1: Data preparation

Prepare the selected open industrial safety-incident report data, identify relevant features, handle missing values, encode categorical variables and scale numerical features before applying unsupervised methods.

**Implementation evidence:** data audit, feature-building pipeline, missingness outputs, One-Hot Encoding, TF-IDF, TruncatedSVD and StandardScaler.

### Official Objective 2: Apply and compare anomaly detectors

Apply Isolation Forest and LOF to the prepared features, compare records flagged by each method across multiple parameter settings, and use PCA visualisation plus available labels or manual review to assess consistency.

**Implementation evidence:** six configured IF/LOF runs, pairwise agreement outputs, PCA plots and experiment summary files.

### Official Objective 3: Evaluate and interpret

Evaluate detection consistency, examine false-positive implications, and document limitations, possible bias and ethical considerations.

**Implementation evidence:** Jaccard, Adjusted Rand and score-correlation measures; descriptive checks against held-out injury-outcome fields; clustering diagnostics; model card and ethics documentation.

## 3. Dataset and coverage

The research pipeline uses the OSHA Severe Injury Reports extract:

**File name:** January2015toNovember2025.csv  
**Inspected extract:** 105,996 rows and 28 columns  
**Event-date range:** 1 January 2015 to 30 November 2025

The local data audit recorded:

- 105,996 non-null, unique UPA values.
- No exact duplicate rows.
- Five repeated distinct ID values affecting ten rows.
- No invalid event dates in the inspected extract.
- No empty narratives in the inspected extract.

### What the OSHA data represent

The OSHA Severe Injury Reports data concern reports of work-related amputations, inpatient hospitalisations and loss of an eye under federal OSHA reporting requirements. The reporting requirement began on 1 January 2015. The public dataset does not include incidents under OSHA-approved State Plans.

It is therefore not a census of all workplace injuries, near misses, unsafe acts or workplace hazards. Results from this project must be interpreted within that reporting scope.

**Official source and coverage notes:** [OSHA Severe Injury Reports](https://www.osha.gov/severeinjury)

### Data handling and privacy

The raw CSV is not included in this repository. It can contain establishment, location and narrative information. Keep the source data in a controlled local environment and do not upload identifiable or confidential incident records to the public repository or the demonstration website.

The modelling workflow excludes direct identifiers, employer and address fields, detailed location fields, inspection identifiers and injury-outcome fields from the primary feature representation. Held-out outcome indicators are used only for a post-hoc descriptive comparison, not as model inputs or verified anomaly labels.

## 4. Methodology

The research representation combines categorical, date-derived and narrative features.

| Stage | Method | Purpose |
|---|---|---|
| Data validation | Type checks, date parsing and missing-value handling | Prepare consistent records |
| Categorical representation | One-Hot Encoding | Represent event, industry and source categories numerically |
| Narrative representation | TF-IDF with unigrams and bigrams | Convert incident text into weighted numerical features |
| Dimensionality reduction | TruncatedSVD | Reduce the sparse feature representation |
| Scaling | StandardScaler | Standardise the reduced numerical representation |
| Anomaly detection | Isolation Forest and LOF | Identify unusual observations using different principles |
| Pattern grouping | K-Means | Group reports with similar feature representations |
| Visualisation | PCA | Project high-dimensional records into a lower-dimensional view |

The principal structured-text experiment uses a 5,000-record deterministic sample with random state 42 and a 24-dimensional representation after TruncatedSVD. The TF-IDF stage is configured for up to 2,500 features, unigrams and bigrams, with a minimum document frequency of three. Categorical levels with frequency below 15 are grouped through the configured encoder behaviour.

### 4.1 Isolation Forest

Isolation Forest identifies observations that can be separated from the sample using relatively few random partitioning steps. The research experiments vary the number of trees and contamination settings. The deployed incident-review model uses 250 trees, random state 42 and a contamination parameter of 0.03.

The contamination parameter controls the model's expected flagged fraction during fitting. It is not an estimate of the real-world proportion of unsafe workplaces or incidents.

### 4.2 Local Outlier Factor

LOF compares the local density around an observation with the local density around its neighbours. The experiment varies neighbour counts and contamination settings. LOF is used in the research comparison; the deployed incident-review workflow uses Isolation Forest for its operational screen.

### 4.3 K-Means and PCA

K-Means is used to provide exploratory pattern groups. The experiment evaluates k values of 4, 6, 8 and 10, including comparisons across random seeds 13, 42 and 77. The deployed application uses k=8 as a documented exploratory choice, not as a proven optimal number of hazard classes.

PCA is used to visualise the reduced feature space. A two- or three-dimensional projection cannot preserve all information in the original representation and does not establish that an observation is truly anomalous.

## 5. Experimental design and reported results

The IF/LOF experiment compares six configurations on the same deterministic 5,000-record feature matrix:

| Configuration | Parameters |
|---|---|
| IF-01 | Isolation Forest, 100 trees, contamination 0.01 |
| IF-02 | Isolation Forest, 100 trees, contamination 0.03 |
| IF-03 | Isolation Forest, 200 trees, contamination 0.03 |
| LOF-01 | LOF, 15 neighbours, contamination 0.01 |
| LOF-02 | LOF, 15 neighbours, contamination 0.03 |
| LOF-03 | LOF, 25 neighbours, contamination 0.03 |

### Selected IF/LOF comparison

For the selected 3% configurations in the checked-in experiment outputs:

| Measure | Result |
|---|---:|
| Sample size | 5,000 |
| Isolation Forest flagged records | 150 |
| LOF flagged records | 150 |
| Shared flagged records | 19 |
| Jaccard similarity | 0.0676 |
| Adjusted Rand Index | 0.0941 |
| Spearman score correlation | 0.1387 |

The selected detectors show low overlap. This is evidence of disagreement between the two unsupervised methods under these settings. It is not evidence that either method is accurate or inaccurate because the dataset does not contain independently adjudicated anomaly labels.

Across the six configurations, the checked-in pairwise summary reports mean Jaccard values of 0.4294 for within-Isolation-Forest comparisons, 0.4265 for within-LOF comparisons and 0.0591 for cross-method comparisons. These values show that parameter choices and detector family affect which records are flagged.

### K-Means cluster-count evaluation

| k | Silhouette | Mean pairwise ARI across seeds |
|---:|---:|---:|
| 4 | 0.0679 | 0.6777 |
| 6 | 0.1062 | 0.5861 |
| 8 | 0.1367 | 0.5291 |
| 10 | 0.1547 | 0.5027 |

For k=8, the checked-in output also reports a Davies-Bouldin index of 2.2188 and a Calinski-Harabasz index of 277.90. The silhouette value is computed on a 2,000-row evaluation sample. K=8 is retained as an exploratory compromise between cluster separation and stability. K=10 has a higher silhouette value, while k=8 has somewhat higher cross-seed ARI. These internal measures do not validate the clusters against known hazard categories.

### Available result files

The aggregate outputs and figures are stored under artifacts/public/:

- experiment_summary.csv
- agreement_metrics.json
- parameter_agreement.csv
- outcome_proxy_comparison.csv
- cluster_evaluation.csv
- cluster_profiles.csv
- pca_iforest.png
- pca_lof.png

The application reads these public aggregate outputs for its research evidence pages.

## 6. Worksite application

The application connects the research representation to a guided incident-review workflow.

### Incident intake and screening

A reviewer can enter the event date, optional industry NAICS code, event category, source/equipment, optional injury descriptors and a factual narrative. The interface warns users not to enter names, medical identifiers, exact addresses or confidential information.

The fitted engine transforms the submitted incident using the saved feature pipeline. It then returns an Isolation Forest score, a relative percentile against the fitted reference sample, a K-Means pattern group and five nearest historical records.

### Review and case record

The application also provides rule-based prompts about the event sequence, immediate response, existing controls, contributing conditions and corrective actions. The reviewer can add notes, an owner role/team and a due date, then export the record as JSON.

The checklist is a set of review prompts. It is not a recommendation engine and does not decide whether a workplace is safe.

### Important interpretation limits

- An anomaly percentile is a relative position against the fitted reference sample, not an injury probability.
- A flagged record requires human assessment.
- A non-flagged record is not evidence that an activity is safe.
- Similar historical reports do not prove a common cause.
- K-Means group IDs are statistical groupings, not validated hazard classes.

### Storage and security

The current case register uses Streamlit session state. It is not a persistent, secure multi-user case-management system. Records may be lost when a session ends or the app restarts. Do not enter names, personal details, medical identifiers, precise addresses or confidential workplace information.

## 7. Technology stack

| Layer | Tools |
|---|---|
| User interface | Python, Streamlit, custom CSS |
| Data processing | pandas, NumPy, SciPy |
| Text representation | scikit-learn TF-IDF |
| Dimensionality reduction | TruncatedSVD and PCA |
| Anomaly detection | Isolation Forest and Local Outlier Factor |
| Clustering | K-Means |
| Similar-case retrieval | NearestNeighbors |
| Visualisation | Plotly, Matplotlib and Seaborn |
| Model persistence | joblib |
| Testing | pytest |
| Version control | Git and GitHub |
| Deployment | Streamlit Community Cloud |

## 8. Repository structure

~~~text
SIH26165-Safety-Incident-Anomaly-Detection/
├── app/
│   ├── streamlit_app.py
│   ├── theme.css
│   ├── utils.py
│   └── pages/
│       ├── incident_review.py
│       ├── overview.py
│       ├── dataset.py
│       ├── methodology.py
│       ├── results.py
│       ├── explorer.py
│       ├── ethics.py
│       └── references.py
├── artifacts/
│   ├── models/
│   │   └── incident_review_engine.joblib
│   └── public/
├── configs/
│   └── default.yaml
├── data/
│   └── raw/                 # local source data; not committed
├── docs/
├── notebooks/
├── reports/
├── scripts/
├── src/
│   └── safety_anomaly/
├── tests/
├── pyproject.toml
├── requirements.txt
└── README.md
~~~

The fitted model at artifacts/models/incident_review_engine.joblib is required for the deployed incident-review workflow. The original raw OSHA CSV is not required to run the already-fitted web application.

## 9. Run locally on Windows

Python 3.13 is recommended to match the model build environment and the repository's .python-version file.

Open PowerShell in the project root, the directory containing README.md:

1. Create a virtual environment:

~~~powershell
py -3.13 -m venv .venv
~~~

2. Activate it:

~~~powershell
.venv\Scripts\Activate.ps1
~~~

3. Install dependencies:

~~~powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e . --no-deps
~~~

4. Start the website:

~~~powershell
streamlit run app/streamlit_app.py
~~~

5. Open the local address printed in the terminal, usually:

~~~text
http://localhost:8501
~~~

If PowerShell blocks environment activation, run:

~~~powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
~~~

## 10. Test the application

Run the automated tests:

~~~powershell
pytest -q
~~~

Compile-check the Python source:

~~~powershell
python -m compileall -q src app scripts tests
~~~

For a manual smoke test, submit a fictional conveyor-cleaning incident. Check that the app returns a pattern group, anomaly screening result, five similar reports, review prompts and a downloadable JSON record. Synthetic test incidents are for interface testing only; do not report their outputs as research findings.

## 11. Reproduce the research pipeline

The full analysis requires the raw OSHA extract downloaded from the official OSHA source. Place the file locally at:

~~~text
data/raw/January2015toNovember2025.csv
~~~

Run the data audit:

~~~powershell
python -m safety_anomaly.cli audit
~~~

Run the IF/LOF experiment:

~~~powershell
python -m safety_anomaly.cli run --quick --sample-size 5000
~~~

Evaluate K-Means cluster counts and seed stability:

~~~powershell
python scripts/evaluate_clusters.py --sample-size 5000
~~~

Rebuild the operational review model:

~~~powershell
python scripts/build_review_model.py --sample-size 5000
~~~

The experiment configuration is in configs/default.yaml. Check available memory and runtime before increasing sample sizes, particularly for LOF.

## 12. Deploy on Streamlit Community Cloud

The current application is deployed from this existing repository. Do not create a second repository just to deploy the project.

1. Open [Streamlit Community Cloud](https://share.streamlit.io/) and sign in with GitHub.
2. Select **Create app** (or open the existing app's settings).
3. Select repository Dhruva105/SIH26165-Safety-Incident-Anomaly-Detection.
4. Select branch main.
5. Set the main file path to app/streamlit_app.py.
6. Select a Python version compatible with the pinned dependencies and fitted model. Python 3.13 is the recommended local parity version.
7. Deploy or reboot the existing app if required.
8. Inspect the deployment logs and test the incident intake, pattern group, anomaly screen, historical matches and JSON export.

**Live deployment:** [https://sih26165-safety-incident-anomaly-detection-kmsgsezehgz7hrnwtbq.streamlit.app/](https://sih26165-safety-incident-anomaly-detection-kmsgsezehgz7hrnwtbq.streamlit.app/)

If the app fails to start, inspect **Manage app → Logs** before changing dependencies. Keep scikit-learn and joblib compatible with the fitted model artifact.

## 13. Limitations, bias and responsible use

1. **Coverage:** the OSHA extract represents selected severe-injury reports under federal OSHA jurisdiction, not all injuries or near misses.
2. **Reporting bias:** records reflect reporting practices, regulatory scope and the industries represented in the data.
3. **No anomaly ground truth:** independently verified labels are unavailable. Agreement scores cannot be interpreted as accuracy.
4. **Detector disagreement:** the selected IF and LOF configurations share few flagged records. This limits claims about stable anomaly identification.
5. **Cluster quality:** K-Means groups show modest internal separation and vary across initialisations.
6. **Feature representation:** TF-IDF and dimensionality reduction can omit context, sequence and meaning from a narrative.
7. **Human validation:** the operational workflow has not been prospectively validated by workplace safety professionals.
8. **Application storage:** the case register is session-based and is not suitable for confidential or regulated records.

Worksite is an academic research prototype. It must not be used as an emergency response service, a legal compliance checker, a calibrated safety-risk model or an automated basis for employment or disciplinary decisions. A qualified safety professional must assess the incident and supporting evidence.

## 14. Research context and selected literature

Prior studies have already applied text mining, natural language processing, clustering and anomaly detection to accident and safety reports. This project does not claim that Isolation Forest, LOF, K-Means, TF-IDF or PCA are new algorithms. Its applied focus is a reproducible comparison of unsupervised detector agreement and parameter sensitivity, together with a reviewer-facing workflow that links pattern context, anomaly screening, historical neighbours and structured follow-up.

Selected related work:

1. B. Song and Y. Suh, "Narrative texts-based anomaly detection using accident report documents: The case of chemical process safety," *Journal of Loss Prevention in the Process Industries*, vol. 57, pp. 47–54, 2019. [https://doi.org/10.1016/j.jlp.2018.08.010](https://doi.org/10.1016/j.jlp.2018.08.010)
2. J. Ricketts, D. Barry, W. Guo, and J. Pelham, "A Scoping Literature Review of Natural Language Processing Application to Safety Occurrence Reports," *Safety*, vol. 9, no. 2, art. 22, 2023. [https://doi.org/10.3390/safety9020022](https://doi.org/10.3390/safety9020022)
3. M. Smetana, L. S. de Salles, I. Sukharev, and L. Khazanovich, "Highway Construction Safety Analysis Using Large Language Models," *Applied Sciences*, vol. 14, no. 4, art. 1352, 2024. [https://doi.org/10.3390/app14041352](https://doi.org/10.3390/app14041352)
4. M. Shayboun, D. Kifokeris, and C. Koch, "A review of machine learning for analysing accident reports in the construction industry," *Journal of Information Technology in Construction*, vol. 30, pp. 439–460, 2025. [https://doi.org/10.36680/j.itcon.2025.019](https://doi.org/10.36680/j.itcon.2025.019)
5. J. B. Macêdo et al., "Identifying low-quality patterns in accident reports from textual data," *International Journal of Occupational Safety and Ergonomics*, vol. 29, no. 3, pp. 1088–1100, 2023. [https://doi.org/10.1080/10803548.2022.2111847](https://doi.org/10.1080/10803548.2022.2111847)

## 15. Citation and licence

The repository includes a CITATION.cff file and an MIT licence. Cite the OSHA dataset and relevant methods papers when reusing the data, code or analysis. Check the source terms and licence before redistributing the raw dataset or derived records.

---

**Project:** SIH26165  
**Student:** Dhruv Pal  
**Application:** [Worksite | Incident Intelligence](https://sih26165-safety-incident-anomaly-detection-kmsgsezehgz7hrnwtbq.streamlit.app/)  
**Source code:** [GitHub repository](https://github.com/Dhruva105/SIH26165-Safety-Incident-Anomaly-Detection)
