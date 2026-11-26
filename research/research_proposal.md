# Research Proposal

## Working title
**Does a CUAD-trained clause detector generalize to later SEC-filed contracts? A cross-temporal evaluation of legal clause extraction.**

## Abstract (proposal-stage)
This study will evaluate whether legal clause-extraction systems trained on the Contract Understanding Atticus Dataset (CUAD) generalize to a separately sampled set of later SEC-filed material contracts. It will compare transparent lexical rules, a classical text classifier, and a compact transformer on five CUAD-aligned clause categories. The study will examine category-level performance differences and characterize errors by pre-defined drafting features. This is a proposed design, not a report of completed experiments.

## Motivation
A benchmark score on one contract collection does not establish that a model will work equally well on later documents. Differences in drafting conventions, contract populations, document structure, and time may affect extraction performance. The project will measure these differences rather than assume that a performance drop exists.

## Primary research question
How does clause-detection performance on a locked sample of later SEC-filed material contracts compare with performance on held-out CUAD contracts?

## Secondary questions
1. Does the source-to-target difference vary by clause category?
2. Are false positives and false negatives associated with pre-defined drafting characteristics?
3. Are observed differences associated with filing year or broad issuer industry?
4. How do lexical, classical ML, and transformer systems compare under a consistent evaluation protocol?

## CUAD-aligned provisional categories
The initial category set is:
- Governing Law
- Non-Compete
- Anti-Assignment
- Termination for Convenience
- Cap on Liability

These names align with CUAD's published category list. Do not silently broaden them to generic "termination" or "limitation of liability." In particular, CUAD separately labels "Uncapped Liability"; it is not interchangeable with "Cap on Liability." Category inclusion remains conditional on a pilot confirming usable label support and reliable target-domain annotation.

## Proposed contribution and novelty boundary
The project will contribute a transparent cross-temporal evaluation protocol and a manually reviewed target-domain sample. Existing work already includes CUAD, LEDGAR, and transfer experiments on contract corpora. Therefore, the project will not claim to be the first study of legal contract transfer or the first evaluation of CUAD models. The narrower potential contribution is a carefully controlled, later-filing-period evaluation using CUAD-aligned categories, contract-level leakage controls, and documented error analysis. A formal novelty claim requires a completed literature review.

## Feasibility and sampling
An initial pilot of approximately 15–20 eligible target contracts is recommended before fixing the final sample size. A prior estimate of 40 contracts is a feasibility placeholder, not a statistically justified sample size. The final target sample should be set after measuring category prevalence, annotation time, extraction quality, and the precision achievable for primary estimates.

## Deliverables
- Dataset and source-provenance audit
- Versioned annotation protocol and schema
- Reproducible preprocessing and model evaluation code
- Per-category metrics with support counts and uncertainty intervals
- Error analysis and a research manuscript

## Integrity statement
No model result, novelty claim, or practical legal-performance claim will be presented as established until supported by completed experiments and documented sources.
