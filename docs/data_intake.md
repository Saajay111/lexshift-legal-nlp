# CUAD Dataset Intake — Step-by-Step

This guide is for local research use. Do not upload the full dataset or raw contracts into the public repository.

## 1. Source and version
Use CUAD v1 from The Atticus Project. The project page and dataset card describe 510 commercial contracts, 41 clause categories, and 13,000+ expert annotations. The Hugging Face dataset card currently identifies the license as CC BY 4.0.

- Project page: https://www.atticusprojectai.org/cuad/
- Dataset card: https://huggingface.co/datasets/theatticusproject/cuad
- Original paper: https://arxiv.org/abs/2103.06268
- Official source repository: https://github.com/The-Atticus-Project/cuad

Record the exact release, download date, source URL, and checksum. Attribute the dataset as required by its terms.

## 2. Download the master-clauses CSV
From the dataset page, open the dataset card and follow its CUAD v1 format/download information. The card describes a master-clauses CSV alongside SQuAD-style JSON, Excel label reports, and the underlying contract files. Prefer the master-clauses CSV for the initial schema and label audit.

Keep the downloaded file in a local/private working directory. Do not commit it to GitHub.

## 3. Run the schema audit
After installing the project in editable mode with its development dependencies, run:

```bash
lexshift-audit-cuad "path/to/CUAD_master_clauses.csv"
```

The command reports:
- row and column counts;
- exact source column names;
- which expected category names appear in those columns;
- categories that were not matched;
- unique values in the first column.

This is a discovery report only. It does not verify the legal correctness of annotations or prove that every category has adequate positive support.

## 4. What to share back
Share the JSON/text output of the audit, especially:
- row count and column count;
- full column-name list;
- category match report;
- any missing expected category names.

Do not share the raw contract text, private issuer notes, credentials, or personal information.

## 5. Decision gate
Before model training, inspect exact category definitions and count positive/negative examples per category. If a category is absent, rare, or not transferable to the target sample under the written definition, revise the category set and record the decision in the protocol. Do not silently substitute a broader label.
