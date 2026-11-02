import streamlit as st

st.title("Methodology")
st.subheader("1. Data preparation")
st.markdown("Dates are parsed into calendar-derived features. Categorical fields are normalized and one-hot encoded. Incident narratives can be represented using TF-IDF. A compact TruncatedSVD representation is used to control dimensionality before model comparison.")
st.subheader("2. Isolation Forest")
st.write("Isolation Forest isolates observations through randomized feature partitions. The project records anomaly labels, continuous anomaly scores, parameter settings and runtime.")
st.subheader("3. Local Outlier Factor")
st.write("LOF compares local sample density with that of neighboring observations. Its computation is bounded to a reproducible sample; the sample size and neighborhood parameters must be reported.")
st.subheader("4. PCA")
st.write("PCA is used to visualize the reduced feature space in two dimensions. The visualization is descriptive and is not used as evidence that detections are correct.")
st.subheader("5. Evaluation")
st.write("Jaccard similarity, Adjusted Rand Index and Spearman score correlation measure agreement between unsupervised detectors. These are agreement/stability measures, not precision, recall or anomaly accuracy without verified labels.")
