# Methodology

## 1. Design overview
A domain-generalization evaluation with CUAD as the source domain and a temporally later SEC-filed contract sample as the target domain. The target test set must be separated from model development and locked before tuning.

## 2. Dataset and license verification
Before data collection:
1. Read the current CUAD paper, dataset card, schema, and license.
2. Confirm exact target labels, annotation conventions, and available positive/negative support.
3. Record dataset version, source URL, retrieval date, license, and checksums where appropriate.
4. Review SEC EDGAR access guidance and the provenance of each selected exhibit.
5. Define the target date window, filing types, and reproducible exhibit-selection rules.
6. Document whether full text may be stored, transformed, or redistributed.

Do not assume that a dataset's license permits every form of redistribution or that the source and target annotation definitions are equivalent.

## 3. Sampling frame
Create a complete sampling frame of eligible SEC-filed material contracts before selecting the evaluation sample. Specify filing/exhibit types, date window, inclusion/exclusion criteria, duplicate handling, amendment handling, and broad industry coding. Do not select documents based on whether the target clause is easy to locate.

A target of roughly 40 contracts is only an initial feasibility estimate. Conduct a pilot and revise based on prevalence, annotation cost, and precision of the intended comparisons. Keep a private provenance manifest; use stable project IDs in analysis outputs.

## 4. Annotation protocol
Define whether the unit is a clause span, passage, or document-category pair. Specify how multi-paragraph provisions, exceptions, headings, and cross-references are handled. Record stable passage IDs and offsets against a versioned text-normalization procedure.

Use a second annotator for a subset if feasible. Report raw agreement and an agreement statistic appropriate to the label design. Cohen's kappa should be used only when its assumptions are suitable; document prevalence effects and adjudication. Retain original and adjudicated labels separately.

## 5. Data splitting and leakage prevention
Split by whole contract, not random paragraph. Related amendments, duplicate versions, and repeated passages must be grouped. No contract may cross train, validation, or test splits. Target-domain test contracts and labels must not influence hyperparameter tuning, feature selection, prompt design, or threshold selection.

## 6. Model families
- **Lexical baseline:** Transparent keyword and regular-expression rules with documented category dictionaries.
- **Classical baseline:** TF-IDF features with logistic regression or another pre-specified classifier.
- **Transformer:** A compact pretrained encoder fine-tuned only on source-domain training data.
- **Optional LLM comparator:** A fixed zero-shot/few-shot protocol with recorded model version, prompt, and decoding settings. Include only if cost, privacy, access, and reproducibility constraints are acceptable.

Use the same eligible text and task definition across model families. Record package versions, random seeds, model revisions, tokenization, truncation, hyperparameters, and compute environment.

## 7. Metrics
For each category, report precision, recall, F1, support, and confusion counts. If span extraction is evaluated, define exact-match and/or overlap criteria in advance and report span metrics separately from passage classification. Include class prevalence and number of distinct contracts represented.

Report absolute percentage-point changes between domains and uncertainty intervals. Bootstrap at the contract level to respect within-contract dependence. Avoid accuracy as the sole metric for imbalanced labels. Report calibration only if probability outputs and the calibration method are documented.

## 8. Error analysis
Use a pre-defined taxonomy: missed clause, false positive, incorrect category, overly broad span, incomplete span, heading-only match, cross-reference dependency, and extraction/formatting failure. Code drafting characteristics independently from model predictions where possible. Treat industry and year subgroup analysis as exploratory when sample sizes are small.

## 9. Robustness extensions
Cross-industry evaluation and controlled wording-variation tests may be considered after the primary design is stable. Synthetic perturbations must be reported separately from naturally occurring contracts and must not replace the main target-domain test.

## 10. Reproducibility
Maintain source manifests, dataset version notes, annotation versions, split assignments, experiment logs, environment files, seeds, and scripts for all reported tables and figures. Do not commit raw contracts, credentials, personal data, or local machine paths.

## 11. Limitations
SEC-filed exhibits are not representative of every contract population. Differences between CUAD and the target sample may reflect source, industry, contract type, or selection as well as time. Annotation ambiguity, modest sample sizes, model-version changes, and text extraction errors may affect conclusions. Observational associations do not establish causality.
