# SFS Project Leap - 146-Field Assumption Audit

Prepared for Conformal internal use
Source compared: `Use Cases details_SFS_Project LEAP.ods` from SFS
Derived artifact compared: `notion-data-fields-full-db-selected.json` / 146-field data-readiness map
Date: May 18, 2026

## 1. Bottom line

SFS did **not** give us a field-level schema. They gave us a use-case document with narratives, current-state gaps, future-state descriptions, key activities, effort/cost estimates, and some source-system hints.

Our 146-field map is therefore a **schema hypothesis**, not a confirmed SFS inventory. It is directionally strong, but several fields are:

- directly supported by the SFS document,
- reasonable but unconfirmed inferences,
- product outputs we should not count as SFS data asks,
- or possibly bad assumptions that should be downgraded before speaking to SFS.

The most important correction is this:

> Do not present "Available" as "confirmed available from SFS." Present it as "likely exists in an SFS-owned system, pending source-owner validation."

## 2. What SFS gave us vs. what we created

| Area | What SFS actually gave | What we derived | Risk |
|---|---|---|---|
| Use cases | 21 use cases across Enterprise, Procurement, Field Force, Logistics, Infra | 15 custom-build use cases mapped to 146 fields, 5 logistics separated, 1 infra foundation | Correct framing, but must say logistics is deliberately unmapped |
| Data fields | No explicit field list | 146 assumed production fields | All field names are our hypothesis unless directly mentioned |
| Source systems | SAP, SAP BW + Power BI, Growthbook, Saathi, Concur, Complinity, Ariba, EXIM, GST, MCA, credit, court records, logistics vendors | Specific table-like sources and extraction routes | Good for planning, not yet confirmed |
| Data availability | Mostly qualitative: available in SAP, manual Excel, not collected, third-party, future capture | Available / Partial / Unavailable flags | Availability labels are the riskiest part |
| Costs / ROI | Theme-level estimates and impacts in ODS | Wave sequencing and build readiness | Good, but do not imply SFS has approved budget |

## 3. Highest-risk assumptions in the 146-field map

| Risk | Our field assumption | What SFS actually says | Why it matters | Fix before SFS discussion |
|---|---|---|---|---|
| High | `Secondary Sales Transaction` marked Available via Growthbook | SFS says secondary sales / inventory liquidation is a future use case and currently not collected in the Field Performance section. Enterprise Assistant mentions primary/secondary sales, but not the source. | This can overstate Wave 1 readiness for sell-out / liquidation views. | Mark as **Unconfirmed**. Ask: where, if anywhere, is secondary sales captured today? Smart Fasal, Growthbook, distributor calls, SAP, or not captured? |
| High | `Saathi Dealer Engagement Event` marked Available | SFS says dealer notes are unstructured and not centralized. The Dealer Profile use case references Saathi as the future app context, not necessarily current structured data. | We may be assuming Saathi already has event-level structured logs. | Downgrade to **Partial / validate schema** until SFS shares Saathi export. |
| High | `Activity Analytics` has 17 fields | SFS provided only the use-case name and no detail. | The full field map is inferred from sibling use cases. | Keep as **Discovery-only, no build claim**. |
| High | Churn uses dealer GST fields (`Dealer GSTIN Registration Status`, `Dealer GST Default Flag`) | SFS churn section mentions sales trends, collections, scheme participation, visit frequency, issue logs, competitor/retail audit optional. It does not mention GST. | These fields are weakly connected to dealer churn and may confuse the story. | Remove from churn or mark as optional external risk enrichment, not core churn data. |
| High | Field Performance does not include Concur expense fields | SFS explicitly says Field Performance should integrate field-related expenditure via Concur. | Our map underrepresents Concur in Field Force while including SG&A under Procurement. | Add Concur expense amount/category to Field Performance or explicitly scope it out of Wave 1. |
| High | Dealer Profiles lacks outstanding receivables / AR ageing as a field | SFS says dealer brief includes outstanding receivables. | Dealer 360 is incomplete without receivables. | Add dealer-level receivables / ageing from SAP FI-AR. |
| High | AI Sales Coaching misses product literature, agronomic guides, safety sheets, field surveys, best-practice pitch recordings | SFS key activities explicitly list these. | Our coaching map over-indexes on sales/dealer analytics and under-indexes on content corpus. | Add document/audio corpus fields and treat as a content ingestion + consent workstream. |
| Medium | `Dealer Voice Capture (Saathi)` assigned to Saathi App | SFS says handheld voice device such as Neosapien, not necessarily Saathi. | Wrong source owner may be asked. | Reword as "voice capture surface, Saathi/handheld device TBD." |
| Medium | `Chatbot Query Log` assigned to Saathi App for Scheme Chatbot | Query logs are generated by the future chatbot, not an SFS source field. | It is product telemetry, not source data. | Retag as Conversational AI telemetry. Do not ask SFS for it. |
| Medium | `Scheme Participation Record` assigned to Growthbook | SFS mentions scheme participation, but not that Growthbook owns it. | Source owner could be SAP pricing, scheme files, claims, Growthbook, or manual. | Mark source as unconfirmed. Ask Commercial/Sales Ops. |
| Medium | `Dealer Tier (Platinum / Gold / Silver / Bronze)` | SFS mentions partner classification as star/growth/maintain/turnaround in Product Visibility, not these labels. | We invented the tier taxonomy. | Rename to "Partner classification / dealer tier, definition TBD." |
| Medium | `Product Hierarchy (Cross-BU Unified)` assigned to SAP Material Master | SFS says inconsistent product hierarchy and data quality issues. | This is governance work, not just SAP extraction. | Keep as unavailable, owner = Master Data / Data Governance. |
| Medium | `SKU Substitution Mapping` assigned to SAP Material Master | SFS wants substitute suggestions, but does not say a substitution master exists. | Could be a product/rules workshop, not SAP. | Mark as definition/rule capture with Product/Commercial owner. |
| Medium | `Vendor Capacity Signal` computed internally | SFS wants capacity-based filtering, but available data may not infer real capacity. | We may be inventing a signal from insufficient history. | Treat as external/vendor declaration or Ariba/onboarding field, not purely computed. |
| Medium | `GRN Quality Rejection Quantity` from SAP Purchase Register | SFS mentions quality score/rejection rate for vendor performance, but source may be SAP QM or manual quality records, not purchase register. | Wrong SAP owner/module. | Ask whether quality rejection exists in SAP QM, GRN, Excel, or Complinity/vendor docs. |
| Medium | Warehouse lat/lng and dealer lat/lng | SFS mentions location filters and field operations, but not lat/lng availability. | Lat/lng often needs geocoding, not direct SAP. | Mark as partial/geocoding needed. |

## 4. Use-case-by-use-case discrepancy audit

### Enterprise Assistant #1 - Enterprise Chat Assistant

**SFS support is strong for:** SAP extracts for supply and sales, SAP BW + Power BI, enterprise metric dictionary, historical decks/review material, leadership queries, charts, source citations.

**Possible gaps in our 146 fields:**

- We include `Vendor Region`, `Spend Category Tag`, `Dealer Tier` as assistant fields, but these are not specifically named in the Enterprise Assistant source. They may be useful, but they are inherited from other use cases.
- We do not explicitly include **historical review decks / leadership materials** as a source corpus, although SFS names this as training data for the intent library.
- `Secondary Sales Transaction` is risky. SFS names secondary sales as part of the Enterprise Assistant data line, but Field Performance says secondary sales/liquidation is not currently collected.
- `Assistant Query Log` and `'What Changed' Weekly Digest` are product outputs/telemetry, not SFS source fields.

**Correction:** Keep Enterprise Assistant as Wave 1, but make the first validation ask "confirm SAP BW / Power BI datasets and available sales/supply metrics" rather than validating every derived assistant field.

### Procurement #1 - Historical Spend Analysis & Price Insights

**SFS support is strong for:** SAP purchase register, 3-year PO-line extract, vendor master, taxonomy mapping, product descriptions, category hierarchy, BPV, price variance, anomaly detection, Complinity and Concur not integrated with SAP.

**Possible bad assumptions:**

- `SG&A Expense Amount/Category` under Procurement is supported by Concur, but it is not necessarily part of procurement spend cube. SFS says Concur tracks expense separately, so it may be contextual rather than core spend.
- `Vendor License Status/Validity` from Complinity is directly named, but export/API availability is not confirmed.
- `Product Category Hierarchy`, `Spend Category Tag`, `Spend Sub-Category Tag`, and `Strategic Spend Classification` are not existing fields. They are taxonomy outputs to be defined.

**Correction:** This use case is a good Wave 1.5 candidate, but only after taxonomy workshop and vendor/material master cleanup.

### Procurement #2 - Real-Time Import Data Analysis

**SFS support is strong for:** EXIM/customs data, HSN codes, import price, import quantity, importer, country of origin, global suppliers, top source countries, SAP purchase register linked to HSN.

**Possible bad assumptions:**

- "Real-time" is likely overstated. EXIM provider freshness and latency must be confirmed.
- `HSN Code (per SKU)` in SAP Material Master is not guaranteed. SFS explicitly says HSN mapping across SFS SKUs is needed.
- We assume provider fields are structured exactly as `EXIM Transaction Date`, `Importer`, `Exporter`, etc. Likely correct, but provider-dependent.

**Correction:** Keep as external-data-gated. Do not include in Wave 1 except as provider discovery.

### Procurement #3 - Negotiation Preparation

**SFS support is strong for:** SAP purchase history, commodity indices, EXIM prices, macro signals, vendor history, target price, price anchors, negotiation brief, outcome log.

**Possible bad assumptions:**

- `Negotiation Outcome Log` does not exist today. SFS lists it as a future learning loop.
- `Recommended Target Price` and `AI-Generated Negotiation Brief` are generated outputs, not source data.
- Macro fields such as USD/INR, MSP, crude/diesel are reasonable but not exhaustively specified by SFS.

**Correction:** Keep in external-data + workflow-capture tier. Requires EXIM/commodity provider and negotiation outcome capture design.

### Procurement #4 - Vendor Identification

**SFS support is strong for:** SAP/Ariba procurement history, vendor master, PO history, GRN records, external vendor databases, RFQ trigger via Ariba, multi-criteria scoring, price, quality, delivery, risk weightings.

**Missing or under-modeled fields:**

- SFS explicitly mentions **quality certifications** and **geographic proximity**. Our map has vendor region but not certifications or precise distance/proximity.
- SFS mentions capacity to supply desired quantity. Our `Vendor Capacity Signal` is marked computed, but may require vendor declarations, onboarding data, or external data.
- Ariba is "to be evaluated / being implemented." We should not assume Ariba RFQ APIs are production-ready.

**Correction:** Add/validate vendor certification, location/proximity, and capacity source. Treat Ariba as dependency status unknown.

### Procurement #5 - Vendor Creditworthiness & Fraud Check

**SFS support is strong for:** GST registrations, MCA filings, credit bureau scores, court/litigation records, duplicate PAN/GST entities, adverse financial signals, vendor onboarding workflow.

**Possible gaps:**

- We do not explicitly model duplicate PAN/GST detection or bank-account verification, though the composite score may cover it.
- API access is not guaranteed. SFS says not all API-accessible databases are leveraged.
- `Vendor Onboarding Workflow Status` in Ariba is a future/validation dependency.

**Correction:** Keep as Tier 3. Strong use case, but blocked on legal, provider contracting, and Ariba/onboarding owner.

### Procurement #6 - Should-Cost Analysis

**SFS support is partial:** SFS names raw materials, labour, overheads, logistics, working capital, commodity feeds, vendor cost sheets, contract data for seeds, conversion costs by grower/region.

**Missing or weak in our 146 fields:**

- We included labour, overhead and electricity benchmarks, but not explicit **logistics cost component**, **working capital cost component**, **vendor submitted cost sheet**, **contract growing conversion cost**, or **BOM/component tree inputs by product**.
- We assume generic benchmarks can power should-cost. For top 5-10 products, the model will be category-specific and workshop-heavy.

**Correction:** Keep as high-value but not easy. Needs category-specific cost model workshops and provider/data-source selection.

### Field Force #1 - Field Performance Tracking Dashboard

**SFS support is strong for:** Growthbook activity logs, SAP sales, collections, targets at TBM x dealer x SKU x month, Excel targets, dealer/territory/product hierarchy alignment, natural language dashboard, incentives, leadership reports.

**Discrepancies:**

- SFS explicitly says field expenditure via Concur should be integrated. Our 146-field map does not attach Concur SG&A fields to Field Performance.
- `Secondary Sales Transaction` is marked available via Growthbook, but SFS says secondary sales / inventory liquidation is currently not collected and PoG trackers are based on calls.
- We include `Saathi Dealer Engagement Event` as available, but Field Performance source text names Growthbook, SAP, Excel and Concur, not Saathi.
- Activity-to-outcome linkage is specifically called out as missing. Any ROI/intelligence layer is not easy Wave 1.

**Correction:** Wave 1 can cover descriptive performance. Add Concur or explicitly defer. Treat secondary sales/liquidation as future capture.

### Field Force #2 - Activity Analytics

**SFS support is weak:** ODS provides only the use-case name and no detail.

**Discrepancy:** The 17-field map is almost entirely inferred from siblings.

**Correction:** Discovery-only. Do not promise scope, feasibility, or data availability until SFS explains the intended workflow.

### Field Force #3 - Pricing, Policy & Scheme Chatbot

**SFS support is strong for:** scheme circulars, PDFs/images/WhatsApp/email, SAP pricing master, scheme eligibility logic, product x region x dealer tier x period, credit policy, commercial terms, circular repository, OCR/vector store.

**Discrepancies:**

- We map `Scheme Definition` to Excel, but SFS also names SAP pricing master and circular/PDF sources.
- We do not explicitly include **credit policy**, **commercial terms**, or **SAP pricing condition/master fields**.
- `Chatbot Query Log` is assigned to Saathi App, which is probably wrong. It is future chatbot telemetry.
- `Scheme Participation Record` from Growthbook is not source-confirmed.

**Correction:** Add SAP pricing master / credit policy / commercial terms and central circular repository as first-class sources. Retag chatbot logs as product telemetry.

### Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs

**SFS support is strong for:** SAP sales, receivables, scheme participation, last-visit notes, recent issues, voice-note capture, central dealer profile, action items.

**Discrepancies:**

- We are missing explicit **outstanding receivables / AR ageing** at dealer level.
- We assume Saathi has structured dealer engagement events. SFS says visit notes are unstructured via emails/Excel today.
- `Dealer Key Contacts` is not named in SFS text. Useful, but assumed.
- Voice capture may be handheld device / Neosapien, not Saathi.

**Correction:** Add dealer receivables and issue/action-item fields. Treat Saathi schema and voice capture as validation asks.

### Field Force #5 - AI-Enabled Sales Coaching

**SFS support is strong for:** product technical literature, safety data sheets, agronomic guides, farmer/dealer objections, field surveys, Growthbook notes, best-practice pitch recordings, voice UX, coaching content and scoring.

**Major discrepancy:** Our current fields are mostly sales/dealer analytics and do not include the core content corpus SFS named.

**Missing fields/sources:**

- Product technical literature
- Safety data sheets
- Agronomic guides
- Historical objections from surveys/Growthbook notes
- Best-practice pitch recordings
- Approved coaching scripts/playbooks
- Consent status for recordings

**Correction:** Sales Coaching should not be represented as mostly SAP + computed fields. It is a content, voice, consent and evaluation product.

### Field Force #6 - Unified Product & Partner-Level Visibility

**SFS support is strong for:** SAP product master, customer master, sales, collections, targets, product hierarchy, partner scorecard, liquidation/PoG, drill-down dashboard.

**Discrepancies:**

- We miss explicit **collections/receivables** and **targets** in this use case.
- `Secondary Sales Transaction` and liquidation/PoG remain unconfirmed.
- `Dealer BU Presence` is inferred. Good to validate but not source-explicit.
- Partner classification labels should be SFS-defined, not "Platinum/Gold/Silver/Bronze."

**Correction:** Add collections and targets. Keep secondary/liquidation as new capture.

### Field Force #7 - Real-Time Warehouse Stock Visibility

**SFS support is strong for:** SAP stock positions, vendor warehouse feeds, in-transit data from Logistics/SAP, SKU search, substitutes, low-stock alerts.

**Possible bad assumptions:**

- `Warehouse Location (Lat/Lng)` and `Dealer Geo-Location` may require geocoding, not direct SAP.
- `SKU Substitution Mapping` may not exist in material master. It may be a Product/Commercial rule set.
- "Real-time" may be scheduled near-real-time refresh, not live.

**Correction:** Keep as Tier 2. Ask exact SAP inventory refresh cadence, vendor warehouse process, in-transit source, and substitution owner.

### Field Force #8 - Dealer Churn Risk

**SFS support is strong for:** SAP sales history, collection patterns, scheme participation, product mix, visit frequency, issue logs, churn definition, intervention workflow, external competitor/retail audit optional.

**Discrepancies:**

- We include dealer GST registration/default fields. SFS does not mention GST for churn.
- We miss explicit **collections/receivables ageing**, **order frequency**, **product mix narrowing**, **issue logs**, and **churn labels**.
- `Intervention Tracking Log` is likely net-new workflow, not necessarily Saathi.

**Correction:** Replace GST fields with receivables/order/product-mix/issue-log fields as core churn inputs. Keep GST as optional risk enrichment only if SFS wants it.

### Logistics #1-#5

**SFS gave detailed logistics use cases**, but they are explicitly buy-and-customise.

**Discrepancy risk:** Our 146-field DB maps only the 15 custom-build use cases. If someone counts 21 use cases, they may think logistics was missed.

**Correction:** Always state: logistics is deliberately excluded from field mapping because the right path is TMS/vendor selection, not a custom AI data build.

### Technology & Infrastructure

**SFS support is strong for:** Azure/cloud, data platform, integration layer, GenAI services, lakehouse, serving layer, governance, shared APIs.

**Discrepancy:** No field map exists because it is not a business data use case.

**Correction:** Keep as Wave 0 foundation and platform ask, not part of 146 fields.

## 5. Fields to downgrade or retag before showing SFS

| Field | Current tag | Better tag |
|---|---|---|
| Secondary Sales Transaction | Available / Growthbook | Unconfirmed. Ask whether captured anywhere today. |
| Saathi Dealer Engagement Event | Available / Saathi | Partial. Validate Saathi event schema and production usage. |
| Dealer Voice Capture (Saathi) | Unavailable / Saathi | Net-new capture surface. Saathi vs handheld device TBD. |
| Chatbot Query Log | Unavailable / Saathi | Product telemetry from chatbot, not SFS source data. |
| Scheme Participation Record | Partial / Growthbook | Source TBD: Growthbook, SAP, scheme claims, Excel, or not captured. |
| Dealer Tier (Platinum/Gold/Silver/Bronze) | Computed | Rename to SFS-defined partner classification. |
| Product Hierarchy (Cross-BU Unified) | SAP Material Master | Master-data governance output, not simple SAP extract. |
| SKU Substitution Mapping | SAP Material Master | Product/Commercial rule set, source TBD. |
| Dealer GSTIN Registration Status / Default Flag for Churn | External risk | Optional enrichment only; not core churn input from SFS doc. |
| Vendor Capacity Signal | Computed | External/vendor declaration or Ariba onboarding signal, source TBD. |
| GRN Quality Rejection Quantity | SAP Purchase Register | SAP QM / GRN / manual quality system TBD. |
| Dealer Geo-Location / Warehouse Lat-Lng | SAP | Partial/geocoding needed. |

## 6. Fields/sources missing from our 146-field map

These are either explicitly named by SFS or strongly implied, but not cleanly represented in our field map.

| Missing item | SFS use case | Why it matters |
|---|---|---|
| Dealer receivables / AR ageing by dealer | Dealer Profiles, Churn, Enterprise | SFS explicitly says dealer brief includes outstanding receivables. |
| Collections at dealer / partner level | Field Performance, Product Visibility, Churn | SFS repeatedly names collections as a core input. |
| Concur field expenditure in Field Performance | Field Performance | SFS explicitly says field-related expenditure via Concur. |
| Product technical literature | Sales Coaching | Core coaching corpus. |
| Safety data sheets | Sales Coaching | Core coaching corpus and compliance. |
| Agronomic guides | Sales Coaching | Core coaching corpus. |
| Historical objections from surveys / Growthbook notes | Sales Coaching | Needed for coaching recommendations. |
| Best-practice pitch recordings | Sales Coaching | Needed for conversation quality and coaching examples. |
| SAP pricing master / pricing conditions | Scheme Chatbot | SFS names SAP pricing master. |
| Credit policy and commercial terms documents | Scheme Chatbot | SFS says chatbot answers pricing, policy, schemes and commercial terms. |
| Quality certifications | Vendor Identification | SFS says vendors filtered by quality certifications. |
| Vendor geographic proximity / distance | Vendor Identification | SFS says vendors filtered by geographic proximity. |
| Duplicate PAN/GST detection | Vendor Fraud | SFS explicitly names duplicate PAN/GST entities. |
| Bank account verification | Vendor onboarding/fraud, implied by document collection | Could matter for fraud checks. |
| Vendor submitted cost sheets | Should-Cost | SFS says LLM reads vendor cost sheets. |
| Logistics cost component and working capital component | Should-Cost | SFS says cost build-up includes logistics and working capital. |
| Contract growing conversion costs by grower/region | Should-Cost | SFS explicitly names seeds / contract growing. |
| Issue logs / complaint rationale | Dealer Profiles, Churn | SFS says recent issues and rationale/corrective actions are not captured. |
| Churn label / churn definition field | Churn | SFS says no labelled churn history or standard churn definition. |
| Historical decks and review materials | Enterprise Assistant | SFS names these as training data for intent library. |

## 7. Clean way to explain this internally

The 146-field DB should be treated as a **first-pass field hypothesis** created from the SFS use-case document. It is useful because it turns vague use cases into concrete source-system conversations. But it should not be positioned as a confirmed schema.

The right language:

> We decomposed the use cases into a likely production field map. The next step is to validate that hypothesis with source owners and sample extracts.

The wrong language:

> These 146 fields are available/missing in SFS systems.

## 8. Specific clarification asks to send SFS

1. Can SFS share the data dictionary or dataset inventory behind the existing SAP BW / Power BI layer?
2. Is secondary sales / liquidation / PoG captured anywhere today? If yes, in which system and at what grain?
3. Is Saathi live as a structured event system today, or is it mainly a planned/future field workflow?
4. Do Growthbook events carry SAP-matching dealer IDs and employee/TBM IDs?
5. Where is scheme participation captured: Growthbook, SAP, claims/settlement, Excel, or not captured?
6. Where are pricing conditions, credit policy and commercial terms maintained?
7. Does SAP FI-AR expose dealer-level receivables and ageing linked to dealer code?
8. Does Concur carry field-expenditure entries that can map to TBM/RBM/cost centre/territory?
9. Does SAP or any quality system store GRN rejection/quality rejection by vendor/material?
10. Is Ariba live, being implemented, or only planned? Which RFQ/onboarding fields are available?
11. Are vendor certifications, capacity declarations and location/proximity captured anywhere?
12. For Sales Coaching, where do product technical literature, safety sheets, agronomic guides, objections and pitch recordings live?
13. For churn, does SFS have labelled churn history or a definition such as no order for 90/180 days?
14. Which external data providers does SFS already subscribe to for EXIM, commodity, GST/GSP, MCA21, credit, litigation and retail audit?
15. Who owns master data governance for product hierarchy, HSN mapping, dealer/vendor IDs and employee/territory hierarchy?

## 9. Practical recommendation

Keep the 146-field analysis, but split the internal field map into four confidence levels:

| Confidence | Meaning | Examples |
|---|---|---|
| Directly source-backed | SFS explicitly named the source and/or field family | SAP PO line, EXIM by HSN, SAP sales, Growthbook activity logs, Concur, Complinity |
| Reasonable inference | Not named exactly, but normal for the source/use case | PO date, unit price, dealer code, vendor ID, primary sales value |
| Derived/product output | We compute or generate it; SFS should not be asked for it as raw data | BPV gap, target attainment, risk score, weekly digest, answer confidence |
| Speculative / validate first | Source is not named, contradicted, or likely future capture | secondary sales, Saathi structured events, churn GST fields, dealer voice capture, SKU substitution, vendor capacity |

This keeps the sales story strong without over-promising. It also gives Amit a sharper working-session agenda: "Here are the fields we think exist, here are the ones we know are computed, and here are the assumptions we need SFS to confirm or correct."
