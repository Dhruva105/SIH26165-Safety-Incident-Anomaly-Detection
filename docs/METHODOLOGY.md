# Methodology

## Data
The supplied CSV contains 105,996 rows and 28 columns. The inspected `UPA` column has 105,996 unique non-null values. Five distinct `ID` values are repeated, affecting ten rows; there are no exact duplicate rows. Event dates parse from 2015-01-01 through 2025-11-30 with no invalid dates in the inspected file. Re-run the audit after replacing/updating the source file.

## Features
The default representation encodes Primary NAICS, EventTitle, SourceTitle and Secondary Source Title. Date fields are converted to year trend and cyclic month/weekday variables. The extended text representation uses TF-IDF on Final Narrative followed by TruncatedSVD and scaling. A supplementary representation can include NatureTitle and Part of Body Title. Identifiers, employer and direct location fields, inspection IDs and injury outcomes are excluded from primary features.

## Models

The research pipeline compares Isolation Forest and Local Outlier Factor on a deterministic sample. Both output binary flags and continuous scores oriented so larger scores indicate more anomalous observations. LOF is limited by a configured maximum sample size because neighborhood search can be expensive.

The operational workflow additionally applies K-Means (k=8) to the same 24-dimensional structured-text feature space. Cluster profiles are summarised using the most frequent event, source, injury-nature and body-part categories. They are descriptive pattern groups, not severity classes, causal explanations or hazard labels. Isolation Forest provides the unusual-pattern screen; nearest-neighbour retrieval supplies record-level historical context. The cluster assignment supplies broader recurring-pattern context.

## Evaluation

Jaccard similarity, Adjusted Rand Index and Spearman correlation quantify Isolation Forest/LOF agreement. They are not accuracy metrics. K-Means configurations k=4, 6, 8 and 10 were compared using silhouette, Davies-Bouldin and Calinski-Harabasz indices; assignment stability was estimated by pairwise Adjusted Rand Index across random seeds 13, 42 and 77. These are internal, unlabeled diagnostics, not validation against true hazard outcomes. A blinded worksheet is created for human review; no labels are invented.

## Visualization
PCA is computed on the compact feature representation for descriptive visualization. Two-dimensional projections do not establish model correctness.

## Limitations
The source includes reported severe injuries and is affected by reporting, jurisdictional, industry and selection biases. The dataset does not establish near-miss rates or the prevalence of all unsafe acts. Anomalies should be treated as review candidates only.
