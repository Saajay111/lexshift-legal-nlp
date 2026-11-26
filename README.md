# LEXSHIFT
### Legal Language & Distribution-Shift Research

<p align="center">
  <strong>Measuring whether legal clause-extraction systems generalize beyond the contracts they were trained on.</strong>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-1f4b6e?logo=python&logoColor=white">
  <img alt="Research status" src="https://img.shields.io/badge/status-protocol%20development-8b9aab">
  <img alt="Reproducibility" src="https://img.shields.io/badge/research-reproducible%20by%20design-426b62">
  <img alt="License" src="https://img.shields.io/badge/license-TBD-lightgrey">
</p>

---

## Research at a glance

**Central question.** How much does clause-detection performance change when systems developed using the Contract Understanding Atticus Dataset (CUAD) are evaluated on newer contracts filed with the U.S. Securities and Exchange Commission (SEC)? Are errors associated with time, industry, or observable drafting characteristics?

LEXSHIFT is an empirical study of **temporal and domain generalization in legal NLP**. It is designed around contract-level data separation, documented annotation, transparent baselines, uncertainty-aware evaluation, and careful error analysis.

> **Current stage:** Research protocol and repository engineering. No model has been trained, no evaluation has been run, and no empirical findings are claimed.

## Study design

| Component | Planned approach |
|---|---|
| Source domain | CUAD, subject to dataset-card, schema, and license verification |
| Target domain | A documented sample of more recent SEC-filed material contracts |
| Initial clause labels | Governing law, termination, limitation of liability, non-compete, anti-assignment |
| Baselines | Lexical rules; TF-IDF + classical classifier |
| Neural model | Compact pretrained transformer, subject to compute feasibility |
| Optional comparator | Fixed zero-shot/few-shot LLM protocol, if reproducible and appropriate |
| Primary analysis | Source-vs-target performance, category-level metrics, contract-level uncertainty |
| Diagnostic analysis | Error taxonomy and exploratory drafting/industry/time slices |

The clause list is provisional. Each category must be confirmed against the exact CUAD annotation schema and tested for consistent application to SEC documents before the main annotation phase.

## Research safeguards

- **Contract-level splits:** related passages and versions of the same agreement stay in one split.
- **Locked target evaluation:** target-domain test labels are not used for tuning or model selection.
- **Documented labels:** annotation definitions, offsets, adjudication, and agreement are versioned.
- **Meaningful metrics:** precision, recall, F1, support, confusion counts, and uncertainty are reported by category.
- **No inflated claims:** small subgroup samples are treated as exploratory; association is not described as causation.
- **Responsible data handling:** raw contracts, credentials, private manifests, and unnecessary personal data are not committed.

## Repository architecture

```text
lexshift-legal-nlp/
├── research/       Research questions, hypotheses, protocol, limitations
├── data/           Schemas and annotation guidance; no raw documents
├── src/lexshift/   Reusable Python package for validation and evaluation
├── tests/          Unit tests for core research utilities
├── configs/        Versioned experiment configuration
├── notebooks/      Exploratory and reporting notebooks (added as needed)
├── results/        Generated outputs; no fabricated or hand-entered findings
├── paper/          Manuscript, references, and figure source
├── docs/           Reproducibility, governance, and project operations
└── .github/        Automated quality checks
```

## Quick start

Requires Python 3.11 or newer.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

The package currently provides research-data validation utilities. Model training and data ingestion are intentionally not implemented until dataset versions, licenses, labels, and sampling rules have been verified.

## Project milestones

| Milestone | Exit criterion | Status |
|---|---|---|
| Repository foundation | Structure, documentation, tests, CI | In progress |
| Dataset verification | CUAD schema/license and SEC collection rules documented | Not started |
| Protocol freeze | Sampling, annotation, splits, metrics finalized | Not started |
| Pilot | Extraction and annotation pilot reviewed | Not started |
| Modeling | Source-domain baselines reproducibly evaluated | Not started |
| Target evaluation | Locked target set evaluated without leakage | Not started |
| Analysis and writing | Error analysis, limitations, manuscript | Not started |

See [the project roadmap](docs/project_roadmap.md) for detailed gates.

## Documentation

- [Research proposal](research/research_proposal.md)
- [Research questions](research/research_questions.md)
- [Methodology](research/methodology.md)
- [Provisional hypotheses](research/hypotheses.md)
- [Limitations and threats to validity](research/limitations.md)
- [Annotation guidelines](data/annotations/annotation_guidelines.md)
- [Data dictionary](docs/data_dictionary.md)
- [Reproducibility protocol](docs/reproducibility.md)
- [Research ethics and data governance](docs/data_governance.md)

## Scope and disclaimer

LEXSHIFT studies NLP system behavior. It is not legal advice, does not provide legal services, and is not designed to make decisions about actual contracts. Any future model output is an experimental prediction and must not be treated as a legal conclusion.

## Citation and licensing

The repository license and citation metadata will be finalized after authorship, third-party dataset terms, and intended reuse are reviewed. CUAD and SEC EDGAR materials have separate terms and provenance. Do not redistribute source documents or derived text until applicable terms have been checked.
