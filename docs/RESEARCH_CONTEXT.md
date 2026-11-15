# Research Context and Project Positioning

Prepared: 15 November 2026  
Project: Safety-Incident Anomaly Pattern Detection Using Isolation Forest and LOF (SIH26165)

## Scope

The implementation uses the supplied OSHA Severe Injury Reports extract, covering reported severe injuries under federal OSHA jurisdiction from 1 January 2015 to 30 November 2025 in the supplied download. OSHA's source description covers amputations, inpatient hospitalisations and loss of an eye, and excludes reports under OSHA-approved State Plans. It is not a full census of workplace injuries, unsafe acts or near misses.

## What prior work already establishes

Prior work has already applied text mining and machine learning to occupational incident narratives. Examples include TF-IDF and supervised classifiers for accident narrative classification, topic modelling to explore incident themes, word embeddings for characterising narratives, text-mining with LOF for narrative accident anomaly detection (Song & Suh, 2019), and NLP / LLM-assisted clustering of OSHA Severe Injury Reports (Smetana et al., 2024). A scoping review of safety occurrence report NLP also describes classification, information extraction, semantic search and topic modelling, and notes the need to test usefulness in real operational settings.

This means K-Means, Isolation Forest, LOF, TF-IDF, TruncatedSVD and PCA must be described as established methods. The project does not claim algorithmic novelty.

## Applied contribution in this implementation

The practical contribution is an integrated, human-led review workflow for a new incident report:

1. Encode structured incident fields and a factual narrative in a shared representation.
2. Provide a descriptive K-Means pattern group and frequent category context.
3. Screen unusual representations against a fitted reference sample with Isolation Forest.
4. Retrieve five nearby historical reports for context.
5. Present rule-based review prompts, follow-up ownership and JSON export.

This is an application-level integration, not proof that the workflow is novel across the literature. A later paper must compare the integrated approach with relevant prior systems and clearly state what is incremental.

## Evaluation guidance for the subsequent paper

- Report the exact OSHA extract version, jurisdiction scope, date range, sampling procedure and random seeds.
- Compare Isolation Forest and LOF without treating either method as ground truth.
- Report anomaly-set overlap and score correlation as agreement measures only.
- Report internal clustering indices and sensitivity across seeds / cluster counts; discuss modest separation and unstable assignments.
- Use expert adjudication or a carefully designed blinded review to evaluate whether flags and retrieved cases are useful. Report inter-rater reliability if multiple reviewers participate.
- Evaluate usefulness of retrieved neighbours and checklist prompts separately from the anomaly score.
- Avoid claims about accident prediction, prevention effectiveness or calibrated risk unless supported by a separate prospective study and appropriate outcome labels.

## Selected related work

1. Ricketts, J., Barry, D. J., Guo, W., & Pelham, J. (2023). A Scoping Literature Review of Natural Language Processing Application to Safety Occurrence Reports. *Safety, 9*(2), 22. https://doi.org/10.3390/safety9020022
2. Song, B., & Suh, Y. (2019). Narrative texts-based anomaly detection using accident report documents: The case of chemical process safety. *Journal of Loss Prevention in the Process Industries, 57*, 47–54. https://doi.org/10.1016/j.jlp.2018.08.010
3. Smetana, M., de Salles, L. S., Sukharev, I., & Khazanovich, L. (2024). Highway Construction Safety Analysis Using Large Language Models. *Applied Sciences, 14*(4), 1352. https://doi.org/10.3390/app14041352
4. Shayboun, M., Kifokeris, D., & Koch, C. (2025). A review of machine learning for analysing accident reports in the construction industry. *Journal of Information Technology in Construction, 30*, 439–460. https://doi.org/10.36680/j.itcon.2025.019
5. Macêdo, J. B., Ramos, P. M. S., Maior, C. B. S., Moura, M. J. C., Lins, I. D., & Vilela, R. F. T. (2023). Identifying low-quality patterns in accident reports from textual data. *International Journal of Occupational Safety and Ergonomics, 29*(3), 1088–1100. https://doi.org/10.1080/10803548.2022.2111847
6. Goh, Y. M., & Ubeynarayana, C. U. (2017). Construction accident narrative classification: An evaluation of text mining techniques. *Accident Analysis & Prevention, 108*, 122–130. https://doi.org/10.1016/j.aap.2017.08.026
7. Passmore, D. L., Chae, C., Kustikova, Y. O., Baker, R. M., & Yim, J. (2018). An exploration of text mining of narrative reports of injury incidents to assess risk. *MATEC Web of Conferences, 251*, 06020. https://doi.org/10.1051/matecconf/201825106020
8. Suh, Y. (2021). Sectoral patterns of accident process for occupational safety using narrative texts of OSHA database. *Safety Science, 142*, 105363. https://doi.org/10.1016/j.ssci.2021.105363

This file documents project scope and research positioning. It is not the IEEE paper and should not be submitted as a substitute for the required research paper.
