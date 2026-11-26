# Literature Review — Scoping Draft

**Status:** Initial scoping review, not exhaustive. Last checked: 2026-11-26. Expand this review before making any priority or novelty claim.

## 1. CUAD: expert-annotated contract review

Hendrycks et al. introduced the Contract Understanding Atticus Dataset (CUAD), an expert-annotated corpus of 510 commercial contracts and more than 13,000 annotations across 41 clause categories. The original task emphasizes locating salient contract passages for human review. CUAD is a natural source-domain benchmark, but its annotation unit and answer conventions must be reproduced rather than replaced with a generic sentence-classification formulation.

**Implication for LEXSHIFT:** Preserve CUAD's category definitions and passage evidence. Document how document-level presence labels are derived from its annotations, and separately evaluate passage retrieval/span quality.

## 2. LEDGAR: SEC contracts and transfer already studied

Tuggener et al. introduced LEDGAR, a large multi-label corpus built from SEC-filed Exhibit 10 material contracts. The paper reports provisions from more than 60,000 contracts, crawled from 2016 through 2019. It also reports experiments transferring classifiers to contracts outside the corpus.

**Implication for LEXSHIFT:** The use of SEC-filed contracts, out-of-domain contract evaluation, and transfer learning are not novel by themselves. A possible narrower angle is a post-2020 target-period evaluation of models trained on CUAD's expert span annotations, using matched CUAD categories, contract-level splits, and a manually adjudicated target sample. This is only a candidate contribution pending a fuller search.

## 3. SEC EDGAR as a source

The SEC makes EDGAR filing information publicly accessible and documents its filing indexes, accession paths, and fair-access requirements. Automated collection should be conservative, declare a descriptive User-Agent, retrieve only necessary documents, and follow current SEC policies.

**Implication for LEXSHIFT:** Use a pre-defined, auditable sampling frame rather than opportunistic document selection. Record CIK, accession number, filing date, exhibit filename, form type, and source URL in a private provenance manifest. Keep public outputs limited to identifiers and derived information that can be shared appropriately.

## 4. Research gap to investigate

The scoping evidence establishes that expert-annotated clause extraction on CUAD has been studied; legal provision classification on SEC-filed contracts has been studied; and transfer to contracts outside a source corpus has been studied.

The literature review must investigate whether prior work has already:
1. Fine-tuned CUAD models and evaluated them on contracts filed after 2020.
2. Compared CUAD and LEDGAR under matched clause definitions.
3. Measured temporal performance change while controlling contract-level leakage and duplicate agreements.
4. Conducted error analysis by drafting features on recent SEC material contracts.
5. Used the exact proposed five categories and a manually adjudicated target sample.

Do not claim a research gap until these questions have been checked against papers, theses, preprints, and benchmark documentation.

## 5. Candidate positioning

If the search supports it, position LEXSHIFT as a reproducible, expert-label-aligned temporal generalization audit, not as the first legal contract transfer study and not as a new general-purpose legal benchmark.

The target filing window should be selected after inspecting CUAD's date distribution and checking overlap with existing corpora. A provisional post-2020 window (2021–2025) is worth evaluating, but it is not yet frozen.

## References

1. Hendrycks, D., Burns, C., Chen, A., & Ball, S. (2021). CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review. NeurIPS 2021 Datasets and Benchmarks. https://arxiv.org/abs/2103.06268
2. Tuggener, D., von Däniken, P., Peetz, T., & Cieliebak, M. (2020). LEDGAR: A Large-Scale Multi-label Corpus for Text Classification of Legal Provisions in Contracts. Proceedings of LREC 2020, 1235–1241. https://aclanthology.org/2020.lrec-1.155/
3. The Atticus Project. Contract Understanding Atticus Dataset (CUAD). https://www.atticusprojectai.org/cuad/
4. Hugging Face Datasets. theatticusproject/cuad — dataset card and category schema. https://huggingface.co/datasets/theatticusproject/cuad
5. U.S. Securities and Exchange Commission. Accessing EDGAR Data. https://www.sec.gov/search-filings/edgar-search-assistance/accessing-edgar-data
6. U.S. Securities and Exchange Commission. Developer Resources. https://www.sec.gov/about/developer-resources

## Review log

| Date | Action | Outcome |
|---|---|---|
| 2026-11-26 | Reviewed CUAD project page, dataset card, and original paper metadata | Confirmed 510 contracts, 41 categories, 13,000+ annotations; CC BY 4.0 stated by current project/dataset pages |
| 2026-11-26 | Reviewed LEDGAR paper | Identified SEC Exhibit 10 corpus (2016–2019) and external-corpus transfer experiments; novelty must be narrower |
| 2026-11-26 | Reviewed SEC EDGAR access guidance | Documented fair-access requirements and filing-index metadata |
