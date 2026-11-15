# Model Card: Workplace Incident Pattern and Anomaly Screening

## Intended use

This project is an INT396 unsupervised-learning study using OSHA Severe Injury Reports. The operational prototype supports a qualified reviewer by placing a newly described incident in the fitted feature space, showing an exploratory K-Means pattern group, screening for unusual representations with Isolation Forest, retrieving nearby historical reports and collecting structured follow-up notes. It is for educational demonstration and human-led review only.

## Not intended for

- Predicting whether an accident will occur.
- Estimating the probability or severity of future injury.
- Determining negligence, fault, preventability, or legal compliance.
- Ranking workers, employers, facilities, or contractors.
- Replacing emergency response, a site inspection, an investigation, or a qualified safety professional.
- Treating anomaly flags, cluster IDs or nearest-neighbour similarity as verified hazard labels or causal explanations.

## Data and scope

- Source: OSHA Severe Injury Reports, downloaded from the official OSHA Severe Injury Dashboard.
- Local source-file coverage in the supplied extract: 1 January 2015 through 30 November 2025.
- Full supplied extract: 105,996 rows and 28 columns.
- Model/experiment sample: 5,000 records selected deterministically with random seed 42.
- The source represents selected severe injuries reported within federal OSHA jurisdiction. It does not include all state-plan records, near misses, all recordable injuries, or a representative census of workplaces.
- Employer names, addresses, coordinates, source identifiers and the injury-outcome fields `Hospitalized`, `Amputation` and `Loss of Eye` are excluded from model input features.
- The deployable model bundle retains fitted transformers, detector/grouping components and non-identifying comparison attributes; it does not retain raw narratives, employer names, establishment addresses, source record identifiers or exact coordinates.
- The raw CSV is not bundled in the deployment ZIP. It must be obtained separately from the official OSHA source to reproduce the full data audit and research pipeline.

## Feature representation

- Structured inputs: Primary NAICS, EventTitle, SourceTitle and Secondary Source Title.
- Narrative input: `Final Narrative`, represented with TF-IDF unigrams and bigrams (up to 2,500 terms).
- Categorical missing values are represented as `Unknown`; calendar-derived values are created from EventDate.
- Categorical features are one-hot encoded. The combined sparse representation is reduced to 24 TruncatedSVD components and standardised with StandardScaler.
- Outcome fields and direct identifiers are held out and are not used in training, clustering, anomaly scoring or nearest-neighbour distance calculations.

## Methods

### Operational prototype

- Pattern grouping: K-Means, k=8, random seed 42, n_init=10 and max_iter=300. Group profiles show frequent descriptive categories only.
- Anomaly screen: Isolation Forest, 250 trees, random seed 42 and contamination parameter 0.03.
- Similarity retrieval: Euclidean nearest-neighbour search in the 24-dimensional fitted representation.
- Reference threshold: percentile relative to anomaly scores on the fitted 5,000-record reference sample.

### Course experiment

Six settings are compared on the same 5,000-record / 24-dimensional sample:

- Isolation Forest: 100 estimators at 1% contamination; 100 estimators at 3%; 200 estimators at 3%.
- Local Outlier Factor: 15 neighbours at 1% contamination; 15 neighbours at 3%; 25 neighbours at 3%; Euclidean distance throughout.

All 15 pairwise configuration comparisons are retained using Jaccard overlap, adjusted Rand index and Spearman score correlation. These quantify agreement and sensitivity, not classification accuracy.

## Evaluation results

- The selected IF (100 estimators, 3%) and LOF (15 neighbours, 3%) configurations each flagged 150 of 5,000 records; 19 flags overlapped. Jaccard = 0.0676, adjusted Rand index = 0.0941 and Spearman score correlation = 0.1387.
- Mean within-IF Jaccard across three IF pairs = 0.4294; mean within-LOF Jaccard across three LOF pairs = 0.4265; mean cross-method Jaccard across nine IF/LOF pairs = 0.0591.
- K-Means candidates k=4, 6, 8 and 10 were compared. The exploratory k=8 configuration reports silhouette = 0.1367 (2,000-row scoring sample), Davies-Bouldin = 2.2188, Calinski-Harabasz = 277.90 and mean pairwise ARI = 0.5291 across seeds 13, 42 and 77. Separation is modest and assignments vary by initialisation.
- The first three PCA components explain approximately 15.71% of variance. The projection is exploratory and does not establish cluster correctness.
- The outcome-proxy analysis is a descriptive post-hoc check using held-out `Hospitalized`, `Amputation` and `Loss of Eye` fields. Those values are not ground-truth anomaly labels. The loss-of-eye-present subset in the sample contains one record and is not interpretable.
- No human expert adjudication or prospective validation was conducted for this submission.

## Interpretation and false-positive implications

A high anomaly percentile means the representation differs from the sampled reported-injury records. It does not mean a 97% risk, a high probability of injury or evidence that a workplace is unsafe. A low percentile does not establish safety. A rare but valid event, unusual wording, sparse category combination, incomplete description or reporting-pattern change can trigger a flag.

The 1% and 3% contamination settings are experimental thresholds, not estimates of real-world anomaly prevalence. Since the data contain only selected severe-injury reports and no verified anomaly labels, true/false positives, precision, recall, sensitivity, specificity and a true false-positive rate cannot be calculated.

## Known limitations and bias

- Reporting and selection bias in the source data; only specified severe injuries are represented.
- Federal OSHA jurisdiction only; OSHA-approved State Plan records are excluded from this source.
- No verified positive/negative anomaly labels and no completed expert adjudication.
- Industry frequencies and reporting practices differ; sparse categories and missing fields can influence representations.
- Narrative wording, spelling, detail and quality affect TF-IDF-based similarity and anomaly scores.
- IF and LOF show low cross-method agreement under the selected configurations.
- K-Means cluster separation is modest and cluster assignments vary with initialisation.
- The operational workflow has not been prospectively evaluated with safety professionals.
- Session-based case records are not a secure multi-user records system.

## Human oversight and privacy

A qualified reviewer must verify facts and decide what follow-up is appropriate. The app warns users not to enter names, addresses, medical identifiers or other personal information. Session cases can be exported but are not enterprise case management. Do not use confidential or identifiable incident records in the public deployment.

## Reproducibility

- Full data audit and IF/LOF experiment: `python -m safety_anomaly.cli run --quick --sample-size 5000` after placing the official source CSV at `data/raw/January2015toNovember2025.csv`.
- Cluster-count/seed evaluation: `python scripts/evaluate_clusters.py --sample-size 5000`.
- Operational model build: `python scripts/build_review_model.py --sample-size 5000`.
- Fitted deployment bundle: `artifacts/models/incident_review_engine.joblib`.
- Detailed outputs: `artifacts/public/`.

## Official data source

OSHA Severe Injury Dashboard: https://www.osha.gov/severe-injury-reports

OSHA Severe Injury Reports information: https://www.osha.gov/severeinjury/
