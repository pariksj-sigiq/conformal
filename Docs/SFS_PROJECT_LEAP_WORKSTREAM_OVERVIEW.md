# SFS Project Leap Workstream Overview

Last updated: May 18, 2026
Owner: Conformal
Primary audience: Conformal internal team, then SFS working-session preparation

## 1. What happened in this workstream

SFS shared the Project Leap use-case workbook:

- `conformal/Use Cases details_SFS_Project LEAP.ods`

Conformal used that workbook, plus the systems named inside it, to derive a field-level data-readiness map:

- `conformal/notion-data-fields-full-db-complete.json`
- `conformal/notion-data-fields-full-db-selected.json`

The selected 146-field map became the basis for:

1. A field-level readiness analysis.
2. A source-system and integration plan.
3. A client-facing deep-dive document.
4. An exact ask pack for SFS.
5. A presentation deck for the next SFS discussion.
6. An internal assumption audit comparing what SFS actually gave us against what we inferred.

The most important framing: **SFS did not provide a field-level schema.** They provided use-case narratives, current-state gaps, system hints and desired outcomes. The 146-field map is therefore a strong schema hypothesis, not a confirmed SFS data inventory.

## 2. Canonical numbers

These numbers have been checked across the JSON-derived analysis and should remain consistent unless the underlying JSON changes.

| Metric | Count | Meaning |
|---|---:|---|
| Total derived fields | 146 | Field-level hypothesis across the 15 mapped custom-build use cases |
| Available | 33 | Likely exists in an SFS-owned system, pending source-owner validation |
| Partial | 19 | Exists but needs cleanup, mapping, connector confirmation or scope validation |
| Unavailable | 94 | Not a direct confirmed field today |
| Computed / derived unavailable fields | 58 | Conformal computes these in the semantic layer once base data lands |
| Externally sourced fields | 27 | Conformal can source via EXIM, GST/GSP, MCA21, credit, commodity, FX, labour, utility or litigation providers |
| Net-new capture / governance fields | Approximately 9 | SFS must confirm workflow capture, master-data governance or new data-entry process |
| Mapped use cases | 15 | Enterprise, Procurement and Field Force custom-build candidates |
| Logistics use cases | 5 | Treated as buy-and-customise vendor/TMS track, deliberately not field-mapped |
| Infrastructure use case | 1 | Treated as mandatory foundation |

## 3. Use-case framing

The 21 SFS use cases are handled as:

| SFS cluster | Treatment |
|---|---|
| Enterprise Assistant | Wave 1 pilot candidate |
| Procurement #1 to #6 | Procurement suite, but split by readiness and external-data dependency |
| Field Force #1 to #8 | Field-force suite, with Field Performance and Dealer Profiles as fast-start candidates |
| Logistics #1 to #5 | Buy-and-customise track, not a custom AI build |
| Technology and Infrastructure | Foundation layer required before production |

## 4. Recommended wave story

The current recommendation is:

| Wave | Scope | Why |
|---|---|---|
| Wave 0 | Data foundation, secure extraction route, columnar store, semantic layer, access control, audit logs, eval harness | Required to make every later agent reliable and reusable |
| Wave 1 | Enterprise Assistant, Field Performance Dashboard, Dealer Profiles | SFS-owned data base is strongest and ROI alignment is highest |
| Wave 1.5 | Historical Spend Analysis | SAP purchase-register base is strong, but taxonomy and BPV definitions need procurement sign-off |
| Wave 2 | Product/Partner Visibility, Warehouse Stock, Scheme Chatbot, Churn Risk, Vendor ID | Mostly feasible after source-owner validation and definition workshops |
| Wave 2/3 | Import Analysis, Negotiation Prep, Should-Cost, Vendor Credit/Fraud | External-data, legal and category-definition gated |
| Separate | Logistics | Vendor selection plus integration/customisation |

## 5. Discovery ask strategy

The discovery request to SFS is intentionally lightweight:

1. Start with masked samples and schemas.
2. Confirm the SAP BW / Power BI extraction route first.
3. Avoid asking for production credentials in the first sprint.
4. Force named owners for SAP, Growthbook, Saathi, Concur, Complinity, Ariba, master data, legal, security, procurement and field-force systems.
5. Use the first meetings to burn down the 146-field map into ready, partial, computed, external-data gated and net-new-capture buckets.

Field discovery burn-down from the current ask pack:

| Step | Fields dispositioned | Cumulative |
|---|---:|---:|
| SAP working session | 40 | 40 / 146 |
| Field-force systems session | 44 | 84 / 146 |
| Procurement systems session | 46 | 130 / 146 |
| Finance/metric dictionary workshop | 3 | 133 / 146 |
| Legal/external-risk review | 13 | 146 / 146 |

By the end of the SAP and field-force working sessions, SFS and Conformal should have enough source truth to validate Wave 1.

## 6. Key caveats to preserve

These should not get softened in client or internal materials:

1. **Available does not mean confirmed.** It means likely available in an SFS-owned system, pending owner validation.
2. **Activity Analytics is assumption-only.** SFS gave a use-case name but no detailed description.
3. **Secondary sales, liquidation and PoG are cross-cutting blockers.** SFS states these are not currently collected in the relevant field-force context.
4. **Logistics is deliberately unmapped.** It belongs in vendor selection and fit-gap, not custom agent build.
5. **Computed fields are not data asks.** They require definitions, examples and validation rules.
6. **External data is a contracting/legal posture question.** It is not a SAP extraction problem.
7. **Master-data crosswalks are critical.** Dealer, vendor, material, employee and HSN matching can make or break the build.

## 7. Primary source files

| File | Role |
|---|---|
| `conformal/Use Cases details_SFS_Project LEAP.ods` | Original SFS workbook |
| `conformal/notion-data-fields-full-db-complete.json` | Full local export of the Notion-derived field database |
| `conformal/notion-data-fields-full-db-selected.json` | Clean selected 146-field dataset used for analysis |
| `conformal/notion-project-leap-full-dataset.json` | Project Leap support dataset exported from Notion |

## 8. Final working artifacts

| File | Audience | Purpose |
|---|---|---|
| `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.md` | SFS-facing | Professional deep-dive and ask document |
| `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.pdf` | SFS-facing | Rendered PDF version of the deep-dive |
| `deliverables/Conformal_SFS_Exact_Asks_For_Discovery.md` | SFS-facing / meeting prep | Exact data, access, people, meeting and workshop asks |
| `deliverables/Conformal_SFS_146_Field_Assumption_Audit.md` | Internal | Discrepancies between SFS source and Conformal assumptions |
| `presentation/Conformal_SFS_Data_DeepDive_Deck.pdf` | SFS-facing | Presentation deck for the data-readiness and ask conversation |
| `presentation/sfs_datadeepdive_deck.html` | Internal/editable | HTML source used to generate the deck |

## 9. What to send externally

Recommended package for SFS:

1. `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.pdf`
2. `presentation/Conformal_SFS_Data_DeepDive_Deck.pdf`
3. A short email using the section at the end of `deliverables/Conformal_SFS_Exact_Asks_For_Discovery.md`

Do **not** send the assumption audit raw unless it is rewritten for client tone. It is deliberately blunt and internal.

## 10. What to do next

1. Align internally with Sidd on Wave 1 scope and pricing.
2. Send Amit a short note requesting a data-readiness working session.
3. Ask SFS to nominate owners before the session.
4. Use the exact ask pack as the agenda.
5. After SFS provides sample extracts, re-run the 146-field analysis against confirmed source truth.
