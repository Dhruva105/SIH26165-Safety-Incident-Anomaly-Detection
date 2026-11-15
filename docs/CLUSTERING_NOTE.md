# Recurring-pattern grouping: build note

## Purpose

The SIH project title refers to cluster-based analysis. The initial application had anomaly screening and nearest-neighbour retrieval but did not assign incidents to recurring pattern groups. Version 1.1.0 adds K-Means grouping to the same structured-text feature representation used by the operational review workflow.

## Representation and setup

- Sample: 5,000 records from the supplied OSHA Severe Injury Reports extract.
- Sampling: pandas sample with `random_state=42` after valid event-date/title filtering.
- Categorical features: Primary NAICS, EventTitle, SourceTitle and Secondary Source Title.
- Date features: scaled year and cyclic month/weekday features.
- Narrative features: TF-IDF unigrams/bigrams, `max_features=2500`, `min_df=3`.
- Dimensionality reduction: TruncatedSVD to 24 dimensions followed by standard scaling.
- K-Means evaluation: k = 4, 6, 8 and 10; `n_init=10`, `max_iter=300`; random seeds 13, 42 and 77 for stability comparison.

## Evaluation on the supplied sample

| k | Silhouette (2,000-row sample) | Davies-Bouldin | Calinski-Harabasz | Mean pairwise ARI across seeds |
|---:|---:|---:|---:|---:|
| 4 | 0.0679 | 2.8638 | 243.77 | 0.6777 |
| 6 | 0.1062 | 2.4009 | 253.01 | 0.5861 |
| 8 | 0.1367 | 2.2188 | 277.90 | 0.5291 |
| 10 | 0.1547 | 2.1740 | 282.13 | 0.5027 |

k=8 is used in the operational prototype as an exploratory compromise between finer separation and across-seed stability. This is not a universal optimum. The stability scores show that assignments change with initialization, so cluster boundaries should be treated cautiously. The silhouette values also indicate modest separation, not sharply distinct natural classes.

## k=8 profile observations

The most frequent categories in the fixed-seed sample include:

- A group dominated by falls from below six feet.
- A group associated with maintenance/cleaning around running equipment.
- A group associated with machinery during regular operation.
- A group dominated by environmental heat exposure.
- Groups with dominant fall, struck-against, or compressed/pinched patterns.

These are sample-level category summaries, not inferred causes, risk severity levels or prevention recommendations. Profile counts and dominant categories are available in `artifacts/public/cluster_profiles.csv`.

## Interpretation limits

The clusters are built from a sample of reported severe injuries, and the source omits State Plan jurisdiction reports. They do not represent all workplace events or near misses. The dataset has no verified cluster labels or anomaly ground truth. Internal clustering scores and seed stability do not measure prevention effectiveness or hazard prediction.

## Reproduction

With the source CSV placed at `data/raw/January2015toNovember2025.csv`, run:

```bash
python scripts/evaluate_clusters.py --sample-size 5000
python scripts/build_review_model.py --sample-size 5000
```

Generated public summary files contain only aggregate categories and metrics, not employer names, addresses, identifiers or raw narratives.
