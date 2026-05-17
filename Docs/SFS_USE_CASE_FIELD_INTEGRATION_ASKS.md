# SFS Project Leap - Use Case Field, Integration, and Ask Pack

Last updated: May 18, 2026

## Purpose

This is the working technical ask document for the next SFS conversation. It translates the 146 assumed data fields into: which use case needs which fields, which systems likely hold those fields, what is available versus missing, how we should extract the data, and what exact asks we need from the SFS team to begin.

Important caveat: this is still Conformal's structured hypothesis from SFS's ODS and Sidd's field mapping. The first SFS workshop should validate source ownership, schema, history, refresh, join keys and capture gaps before we price or promise every use case.

## Executive Read

- Keep the headline count, but change how it is explained: 146 fields mapped; 33 available, 19 partial, 94 unavailable.
- The real story is better than the raw unavailable number: 58 unavailable fields are computed in our semantic layer once base data lands; 27 need external providers; the remaining gaps are source access, ID mapping, workflow capture or business definition.
- The first build should not be 21 independent use cases. It should be a shared data foundation plus the use cases that exercise the most reusable base marts.
- Recommended first technical slices: SAP BW / Power BI sales-dealer-targets, Growthbook/Saathi field activity and dealer interactions, SAP MM purchase-vendor-material. These create the base for later field-force, procurement, churn, scheme and enterprise assistant work.

## Recommended Triage

| Decision | Use cases | Why | What foundation it creates |
|---|---|---|---|
| Wave 0: data foundation | No business use case alone | Required for trust, repeatability and speed | Raw landing, standardized columnar tables, ID crosswalks, metric dictionary, role-aware agent tools |
| Wave 1 build | Enterprise Assistant #1, Field Force #1, Field Force #4 | Strongest mix of SFS ROI and data readiness | Enterprise KPI mart, field-performance mart, dealer 360, reusable SQL/chart/retrieval agent tools |
| Wave 1 discovery / Wave 2 build | Procurement #1 Historical Spend | SAP purchase base is strong, but taxonomy/BPV needs procurement sign-off | Spend cube, vendor/material dimensions, price variance and anomaly framework |
| Wave 2 build | Field Force #6, #7, #3, #8; Procurement #4 | Mostly owned data plus definitions/integration | Product/partner mart, stock mart, scheme eligibility, churn labels, vendor scoring |
| Tier 2.5 discovery | Procurement #3 Negotiation Prep, Procurement #6 Should-Cost | Heavy external-market and category assumptions | External data connectors and category cost models reusable across procurement suite |
| Workshop-heavy / later | Procurement #2, #5; Field Force #5; Field Force #2 | External/legal/capture dependencies or ODS lacks detail | Risk provider layer, voice/call capture governance, activity taxonomy |
| Separate track | Logistics #1-#5 | Buy-and-customize vendor/TMS track, not custom agent build | Vendor fit-gap, lane/shipment/POD integration if SFS proceeds |

## Integration Vision

The architecture should make source-system access a foundation, not a one-off integration per use case.

1. Source read access: SAP BW / Power BI, SAP SD/MM/FI/Inventory, Growthbook, Saathi, Concur, Complinity, Ariba, external data providers.
2. Raw landing: store extracts exactly as received, partitioned by source and date, with file/run metadata.
3. Standard columnar layer: typed Parquet/Delta tables, data quality checks, ID crosswalks, refresh timestamps.
4. Gold marts: dealer 360, field performance, enterprise KPIs, spend cube, stock visibility, vendor score, scheme eligibility, churn risk.
5. Governed agent tools: SQL over semantic views, retrieval over circulars/docs, chart/report generation, audit logs and golden-question evals.

Agent rule: agents should query governed views, not SAP, Concur, Saathi or Ariba directly.

## How We Get Data Out Of Each System

| System | Preferred route | Fallback route | First extract to ask for | Owner needed |
|---|---|---|---|---|
| SAP BW / Power BI | Read-only export from existing BW queries / Power BI semantic layer or dataflows | If line-level columns are missing, go to SAP module owner for S/4 CDS/OData or scheduled flat-file export | Dataset inventory, data dictionary, sample export, refresh cadence, preserved join keys | SAP Basis/BW + Power BI owner |
| SAP SD | Existing BW sales/billing cube | S/4 read-only CDS/OData or scheduled SD export | Sales order/billing line with dealer, material, plant, territory, date, quantity, value, pricing/scheme refs | SAP SD owner |
| SAP MM | Existing BW procurement/purchase cube | S/4 read-only CDS/OData or scheduled MM export | PO line, vendor, material, HSN, UoM, quantity, price, currency, GRN/receipt status | SAP MM owner |
| SAP FI/CO | Existing BW/Power BI finance model | Controlled FI/CO export at approved grain | Receivables, collections, ageing, GL/P&L, budget/target metrics | Finance FI/CO owner |
| SAP Stock / Inventory | BW inventory cube or stock snapshot job | Scheduled stock extract by plant/warehouse/SKU/date | On-hand stock, open orders, ATP if available, plant/warehouse mapping | SAP inventory/MM owner |
| Growthbook | API or event export | Database/file export for discovery | Activity events by employee/dealer/timestamp/type/outcome | Growthbook owner |
| Saathi | API/export from app DB | Controlled CSV extract for discovery | Dealer profile, visit notes, voice/call capture status, intervention logs, chatbot logs | Saathi owner + legal/compliance |
| Concur | Concur API or scheduled expense export | Monthly file export | Expense entries with amount/category/employee/cost center/date/status | Concur owner |
| Complinity | API or scheduled vendor-compliance export | Monthly file export | Vendor license status, validity date, vendor identifier, PAN/GSTIN if available | Complinity owner |
| Ariba | Ariba API/export | Manual RFQ/supplier export for discovery | Supplier onboarding status, RFQ events, contract/supplier IDs | Ariba owner |
| External market data | Provider API/export | Initial CSV sample from selected provider | EXIM, commodity, FX, fuel, labor, utility benchmark fields | External-data contracting owner |
| External risk/compliance | GSP/MCA/credit/litigation provider API/export | Provider sample export | GST, MCA21, credit, litigation, NCLT/insolvency fields | External-data contracting + legal |
| Logistics/TMS | Vendor/TMS export once vendor/source is known | Manual shipment/lane/POD samples | Lane rates, shipments, POD, carrier, in-transit status | Logistics owner |

## Exact First Ask Pack

| Owner | What they unblock | Exact ask for the next working session | Use cases blocked until this owner joins |
|---|---|---|---|
| SAP Basis / BW / Power BI | SAP BW datasets, Power BI semantic models, service users, extraction schedules | SAP BW/Power BI dataset inventory; read-only export for SD, MM, FI/CO, inventory, targets; data dictionary; last refresh timestamps | Enterprise, Field #1/#4/#6/#7/#8, Procurement #1/#3/#4/#6 |
| SAP SD owner | Sales orders, billing, dealer/customer master, pricing conditions, territory and primary-sales grain | 24-36 months line-level sales/billing sample with dealer ID, material code, plant/warehouse, date, qty, value, scheme/pricing refs; confirm CDS/OData or BW route | Field #1/#3/#4/#6/#8, Enterprise |
| SAP MM owner | PO lines, GRN, vendor master, material master, HSN, UoM, stock links | 36 months PO-line extract, vendor master, material master, HSN/material map, UoM conversion rules, GRN/receipt status | Procurement #1/#3/#4/#6, Field #7 |
| SAP FI/CO owner | Collections, receivables, GL/P&L, budgets, working capital metrics | Receivables/collections sample by dealer, ageing buckets, GL/P&L extract at approved aggregation, official metric definitions | Enterprise, Field #1/#8 |
| Master Data / Governance | Dealer/vendor/material/employee/HSN crosswalks and cross-BU product hierarchy | Authoritative ID crosswalk files, ownership for duplicates, hierarchy definition, change-management cadence | All joined marts; especially Product/Partner Visibility, EXIM, Vendor ID |
| Growthbook owner | Field activity events and visit tracking | 12-month event export/API docs with employee ID, dealer ID, activity type, timestamp, outcome, geo if approved | Field #1/#2/#4/#5/#8 |
| Saathi owner | Dealer profile, field visit notes, voice/call capture, chatbot logs, intervention logs | Schema/export for dealer profile and notes; confirm whether voice capture/call recording is live, planned, or prohibited | Field #2/#3/#4/#5/#8 |
| Concur owner | SG&A and T&E expense fields | Expense report/entry export with amount, category, employee, cost center, date, approval status; SAP cost-center mapping | Procurement #1, Field Performance expense views |
| Complinity owner | Vendor license/compliance status and validity | Vendor license export/API with vendor ID, PAN/GSTIN, license status, validity date, compliance category | Procurement #1 and vendor compliance views |
| Ariba owner | RFQ, supplier onboarding, supplier workflow status | Ariba rollout status; supplier/RFQ/contract export; supplier-to-SAP-vendor mapping | Procurement #3/#4/#5 |
| External data contracting owner | EXIM, commodity, GST/GSP, MCA21, credit, litigation, labor/utility providers | List existing subscriptions; approve provider shortlist and commercial owner; confirm allowed usage inside analytics/AI product | Procurement #2/#3/#5/#6, Vendor ID |
| Legal / compliance | Risk data, dealer voice capture, call recording/classification, privacy approvals | Approval stance for GST/MCA/credit/litigation use, dealer voice/call recording, retention, consent and access controls | Procurement #5, Field #4/#5 |
| Logistics owner | TMS/vendor fit-gap, shipment/POD/lane/rate data | TMS shortlist, shipment/rate/POD samples, carrier data availability; keep as buy-and-customize track | All 5 logistics use cases |
| Azure / Security owner | Landing zone, SSO, VPC/network, audit, model gateway | Approved tenant/subscription, storage/account pattern, SSO groups, logging/audit, data residency, model access policy | All production agents |

## Data That Is Not Captured Or Cannot Be Computed Internally

These fields should not be hand-waved as AI. They either need a third-party provider, a workflow change, or a governance decision.

- External provider fields: 27. These cannot be computed reliably from SFS internal data.
- Net-new/internal capture or master-data fields: 9. These need workflow, master-data or app-owner decisions.
- Computed fields: 58. These are not raw-data asks; they need definitions, formulas, owners and validation examples.

### External Provider Fields

| Field | Source | Use cases | Ask |
|---|---|---|---|
| Commodity Price Index | Commodity Price Provider | Procurement #1 - Historical Spend Analysis & Price Insights; Procurement #3 - AI-Driven Preparation Material for Negotiations | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Transaction Date | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM HSN Code | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Importer Name | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Import Quantity | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis; Procurement #3 - AI-Driven Preparation Material for Negotiations; Procurement #4 - AI-Led Vendor Identification & Recommendation | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Country of Origin | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis; Procurement #3 - AI-Driven Preparation Material for Negotiations; Procurement #4 - AI-Led Vendor Identification & Recommendation | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Exporter / Global Supplier | EXIM Data Provider | Procurement #2 - Real-Time Import Data Analysis; Procurement #3 - AI-Driven Preparation Material for Negotiations; Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| USD/INR FX Rate | Macro Indicators (Public) | Procurement #3 - AI-Driven Preparation Material for Negotiations; Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Agri Commodity / MSP Index | Macro Indicators (Public) | Procurement #3 - AI-Driven Preparation Material for Negotiations; Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Crude Oil / Diesel Price Index | Macro Indicators (Public) | Procurement #3 - AI-Driven Preparation Material for Negotiations; Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Credit Default History | Credit Bureau | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Company Status | MCA21 | Procurement #5 - Vendor Creditworthiness & Fraud Check; Procurement #4 - AI-Led Vendor Identification & Recommendation | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GST Return Filing History | GST Portal (via GSP) | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GST Default Flag | GST Portal (via GSP) | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Charges / Encumbrances | MCA21 | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Insolvency / NCLT Filings | Court / Litigation Records | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Commercial Credit Score | Credit Bureau | Procurement #5 - Vendor Creditworthiness & Fraud Check; Procurement #4 - AI-Led Vendor Identification & Recommendation | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Incorporation Date | MCA21 | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GSTIN Registration Status | GST Portal (via GSP) | Procurement #5 - Vendor Creditworthiness & Fraud Check; Procurement #4 - AI-Led Vendor Identification & Recommendation | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Directors / Beneficial Owners | MCA21 | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Litigation Records | Court / Litigation Records | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Labor Rate Benchmark (Region x Skill Tier) | Industry / Labor Benchmarks | Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Manufacturing Overhead Benchmark | Industry / Labor Benchmarks | Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Industrial Electricity Tariff (Region) | Energy / Utility Rate Source | Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products) | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Dealer GSTIN Registration Status | GST Portal (via GSP) | Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Dealer GST Default Flag | GST Portal (via GSP) | Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |

### Net-New Capture / Internal Master-Data Fields

| Field | Source | Use cases | Ask |
|---|---|---|---|
| Vendor Onboarding Workflow Status | Ariba | Procurement #5 - Vendor Creditworthiness & Fraud Check | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Ariba RFQ Trigger Event | Ariba | Procurement #4 - AI-Led Vendor Identification & Recommendation | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Dealer Voice Capture (Saathi) | Saathi App | Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app); Field Force #2 - Activity Analytics (Growthbook + SAP); Field Force #5 - AI-Enabled Sales Coaching | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Dealer Key Contacts | Saathi App | Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app) | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Chatbot Query Log | Saathi App | Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Coaching Action Item Tracking | Saathi App | Field Force #5 - AI-Enabled Sales Coaching | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Product Hierarchy (Cross-BU Unified) | SAP - Material Master | Field Force #6 - Unified Product & Partner-Level Visibility; Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales) | Confirm whether field exists in SAP master/transaction table; if not, define master-data owner or alternate source. |
| SKU Substitution Mapping | SAP - Material Master | Field Force #7 - Real-Time Warehouse Stock Visibility | Confirm whether field exists in SAP master/transaction table; if not, define master-data owner or alternate source. |
| Intervention Tracking Log | Saathi App | Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

## Use-Case Deep Dive

### Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)

- Decision: Pick first / Wave 1 build
- Readiness: Strong pilot / definition work
- Field count: 18 total; 8 available, 4 partial, 6 unavailable.
- Systems needed: Internal Computed / Derived (4), SAP - Sales & Distribution (3), SAP - Customer / Dealer Master (3), SAP - Vendor Master (2), Excel - Targets / Schemes (2), Growthbook (1), SAP - Material Master (1), Conversational AI Surface (1), SAP - Financials (GL/P&L) (1)
- Source groups: SAP 10, Computed / Derived 5, Internal Apps 3
- Caveat: Strong Wave 1 if scoped to confirmed SAP BW / Power BI extracts and metric dictionary.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| SAP - Financials Extracts (Working Capital / Receivables / GL) | Available | SAP - Financials (GL/P&L) | SAP BW/FI-CO extract or controlled GL/receivables export; avoid direct ledger access in phase 1. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Target (TBM x SKU x Period) | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardize owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Definition | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardize owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Assistant Query Log | Unavailable | Conversational AI Surface | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| 'What Changed' Weekly Digest | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Enterprise Metrics Dictionary | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Spend Category Tag | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Product Hierarchy (Cross-BU Unified) | Unavailable | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm whether field exists in SAP master/transaction table; if not, define master-data owner or alternate source. |

### Field Force #1 - Field Performance Tracking Dashboard

- Decision: Pick first / Wave 1 build
- Readiness: Fast start / descriptive base
- Field count: 20 total; 13 available, 4 partial, 3 unavailable.
- Systems needed: SAP - Sales & Distribution (6), SAP - Customer / Dealer Master (4), Internal Computed / Derived (3), SAP - Material Master (2), Growthbook (2), Excel - Targets / Schemes (2), Saathi App (1)
- Source groups: SAP 12, Internal Apps 5, Computed / Derived 3
- Caveat: Fast descriptive base; liquidation and secondary-sales completeness require new SFS capture.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Name | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit of Measure (UoM) | Available | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Order Date | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Order Number | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| TBM ID / Sales Rep Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Target (TBM x SKU x Period) | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardize owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Definition | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardize owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Channel Stock Estimate (Primary Secondary) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Early-Warning Alert Flag (Trending Below Target) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Target Attainment % (Period-to-Date) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |

### Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)

- Decision: Pick first / Wave 1 build
- Readiness: Fast start / descriptive base
- Field count: 20 total; 12 available, 4 partial, 4 unavailable.
- Systems needed: SAP - Customer / Dealer Master (9), Saathi App (4), SAP - Sales & Distribution (3), Growthbook (2), Internal Computed / Derived (2)
- Source groups: SAP 12, Internal Apps 6, Computed / Derived 2
- Caveat: Strong dealer/SAP base; relationship intelligence and voice capture need workflow validation.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer GSTIN | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Name | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Onboarding Date | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Last Visit Timestamp | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Geo-Location (Lat / Lng) | Partial | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Relationship Profile (Structured) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Key Contacts | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Dealer Voice Capture (Saathi) | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

### Procurement #1 - Historical Spend Analysis & Price Insights

- Decision: Wave 1 discovery, Wave 2 build candidate
- Readiness: Strong pilot / definition work
- Field count: 26 total; 11 available, 6 partial, 9 unavailable.
- Systems needed: SAP - Purchase Register (8), Internal Computed / Derived (8), SAP - Vendor Master (3), SAP - Material Master (2), Concur (2), Complinity (2), Commodity Price Provider (1)
- Source groups: SAP 13, Computed / Derived 8, Internal Apps 4, External (Market Data) 1
- Caveat: SAP purchase base is strong; taxonomy, BPV and anomaly rules need procurement workshops.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Unit of Measure (UoM) | Available | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Line Item Value (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Material Code (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Number | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Plant / Region (on PO) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor ID (on PO) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor GSTIN | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor License Status | Partial | Complinity | Complinity API or scheduled vendor-compliance export; map vendor ID, PAN/GSTIN and validity dates. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor License Validity Date | Partial | Complinity | Complinity API or scheduled vendor-compliance export; map vendor ID, PAN/GSTIN and validity dates. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| SG&A Expense Amount | Partial | Concur | Concur API or scheduled expense export; map employee, cost center, category and date to SAP dimensions. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| SG&A Expense Category | Partial | Concur | Concur API or scheduled expense export; map employee, cost center, category and date to SAP dimensions. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| BPV Gap | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Best Price Vendor (BPV) per SKU | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Price Variance (SKU x Vendor x Time) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Product Category Hierarchy | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Spend Anomaly Flag | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Spend Category Tag | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Spend Sub-Category Tag | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Strategic Spend Classification | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Commodity Price Index | Unavailable | Commodity Price Provider | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |

### Field Force #6 - Unified Product & Partner-Level Visibility

- Decision: Wave 2 build candidate after foundation
- Readiness: Strong pilot / definition work
- Field count: 15 total; 8 available, 2 partial, 5 unavailable.
- Systems needed: SAP - Customer / Dealer Master (5), Internal Computed / Derived (4), SAP - Material Master (3), SAP - Sales & Distribution (2), Growthbook (1)
- Source groups: SAP 10, Computed / Derived 4, Internal Apps 1
- Caveat: Strong SAP base; secondary-sales, liquidation and PoG-led intelligence need new capture.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Secondary Sales Transaction | Available | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Name | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit of Measure (UoM) | Available | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Cross-Sell Opportunity Score (per Dealer x BU) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Cross-BU Revenue Aggregation | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Product Launch Cross-BU Impact Analysis | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Product Hierarchy (Cross-BU Unified) | Unavailable | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm whether field exists in SAP master/transaction table; if not, define master-data owner or alternate source. |

### Field Force #7 - Real-Time Warehouse Stock Visibility

- Decision: Wave 2 build candidate after foundation
- Readiness: Strong pilot / definition work
- Field count: 18 total; 7 available, 6 partial, 5 unavailable.
- Systems needed: SAP - Stock / Inventory (4), Internal Computed / Derived (4), SAP - Material Master (3), SAP - Customer / Dealer Master (3), SAP - Purchase Register (1), SAP - Sales & Distribution (1), Logistics System (1), Vendor / External Warehouse System (1)
- Source groups: SAP 12, Computed / Derived 4, Logistics 2
- Caveat: SAP stock is likely available; vendor warehouse, in-transit, substitution and freshness need validation.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit of Measure (UoM) | Available | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Order Date | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Stock Quantity (per SKU x Warehouse) | Available | SAP - Stock / Inventory | SAP BW inventory cube or scheduled stock snapshot export; confirm plant/warehouse/SKU/date grain. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Warehouse / Plant Code | Available | SAP - Stock / Inventory | SAP BW inventory cube or scheduled stock snapshot export; confirm plant/warehouse/SKU/date grain. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| In-Transit Stock | Partial | Logistics System | TMS/vendor export or fit-gap track; do not custom-build until source system/vendor is selected. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor / External Warehouse Stock | Partial | Vendor / External Warehouse System | TMS/vendor export or fit-gap track; do not custom-build until source system/vendor is selected. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Geo-Location (Lat / Lng) | Partial | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Stock Batch / Expiry Date (per SKU x Warehouse x Batch) | Partial | SAP - Stock / Inventory | SAP BW inventory cube or scheduled stock snapshot export; confirm plant/warehouse/SKU/date grain. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Warehouse Location (Lat / Lng) | Partial | SAP - Stock / Inventory | SAP BW inventory cube or scheduled stock snapshot export; confirm plant/warehouse/SKU/date grain. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Expiry-Risk Stock View | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Low-Stock Alert Flag (per SKU x Warehouse) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Recommended Source Warehouse (per Order) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Stock Source Freshness / Staleness Indicator | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| SKU Substitution Mapping | Unavailable | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm whether field exists in SAP master/transaction table; if not, define master-data owner or alternate source. |

### Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot

- Decision: Wave 2 after source-owner validation
- Readiness: Moderate integration work
- Field count: 14 total; 3 available, 4 partial, 7 unavailable.
- Systems needed: Internal Computed / Derived (6), SAP - Customer / Dealer Master (3), SAP - Material Master (1), Growthbook (1), Excel - Targets / Schemes (1), Saathi App (1), Internal Docs (PDF / Circulars) (1)
- Source groups: Computed / Derived 6, SAP 4, Internal Apps 4
- Caveat: Circulars, pricing conditions and eligibility rules must be structured.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Scheme Circular Document | Available | Internal Docs (PDF / Circulars) | Central document repository for circulars/PDFs; ingest with metadata, version, applicability and owner. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Definition | Partial | Excel - Targets / Schemes | Controlled file repository or SharePoint/Drive drop; standardize owner, version, period and upload cadence. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer BU Presence | Partial | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Chatbot Answer Confidence Score | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Circular Ambiguity Detection | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Discount Calculation (per Dealer x Scheme x Quantity) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Scheme Eligibility Result (per Dealer x Scheme) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Top Scheme Questions (Aggregated) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Chatbot Query Log | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

### Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk

- Decision: Wave 2 after source-owner validation
- Readiness: Moderate integration work
- Field count: 19 total; 7 available, 2 partial, 10 unavailable.
- Systems needed: Internal Computed / Derived (7), SAP - Customer / Dealer Master (4), Saathi App (3), SAP - Sales & Distribution (2), GST Portal (via GSP) (2), Growthbook (1)
- Source groups: Computed / Derived 7, SAP 6, Internal Apps 4, External (Risk/Compliance) 2
- Caveat: Churn definition, intervention tracking and risk labels needed. Field count is 19 after removing BPV Gap.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Credit Terms | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer GSTIN | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Dealer Last Visit Timestamp | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Call Type Classification | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Churn Risk Factor Breakdown | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Churn Risk Score | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Relationship Profile (Structured) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Sales Decline Trajectory (per Dealer) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Target Attainment % (Period-to-Date) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer GST Default Flag | Unavailable | GST Portal (via GSP) | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Dealer GSTIN Registration Status | Unavailable | GST Portal (via GSP) | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Intervention Tracking Log | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

### Procurement #4 - AI-Led Vendor Identification & Recommendation

- Decision: Wave 2 after source-owner validation
- Readiness: Moderate integration work
- Field count: 23 total; 8 available, 4 partial, 11 unavailable.
- Systems needed: SAP - Purchase Register (6), Internal Computed / Derived (5), SAP - Vendor Master (4), SAP - Material Master (2), EXIM Data Provider (2), MCA21 (1), Credit Bureau (1), GST Portal (via GSP) (1), Ariba (1)
- Source groups: SAP 12, Computed / Derived 5, External (Risk/Compliance) 3, External (Market Data) 2, Internal Apps 1
- Caveat: Keep in Tier 2 because the owned internal base can start; external signals improve the recommendation layer.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| GRN Quantity Received | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| GRN Receipt Date | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Material Code (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor GSTIN | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor PAN | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| GRN Quality Rejection Quantity | Partial | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Composite Vendor Risk Score | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Per-Vendor Pricing Pattern | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Vendor Capacity Signal | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Vendor Composite Performance Score | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Vendor Risk Tier | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| EXIM Country of Origin | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Commercial Credit Score | Unavailable | Credit Bureau | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GSTIN Registration Status | Unavailable | GST Portal (via GSP) | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Company Status | Unavailable | MCA21 | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Ariba RFQ Trigger Event | Unavailable | Ariba | Ariba export/API for supplier onboarding, RFQs and contracts; map supplier IDs to SAP vendor IDs. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

### Procurement #3 - AI-Driven Preparation Material for Negotiations

- Decision: Tier 2.5 discovery until external data contracted
- Readiness: Tier 2.5 / external-data + definition
- Field count: 21 total; 5 available, 3 partial, 13 unavailable.
- Systems needed: SAP - Purchase Register (5), Internal Computed / Derived (4), EXIM Data Provider (3), Macro Indicators (Public) (3), SAP - Material Master (2), Conversational AI Surface (2), SAP - Vendor Master (1), Commodity Price Provider (1)
- Source groups: SAP 8, External (Market Data) 7, Computed / Derived 6
- Caveat: Moved out of normal Tier 2 because it depends on EXIM/commodity feeds and negotiation outcome capture.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Material Code (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Number | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| AI-Generated Negotiation Brief | Unavailable | Conversational AI Surface | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Negotiation Outcome Log | Unavailable | Conversational AI Surface | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Buyer Price Variance (Same SKU x Period) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Per-Vendor Pricing Pattern | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Recommended Target Price | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Seasonal Buy Pattern per Commodity | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Commodity Price Index | Unavailable | Commodity Price Provider | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Country of Origin | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Exporter / Global Supplier | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Agri Commodity / MSP Index | Unavailable | Macro Indicators (Public) | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Crude Oil / Diesel Price Index | Unavailable | Macro Indicators (Public) | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| USD/INR FX Rate | Unavailable | Macro Indicators (Public) | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |

### Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products)

- Decision: Tier 2.5 discovery until external data contracted
- Readiness: Tier 2.5 / external-data + definition
- Field count: 17 total; 4 available, 2 partial, 11 unavailable.
- Systems needed: Internal Computed / Derived (4), SAP - Purchase Register (3), SAP - Material Master (3), Macro Indicators (Public) (3), Industry / Labor Benchmarks (2), EXIM Data Provider (1), Energy / Utility Rate Source (1)
- Source groups: External (Market Data) 7, SAP 6, Computed / Derived 4
- Caveat: Moved out of normal Tier 2 because it needs external market feeds and category-specific assumptions.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Unit of Measure (UoM) | Available | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Quantity Ordered (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Material Description | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Cost Build-Up Template per Commodity | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Input Cost Pass-Through Coefficient | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Should-Cost Gap (Actual vs. Target) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Should-Cost Target Price (per SKU) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| EXIM Exporter / Global Supplier | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Industrial Electricity Tariff (Region) | Unavailable | Energy / Utility Rate Source | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Labor Rate Benchmark (Region x Skill Tier) | Unavailable | Industry / Labor Benchmarks | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Manufacturing Overhead Benchmark | Unavailable | Industry / Labor Benchmarks | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Agri Commodity / MSP Index | Unavailable | Macro Indicators (Public) | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Crude Oil / Diesel Price Index | Unavailable | Macro Indicators (Public) | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| USD/INR FX Rate | Unavailable | Macro Indicators (Public) | External data subscription/API/export; confirm provider, terms, refresh, identifiers and history. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |

### Procurement #2 - Real-Time Import Data Analysis

- Decision: Workshop-heavy; do not promise production yet
- Readiness: Workshop-heavy
- Field count: 16 total; 3 available, 2 partial, 11 unavailable.
- Systems needed: EXIM Data Provider (7), Internal Computed / Derived (4), SAP - Purchase Register (3), SAP - Vendor Master (1), SAP - Material Master (1)
- Source groups: External (Market Data) 7, SAP 5, Computed / Derived 4
- Caveat: EXIM provider, HSN mapping, landed-cost normalization and provider lag must be validated.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Material Code (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| PO Date | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Unit Price (PO line) | Available | SAP - Purchase Register | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| HSN Code (per SKU) | Partial | SAP - Material Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Vendor Name | Partial | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| EXIM Benchmark Deviation Alert | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Largest Importers per HSN | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Top Source Countries per HSN | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Trader Premium per SKU | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| EXIM Country of Origin | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Exporter / Global Supplier | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM HSN Code | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Import Price (CIF / Landed Cost) | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Import Quantity | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Importer Name | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| EXIM Transaction Date | Unavailable | EXIM Data Provider | Contract EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |

### Procurement #5 - Vendor Creditworthiness & Fraud Check

- Decision: Workshop-heavy; do not promise production yet
- Readiness: Workshop-heavy
- Field count: 18 total; 3 available, 1 partial, 14 unavailable.
- Systems needed: SAP - Vendor Master (4), MCA21 (4), GST Portal (via GSP) (3), Credit Bureau (2), Internal Computed / Derived (2), Court / Litigation Records (2), Ariba (1)
- Source groups: External (Risk/Compliance) 11, SAP 4, Computed / Derived 2, Internal Apps 1
- Caveat: Mostly external risk/compliance data plus entity resolution and legal/privacy approval.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Vendor GSTIN | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor PAN | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Region | Available | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Vendor Name | Partial | SAP - Vendor Master | SAP BW / Power BI or MM read-only extract; if missing, S/4 CDS/OData or scheduled PO/vendor/material export. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Composite Vendor Risk Score | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Vendor Risk Tier | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Insolvency / NCLT Filings | Unavailable | Court / Litigation Records | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Litigation Records | Unavailable | Court / Litigation Records | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Commercial Credit Score | Unavailable | Credit Bureau | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Credit Default History | Unavailable | Credit Bureau | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GST Default Flag | Unavailable | GST Portal (via GSP) | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GST Return Filing History | Unavailable | GST Portal (via GSP) | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| GSTIN Registration Status | Unavailable | GST Portal (via GSP) | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Charges / Encumbrances | Unavailable | MCA21 | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Company Status | Unavailable | MCA21 | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Directors / Beneficial Owners | Unavailable | MCA21 | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| MCA Incorporation Date | Unavailable | MCA21 | External risk provider/GSP or approved API/export; legal approval and entity-resolution keys required. | Confirm whether SFS already has this provider; if not, nominate contracting owner and approve provider shortlist. |
| Vendor Onboarding Workflow Status | Unavailable | Ariba | Ariba export/API for supplier onboarding, RFQs and contracts; map supplier IDs to SAP vendor IDs. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

### Field Force #5 - AI-Enabled Sales Coaching

- Decision: Workshop-heavy; do not promise production yet
- Readiness: Workshop-heavy
- Field count: 18 total; 4 available, 2 partial, 12 unavailable.
- Systems needed: Internal Computed / Derived (9), SAP - Sales & Distribution (3), Saathi App (3), Growthbook (1), SAP - Customer / Dealer Master (1), Conversational AI Surface (1)
- Source groups: Computed / Derived 10, Internal Apps 4, SAP 4
- Caveat: Approved coaching content, voice/call capture, classification and coaching rubric are required.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| TBM ID / Sales Rep Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Scheme Participation Record | Partial | Growthbook | Growthbook event export/API; map employee, dealer, activity type, timestamp and outcome to SAP IDs. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| TBM Visit Log | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| AI-Generated Coaching Recommendation | Unavailable | Conversational AI Surface | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Activity-Outcome Correlation | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Call Type Classification | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Conversation Quality Framework | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Relationship Profile (Structured) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Peer Benchmark (Anonymized Cohort) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| TBM Conversation Quality Score (per Dimension) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| TBM Time Allocation Analysis | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Target Attainment % (Period-to-Date) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Coaching Action Item Tracking | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
| Dealer Voice Capture (Saathi) | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |

### Field Force #2 - Activity Analytics (Growthbook + SAP)

- Decision: Scope first; no build claim yet
- Readiness: Assumption-only
- Field count: 17 total; 8 available, 2 partial, 7 unavailable.
- Systems needed: Internal Computed / Derived (6), SAP - Sales & Distribution (4), Saathi App (4), SAP - Customer / Dealer Master (3)
- Source groups: SAP 7, Computed / Derived 6, Internal Apps 4
- Caveat: ODS has only a name and no detailed content; field map is inferred from sibling use cases and must be scoped with SFS.

| Field assumed | Availability | Source system | Access route | Concrete ask |
|---|---|---|---|---|
| Saathi Dealer Engagement Event | Available | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Assigned TBM | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Code | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Region | Available | SAP - Customer / Dealer Master | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Quantity | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Primary Sales Value | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Sales Region / Territory Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| TBM ID / Sales Rep Code | Available | SAP - Sales & Distribution | SAP BW / Power BI first; if missing, SD read-only extract via S/4 CDS/OData or scheduled billing/order/customer-master flat file. | Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence. |
| Dealer Last Visit Timestamp | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| TBM Visit Log | Partial | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable. |
| Activity-Outcome Correlation | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Call Type Classification | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Coverage % (Tier-Weighted) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Tier (Platinum / Gold / Silver / Bronze) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| TBM Time Allocation Analysis | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| TBM Visit Count (Period) | Unavailable | Internal Computed / Derived | Computed in Conformal semantic layer after base data lands; needs metric definition, formula owner and validation examples. | Do not ask for this as a raw field. Ask SFS to confirm definition, formula, examples and owner; Conformal computes it. |
| Dealer Voice Capture (Saathi) | Unavailable | Saathi App | Saathi DB/API/export; confirm dealer profile, notes, voice capture, visit logs and consent controls. | Confirm whether workflow is live; if not, approve net-new capture in Saathi/Growthbook/Ariba and define owner. |
