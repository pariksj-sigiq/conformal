# SFS Project Leap - Data Deep-Dive, Integration Vision and Working Session Asks

Prepared for Shriram Farm Solutions
Prepared by Conformal
Last updated: May 18, 2026

## 1. Purpose

SFS shared the Project Leap use-case document with Conformal. We reviewed those use cases and decomposed the 15 custom-build use cases into the individual data fields needed to move from prototype to production. We then mapped each field to the likely source system, assessed whether it is available, partially available, computed, externally sourced or net-new capture, and converted that into a concrete ask pack for the next SFS working session.

This document is not a final scope or commercial proposal. It is a data-readiness working paper. Its purpose is to help SFS and Conformal validate source-system truth quickly, agree the right owners, and begin the first discovery sprint with specific, low-risk data asks.

## 2. Executive summary

- We mapped 146 fields across 15 custom-build use cases. Logistics is treated separately as a buy-and-customise vendor/TMS track.
- The headline readiness split is 33 Available, 19 Partial and 94 Unavailable.
- The 94 Unavailable fields should not be read as 94 blockers. 58 are computed by Conformal once base data lands, 27 are external feeds that Conformal can source, and roughly 9 require SFS workflow or master-data capture decisions.
- The first build should start with reusable foundations: SAP BW / Power BI sales and finance extracts, Growthbook/Saathi field activity, SAP MM procurement extracts, and master-data crosswalks.
- Recommended Wave 1: Enterprise Assistant, Field Performance Tracking Dashboard and Dealer Profiles. These create the data spine for later field-force, procurement, churn, scheme and enterprise assistant use cases.

## 3. How to read the field analysis

We worked from the SFS-provided use-case document. For each use case, we asked four practical questions:

1. What data fields would this need in production?
2. Which source system is most likely to hold each field?
3. Is the field available today, partially available, computed, externally sourced, or not captured?
4. What exact owner, extract or decision is needed from SFS to validate it?

Because this is derived from the use-case document and referenced systems, every finding should be validated with SFS source owners before final pricing or production scope.

## 4. Readiness snapshot

| Readiness bucket | Count | Practical meaning |
|---|---:|---|
| Available | 33 | Likely exists in an SFS-owned system, mostly SAP. Discovery asks for masked extracts and schemas. |
| Partial | 19 | Exists but needs integration, cleanup, mapping or scope confirmation. |
| Unavailable | 94 | Not a direct field today. It may still be computed by Conformal or sourced externally. |
| Total | 146 | Field-level data map across 15 mapped build use cases. |

The Unavailable fields split as follows:

| Gap type | Count | Primary action |
|---|---:|---|
| Computed / derived | 58 | Conformal computes these in the semantic layer after base data lands. SFS provides definitions and examples, not raw data. |
| Externally sourced | 27 | Conformal integrates external providers such as EXIM, GST/GSP, MCA21, credit, commodity, FX, labour and utilities. SFS confirms provider posture and contracting owner. |
| Net-new SFS capture or governance | 9 | SFS confirms whether the workflow or master-data field exists. If not, SFS names the owner and approves capture. |

## 5. Recommended sequencing

| Sequence | Use cases | Why this comes here | Reusable foundation created |
|---|---|---|---|
| Wave 0: foundation | Shared data layer | Required for trust, speed and re-use | Raw landing, standard columnar layer, ID crosswalks, metric dictionary, access control, audit trail |
| Wave 1 build | Enterprise Assistant, Field Performance, Dealer Profiles | Strong SFS-owned data base and direct ROI alignment | Enterprise KPI mart, field performance mart, dealer 360, semantic SQL/chart/retrieval tools |
| Wave 1 discovery / Wave 2 build | Historical Spend | SAP purchase base is strong, but taxonomy and BPV require procurement sign-off | Spend cube, vendor/material dimensions, variance and anomaly framework |
| Wave 2 build | Product/Partner Visibility, Warehouse Stock, Scheme Chatbot, Churn Risk, Vendor ID | Mostly owned data, but requires definitions and source-owner validation | Product/partner mart, stock mart, scheme eligibility, churn labels, vendor scoring |
| External-data discovery | Negotiation Prep, Should-Cost, Import Analysis, Vendor Credit/Fraud | Depends on EXIM, commodity, GST, MCA, credit or litigation providers | External connector layer and provider governance |
| Discovery-only | Activity Analytics | SFS document gives a name but no detail. Field map is inferred and must be scoped with SFS. | Activity taxonomy and field workflow definition |
| Separate track | Logistics use cases | Buy-and-customise vendor/TMS track, not a custom AI build | Vendor fit-gap, shipment/POD/lane integration if SFS proceeds |

## 6. Integration vision

The architecture should make source-system access a shared foundation, not a one-off integration per use case.

1. Source read access: SAP BW / Power BI, SAP SD/MM/FI/Inventory, Growthbook, Saathi, Concur, Complinity, Ariba and approved external data providers.
2. Raw landing: store extracts exactly as received, partitioned by source and date, with run metadata.
3. Standard columnar layer: typed tables, data quality checks, ID crosswalks and refresh timestamps.
4. Gold semantic marts: dealer 360, field performance, enterprise KPIs, spend cube, stock visibility, vendor score, scheme eligibility and churn risk.
5. Governed agent tools: SQL over semantic views, retrieval over policy/circular documents, chart/report generation, audit logs and evaluation sets.

Agents should query governed semantic views. They should not connect directly to SAP, Concur, Saathi, Ariba or other source systems.

## 7. How we propose to extract data

| System | Preferred route | First ask | Owner needed |
|---|---|---|---|
| SAP BW / Power BI | Read-only extract from existing BW queries, Power BI semantic model or dataflow | Dataset inventory, data dictionary, sample export, refresh cadence and preserved join keys | SAP Basis/BW and Power BI owner |
| SAP SD | Existing BW sales/billing cube; fallback to S/4 CDS/OData or scheduled SD export | Sales/billing line extract with dealer, material, territory, date, quantity, value and pricing/scheme refs | SAP SD owner |
| SAP MM | Existing BW purchasing cube; fallback to S/4 CDS/OData or scheduled MM export | PO line extract with vendor, material, HSN, UoM, quantity, price, currency and GRN status | SAP MM owner |
| SAP FI/CO | Existing BW/Power BI finance model; fallback to controlled FI/CO export | Receivables, collections, ageing, GL/P&L and budget/target metrics at approved grain | Finance FI/CO owner |
| SAP Stock / Inventory | BW inventory cube or scheduled stock snapshot | On-hand stock, open orders, ATP if available and plant/warehouse mapping | SAP inventory/MM owner |
| Growthbook | API or event export | 12-month activity event export with employee ID, dealer ID, timestamp, activity type and outcome | Growthbook owner |
| Saathi | API/export from app DB | Dealer profile, visit notes, voice/call capture status, intervention logs and chatbot logs | Saathi owner plus legal/compliance |
| Concur | Concur API or scheduled expense export | Expense entries with amount, category, employee, cost centre, date and approval status | Concur owner |
| Complinity | API or scheduled vendor-compliance export | Vendor licence status, validity date, vendor ID and PAN/GSTIN if available | Complinity owner |
| Ariba | Ariba API/export | Supplier onboarding status, RFQ events, contracts and supplier-to-SAP-vendor mapping | Ariba owner |
| External data | Provider API/export | Existing subscriptions, provider shortlist, permitted use and contracting owner | External-data contracting plus legal |
| Logistics/TMS | Vendor/TMS export once source is known | Lane rates, shipment examples, POD examples and carrier status data | Logistics owner |

## 8. Exact first ask pack

| Owner | What they unblock | Exact ask for the working session | Use cases blocked until present |
|---|---|---|---|
| Executive sponsor | Cross-functional priority and decisions | Confirm the working-session mandate and nominate source owners | All |
| SFS IT lead | Access pattern and deployment constraints | Confirm target environment, security path and data-sharing mechanism | All |
| SAP Basis / BW / Power BI | SAP extraction route | Confirm read-only extract access off the existing SAP BW / Power BI layer | Enterprise, field, procurement and stock use cases |
| SAP SD owner | Sales, billing, dealer master and pricing | Provide masked sales/billing sample and pricing-condition availability | Field #1, #3, #4, #6, #8 and Enterprise |
| SAP MM owner | PO lines, vendor, material and inventory | Provide masked PO-line, vendor, material and stock samples | Procurement #1, #3, #4, #6 and Field #7 |
| SAP FI/CO owner | Receivables, collections and metric definitions | Provide collections/receivables sample and official metric definitions | Enterprise, Field #1 and Field #8 |
| Master Data / Governance | Crosswalks and hierarchies | Provide dealer/vendor/material/employee/HSN crosswalk ownership and product hierarchy decision process | Joined marts, Product/Partner Visibility, EXIM and Vendor ID |
| Growthbook / Saathi owners | Field activity and dealer interactions | Provide schemas, 12-month exports and voice/call capture status | Field #1, #2, #4, #5 and #8 |
| Concur / Complinity owners | Expense and vendor licence connectors | Provide export/API options and mapping owners | Procurement #1 and field expense views |
| Ariba owner | Supplier and RFQ workflow | Confirm rollout status, exports/APIs and supplier ID mapping | Procurement #3, #4 and #5 |
| External-data contracting | EXIM, commodity, GST, MCA, credit and litigation | Confirm existing subscriptions or approve provider selection | Procurement #2, #3, #5 and #6 |
| Legal / compliance | Risk data, voice capture and call recording | Confirm approval stance, consent, retention and classification rules | Procurement #5, Field #4 and Field #5 |
| Azure / security | VPC, SSO, audit, data residency and model gateway | Confirm approved tenant, logging, access groups and model path | All production agents |

## 9. Initial masked data pack

The first discovery sprint does not require production credentials. Masked samples are sufficient to validate schema, grain, data quality and join keys.

1. 36 months SAP purchase register at PO-line grain.
2. 36 months SAP primary sales and billing at invoice-line grain.
3. 24 to 36 months collections and receivables ageing.
4. Current material master, including hierarchy, HSN, UoM and active flag.
5. Current vendor master, including GSTIN, legal name, region, category and active flag.
6. Current customer/dealer master, including territory, credit terms, onboarding date and assigned field owner.
7. Field hierarchy: ZBM, RBM, TBM and MGO mapping.
8. Growthbook activity export for at least 12 months with SAP-matching dealer and employee IDs.
9. Target and incentive files by period and field role.
10. Scheme circular repository and active scheme list.
11. Inventory snapshot by plant, storage location and SKU.
12. Concur SG&A export and Complinity vendor-licence export.

## 10. Definition workshops required

Computed fields need business definitions before they can become trusted metrics. These are decision workshops, not integration work.

| Workshop | SFS owner needed | Defines | Unblocks |
|---|---|---|---|
| Enterprise metric dictionary | CFO/Controller plus Sales Ops | Revenue, margin, PBDIT, DSO, target attainment and metric ownership | Enterprise Assistant and every dashboard |
| Spend taxonomy and BPV rules | Procurement head and category managers | Category hierarchy, strategic classification, BPV logic and anomaly thresholds | Historical Spend, Vendor ID and Should-Cost |
| Product hierarchy | Master Data plus category owners | Unified cross-BU product hierarchy | Product/Partner Visibility and Enterprise Assistant |
| Partner scorecard and dealer tier | Sales Ops plus Field leadership | Dealer tier logic, scorecard formula and cross-sell rules | Field Performance, Dealer Profiles, Product Visibility and Churn |
| Churn and intervention logic | Sales Ops plus Finance/Collections | Churn definition, labels, intervention workflow and success criteria | Dealer Churn Risk |
| Scheme eligibility logic | Sales Ops plus scheme owner | Eligibility rules, source of truth and approval process | Scheme Chatbot |
| Negotiation outcome capture | Procurement category managers | Outcome logging workflow and learning loop | Negotiation Prep |

## 11. Use-case readiness table

| Use case | Fields | Available | Partial | Unavailable | Proposed treatment |
|---|---:|---:|---:|---:|---|
| Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales) | 18 | 8 | 4 | 6 | Wave 1 build candidate |
| Field Force #1 - Field Performance Tracking Dashboard | 20 | 13 | 4 | 3 | Wave 1 build candidate |
| Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app) | 20 | 12 | 4 | 4 | Wave 1 build candidate |
| Procurement #1 - Historical Spend Analysis & Price Insights | 26 | 11 | 6 | 9 | Wave 1 discovery, Wave 2 build candidate |
| Field Force #6 - Unified Product & Partner-Level Visibility | 15 | 8 | 2 | 5 | Wave 2 build candidate after foundation |
| Field Force #7 - Real-Time Warehouse Stock Visibility | 18 | 7 | 6 | 5 | Wave 2 build candidate after foundation |
| Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot | 14 | 3 | 4 | 7 | Wave 2 after source-owner validation |
| Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk | 19 | 7 | 2 | 10 | Wave 2 after source-owner validation |
| Procurement #4 - AI-Led Vendor Identification & Recommendation | 23 | 8 | 4 | 11 | Wave 2 after source-owner validation |
| Procurement #3 - AI-Driven Preparation Material for Negotiations | 21 | 5 | 3 | 13 | External-data discovery before build claim |
| Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | 17 | 4 | 2 | 11 | External-data discovery before build claim |
| Procurement #2 - Real-Time Import Data Analysis | 16 | 3 | 2 | 11 | Workshop-heavy; do not anchor Wave 1 |
| Procurement #5 - Vendor Creditworthiness & Fraud Check | 18 | 3 | 1 | 14 | Workshop-heavy; do not anchor Wave 1 |
| Field Force #5 - AI-Enabled Sales Coaching | 18 | 4 | 2 | 12 | Workshop-heavy; do not anchor Wave 1 |
| Field Force #2 - Activity Analytics (Growthbook + SAP) | 17 | 8 | 2 | 7 | Discovery-only; no build claim yet |

## 12. Detailed appendix: field-level asks

The tables below list every assumed field, its readiness status, likely source system, extraction route and concrete ask. Computed fields should not be requested from SFS as raw data. They need definitions and validation examples, after which Conformal computes them in the semantic layer.

### Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)

Fields: 18. Available: 8. Partial: 4. Unavailable: 6. Treatment: Wave 1 build candidate.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| SAP - Financials Extracts (Working Capital / Receivables / GL) | Available | SAP - Financials (GL/P&L) | Primary route: SAP BW / FI-CO extract or controlled receivables and GL export at approved grain. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Target (TBM x SKU x Period) | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardise owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Definition | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardise owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Assistant Query Log | Unavailable | Conversational AI Surface | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| 'What Changed' Weekly Digest | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Enterprise Metrics Dictionary | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Spend Category Tag | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Product Hierarchy (Cross-BU Unified) | Unavailable | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm whether field exists in SAP master/transaction layer; if not, name master-data owner or alternate source. |

### Field Force #1 - Field Performance Tracking Dashboard

Fields: 20. Available: 13. Partial: 4. Unavailable: 3. Treatment: Wave 1 build candidate.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Name | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit of Measure (UoM) | Available | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Order Date | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Order Number | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| TBM ID / Sales Rep Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Target (TBM x SKU x Period) | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardise owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Definition | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardise owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Channel Stock Estimate (Primary - Secondary) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Early-Warning Alert Flag (Trending Below Target) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Target Attainment % (Period-to-Date) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |

### Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)

Fields: 20. Available: 12. Partial: 4. Unavailable: 4. Treatment: Wave 1 build candidate.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer GSTIN | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Name | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Onboarding Date | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Last Visit Timestamp | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Geo-Location (Lat / Lng) | Partial | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Relationship Profile (Structured) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Key Contacts | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |
| Dealer Voice Capture (Saathi) | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |

### Procurement #1 - Historical Spend Analysis & Price Insights

Fields: 26. Available: 11. Partial: 6. Unavailable: 9. Treatment: Wave 1 discovery, Wave 2 build candidate.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Unit of Measure (UoM) | Available | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Line Item Value (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Material Code (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Number | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Plant / Region (on PO) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor ID (on PO) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor GSTIN | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor License Status | Partial | Complinity | Complinity API or scheduled vendor-compliance export; map vendor ID, PAN/GSTIN and validity dates. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor License Validity Date | Partial | Complinity | Complinity API or scheduled vendor-compliance export; map vendor ID, PAN/GSTIN and validity dates. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| SG&A Expense Amount | Partial | Concur | Concur API or scheduled expense export; map employee, cost centre, category and date to SAP dimensions. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| SG&A Expense Category | Partial | Concur | Concur API or scheduled expense export; map employee, cost centre, category and date to SAP dimensions. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| BPV Gap | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Best Price Vendor (BPV) per SKU | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Price Variance (SKU x Vendor x Time) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Product Category Hierarchy | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Spend Anomaly Flag | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Spend Category Tag | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Spend Sub-Category Tag | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Strategic Spend Classification | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Commodity Price Index | Unavailable | Commodity Price Provider | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |

### Field Force #6 - Unified Product & Partner-Level Visibility

Fields: 15. Available: 8. Partial: 2. Unavailable: 5. Treatment: Wave 2 build candidate after foundation.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Name | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit of Measure (UoM) | Available | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Cross-Sell Opportunity Score (per Dealer x BU) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Cross-BU Revenue Aggregation | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Product Launch Cross-BU Impact Analysis | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Product Hierarchy (Cross-BU Unified) | Unavailable | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm whether field exists in SAP master/transaction layer; if not, name master-data owner or alternate source. |

### Field Force #7 - Real-Time Warehouse Stock Visibility

Fields: 18. Available: 7. Partial: 6. Unavailable: 5. Treatment: Wave 2 build candidate after foundation.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit of Measure (UoM) | Available | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Order Date | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Stock Quantity (per SKU x Warehouse) | Available | SAP - Stock / Inventory | Primary route: BW inventory cube or scheduled stock snapshot by plant, warehouse, SKU and date. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Warehouse / Plant Code | Available | SAP - Stock / Inventory | Primary route: BW inventory cube or scheduled stock snapshot by plant, warehouse, SKU and date. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| In-Transit Stock | Partial | Logistics System | TMS/vendor export or fit-gap track; do not custom-build until source system/vendor is selected. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor / External Warehouse Stock | Partial | Vendor / External Warehouse System | TMS/vendor export or fit-gap track; do not custom-build until source system/vendor is selected. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Geo-Location (Lat / Lng) | Partial | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Stock Batch / Expiry Date (per SKU x Warehouse x Batch) | Partial | SAP - Stock / Inventory | Primary route: BW inventory cube or scheduled stock snapshot by plant, warehouse, SKU and date. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Warehouse Location (Lat / Lng) | Partial | SAP - Stock / Inventory | Primary route: BW inventory cube or scheduled stock snapshot by plant, warehouse, SKU and date. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Expiry-Risk Stock View | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Low-Stock Alert Flag (per SKU x Warehouse) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Recommended Source Warehouse (per Order) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Stock Source Freshness / Staleness Indicator | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| SKU Substitution Mapping | Unavailable | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm whether field exists in SAP master/transaction layer; if not, name master-data owner or alternate source. |

### Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot

Fields: 14. Available: 3. Partial: 4. Unavailable: 7. Treatment: Wave 2 after source-owner validation.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Scheme Circular Document | Available | Internal Docs (PDF / Circulars) | Central circular/PDF repository; ingest with metadata, version, applicability and owner. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Definition | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardise owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Chatbot Answer Confidence Score | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Circular Ambiguity Detection | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Discount Calculation (per Dealer x Scheme x Quantity) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Scheme Eligibility Result (per Dealer x Scheme) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Top Scheme Questions (Aggregated) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Chatbot Query Log | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |

### Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk

Fields: 19. Available: 7. Partial: 2. Unavailable: 10. Treatment: Wave 2 after source-owner validation.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer GSTIN | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Last Visit Timestamp | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Call Type Classification | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Churn Risk Factor Breakdown | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Churn Risk Score | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Relationship Profile (Structured) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Sales Decline Trajectory (per Dealer) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Target Attainment % (Period-to-Date) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer GST Default Flag | Unavailable | GST Portal (via GSP) | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Dealer GSTIN Registration Status | Unavailable | GST Portal (via GSP) | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Intervention Tracking Log | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |

### Procurement #4 - AI-Led Vendor Identification & Recommendation

Fields: 23. Available: 8. Partial: 4. Unavailable: 11. Treatment: Wave 2 after source-owner validation.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| GRN Quantity Received | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| GRN Receipt Date | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Material Code (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor GSTIN | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor PAN | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| GRN Quality Rejection Quantity | Partial | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Composite Vendor Risk Score | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Per-Vendor Pricing Pattern | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Vendor Capacity Signal | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Vendor Composite Performance Score | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Vendor Risk Tier | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| EXIM Country of Origin | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Commercial Credit Score | Unavailable | Credit Bureau | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| GSTIN Registration Status | Unavailable | GST Portal (via GSP) | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| MCA Company Status | Unavailable | MCA21 | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Ariba RFQ Trigger Event | Unavailable | Ariba | Ariba export/API for supplier onboarding, RFQs and contracts; map supplier IDs to SAP vendor IDs. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |

### Procurement #3 - AI-Driven Preparation Material for Negotiations

Fields: 21. Available: 5. Partial: 3. Unavailable: 13. Treatment: External-data discovery before build claim.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Material Code (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Number | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| AI-Generated Negotiation Brief | Unavailable | Conversational AI Surface | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Negotiation Outcome Log | Unavailable | Conversational AI Surface | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Buyer Price Variance (Same SKU x Period) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Per-Vendor Pricing Pattern | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Recommended Target Price | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Seasonal Buy Pattern per Commodity | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Commodity Price Index | Unavailable | Commodity Price Provider | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Country of Origin | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Exporter / Global Supplier | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Agri Commodity / MSP Index | Unavailable | Macro Indicators (Public) | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Crude Oil / Diesel Price Index | Unavailable | Macro Indicators (Public) | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| USD/INR FX Rate | Unavailable | Macro Indicators (Public) | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |

### Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products)

Fields: 17. Available: 4. Partial: 2. Unavailable: 11. Treatment: External-data discovery before build claim.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Unit of Measure (UoM) | Available | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Cost Build-Up Template per Commodity | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Input Cost Pass-Through Coefficient | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Should-Cost Gap (Actual vs. Target) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Should-Cost Target Price (per SKU) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| EXIM Exporter / Global Supplier | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Industrial Electricity Tariff (Region) | Unavailable | Energy / Utility Rate Source | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Labor Rate Benchmark (Region x Skill Tier) | Unavailable | Industry / Labor Benchmarks | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Manufacturing Overhead Benchmark | Unavailable | Industry / Labor Benchmarks | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Agri Commodity / MSP Index | Unavailable | Macro Indicators (Public) | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Crude Oil / Diesel Price Index | Unavailable | Macro Indicators (Public) | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| USD/INR FX Rate | Unavailable | Macro Indicators (Public) | External provider API/export; confirm provider, terms, refresh, identifiers and history. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |

### Procurement #2 - Real-Time Import Data Analysis

Fields: 16. Available: 3. Partial: 2. Unavailable: 11. Treatment: Workshop-heavy; do not anchor Wave 1.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Material Code (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| EXIM Benchmark Deviation Alert | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Largest Importers per HSN | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Top Source Countries per HSN | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Trader Premium per SKU | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| EXIM Country of Origin | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Exporter / Global Supplier | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM HSN Code | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Import Quantity | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Importer Name | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| EXIM Transaction Date | Unavailable | EXIM Data Provider | External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |

### Procurement #5 - Vendor Creditworthiness & Fraud Check

Fields: 18. Available: 3. Partial: 1. Unavailable: 14. Treatment: Workshop-heavy; do not anchor Wave 1.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Vendor GSTIN | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor PAN | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Name | Partial | SAP - Vendor Master | Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Composite Vendor Risk Score | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Vendor Risk Tier | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Insolvency / NCLT Filings | Unavailable | Court / Litigation Records | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Litigation Records | Unavailable | Court / Litigation Records | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Commercial Credit Score | Unavailable | Credit Bureau | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Credit Default History | Unavailable | Credit Bureau | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| GST Default Flag | Unavailable | GST Portal (via GSP) | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| GST Return Filing History | Unavailable | GST Portal (via GSP) | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| GSTIN Registration Status | Unavailable | GST Portal (via GSP) | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| MCA Charges / Encumbrances | Unavailable | MCA21 | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| MCA Company Status | Unavailable | MCA21 | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| MCA Directors / Beneficial Owners | Unavailable | MCA21 | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| MCA Incorporation Date | Unavailable | MCA21 | Approved external risk provider/API; requires legal sign-off and entity-resolution keys. | Confirm existing provider or nominate contracting owner and approve provider shortlist. |
| Vendor Onboarding Workflow Status | Unavailable | Ariba | Ariba export/API for supplier onboarding, RFQs and contracts; map supplier IDs to SAP vendor IDs. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |

### Field Force #5 - AI-Enabled Sales Coaching

Fields: 18. Available: 4. Partial: 2. Unavailable: 12. Treatment: Workshop-heavy; do not anchor Wave 1.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| TBM ID / Sales Rep Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| TBM Visit Log | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| AI-Generated Coaching Recommendation | Unavailable | Conversational AI Surface | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Activity-Outcome Correlation | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Call Type Classification | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Conversation Quality Framework | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Relationship Profile (Structured) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Peer Benchmark (Anonymized Cohort) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| TBM Conversation Quality Score (per Dimension) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| TBM Time Allocation Analysis | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Target Attainment % (Period-to-Date) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Coaching Action Item Tracking | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |
| Dealer Voice Capture (Saathi) | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |

### Field Force #2 - Activity Analytics (Growthbook + SAP)

Fields: 17. Available: 8. Partial: 2. Unavailable: 7. Treatment: Discovery-only; no build claim yet.

| Field | Status | Source system | Route | Ask |
|---|---|---|---|---|
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| TBM ID / Sales Rep Code | Available | SAP - Sales & Distribution | Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Last Visit Timestamp | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| TBM Visit Log | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Activity-Outcome Correlation | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Call Type Classification | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Coverage % (Tier-Weighted) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| TBM Time Allocation Analysis | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| TBM Visit Count (Period) | Unavailable | Internal Computed / Derived | Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples. | No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it. |
| Dealer Voice Capture (Saathi) | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture and name owner. |
