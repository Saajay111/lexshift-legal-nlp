# CUAD Full-Text Retrieval and Evidence Alignment

**Status:** Alignment utility implemented; full-text archive retrieval and alignment must be run and audited before training.

## Official source

Use the official CUAD v1 archive on Zenodo: https://zenodo.org/records/4595826. The archive is approximately 105.9 MB and includes the full contract TXT and PDF collections alongside annotation materials. The official dataset documentation describes 510 TXT files corresponding to the contracts in the master CSV.

Do not commit the downloaded archive or extracted contract text to this public repository. Keep source data in a private Colab runtime or private storage. The CUAD release identifies CC BY 4.0; retain attribution and review the source datasheet and limitations.

## Alignment policy

The utility maps the PDF-style `source_reference` filename to a same-stem TXT file, then searches for each positive evidence passage after collapsing whitespace. It emits character offsets only when exactly one match exists.

Statuses:
- `unique_whitespace_normalized_match`: one unambiguous match; offsets refer to original TXT characters.
- `ambiguous_multiple_matches`: passage occurs more than once; manual review required.
- `not_found`: no conservative match; manual review required.
- `not_applicable_contract_level_negative`: CUAD records absence for the contract/category; this is not a negative passage.

The utility never case-folds, paraphrases, or guesses spans. It records file hashes and character counts, not full contract text. A TXT file may have conversion artifacts; alignment success is not proof that the underlying PDF formatting is faithfully represented.

## Run

After extracting the official archive, locate the `full_contract_txt` directory (folder capitalization may vary), then run:

```bash
pip install -e ".[dev]"
lexshift-align-cuad data/interim/cuad_annotations.csv /path/to/full_contract_txt data/processed/cuad_alignment
```

Inspect `cuad_alignment_report.json`, `cuad_fulltext_manifest.csv`, and `cuad_passage_alignment.csv`. Review all non-unique and unmatched positive passages before using offsets. Do not create negative passage examples merely by assigning the contract-level negative label to arbitrary text.
