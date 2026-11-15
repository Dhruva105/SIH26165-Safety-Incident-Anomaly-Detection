import streamlit as st

st.markdown('<div class="eyebrow">PROJECT EVIDENCE / METHODS</div>', unsafe_allow_html=True)
st.title("How the review pipeline works")
st.markdown('<div class="page-deck">The project combines structured incident fields and narrative text, then uses separate unsupervised methods for pattern grouping and unusual-record screening.</div>', unsafe_allow_html=True)

st.markdown("### 1. Feature representation")
st.markdown(
    """The representation combines:

- One-hot encoded industry, event, source and secondary-source categories.
- Calendar features derived from the event date.
- TF-IDF unigrams and bigrams from the incident narrative.
- TruncatedSVD reduction to 24 dimensions, followed by standard scaling.

Employer names, addresses, UPA/ID fields, exact coordinates and injury outcome fields are excluded from the primary feature representation.
"""
)
st.markdown("### 2. K-Means recurring-pattern groups")
st.write("K-Means with k=8 assigns each record to a broad statistical group. The app describes a group using its most frequent event, source and injury categories. The group is not a validated hazard class or causal label.")
st.markdown("### 3. Isolation Forest unusual-pattern screen")
st.write("The deployed model uses 250 trees, random seed 42 and a 3% contamination setting. The score percentile compares a submitted record with scores from the fitted reference sample. The percentile is not an injury probability or validated risk score.")
st.markdown("### 4. Local Outlier Factor comparison")
st.write("LOF compares local sample density with neighbouring records in the research pipeline. Its sample size is bounded in configuration to control runtime and memory.")
st.markdown("### 5. Historical neighbours")
st.write("Nearest-neighbour retrieval returns five historical records in the same feature space. These are context references, not confirmed causal analogues.")
st.markdown("### 6. PCA and evaluation")
st.write("PCA plots support visual inspection of reduced feature space. Jaccard, Adjusted Rand and Spearman metrics describe agreement between detectors, not anomaly accuracy. Silhouette, Davies–Bouldin, Calinski–Harabasz and cross-seed ARI are used for unlabeled cluster diagnostics.")
