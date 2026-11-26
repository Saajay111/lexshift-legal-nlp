# Methodology

## 1. Design overview
A cross-temporal domain-generalization evaluation using CUAD as the source benchmark and a separately sampled, later SEC-filed contract collection as the target set. The target set must be locked before model tuning. Because CUAD and the target sample may differ in contract type, issuer, and collection process, describe the study as a cross-temporal/domain-shift evaluation rather than a causal test of time alone.

## 2. Dataset verification
CUAD v1 is described by The Atticus Project as 510 commercial contracts, more than 13,000 expert annotations, and 41 clause categories. The Hugging Face dataset card identifies the dataset license as CC BY 4.0. Record the exact release/version and consult the original paper, dataset card, category list, and repository before use.

Verify the exact label names and annotation structure. The selected categories are Governing Law, Non-Compete, Anti-Assignment, Termination for Convenience, and Cap on Liability. CUAD separately includes Uncapped Liability; do not merge it with Cap on Liability. Confirm support counts and annotation semantics directly from the selected CUAD release. CUAD's 41 labels do not all have the same answer format: Governing Law is an extracted jurisdiction value, while several selected categories use Yes/No answers. For the primary detector task, define presence consistently from the existence of a valid annotated evidence context, and evaluate passage retrieval separately. Do not treat a jurisdiction string as if it were a Yes/No source label. Any normalized jurisdiction extraction should be a separately specified secondary task.

Use contract-level source data as the unit for splitting. Do not assume that row-level or paragraph-level splits in a convenient data export are safe for this research question.

## 3. Target sampling frame
Build a reproducible sampling frame from SEC EDGAR material-contract exhibits (typically Exhibit 10-series, with eligibility rules documented). Define:
- filing-date window and rationale;
- eligible filing forms and exhibit types;
- contract-type inclusion/exclusion criteria;
- how amendments, restatements, duplicate filings, and multiple exhibits are handled;
- how issuer industry is assigned;
- how CUAD contracts and close duplicates are screened out.

Use the SEC filing date as the temporal index unless a different date is justified. A contract's execution/effective date is not interchangeable with the filing date. Record both when available.

Start with a 15–20 contract pilot. The earlier 40-contract target is provisional and must not be treated as statistically powered. Determine the final sample after reviewing clause prevalence, extraction quality, annotation time, and the desired precision of primary estimates. Sample without looking at model predictions or selecting documents because a target clause is easy to find.

SEC fair-access guidance currently states a maximum of 10 requests per second and asks automated users to declare a descriptive User-Agent and make efficient requests. Use a much lower request rate, retrieve only necessary filings, and comply with current SEC guidance.

## 4. Annotation protocol
Use a document-category presence label plus evidence passage(s). For positive labels, store one row per evidence passage; for negative labels, store one row with no passage ID or offsets. Define how multi-paragraph provisions, exceptions, headings, and cross-references are handled. Store offsets against a versioned normalized text. Preserve the original extracted text separately from normalized model input.

Use a second annotator on a subset if feasible. Report raw agreement and an agreement statistic appropriate to the label design. Cohen's kappa is not automatically appropriate for every multi-label/span setup; explain the selected statistic and prevalence limitations. Retain original and adjudicated labels separately.

## 5. Leakage prevention
Split by whole contract, never by random paragraph. Group amendments, duplicate versions, and repeated agreements. No contract may cross train, validation, source test, or target test. The target test labels must not influence feature selection, prompt design, threshold selection, or hyperparameter tuning.

## 6. Model families
- **Lexical baseline:** Transparent category-specific keyword/regular-expression rules.
- **Classical baseline:** TF-IDF with logistic regression, trained on source-domain examples.
- **Transformer:** A compact pretrained encoder fine-tuned on source-domain data only.
- **Optional LLM comparator:** A fixed, versioned inference protocol; include only if reproducibility, cost, and data-handling requirements are met.

Use identical task definitions and eligible text across model families. Record model/tokenizer revisions, random seeds, preprocessing, truncation, hyperparameters, and compute environment.

## 7. Evaluation
For document-category presence, report per-category precision, recall, F1, support, and confusion counts. For passage retrieval or span extraction, define exact-match and/or overlap criteria in advance and report separate metrics. Include positive/negative prevalence and distinct-contract support.

Report absolute percentage-point changes between source and target. Use contract-level bootstrap intervals where feasible to respect within-contract dependence. Do not rely on accuracy alone for imbalanced categories. Calibration metrics require probability outputs and a documented calibration procedure.

## 8. Error analysis
Use a pre-defined taxonomy: missed clause, false positive, wrong category, overly broad passage, incomplete passage, heading-only match, cross-reference dependency, and extraction/formatting failure. Code drafting features independently from model outputs where possible. Treat industry/year subgroup analysis as exploratory unless sample size supports stronger inference.

## 9. Robustness and sensitivity
Potential extensions include cross-industry analysis, alternate category definitions, and controlled wording-variation tests. Synthetic perturbations must be clearly separated from naturally occurring SEC contracts. Conduct sensitivity analyses for document extraction failures and ambiguous annotations.

## 10. Reproducibility
Maintain dataset version notes, source manifests, annotation versions, split assignments, experiment logs, package versions, seeds, and scripts for every reported table/figure. Keep raw contract files and private source mappings out of the public repository unless redistribution permission is verified.

## 11. Limitations
SEC-filed exhibits are not representative of all contracts. CUAD and a later SEC sample may differ by contract type, issuer, industry, and selection process as well as filing date. Annotation ambiguity, small samples, extraction artifacts, and model-version changes can affect conclusions. Observational subgroup associations do not establish causality.
