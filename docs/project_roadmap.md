# Project Roadmap

The project advances through evidence gates. A phase is complete only when its exit criterion is met.

| Phase | Workstream | Exit criterion |
|---|---|---|
| 0. Foundation | Repository, package skeleton, documentation, tests, CI | Clean test run and documented scope |
| 1. Verification | CUAD schema/license, literature review, SEC access rules | Dataset feasibility memo with sources |
| 2. Protocol | Sampling frame, annotation codebook, metrics, split plan | Protocol v1.0 frozen |
| 3. Pilot | Text extraction, annotation pilot, quality review | Pilot report and revised codebook |
| 4. Baselines | Lexical and classical source-domain models | Reproducible baseline report |
| 5. Neural model | Transformer training and validation | Model card and locked configuration |
| 6. Target evaluation | Target annotations and one-time locked evaluation | Metrics with contract-level uncertainty |
| 7. Analysis | Error taxonomy and cautious subgroup analysis | Auditable analysis tables |
| 8. Publication | Manuscript, reproducibility, release review | Complete paper and release checklist |

## Decision gates
- **Gate A — Dataset feasibility:** Do the selected CUAD categories exist with usable labels and sufficient support?
- **Gate B — Annotation feasibility:** Can annotators apply the definitions consistently to the target documents?
- **Gate C — Statistical feasibility:** Is the sample large enough for the planned primary comparisons?
- **Gate D — Leakage audit:** Are contracts, amendments, and duplicates isolated across splits?
- **Gate E — Release audit:** Are all files safe and legally appropriate to publish?

A failed gate means revise the design; it does not mean hide the limitation.
