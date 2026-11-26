# CUAD Full-Text Acquisition

**Status:** Reproducible downloader implemented; run locally or in Colab before alignment.

The pinned CUAD v1 release contains 510 canonical full-contract TXT files under `CUAD_v1/full_contract_txt`, organized into agreement-category subdirectories. This snapshot also contains a flat 200-file mirror at the `Part_I` and `Part_II` level. Those mirror files overlap with the category-organized collection and must not be counted as additional contracts. The downloader prefers the complete category-organized set when it contains exactly 510 files with unique basenames. The alignment stage separately indexes all TXT candidates, including mirrors, because same-basename copies can differ in extracted content.

- Dataset repository: https://huggingface.co/datasets/theatticusproject/cuad
- Pinned revision: `a3c393f5d103fd0c516374e4fdff676c8176dcb1`
- Dataset documentation: https://huggingface.co/datasets/theatticusproject/cuad/blob/main/CUAD_v1/CUAD%20v1%20ReadMe%20_%20Datasheet/CUAD_v1_README.txt

## Download

Install the optional data dependency and run:

```bash
pip install -e ".[data]"
lexshift-download-cuad-text data/raw/cuad_release
```

If the category-organized TXT collection is incomplete, the downloader can recover missing files from the PDF subtree using PyMuPDF. Completed recovered TXT files are preserved across interrupted Colab runs, so a retry does not repeat completed work. The downloader validates the final count and unique basenames, then writes a manifest with the pinned revision, selection strategy, discovered and selected TXT counts, number recovered from PDF, filename, byte size, and SHA-256 checksum. Raw contract text stays in the local destination and is never added to Git.

## Alignment

```bash
lexshift-align-cuad data/interim/cuad_annotations.csv data/raw/cuad_release/CUAD_v1/full_contract_txt data/interim/cuad_alignment
```

Review `cuad_alignment_report.json` and `cuad_fulltext_manifest.csv` before building training examples. For duplicate basenames, the aligner scores each candidate against the contract's positive annotated passages and selects a file only when it has a unique highest exact/casefolded-whitespace match count. Ties with positive evidence remain `ambiguous_full_text_filename`; no-match ties are not silently resolved. The manifest records candidate counts, relative selected path, per-candidate match scores, selection reason, and selected text checksum. Only unique passage matches within the selected file receive offsets. Missing or repeated matches remain flagged for review. Negative contract/category labels remain contract-level labels; this process does not fabricate negative passage annotations.

## Data governance

The dataset card identifies CUAD v1 as CC BY 4.0 and requests attribution. Preserve the original citation and dataset provenance. The dataset documentation notes that TXT conversion can introduce formatting differences. Do not publish raw contracts or derived contract text in this repository; check source-document reuse terms before redistribution.
