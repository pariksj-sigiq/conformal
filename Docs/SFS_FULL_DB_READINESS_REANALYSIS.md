# SFS Project Leap - Full Data Field Readiness Re-Analysis

Last updated: May 17, 2026

## Changelog vs Prior Version

- **D1 - Numbering fixed:** Added an SFS source-numbering crosswalk and switched SFS-facing labels to SFS cluster numbering. Procurement #4/#5 are corrected, and field-force use cases now use SFS Field Force #1-#8 labels.
- **D2 - Activity Analytics caveat added:** Activity Analytics is now marked assumption-only because the ODS has only a name and no detailed row content.
- **D3 - Churn count fixed:** Removed the incorrect churn tag from `BPV Gap`. Churn is now 19 fields, not 20.
- **D4 - Complinity/Concur fixed:** Vendor license fields are attributed to Complinity, and SG&A/T&E fields to Concur. These are now described as separate SFS systems needing integration.
- **D5 - Stakeholder asks widened:** Added Master Data/Data Governance, External-Data Contracting, and Complinity/Concur owners. Legal/compliance now also covers voice/call capture.
- **D6 - Tiers corrected:** Negotiation Prep and Should-Cost moved out of normal Tier 2 into Tier 2.5: external-data plus definition work.
- **D7 - Secondary sales/PoG blocker added:** Added cross-cutting dependency for secondary sales, inventory liquidation, and PoG capture.
- **D8 - SAP ask sharpened:** SAP route now explicitly asks for read-only extract access off the existing SAP BW / Power BI layer.
- **D9 - ROI/effort anchors added:** Added SFS-provided impact/build anchors and the ROI-aligned Wave 1 recommendation.

## Context

SFS gave Conformal the Project Leap use-case document. Sidd converted those use cases into a 146-field structured data-field database with assumed fields, likely systems, gap types, and availability. The current machine-readable file is:

`conformal/notion-data-fields-full-db-complete.json`

This is not confirmed SFS source inventory. It is Conformal's structured hypothesis from the ODS and the systems mentioned there. The next step with SFS is validation through source owners, sample extracts, integration routes, and workshops.

## Verified Headline Numbers

| Metric | Count | Read |
|---|---:|---|
| Total fields | 146 | Current full DB field count. |
| Available | 33 | Likely available in owned systems. |
| Partial | 19 | Exists partly but needs integration, cleanup, mapping, or scope confirmation. |
| Unavailable | 94 | Not a direct field today; may be computed, externally sourced, or newly captured. |
| Computed-unavailable | 58 | Not SFS blockers. Conformal can build these once base data lands. |
| Externally sourced | 27 | Needs EXIM, GST/GSP, MCA21, credit, litigation, commodity, FX/fuel, or similar providers. |
| Field-mapped business use cases | 15 | Procurement, Field Force/Salesforce, and Enterprise Assistant. |
| Logistics use cases | 5 | Not field-mapped; handled as buy-and-customize vendor/TMS track. |
| Infrastructure use case | 1 | Platform foundation, not a business field map. |

## The Main SFS Message

Do not lead with "94 fields are unavailable." Lead with:

> Most of the apparent gap is not missing SFS data. 58 fields are computed fields we build in the semantic layer. The real blockers are source access, external-data contracting, and a smaller number of new workflow-capture decisions.

That reframes the project from "SFS must already have every field" to "SFS gives read-only base data and owners; Conformal builds the derived intelligence layer."

## Source-System Readiness

After correcting Concur and Complinity attribution, the source grouping is:

| Source group | Available | Partial | Unavailable | Read |
|---|---:|---:|---:|---|
| SAP | 30 | 8 | 2 | Strongest base. Route is likely SAP BW / Power BI or SAP-controlled extract layer, not greenfield discovery. |
| Internal Apps | 3 | 9 | 7 | Growthbook/Saathi/ByteEdge plus Concur and Complinity. Needs API/export access and ID mapping. |
| Computed / Derived | 0 | 0 | 58 | Buildable by Conformal after base data lands. |
| External Market Data | 0 | 0 | 14 | EXIM, commodity, FX, fuel, labor/industry benchmarks. |
| External Risk/Compliance | 0 | 0 | 13 | GST/GSP, MCA21, credit bureau, litigation, NCLT/insolvency. |
| Logistics | 0 | 2 | 0 | Too thin for build scoring; handle through TMS/vendor fit-gap. |

## SFS Source Numbering Crosswalk

Use SFS labels in decks and workshops. Keep internal labels only as traceability.

| Internal analysis label | SFS cluster | SFS no. | SFS source name |
|---|---|---:|---|
| 1. Historical Spend Analysis & Price Insights | Procurement | 1 | Historical Spend Analysis & Price Insights |
| 2. Real-Time Import Data Analysis | Procurement | 2 | Real-Time Import Data Analysis |
| 3. AI-Driven Preparation Material for Negotiations | Procurement | 3 | AI-Driven Preparation Material for Negotiations |
| 5. AI-Led Vendor Identification & Recommendation | Procurement | 4 | AI-Led Vendor Identification & Recommendation |
| 4. Vendor Creditworthiness & Fraud Check | Procurement | 5 | Vendor Creditworthiness & Fraud Check |
| 6. Should-Cost Modelling & Analysis | Procurement | 6 | AI-Driven Should-Cost Analysis (across the top 5-10 products) |
| 7. Field Performance Dashboard | Field Force + Salesforce | 1 | Field Performance Tracking Dashboard |
| 9. Activity Analytics | Field Force + Salesforce | 2 | Activity Analytics (Growthbook + SAP) |
| 10. Scheme Chatbot | Field Force + Salesforce | 3 | Pricing, Policy & Scheme Dissemination Chatbot |
| 8. Dealer Profiles (Saathi) | Field Force + Salesforce | 4 | Dealer Profiles & Field-Visit Conversation Inputs (Saathi app) |
| 11. AI Sales Coaching | Field Force + Salesforce | 5 | AI-Enabled Sales Coaching |
| 12. Unified Product & Partner-Level Visibility | Field Force + Salesforce | 6 | Unified Product & Partner-Level Visibility |
| 14. Warehouse Stock Visibility | Field Force + Salesforce | 7 | Real-Time Warehouse Stock Visibility |
| 13. Early Warning for Sales Performance & Dealer Churn Risk | Field Force + Salesforce | 8 | Early Warning for Sales Performance & Dealer Churn Risk |
| Enterprise Chat Assistant (Supply & Sales) | Enterprise Assistant | 1 | Enterprise Chat Assistant (Supply & Sales) |
| Not field-mapped in 146-field DB | Logistics - Buy and Customize | 1 | Freight Price Discovery |
| Not field-mapped in 146-field DB | Logistics - Buy and Customize | 2 | Optimal Route & Pickup/Drop Recommendation |
| Not field-mapped in 146-field DB | Logistics - Buy and Customize | 3 | E-Proof of Delivery (E-PoD) Execution |
| Not field-mapped in 146-field DB | Logistics - Buy and Customize | 4 | Real-Time Consignment Monitoring |
| Not field-mapped in 146-field DB | Logistics - Buy and Customize | 5 | Ocean Freight Tracking & Optimization |
| Not a business field map | Technology & Infrastructure Setup | 1 | Technology and Infrastructure set-up |

## Corrected Readiness Tiers

### Tier 1: Fast Start / Descriptive Base

These are the fastest starts for descriptive surfaces. The dashboard/profile base is extraction-led. The prescriptive/intelligence layer is not fully extraction-led.

| SFS use case | Fields | Available | Partial | Unavailable | Honest read |
|---|---:|---:|---:|---:|---|
| Field Force #1 - Field Performance Tracking Dashboard | 20 | 13 | 4 | 3 | Strongest data start. Fast for descriptive dashboard; liquidation and secondary-sales completeness still need new SFS capture. |
| Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs | 20 | 12 | 4 | 4 | Strong dealer/SAP base. Profile can ship early; relationship intelligence and voice capture need workflow validation. |

### Tier 1.5: Strong Pilot / Definition Work

| SFS use case | Fields | Available | Partial | Unavailable | Honest read |
|---|---:|---:|---:|---:|---|
| Enterprise Assistant #1 - Enterprise Chat Assistant | 18 | 8 | 4 | 6 | Strong Wave 1 if scoped to confirmed SAP/internal-app marts and metric dictionary. |
| Procurement #1 - Historical Spend Analysis & Price Insights | 26 | 11 | 6 | 9 | SAP purchase base is strong; taxonomy, BPV and anomaly rules need procurement workshops. |
| Field Force #6 - Unified Product & Partner-Level Visibility | 15 | 8 | 2 | 5 | Strong SAP base; product/partner visibility is fast, but liquidation, secondary-sales and PoG-led intelligence need new SFS capture. |
| Field Force #7 - Real-Time Warehouse Stock Visibility | 18 | 7 | 6 | 5 | SAP stock likely available; vendor warehouse, in-transit, substitution and freshness need validation. |

### Tier 2: Moderate Integration Plus Definition Work

| SFS use case | Fields | Available | Partial | Unavailable | Main friction |
|---|---:|---:|---:|---:|---|
| Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot | 14 | 3 | 4 | 7 | Circulars, pricing conditions and eligibility rules must be structured. |
| Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk | 19 | 7 | 2 | 10 | Churn definition, intervention tracking, and risk labels needed. |
| Procurement #4 - AI-Led Vendor Identification & Recommendation | 23 | 8 | 4 | 11 | Keep in Tier 2 because 12 fields are owned and 5 sourced; external signals improve it but do not fully block the base. |

### Tier 2.5: External-Data Plus Definition Work

These should not sit in normal Tier 2. They have heavy external-data and business-assumption dependencies, but are still strategically important.

| SFS use case | Fields | Available | Partial | Unavailable | Main friction |
|---|---:|---:|---:|---:|---|
| Procurement #3 - AI-Driven Preparation Material for Negotiations | 21 | 5 | 3 | 13 | EXIM, commodity/macro feeds, vendor history, and negotiation outcome capture. |
| Procurement #6 - AI-Driven Should-Cost Analysis | 17 | 4 | 2 | 11 | EXIM, commodity, FX/fuel/labor benchmarks plus category-specific cost model assumptions. |

### Tier 3: Workshop-Heavy / Discovery-Only For Now

| SFS use case | Fields | Available | Partial | Unavailable | Why it is discovery-first |
|---|---:|---:|---:|---:|---|
| Procurement #2 - Real-Time Import Data Analysis | 16 | 3 | 2 | 11 | EXIM provider, HSN mapping, landed-cost normalization and provider lag. |
| Procurement #5 - Vendor Creditworthiness & Fraud Check | 18 | 3 | 1 | 14 | GST, MCA21, credit, litigation and legal/privacy approval. |
| Field Force #5 - AI-Enabled Sales Coaching | 18 | 4 | 2 | 12 | Approved coaching content, voice/call capture, classification and coaching rubric. |

### Assumption-Only: Highest Discovery Priority

| SFS use case | Fields | Available | Partial | Unavailable | Caveat |
|---|---:|---:|---:|---:|---|
| Field Force #2 - Activity Analytics (Growthbook + SAP) | 17 | 8 | 2 | 7 | The ODS has name only and no detailed content. The field map is inferred from sibling use cases; scope with SFS before any build claim. |

## Cross-Cutting Net-New-Capture Dependency

### Secondary Sales / Inventory Liquidation / PoG

SFS explicitly notes that secondary sales, inventory liquidation, and PoG trackers are not fully collected today. This is a blocker for the "smart" versions of several field-force use cases.

Affected:

- Field Force #1 - Field Performance Tracking Dashboard.
- Field Force #2 - Activity Analytics.
- Field Force #6 - Unified Product & Partner-Level Visibility.
- Channel Stock Estimate and liquidation-related derived fields.

Honest caveat to use:

> The descriptive base is fast if SAP/Growthbook data lands. But liquidation, secondary-sales completeness, and PoG-led intelligence require new SFS capture or a distributor/dealer reporting workflow.

## Integration Architecture

### Layer 1: Raw Landing

Store source extracts exactly as received, partitioned by source and ingestion date.

Examples:

- `raw_sap_bw_sales_billing`
- `raw_sap_bw_purchase_order_line`
- `raw_sap_bw_receivables`
- `raw_sap_stock_snapshot`
- `raw_growthbook_activity_event`
- `raw_saathi_interaction`
- `raw_concur_expense`
- `raw_complinity_vendor_license`
- `raw_scheme_document`
- `raw_ariba_supplier`
- `raw_exim_transaction`

### Layer 2: Standardized Columnar Tables

Convert raw extracts into typed, validated, deduplicated Parquet/Delta tables.

Core dimensions:

- `dim_dealer`
- `dim_product`
- `dim_vendor`
- `dim_employee`
- `dim_territory`
- `dim_plant_warehouse`
- `dim_calendar`

Core facts:

- `fact_sales_invoice_line`
- `fact_collection`
- `fact_purchase_order_line`
- `fact_inventory_snapshot`
- `fact_field_activity`
- `fact_target`
- `fact_scheme`
- `fact_concur_expense`
- `fact_vendor_license`

Crosswalks:

- `dealer_id_crosswalk`
- `vendor_id_crosswalk`
- `material_code_crosswalk`
- `employee_id_crosswalk`
- `hsn_material_map`

### Layer 3: Gold Semantic Marts

- `mart_field_performance`
- `mart_dealer_360`
- `mart_partner_visibility`
- `mart_stock_visibility`
- `mart_spend_cube`
- `mart_enterprise_kpis`
- `mart_procurement_vendor_score`
- `mart_churn_risk`
- `mart_scheme_eligibility`

### Layer 4: Governed Agent Access

Agents should query semantic views, not source tables.

Reusable tools:

- SQL over governed marts.
- Retrieval over circulars, decks, policy docs and product content.
- Chart/report rendering.
- Metric glossary and data dictionary.
- Tool-call audit log.
- Golden-question eval suite.
- Role-aware access.

## Sharpened Integration Asks

### SAP

The SAP route is more known than exploratory because the SFS Enterprise Assistant row names **SAP BW + Power BI**.

Ask:

- Confirm read-only extract access off the existing SAP BW / Power BI layer.
- Confirm which SAP domains are covered there: SD, MM, FI/CO, inventory, targets, stock.
- Confirm whether BW/Power BI dimensions preserve dealer ID, material code, vendor ID, employee ID, HSN, plant and warehouse keys.
- Confirm sample extract process and refresh frequency.

### Growthbook / Saathi / Internal Apps

- Provide event schema and 12-month export.
- Confirm dealer/employee ID alignment with SAP.
- Confirm whether visit outcomes are structured or free text.
- Confirm whether voice capture is live, planned, or not approved.

### Concur / Complinity

- Concur unblocks SG&A/T&E spend fields for Historical Spend and field-performance expense views.
- Complinity unblocks vendor license status and validity for procurement/vendor compliance views.
- Both need separate owners because the ODS explicitly says they are not integrated with SAP.

### External Data

- EXIM/customs provider.
- Commodity indices.
- FX/fuel/labor/utility benchmarks.
- GST via GSP.
- MCA21.
- Commercial credit bureau.
- Litigation/court/NCLT sources.

Do not commit production scope for these until the external-data contracting owner is in the room.

## Stakeholder-Keyed Ask Pack

| SFS stakeholder | What they unblock | Use cases blocked until present | First ask |
|---|---|---|---|
| Amit / executive sponsor | Cross-functional ownership and priority | All | Nominate owners and approve the 2-week discovery sprint. |
| SFS IT lead | Access pattern, security constraints, deployment path | All | Confirm read-only integration path and target environment. |
| SAP Basis / integration owner | SAP BW/Power BI extraction, service users, scheduling | Enterprise, field, procurement, stock | Confirm extract access off existing SAP BW / Power BI layer. |
| SAP SD owner | Sales, billing, dealer/customer master, pricing conditions | Field #1, #3, #4, #6, #8, Enterprise | Provide sales/billing sample and pricing-condition availability. |
| SAP MM owner | PO lines, material master, vendor master, stock | Procurement #1, #3, #4, #6, Field #7, Enterprise | Provide PO-line, material, vendor and stock samples. |
| SAP FI/CO / Finance owner | Receivables, collections, P&L, budgets, metric definitions | Enterprise, Field #1, Field #8 | Provide collections/receivables sample and metric definitions. |
| Master Data / Data Governance owner | Product hierarchy, dealer/vendor/employee/HSN crosswalks | Product/Partner Visibility, Enterprise cross-BU, Spend, EXIM, Vendor ID | Own cross-BU product hierarchy and ID crosswalk validation. |
| Growthbook / Saathi owner | Activity logs, visit events, voice/note capture, field IDs | Field #1, #2, #4, #5, #8 | Share schema, 12-month export and dealer/employee ID mapping. |
| Sales ops / field excellence | Targets, incentives, hierarchy, field workflow | Field #1, #2, #4, #5, #6, #8 | Validate field hierarchy, targets, visit outcomes and capture gaps. |
| Scheme / pricing owner | Circulars, eligibility rules, source of truth | Field #3, Enterprise | Share active schemes, circular repository and SAP pricing linkage. |
| Procurement category managers | Spend taxonomy, BPV, should-cost assumptions | Procurement #1, #3, #4, #6 | Run taxonomy/BPV/should-cost workshops and select priority commodities. |
| Ariba owner | RFQ, supplier onboarding, contracts, workflow status | Procurement #3, #4, #5 | Confirm rollout status, exports/APIs and supplier ID mapping. |
| External-Data Contracting owner | EXIM, commodity, GST/GSP, MCA21, credit, litigation providers | Procurement #2, #3, #5, #6 | Confirm existing subscriptions or approve vendor selection. |
| Legal/compliance owner | Data-use approval, vendor risk, voice/call capture | Procurement #5, Field #4, Field #5 | Approve external risk data, dealer voice capture, call recording/classification. |
| Complinity / Concur owner | Vendor license and SG&A/T&E integration | Procurement #1, Field Performance expense views | Provide exports/API options and owner for ID mapping. |
| Logistics owner | TMS/vendor fit-gap, lane/rate/shipment/POD data | All logistics use cases | Treat as separate buy-and-customize track with vendor shortlist. |
| Azure/security owner | VPC, SSO, model gateway, audit and logging | All production agents | Confirm tenant, data residency, SSO, logs and approved model path. |

## SFS ROI / Effort Anchors

The data-readiness result converges with SFS's own impact and effort logic.

| SFS anchor from ODS | Our readiness read | Consequence |
|---|---|---|
| Field Force impact: INR 50-80 Cr incremental revenue; 8-month solution build estimate | Field Performance is the fastest data start | Field Performance should be a Wave 1 anchor. |
| Enterprise Assistant: shortest 4-month build estimate | Strong pilot if scoped to confirmed SAP/internal metrics | Enterprise Assistant should be Wave 1 with platform foundation. |
| Procurement: INR 10-15 Cr sourcing savings | Historical Spend has strong SAP purchase-register base | Spend cube should enter discovery early, with taxonomy workshop. |
| Logistics: low custom build cost and explicitly buy-and-customize | Not field-mapped in the 146-field DB | Keep logistics as vendor/TMS fit-gap, not custom agent build. |

Recommended ROI-aligned Wave 1:

1. Platform foundation and governed columnar store.
2. Enterprise Assistant scoped to confirmed SAP BW / Power BI extracts.
3. Field Force #1 - Field Performance Tracking Dashboard.
4. Field Force #4 - Dealer Profiles as the field-facing companion.
5. Procurement #1 - Historical Spend in discovery, not necessarily same build sprint.

## Practical Next Actions

### Before the SFS meeting

- Convert the crosswalk and stakeholder ask pack into the meeting pre-read.
- Ask Amit to bring the named owners, not just business sponsors.
- Prepare masked-extract request list by source owner.

### During the SFS meeting

- Validate the source-system hypothesis.
- Confirm SAP BW / Power BI read-only extract route.
- Separate 15 build use cases from 5 logistics vendor-fit-gap use cases.
- Confirm which unavailable fields are computed, sourced, or workflow-capture gaps.

### After the SFS meeting

- Build a data-readiness heatmap from actual extracts.
- Load 2-3 source slices into a columnar POC.
- Run 20 golden questions against real data.
- Reprice waves based on actual data friction, not the use-case sheet alone.
