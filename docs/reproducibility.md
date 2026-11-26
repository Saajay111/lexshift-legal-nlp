# Reproducibility Protocol

## Before data collection
- [ ] Record CUAD version, source, license, schema, and retrieval date.
- [ ] Record SEC collection rules, access guidance, query strategy, and retrieval dates.
- [ ] Define target date range, exhibit types, inclusion/exclusion rules, and duplicate handling.
- [ ] Separate private provenance manifests from public analysis identifiers.

## Before annotation
- [ ] Version the text extraction and normalization pipeline.
- [ ] Pilot and freeze annotation guidelines.
- [ ] Define annotation unit, category definitions, and adjudication rules.
- [ ] Define contract-level grouping and split strategy.

## Before modeling
- [ ] Freeze the target test set and prevent test-label access during tuning.
- [ ] Record Python and package versions, hardware, seeds, and configuration.
- [ ] Record model names/revisions, tokenizer, prompt, and inference settings.
- [ ] Record all preprocessing, thresholds, and hyperparameter decisions.

## Before reporting
- [ ] Report metrics, support counts, prevalence, and uncertainty intervals.
- [ ] Generate tables and figures from scripts.
- [ ] Preserve run identifiers and machine-readable outputs.
- [ ] Document exclusions, missing data, protocol deviations, and failed runs.
- [ ] Verify no restricted text, credentials, personal data, or local paths are committed.
