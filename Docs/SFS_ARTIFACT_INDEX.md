# SFS Project Leap Artifact Index

Last updated: May 18, 2026

This index explains what each generated artifact is for, what is safe to share externally, and what should remain internal.

## 1. Source and derived data

| Path | Status | Audience | Notes |
|---|---|---|---|
| `conformal/Use Cases details_SFS_Project LEAP.ods` | Source | Internal | Original workbook from SFS. Treat as confidential. |
| `conformal/notion-data-fields-full-db-complete.json` | Derived source | Internal | Full Notion-local export. More verbose than the selected dataset. |
| `conformal/notion-data-fields-full-db-selected.json` | Derived source | Internal | Clean 146-field source of truth for current analysis. |
| `conformal/notion-project-leap-full-dataset.json` | Derived support | Internal | Support export from Notion. |

## 2. Client-facing documents

| Path | Audience | Use |
|---|---|---|
| `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.pdf` | SFS-facing | Primary polished PDF to share before or after the working session. |
| `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.md` | SFS-facing source | Editable source for the PDF. |
| `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.html` | Internal/source | Rendered HTML used in PDF generation. |
| `deliverables/Conformal_SFS_Exact_Asks_For_Discovery.md` | SFS-facing / meeting prep | The most operational ask pack. Use for agenda, owner mapping and data checklist. |

## 3. Internal documents

| Path | Audience | Use |
|---|---|---|
| `deliverables/Conformal_SFS_146_Field_Assumption_Audit.md` | Internal | Honest audit of where Conformal may have over-assumed fields, systems or availability. |
| `Docs/SFS_FULL_DB_READINESS_REANALYSIS.md` | Internal | Re-analysis against the full field database. |
| `Docs/SFS_DATA_READINESS_AND_TEAM_ASKS.md` | Internal | Earlier readiness and team-asks synthesis. |
| `Docs/SFS_USE_CASE_FIELD_INTEGRATION_ASKS.md` | Internal | Use-case to field/source ask mapping. |
| `Docs/SFS_21_USE_CASE_TECH_DEEP_DIVE.md` | Internal | Per-use-case technical deep dive. |
| `Docs/SFS_PROJECT_LEAP_WORKSTREAM_OVERVIEW.md` | Internal | Current master narrative of the whole workstream. |

## 4. Presentation artifacts

| Path | Audience | Use |
|---|---|---|
| `presentation/Conformal_SFS_Data_DeepDive_Deck.pdf` | SFS-facing | Current polished deck. |
| `presentation/Conformal_SFS_Data_DeepDive_Deck copy.pdf` | Internal/reference | Prior exported copy. Keep only if comparing versions. |
| `presentation/sfs_datadeepdive_deck.html` | Internal/editable | HTML deck source. |

## 5. Interactive/readiness viewers

| Path | Audience | Use |
|---|---|---|
| `conformal/sfs_readiness_integration_plan_first_sample.html` | Internal / possible SFS working artifact | Interactive readiness and integration plan viewer. |
| `conformal/sfs_use_case_field_ask_matrix.html` | Internal / possible SFS working artifact | Use-case field ask matrix. |
| `Docs/sfs_data_readiness_workbench.html` | Internal | Data readiness workbench snapshot. |
| `Docs/sfs_project_leap_workbench.html` | Internal | Project Leap workbench snapshot. |

## 6. Build and QA outputs

| Path | Audience | Use |
|---|---|---|
| `outputs/sfs_client_work/build_client_artifacts.py` | Internal | Script used to generate client document artifacts. |
| `outputs/sfs_client_work/build_detailed_deck.py` | Internal | Script used to generate the detailed deck. |
| `outputs/sfs_client_work/rendered_doc/` | Internal | Rendered PNG pages of the client document for visual QA. |
| `outputs/sfs_client_work/rendered_deck_notes/` | Internal | Rendered PNG pages of the latest deck for visual QA. |
| `outputs/sfs_client_work/*contact_sheet.png` | Internal | Contact sheets for reviewing page quality quickly. |
| `outputs/sfs_review/` | Internal | Reference/current render comparison outputs. |

## 7. Which artifacts to send when

### Before the working session

Send:

- `deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.pdf`
- `presentation/Conformal_SFS_Data_DeepDive_Deck.pdf`

Use the email copy in:

- `deliverables/Conformal_SFS_Exact_Asks_For_Discovery.md`

### During the working session

Use:

- `deliverables/Conformal_SFS_Exact_Asks_For_Discovery.md`
- `conformal/sfs_use_case_field_ask_matrix.html`
- `conformal/sfs_readiness_integration_plan_first_sample.html`

### Internal prep only

Use:

- `deliverables/Conformal_SFS_146_Field_Assumption_Audit.md`
- `Docs/SFS_PROJECT_LEAP_WORKSTREAM_OVERVIEW.md`
- `Docs/SFS_FULL_DB_READINESS_REANALYSIS.md`

## 8. Naming discipline

Use SFS's own cluster numbering in SFS-facing artifacts:

- Enterprise Assistant #1
- Procurement #1 to #6
- Field Force #1 to #8
- Logistics #1 to #5
- Technology and Infrastructure #1

Earlier internal artifacts may have used a Conformal sequence. The crosswalk in the deep-dive materials supersedes that numbering.
