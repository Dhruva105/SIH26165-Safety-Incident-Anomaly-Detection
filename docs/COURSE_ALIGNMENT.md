# INT396 Course Alignment and Implementation Evidence

**Student:** Dhruv Pal  
**Roll No.:** RK3P24RDA26  
**Registration ID:** 12408224  
**Section:** K3P24RD  
**Project type:** Individual  
**Official project title:** Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF  
**Mapped project:** SIH  |  **Mapped ID:** SIH26165  
**Course:** INT396 – Unsupervised Learning  
**Course outcomes:** CO2, CO4, CO5  
**Mapped units:** Unit V & IV – Anomaly Detection (Isolation Forest / LOF) and PCA Visualisation

## Objective 1 – Data preparation and feature construction

**Required:** Prepare a sample of open industrial safety-incident report text, identify relevant features, handle missing values, encode categorical variables and scale numerical variables where required.

**Implemented evidence:**
- Source: OSHA Severe Injury Reports, 105,996 records and 28 columns in the supplied extract; deterministic 5,000-record modelling sample, random seed 42.
- Selected structured features: Primary NAICS, EventTitle, SourceTitle and Secondary Source Title.
- Narrative feature: Final Narrative, represented using TF-IDF unigrams and bigrams (maximum 2,500 terms).
- Missing categorical values are normalised to `Unknown`; blank text is treated as empty text; invalid/missing dates are parsed safely and date-derived numeric values use documented fallback values.
- Categorical fields use OneHotEncoder. The combined sparse representation is reduced with TruncatedSVD to 24 numeric components and those components are transformed with StandardScaler.
- Identifiers, employer and address fields, coordinates, inspection IDs and outcome fields (`Hospitalized`, `Amputation`, `Loss of Eye`) are excluded from model features.

**Evidence files:** `src/safety_anomaly/data/clean.py`, `src/safety_anomaly/features/build.py`, `notebooks/01_dataset_audit.ipynb`, `notebooks/03_preprocessing_and_features.ipynb`, `reports/data_audit/audit_summary.json`.

## Objective 2 – Isolation Forest and LOF parameter comparison, with PCA

**Required:** Apply Isolation Forest and Local Outlier Factor to prepared features, compare flags across multiple parameter settings, and use PCA visualisation plus available labels or manual review to examine detection consistency.

**Implemented evidence:**
- Both detectors are run on the same 5,000-record, 24-dimensional structured-text sample.
- Isolation Forest configurations: 100 trees at 1% contamination; 100 trees at 3%; 200 trees at 3%.
- LOF configurations: 15 neighbours at 1%; 15 neighbours at 3%; 25 neighbours at 3%; Euclidean distance throughout.
- Every one of the 15 pairwise configuration comparisons is saved using Jaccard anomaly-set overlap, adjusted Rand index and Spearman score correlation.
- PCA projections are generated for the selected IF and LOF configurations. The first three components explain approximately 15.71% of variance in total; the two-dimensional plots are exploratory projections, not proof of separation or correctness.

**Available-label analysis:** OSHA outcome fields are used only after model fitting for a descriptive association check. They are never included in the feature matrix. Presence indicators are derived from values greater than zero. These are injury-outcome descriptors, not ground-truth anomaly labels. They support an available-label-style post-hoc comparison but cannot establish whether an anomaly flag is correct; no precision, recall or accuracy is calculated. No expert adjudication was conducted for this submission.

**Evidence files:** `src/safety_anomaly/models/detectors.py`, `src/safety_anomaly/models/experiments.py`, `src/safety_anomaly/evaluation/metrics.py`, `artifacts/public/experiment_summary.csv`, `artifacts/public/parameter_agreement.csv`, `artifacts/public/outcome_proxy_comparison.csv`, `artifacts/public/pca_iforest.png`, `artifacts/public/pca_lof.png`, `notebooks/04_anomaly_detection_models.ipynb`, `notebooks/05_pca_and_evaluation.ipynb`.

## Objective 3 – Consistency, false-positive implications, limitations, bias and ethics

**Required:** Evaluate consistency across methods and parameter settings using available labels or manual review, examine false-positive implications, and document limitations, possible bias and responsible interpretation.

**Implemented evidence:**
- Parameter consistency is quantified across all 15 pairs of the six configurations. The selected IF and LOF 3% configurations share 19 of 150 flags each (Jaccard 0.0676; ARI 0.0941; Spearman score correlation 0.1387).
- Within-method parameter stability and cross-method agreement are reported separately. Mean pairwise Jaccard is 0.4294 for IF-versus-IF, 0.4265 for LOF-versus-LOF, and 0.0591 for IF-versus-LOF comparisons.
- Held-out outcome proxy analysis demonstrates how flag rates vary across report outcome fields. The fields are too sparse or context-dependent to serve as verified anomaly labels. The loss-of-eye subset contains only one case in the 5,000-record sample and cannot support a meaningful comparison.
- No true false-positive rate can be estimated because the dataset contains reported severe-injury cases and no independently adjudicated normal/anomalous labels. No manual expert review labels were created or represented as completed. The contamination value is a model threshold, not the true anomaly prevalence.
- False-positive implications include unusual wording, rare source/category combinations, incomplete descriptions and changing reporting practices triggering flags even when no unusual hazard is present. A qualified reviewer must check the evidence.
- Documented limits include federal-jurisdiction coverage, severe-injury selection, reporting bias, sector imbalance, narrative quality, feature representation, low IF/LOF agreement, modest cluster separation and no prospective validation.
- The interface excludes direct identifiers from model inputs, warns against entering personal data and explicitly states that it is not an accident predictor or compliance tool.

**Evidence files:** `docs/MODEL_CARD.md`, `docs/VALIDATION_REPORT.md`, `docs/RESEARCH_CONTEXT.md`, `docs/USER_GUIDE.md`, `app/pages/ethics.py`, `artifacts/public/parameter_agreement.csv`, `artifacts/public/outcome_proxy_comparison.csv`.

## Course outcome mapping

| Course outcome | Implementation alignment |
|---|---|
| CO2 | Data audit, missing-value handling, categorical encoding, TF-IDF representation, dimensionality reduction, scaling, Isolation Forest and LOF. |
| CO4 | PCA projections, comparison of anomaly patterns and exploratory K-Means recurring-pattern grouping. |
| CO5 | Parameter sensitivity, IF/LOF consistency, held-out outcome proxy analysis, false-positive implications, bias, limitations and responsible human interpretation. |

## Project outcome

A reproducible unsupervised anomaly-pattern study with documented preprocessing, Isolation Forest and LOF comparisons over multiple settings, PCA visualisation, post-hoc outcome-proxy checks, and explicit discussion of model consistency, possible false-positive behaviour, source bias and ethical limits. The available evidence does not justify claims of validated anomaly accuracy, accident prediction or causal discovery.
