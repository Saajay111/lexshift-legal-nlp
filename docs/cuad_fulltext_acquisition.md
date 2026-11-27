# CUAD Full-Text Acquisition

**Status:** Downloader updated for the verified pinned Hugging Face repository structure; validate in Colab before alignment.

The pinned CUAD v1 revision contains 510 canonical contract PDFs with unique basenames, plus 200 flat TXT mirrors (100 in `Part_I` and 100 in `Part_II`). The verified inventory shows 196 mirror basenames match PDFs and 314 PDFs have no corresponding flat TXT copy. The downloader now uses the canonical PDF paths as the contract inventory, copies each matching TXT mirror into that PDF's category-relative path, and extracts text from the remaining PDFs.

- Dataset repository: https://huggingface.co/datasets/theatticusproject/cuad
- Pinned revision: `a3c393f5d103fd0c516374e4fdff676c8176dcb1`
- Dataset documentation: https://huggingface.co/datasets/theatticusproject/cuad/blob/main/CUAD%20v1%20ReadMe%20_%20Datasheet/CUAD_v1_README.txt

## Download

Install the optional data dependency and run:

```bash
pip install -e ".[data]"
lexshift-download-cuad-text data/raw/cuad_release
```

The downloader validates exactly 510 unique PDF basenames and expects the verified 196 TXT-to-PDF basename matches. Each TXT is written under the same relative category path as its canonical PDF. PDF extraction uses PyMuPDF without the additional layout-sorting pass that caused slow execution in the previous attempt. Nonempty extracted files are preserved across interrupted runs; matching official TXT mirrors are recopied from the pinned source to keep them authoritative.

A manifest is written only after all 510 category-mapped TXT files are present and nonempty. It records the pinned revision, counts copied from TXT and recovered from PDF, relative paths, byte sizes, and SHA-256 checksums. Raw contract text stays in the local destination and is never added to Git.

## Alignment

After successful acquisition, review the manifest and run:

```bash
lexshift-align-cuad data/interim/cuad_annotations.csv data/raw/cuad_release/CUAD_v1/full_contract_txt data/interim/cuad_alignment
```

Review `cuad_alignment_report.json` and `cuad_fulltext_manifest.csv` before building training examples. For duplicate basenames in candidate collections, the aligner first collapses candidates with identical decoded text after normalizing only newline conventions (CRLF/CR to LF). It preserves every candidate path in the score audit, but scores each distinct text only once. If all copies have equivalent content, one deterministic representative is selected. If contents differ, a candidate is selected only when it has a unique highest exact/casefolded-whitespace match count against the contract's positive annotated passages. Ties between distinct contents remain ambiguous; no-match ties are not silently resolved. Missing or repeated matches remain flagged for review. Negative contract/category labels remain contract-level labels; this process does not fabricate negative passage annotations.

## Data governance

The dataset card identifies CUAD v1 as CC BY 4.0 and requests attribution. Preserve the original citation and dataset provenance. The dataset documentation notes that TXT conversion can introduce formatting differences. Do not publish raw contracts or derived contract text in this repository; check source-document reuse terms before redistribution.
