# CUAD v1 Conversion Pipeline

**Status:** Implemented; validate against the downloaded source before treating the converted file as a frozen research artifact.

## Input and output

The converter reads the CUAD v1 master-clauses CSV and writes one row per annotated evidence passage for positive categories, or one negative contract-category row when no evidence passage is supplied.

Five categories are mapped without broadening their definitions:

| CUAD source label | LEXSHIFT category |
|---|---|
| Governing Law | `governing_law` |
| Non-Compete | `non_compete` |
| Anti-Assignment | `anti_assignment` |
| Termination For Convenience | `termination_for_convenience` |
| Cap On Liability | `cap_on_liability` |

## Important data handling

- Original evidence passages are preserved verbatim in `passage_text`.
- CUAD's jurisdiction-valued Governing Law answer is preserved verbatim in `source_answer`; presence is based on whether evidence passages are supplied. Missing jurisdiction answers do not erase available evidence.
- The four Yes/No categories are checked for consistency between the source answer and passage availability. A mismatch stops conversion rather than silently correcting the source.
- The original filename is retained as both `contract_id` and `source_reference`.
- CUAD does not provide document date or industry in this master CSV; these fields remain missing.
- Character offsets are not emitted by this import because the master CSV supplies evidence passages but not offsets aligned to a versioned full-text representation. Passage-level evidence and span-offset annotation are kept distinct.
- Multiple passages for one contract/category become separate rows with deterministic passage IDs.
- The converter never writes source contracts or raw source CSVs into the repository.

## Run

Install the project and dependencies, then run:

```bash
pip install -e ".[dev]"
lexshift-convert-cuad path/to/master_clauses.csv data/interim/cuad_annotations.csv
```

The command prints a JSON summary with contract, row, category, positive and negative counts.

## Validation

Run `pytest` and `ruff check .`. Review the generated counts and inspect a sample of converted rows before using the file in experiments. This is a format conversion, not a new legal review or independent verification of CUAD's expert annotations.
