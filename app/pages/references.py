import streamlit as st

st.markdown('<div class="eyebrow">GOVERNANCE / SOURCES</div>', unsafe_allow_html=True)
st.title("References and source material")
st.markdown("### Dataset")
st.markdown("- U.S. Occupational Safety and Health Administration (OSHA). **Severe Injury Reports**. https://www.osha.gov/severeinjury")
st.markdown("### Related occupational-safety text analytics")
st.markdown("""- Smetana, M., de Salles, L. S., Sukharev, I., & Khazanovich, L. (2024). Highway Construction Safety Analysis Using Large Language Models. *Applied Sciences, 14*(4), 1352. [https://doi.org/10.3390/app14041352](https://doi.org/10.3390/app14041352)
- Ricketts, J., Barry, D., Guo, W., & Pelham, J. (2023). A Scoping Literature Review of Natural Language Processing Application to Safety Occurrence Reports. *Safety, 9*(2), 22. [https://doi.org/10.3390/safety9020022](https://doi.org/10.3390/safety9020022)
- Shayboun, M., Kifokeris, D., & Koch, C. (2025). A review of machine learning for analysing accident reports in the construction industry. *Journal of Information Technology in Construction, 30*, 439–460. [https://doi.org/10.36680/j.itcon.2025.019](https://doi.org/10.36680/j.itcon.2025.019)
- Macêdo, J. B., Ramos, P. M. S., Maior, C. B. S., Moura, M. J. C., Lins, I. D., & Vilela, R. F. T. (2023). Identifying low-quality patterns in accident reports from textual data. *International Journal of Occupational Safety and Ergonomics, 29*(3), 1088–1100. [https://doi.org/10.1080/10803548.2022.2111847](https://doi.org/10.1080/10803548.2022.2111847)""")
st.markdown("### Method references")
st.markdown("""- Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. *2008 Eighth IEEE International Conference on Data Mining*. DOI: 10.1109/ICDM.2008.17.
- Breunig, M. M., Kriegel, H.-P., Ng, R. T., & Sander, J. (2000). LOF: Identifying Density-Based Local Outliers. *Proceedings of the 2000 ACM SIGMOD International Conference on Management of Data*. DOI: 10.1145/342009.335388.
- Jolliffe, I. T., & Cadima, J. (2016). Principal component analysis: a review and recent developments. *Philosophical Transactions of the Royal Society A, 374*(2065). DOI: 10.1098/rsta.2015.0202.
- scikit-learn documentation: https://scikit-learn.org/stable/\n- Streamlit documentation: https://docs.streamlit.io/""")
st.caption("The literature has already used NLP, text mining and clustering for safety occurrence reports. The project contribution is framed as an applied review workflow, not a claim of new algorithms. Check every bibliographic record against the publisher before preparing the IEEE manuscript.")
