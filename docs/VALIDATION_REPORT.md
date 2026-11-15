# Local Build Validation Report

Date: 15 November 2026  
Dataset: OSHA Severe Injury Reports extract from 1 January 2015 through 30 November 2025

## Dataset audit

- 105,996 rows and 28 columns.
- `UPA`: 105,996 unique, non-null values.
- `ID`: five distinct repeated values affect ten records; exact duplicate rows: 0.
- Event date range: 2015-01-01 to 2025-11-30; invalid dates: 0.
- Empty `Final Narrative` values in the supplied extract: 0.
- Most-missing fields include `Address2` (91.223%), `Inspection` (66.536%) and `Secondary Source Title` (52.249%). The selected modelling path does not require address/inspection fields; missing categories are represented as `Unknown`.

## Feature construction

- Deterministic modelling sample: 5,000 records, random seed 42.
- Categorical fields: Primary NAICS, EventTitle, SourceTitle and Secondary Source Title, one-hot encoded.
- Narrative field: Final Narrative, TF-IDF unigrams and bigrams, up to 2,500 terms.
- Calendar fields are derived from EventDate. The combined sparse feature representation is reduced to 24 TruncatedSVD components and standardised using StandardScaler.
- Employer, addresses, coordinates, source IDs and injury outcome fields are excluded from model inputs.

## Isolation Forest and LOF experiments

Six configurations were run on the same 5,000-record / 24-dimensional sample:

| Detector | Parameters | Flagged |
|---|---|---:|
| Isolation Forest | 100 estimators, contamination 0.01 | 50 (1%) |
| Isolation Forest | 100 estimators, contamination 0.03 | 150 (3%) |
| Isolation Forest | 200 estimators, contamination 0.03 | 150 (3%) |
| LOF | 15 neighbours, contamination 0.01, Euclidean | 50 (1%) |
| LOF | 15 neighbours, contamination 0.03, Euclidean | 150 (3%) |
| LOF | 25 neighbours, contamination 0.03, Euclidean | 150 (3%) |

All 15 pairwise configuration comparisons are stored in `artifacts/public/parameter_agreement.csv`. Mean Jaccard overlap is 0.4294 across the three IF-vs-IF pairs, 0.4265 across the three LOF-vs-LOF pairs and 0.0591 across the nine IF-vs-LOF pairs. These values indicate meaningful configuration/method dependence; they are not accuracy measures.

For the selected IF (100 estimators, 3%) and LOF (15 neighbours, 3%) configurations, each flagged 150 records and only 19 flags overlapped. Jaccard = 0.0676, adjusted Rand index = 0.0941 and Spearman score correlation = 0.1387.

## Available outcome-proxy check

`Hospitalized`, `Amputation` and `Loss of Eye` are excluded from the feature matrix and used only for descriptive post-hoc comparison. An outcome is marked present when its numeric value is greater than zero. In this sample:

- IF flag rate: 3.520% among records with a reported hospitalization versus 0.747% without one.
- IF flag rate: 0.853% among records with a reported amputation versus 3.748% without one.
- Only one record has a positive `Loss of Eye` indicator in this sample; that subset is too small for interpretation.
- LOF flag rates are 3.052% versus 2.775% for hospitalization presence/absence and 3.178% versus 2.939% for amputation presence/absence.

These outcomes are not anomaly ground truth. The descriptive differences cannot identify false positives, true positives, sensitivity or specificity. The dataset consists of severe-injury reports, not a representative set of normal and anomalous workplace situations.

## Clustering and PCA

- K-Means candidates k=4, 6, 8 and 10 were compared using silhouette, Davies-Bouldin and Calinski-Harabasz indices.
- The selected exploratory k=8 configuration has silhouette 0.1367 (2,000-row scoring sample), Davies-Bouldin 2.2188, Calinski-Harabasz 277.90 and mean pairwise ARI 0.5291 across seeds 13, 42 and 77. Cluster separation is modest and assignments vary with initialisation.
- PCA plots for IF and LOF are included. The first three components explain approximately 15.71% of variance; projections are exploratory.

## Automated checks

- `pytest -q`: 10 passed.
- `python -m compileall -q src app scripts tests`: passed.
- Model artifact loads; direct fictional-incident inference returns a cluster group, five similar records and review prompts. This is a software-path test, not an evaluation of real-world safety outcomes.

## Interpretation and limitations

There are no independently adjudicated anomaly labels. The contamination parameter controls how many training observations are flagged; it is not the true anomaly prevalence. The source includes only reported severe injuries under federal OSHA jurisdiction and excludes State Plan jurisdiction records. Reporting, industry, selection and narrative-quality biases remain. The results do not establish false-positive rates, validated hazard labels, future-accident prediction, causal explanations or operational effectiveness. Human review remains essential.

## Browser verification

The model/backend and automated tests were validated in the build environment. The Streamlit browser interface was not end-to-end launched here because Streamlit installation was unavailable in the offline execution environment. Complete the workflow smoke test after local dependency installation or deployment before sharing the live URL.
