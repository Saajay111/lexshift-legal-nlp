# CUAD Training-Data Preparation

**Status:** Contract-level label preparation implemented. Passage-classification training is not yet authorized by the current export alone.

## What the converted file supports

The converted master-clauses file contains 510 contracts and five category labels per contract. Positive records contain CUAD evidence passages; negative records indicate that no passage was annotated for that contract/category.

The preparation pipeline aggregates multiple positive passages into one contract/category presence label and produces:
- `cuad_contract_labels.csv`: one row per contract, with one Boolean column per category;
- `cuad_contract_splits.csv`: deterministic train/validation/test assignment by contract;
- `cuad_preparation_report.json`: per-category class support within each split.

Default split proportions are 70% train, 15% validation, and 15% test, using a fixed random seed. This initial split is a reproducible baseline, not an optimized multilabel-stratified split. Always inspect class support before fitting a model. Do not tune on the test set.

## Why we do not train a passage classifier yet

A negative contract/category label is not a negative passage. The current export has no corresponding negative text passage for those rows. Treating empty passage cells as text examples would create invalid training data.

To train and evaluate passage retrieval/classification fairly, obtain the versioned full contract text for each CUAD contract, segment it using a documented procedure, align the expert evidence passages to that text, and sample candidate negative passages from the remaining text. Candidate negatives require quality checks because a clause may be present even if CUAD did not annotate a passage for it.

For a contract-level presence model, the full contract text is also required as model input. The annotation CSV contains evidence passages, not complete contracts.

## Known metadata gaps

The imported master CSV has no document-date or industry values in the converted rows. Do not infer these from filenames without a separately documented and validated metadata-enrichment step. Date and industry subgroup analyses remain unavailable until then.

## Run

```bash
pip install -e ".[dev]"
lexshift-prepare-cuad data/interim/cuad_annotations.csv data/processed/cuad_preparation
```

The command writes the three artifacts listed above. It does not copy raw contracts or source annotations into the repository.
