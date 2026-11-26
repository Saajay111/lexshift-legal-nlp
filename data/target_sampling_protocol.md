# Target-Domain Sampling Protocol — Draft

**Status:** Planning template. No target contracts have been selected or annotated.

## 1. Provisional target window
Candidate period: filing dates from 2021-01-01 through 2025-12-31. This window is not frozen. First inspect CUAD's filing-date distribution and check for overlap with LEDGAR and other known corpora.

## 2. Sampling frame
Build a reproducible list of eligible SEC EDGAR filings before selecting the sample. Focus on material-contract exhibits (commonly Exhibit 10 variants), but record the exact inclusion rules and exclusions. Do not assume every Exhibit 10 document is a complete contract.

## 3. Eligibility rules to finalize
- Filing date falls within the frozen window.
- Exhibit is a substantive agreement or amendment that meets the contract-type definition.
- Text is accessible and sufficiently complete for annotation.
- Document is not an obvious duplicate, cover sheet, signature-only page, or unrelated attachment.
- Contract is not in CUAD and is not a duplicate/near-duplicate of another selected document.
- Amendments are either excluded or grouped with the underlying agreement under a pre-defined rule.

## 4. Selection
Create the frame first, then select using a reproducible random seed. If stratifying by industry or contract type, define strata and minimums before inspecting clause labels. Do not select documents because a target clause is present or easy to locate.

## 5. Pilot
Start with 15–20 documents to test HTML/text extraction quality, contract completeness, duplicate and amendment grouping, annotation time and ambiguity, and category prevalence and support.

The pilot informs feasibility and annotation rules. If pilot documents are used to revise the protocol, keep them out of the locked final test set or document the separation clearly.

## 6. Provenance manifest
Keep this manifest private unless public release has been reviewed. Suggested columns:
- project_contract_id
- cik
- issuer_name
- accession_number
- filing_date
- form_type
- exhibit_filename
- source_url
- contract_type
- industry_code
- amendment_group_id
- duplicate_group_id
- included
- exclusion_reason
- retrieval_date
- text_extraction_status
- text_sha256

Avoid storing unnecessary personal information. Do not commit raw contracts or private provenance mappings to the public repository without a documented permission and privacy review.

## 7. SEC collection compliance
Use official SEC filing indexes and archive paths. Declare a descriptive User-Agent, keep request rates conservative and well below the SEC's published maximum, cache results, and retrieve only needed files. Re-check SEC guidance before automated collection.

## 8. Freeze criteria
Do not begin main-study annotation until the filing-date window, eligible forms and exhibit types, contract-type rules, duplicate/amendment handling, sample size and selection method, industry coding scheme, annotation protocol, and target-test lock/access controls are approved and versioned.
