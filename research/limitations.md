# Limitations and Threats to Validity

| Threat | Why it matters | Mitigation |
|---|---|---|
| Sampling bias | SEC-filed material contracts are not a random sample of all commercial agreements. | Publish inclusion criteria and characterize the sampling frame. |
| Temporal confounding | Source and target datasets may differ in industry, contract type, or collection process as well as date. | Describe covariates and avoid causal claims. |
| Annotation ambiguity | Legal provisions can combine concepts or rely on definitions elsewhere. | Pilot, version guidelines, adjudicate, and report agreement. |
| Category mismatch | CUAD labels may not map perfectly to the target annotation task. | Verify schema and define a crosswalk before labeling. |
| Small sample | Limited contracts reduce precision and make subgroup analysis unstable. | Report support and uncertainty; keep subgroup work exploratory. |
| Task mismatch | Presence classification, passage retrieval, and span extraction are different tasks. | Define each task and report separate metrics. |
| Model dependence | Versions, tokenization, prompts, and preprocessing can change results. | Record full experiment configuration and versions. |
| Extraction artifacts | PDF/HTML conversion can damage structure or omit text. | Validate extraction and retain quality-control flags. |
| External validity | Findings may apply only to sampled exhibit types and years. | Limit claims to the observed sample and setup. |

The study should report limitations that emerge during implementation, not only this initial list.
