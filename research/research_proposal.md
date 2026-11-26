# Research Proposal

## Working title
**Does a CUAD-trained clause detector survive newer contracts? A distribution-shift test for contract review.**

## Abstract
This project proposes an empirical evaluation of legal contract clause-extraction systems under temporal and domain shift. Systems developed using CUAD will be evaluated on held-out source-domain contracts and a separately sampled set of more recent SEC-filed material contracts. The study will compare transparent lexical rules, a classical text classifier, and a compact transformer, then investigate whether errors vary by clause category or observable document characteristics. The abstract will be rewritten after the study is completed; it currently describes the planned design, not findings.

## Motivation
Legal documents are not static. Contract language, formatting, transaction practices, and industry conventions can change across time and document populations. A model's score on a benchmark therefore does not, by itself, establish reliable performance on later contracts. This study tests generalization empirically and documents the conditions under which results should be interpreted.

## Primary research question
How does clause-detection performance change between held-out CUAD contracts and a separately sampled set of newer SEC-filed material contracts?

## Secondary questions
1. Does the performance difference vary across clause categories?
2. Are errors associated with contract year or broad industry group?
3. Which observable drafting characteristics are associated with false positives and false negatives?
4. How do lexical, classical ML, and transformer approaches compare under the same evaluation protocol?

## Provisional categories
Governing law, termination, limitation of liability, non-compete, and anti-assignment. This list is not final. Verify the exact CUAD schema, label definitions, class support, and target-domain applicability before committing to the categories.

## Proposed contribution
A reproducible, contract-level evaluation protocol for studying temporal and industry generalization in legal clause extraction, accompanied by a carefully documented annotation sample and an analysis of model errors.

## Feasibility
A starting estimate of approximately 40 target contracts and several hundred annotated passages is a planning hypothesis, not a statistical justification. A pilot must establish extraction feasibility, category prevalence, annotation time, and whether the intended comparisons are supportable. Revise the sample plan before the main study.

## Deliverables
- Dataset and source-provenance documentation
- Versioned annotation schema and guidelines
- Reproducible preprocessing and model-evaluation code
- Metrics with support counts and uncertainty intervals
- Error-analysis tables and a research manuscript

## Integrity statement
No result, benchmark comparison, novelty claim, or practical legal-performance claim will be stated as established until supported by completed experiments and a documented literature review.
