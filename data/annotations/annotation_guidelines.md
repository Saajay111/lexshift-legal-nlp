# Annotation Guidelines — Draft v0.2

**Status:** Draft for pilot use. Do not begin main-study annotation until the pilot is reviewed and protocol v1.0 is frozen.

## 1. Purpose
Create consistent labels for five CUAD-aligned categories in SEC-filed material contracts. These are research definitions, not legal advice.

## 2. Annotation unit
For each contract and category, record whether the clause is present. For a positive label, create one row per supporting passage and include its passage ID and offsets. For a negative label, record one row with no passage ID or offsets. A provision may span multiple paragraphs. Store offsets against a versioned normalized text and retain the source document separately.

## 3. Exact CUAD category names and working definitions
- **Governing Law:** A provision specifying the law governing interpretation or enforcement of the agreement.
- **Non-Compete:** A provision restricting a party from specified competitive activities, as defined by CUAD's category guidance.
- **Anti-Assignment:** A provision requiring consent or notice when the contract is assigned to a third party, following CUAD's category description.
- **Termination for Convenience:** A provision allowing a party to terminate without cause by giving notice and allowing the specified waiting period to expire.
- **Cap on Liability:** A provision establishing a ceiling or cap on liability. Do not label a clause as Cap on Liability merely because it excludes a category of damages. Consult CUAD examples and document the boundary rule during the pilot.

CUAD separately contains **Uncapped Liability**. It is not the same label as Cap on Liability and is excluded from the initial five-category scope.

## 4. Decision rules
1. Apply the exact category definition, not a broad intuitive interpretation.
2. A heading alone is not evidence that the clause is present.
3. Include exceptions and qualifications that are part of the provision.
4. A passing mention is not necessarily a qualifying clause.
5. Record cross-references when the provision depends on another section.
6. Mark ambiguous items for adjudication rather than guessing.
7. A contract may have multiple distinct passages for one category; record each passage with a stable passage ID.
8. Keep category presence separate from passage boundaries.

## 5. Pilot and quality assurance
Pilot a small sample, discuss disagreements, revise definitions, and freeze version 1.0 before main annotation. If a second annotator is available, have them independently annotate a subset. Report raw agreement and a statistic suitable for the actual label structure. Preserve original labels and adjudication decisions.
