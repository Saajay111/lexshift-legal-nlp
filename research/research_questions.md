# Research Questions and Operational Definitions

## Primary question

**RQ1.** How does clause-detection performance change between held-out CUAD contracts and a newer SEC-filed contract sample?

## Secondary questions

- **RQ2.** Does the source-to-target performance difference vary by clause category?
- **RQ3.** Are error rates associated with contract year or broad industry group?
- **RQ4.** Which pre-defined drafting features (heading presence, clause length, cross-references, lexical variation, or provision dispersion) are associated with errors?
- **RQ5.** How do lexical rules, classical machine learning, and transformer-based systems compare under the same split and metric definitions?

## Operational definitions

- **Source domain:** CUAD examples used for model development and held-out source-domain evaluation.
- **Target domain:** A separately sampled set of newer SEC-filed material contracts.
- **Distribution shift:** A measured difference between source and target data distributions. It is not automatically evidence of a temporal causal effect.
- **Clause detection:** The task of determining whether a target clause category is present and identifying the relevant passage according to the annotation protocol.
- **Contract-level split:** All passages and related versions belonging to one agreement are assigned to a single data split.
- **Drafting feature:** An observable textual or structural characteristic coded using a pre-defined rule.

## Analysis discipline

Distinguish document-level classification, passage retrieval, and exact span extraction. Do not combine their scores into a single headline metric. Report the unit of analysis and support count for every result.
