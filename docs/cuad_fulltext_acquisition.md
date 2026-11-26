# CUAD Full-Text Acquisition

**Status:** Reproducible downloader implemented; run locally or in Colab before alignment.

The official CUAD v1 release contains 510 full-contract TXT files in addition to the master-clauses CSV. The text files are grouped under `CUAD_v1/full_contract_txt` in the official Hugging Face dataset repository. LEXSHIFT pins the repository revision below so that upstream changes cannot silently alter the source snapshot.

- Dataset repository: https://huggingface.co/datasets/theatticusproject/cuad
- Pinned revision: `a3c393f5d103fd0c516374e4fdff676c8176dcb1`
- Dataset documentation: https://huggingface.co/datasets/theatticusproject/cuad/blob/main/CUAD_v1/CUAD%20v1%20ReadMe%20_%20Datasheet/CUAD_v1_README.txt

## Download

Install the optional data dependency and run:

```bash
pip install -e ".[data]"
lexshift-download-cuad-text data/raw/cuad_release
```

The pinned Hugging Face snapshot currently exposes only 200 of the 510 TXT files. The downloader therefore retrieves the official PDF subtree as well, extracts text only for contracts whose TXT counterpart is absent, and requires exactly 510 PDF sources and 510 resulting text files with unique basenames. PDF extraction uses PyMuPDF for faster page-level text extraction. Completed recovered TXT files are preserved across interrupted Colab runs, so a retry does not repeat completed work. The manifest records the original TXT count, number recovered from PDF, filename, byte size, and SHA-256 checksum. Raw contract text stays in the local destination and is never added to Git.

## Alignment

```bash
lexshift-align-cuad data/interim/cuad_annotations.csv data/raw/cuad_release/CUAD_v1/full_contract_txt data/interim/cuad_alignment
```

Review `cuad_alignment_report.json` before building training examples. Only unique whitespace-normalized matches receive offsets. Missing or repeated matches remain flagged for review. Negative contract/category labels remain contract-level labels; this process does not fabricate negative passage annotations.

## Data governance

The dataset card identifies CUAD v1 as CC BY 4.0 and requests attribution. Preserve the original citation and dataset provenance. The dataset documentation notes that TXT conversion can introduce formatting differences. Do not publish raw contracts or derived contract text in this repository; check source-document reuse terms before redistribution.