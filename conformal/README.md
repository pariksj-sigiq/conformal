# Conformal SFS Working Data

This folder holds the source files and derived datasets used for the SFS Project Leap analysis.

## Source files

| File | Description |
|---|---|
| `Use Cases details_SFS_Project LEAP.ods` | Original SFS use-case workbook. This is the source document SFS provided. |
| `Conformal_AI Transformation for SFS_May 2026.pdf` | Earlier Conformal presentation shared with SFS. Used as style/content reference. |

## Derived data files

| File | Description |
|---|---|
| `notion-data-fields-full-db-complete.json` | Full local export of the Notion data-field database. |
| `notion-data-fields-full-db-selected.json` | Clean selected 146-field dataset used by the current analysis. |
| `notion-project-leap-full-dataset.json` | Supporting Project Leap dataset exported locally. |

## Interactive working artifacts

| File | Description |
|---|---|
| `sfs_readiness_integration_plan_first_sample.html` | Interactive readiness and integration plan viewer. |
| `sfs_use_case_field_ask_matrix.html` | Use-case to field/source/ask matrix. |
| `conformal_people_v2_narrative.html` | Earlier Conformal people-section narrative artifact. Not part of the SFS data ask package. |

## Data interpretation rules

1. The JSON is a Conformal-derived schema hypothesis, not a confirmed SFS data inventory.
2. Availability values mean "likely available based on source-system hints", not "verified by SFS".
3. The ODS remains the SFS source of truth for use-case wording, cluster numbering and SFS-stated ROI/effort anchors.
4. The 146-field dataset intentionally maps 15 custom-build use cases. Logistics is handled separately as a buy-and-customise track.
