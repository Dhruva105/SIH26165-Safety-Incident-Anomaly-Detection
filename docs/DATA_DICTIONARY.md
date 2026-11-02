# Data Dictionary

The source CSV schema observed during initial inspection is listed below. Confirm meanings against current OSHA documentation before publication.

| Field | Observed role | Modeling policy |
|---|---|---|
| ID | Source identifier with repeated values | Exclude |
| UPA | Unique source record identifier in this file | Internal key only |
| EventDate | Incident date | Derive calendar features |
| Employer | Employer name | Exclude from modeling and public exports |
| Address1, Address2, City, State, Zip | Location fields | Exclude from model; public display restricted |
| Latitude, Longitude | Exact coordinates | Exclude |
| Primary NAICS | Industry classification | Categorical feature |
| Hospitalized, Amputation, Loss of Eye | Injury outcome/severity indicators | Exclude from primary model; separate descriptive analysis only |
| Inspection | Inspection identifier | Exclude |
| Final Narrative | Incident narrative | Optional TF-IDF text feature; do not publish raw text by default |
| Nature, NatureTitle | Injury nature | Supplementary analysis; excluded from default feature set |
| Part of Body, Part of Body Title | Body-part classification | Supplementary analysis; excluded from default feature set |
| Event, EventTitle | Event classification | Categorical feature |
| Source, SourceTitle | Source/equipment classification | Categorical feature |
| Secondary Source, Secondary Source Title | Secondary source classification | Categorical feature; missingness retained as Unknown |
| FederalState | Jurisdiction field | Excluded by default pending bias/scope rationale |
