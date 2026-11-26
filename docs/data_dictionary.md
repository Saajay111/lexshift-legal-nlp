# Data Dictionary

## Data-handling principles
Use stable project IDs rather than personal names. Keep raw contract text and downloaded source files outside the public repository unless redistribution rights are explicitly verified. Separate private source manifests from public analysis tables.

## Annotation table

| Field | Type | Description |
|---|---|---|
| contract_id | string | Stable project identifier for one agreement |
| source_domain | string | Dataset/domain identifier, e.g. CUAD or SEC |
| source_reference | string | Public reference or private manifest key |
| document_date | date/string | Relevant date; date semantics must be documented |
| industry | string | Broad industry code and coding source |
| clause_category | string | One pre-specified category |
| presence | boolean | Clause presence under the annotation protocol |
| passage_id | string | Stable passage identifier |
| start_char / end_char | integer | Character offsets in versioned normalized text |
| annotator_id | string | Pseudonymous annotator code |
| confidence | string | Defined confidence level |
| needs_review | boolean | Whether review/adjudication is needed |
| adjudication_status | string | Pending, adjudicated, or not applicable |
| annotation_version | string | Version of the annotation codebook |
| notes | string | Brief rationale; avoid unnecessary personal data |

## Prediction table (planned)

| Field | Description |
|---|---|
| contract_id | Stable agreement ID |
| model_id | Model and revision identifier |
| clause_category | Target category |
| predicted_presence | Predicted label |
| predicted_score | Model score, if available |
| predicted_span | Predicted span reference, if applicable |
| split | Train, validation, source test, or target test |
| run_id | Unique experiment identifier |

Every export should record dataset, preprocessing, annotation, and split versions. Never overwrite original annotations; create a new version.
