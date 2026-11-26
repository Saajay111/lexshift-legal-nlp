# Research Questions and Operational Definitions

## Primary question
**RQ1.** How does clause-detection performance on a locked sample of later SEC-filed material contracts compare with performance on held-out CUAD contracts?

## Secondary questions
- **RQ2.** Does the source-to-target performance difference vary by clause category?
- **RQ3.** Are false positives and false negatives associated with pre-defined drafting features (heading presence, clause length, cross-references, lexical variation, or provision dispersion)?
- **RQ4.** Are performance differences associated with filing year or broad issuer industry?
- **RQ5.** How do lexical rules, classical machine learning, and transformer systems compare under the same data split and metric definitions?

## CUAD-aligned categories
Use the dataset's exact category names:
1. Governing Law
2. Non-Compete
3. Anti-Assignment
4. Termination for Convenience
5. Cap on Liability

Do not treat generic termination as equivalent to Termination for Convenience. Do not merge Cap on Liability with Uncapped Liability. The pilot may remove a category if its prevalence or annotation reliability is inadequate; any change must be documented before final evaluation.

## Operational definitions
- **Source domain:** CUAD contracts used for model development and held-out source-domain evaluation.
- **Target domain:** A separately sampled set of SEC-filed material contracts with filing dates after a pre-specified cutoff.
- **Temporal evaluation:** Comparison across document populations separated by a declared filing-date boundary. This does not isolate time as the only cause of a difference.
- **Distribution shift:** A difference between source and target data distributions; it is not automatically a causal temporal effect.
- **Clause detection:** Identifying whether a category is present and retrieving its relevant passage under the annotation protocol.
- **Contract-level split:** All passages and related versions of one agreement remain in one split.

## Analysis discipline
Distinguish document-category presence classification from passage retrieval and exact span extraction. Report them separately. For every metric, state the unit of analysis, number of positive examples, number of negative examples, and number of unique contracts.
