# SFS Project Leap - Exact Discovery Asks From SFS

Prepared by Conformal
Working document for SFS and Conformal alignment
Date: May 18, 2026

## 1. What we are asking for now

At this stage, we are **not** asking SFS for full production credentials or write access into enterprise systems. We are asking for enough data, access paths, source owners and working sessions to validate the 146-field readiness map and begin a controlled discovery sprint.

The first sprint should answer four questions:

1. Which data fields already exist in SFS-owned systems?
2. Which systems can expose those fields through read-only extracts, APIs or existing BI/BW layers?
3. Which fields require business definitions, master-data governance or new capture?
4. Which use cases should move first because the data foundation already exists?

The discovery request has five parts:

| Ask type | What we need from SFS | Why it matters |
|---|---|---|
| Data access | Masked extracts, schemas, dictionaries and refresh cadence from SAP, Growthbook, Saathi, Concur, Complinity, Ariba and scheme/target repositories | Confirms what exists and at what grain |
| System privileges | Read-only export paths, API/export options, service account approach and approved data-sharing mechanism | Lets us build the columnar data foundation safely |
| People access | Named owners for every system and business definition | Prevents the work from stalling at "who owns this?" |
| Meetings | Focused working sessions with IT, SAP, field force, procurement, finance, master-data, legal and security | Converts assumptions into signed-off source truth |
| Decision workshops | Metric dictionary, spend taxonomy, product hierarchy, dealer tiers, churn rules, scheme rules and external-data posture | Turns computed fields into trusted business logic |

## 2. The principle: sample extracts first, production access later

For the first discovery sprint, Conformal can work with:

- Masked or anonymised extracts.
- Read-only exports from SAP BW / Power BI.
- CSV, parquet, Excel, API exports or SFTP/Azure Blob drops.
- Data dictionaries and schema screenshots if full exports are delayed.
- Limited history samples if full 36-month history is not immediately available.

We do **not** need, and should not request on day one:

- Write access to SAP, Ariba, Concur, Saathi, Growthbook or any production application.
- Direct production database credentials.
- Unmasked PII or voice recordings before legal/privacy approval.
- Real-time integrations before schema validation.
- Access to systems outside the agreed use-case scope.

The clean model is:

1. Discovery: masked extracts and schema validation.
2. Pilot: read-only scheduled extracts or read-only API/service-account access.
3. Production: approved integration pattern, SSO, audit logs, access groups, monitoring and data-retention controls.

## 3. Exact data access asks

### 3.1 SAP BW / Power BI and SAP S/4HANA

SFS's Enterprise Assistant use case names **SAP BW + Power BI** as the reporting layer. This should be our first route. We should ask SFS to confirm whether Conformal can receive read-only extracts from the existing SAP BW queries, Power BI datasets, dataflows or semantic models.

If the BW / Power BI route cannot expose line-level data, the fallback route is controlled SAP S/4HANA extract through CDS/OData, SLT, scheduled flat file or an IT-approved export job.

| SAP area | Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|---|
| SAP SD sales and billing | Sales order / billing extract with dealer, material, plant, territory, order date, invoice date, quantity, value, pricing and scheme references | Invoice-line or order-line | 36 months | Dealer/customer code, material code, plant code, territory code, TBM/employee code, document number | SAP SD owner plus BW/Power BI owner |
| SAP customer/dealer master | Dealer code, legal name, region, territory, assigned TBM/MGO, credit terms, credit limit, onboarding date, GSTIN, active status, BU presence if available | Dealer/customer master row | Current snapshot plus change history if available | Dealer/customer code, GSTIN, territory code, employee code | SAP SD or customer master owner |
| SAP FI/CO and receivables | Collections, outstanding receivables, AR ageing, working capital extracts, GL/P&L extracts at approved grain | Dealer/customer x period or document-level where approved | 24 to 36 months | Dealer/customer code, company code, document number, posting date, profit/cost centre | SAP FI/CO owner |
| SAP MM purchase register | PO-line extract with vendor, material, HSN, plant, PO date, quantity, UoM, unit price, currency, line value, GRN quantity and receipt status | PO-line | 36 months | Vendor code, material code, HSN, plant code, PO number, GRN number | SAP MM owner |
| SAP vendor master | Vendor code, legal name, region, GSTIN, PAN, category, active status, bank status if available | Vendor master row | Current snapshot plus change history if available | Vendor code, GSTIN, PAN | SAP MM/vendor master owner |
| SAP material master | Material code, description, UoM, HSN, category, product hierarchy, active flag and substitution mapping if available | Material/SKU row | Current snapshot plus change history if available | Material code, HSN, product hierarchy code | SAP MM/material master owner plus master-data owner |
| SAP stock/inventory | Stock by plant, storage location, batch, expiry, in-transit quantity, open orders and ATP if available | SKU x plant/storage x date | Current snapshot plus 12 to 24 months snapshots if available | Material code, plant code, storage location, batch number | SAP inventory/MM owner |
| SAP pricing and scheme references | Pricing conditions, discount/scheme references, dealer/product/region eligibility where available | Condition record or pricing reference | Active and last 24 months | Dealer code, material code, scheme id, region, period | SAP SD/pricing owner plus scheme owner |

**SAP privilege ask:** read-only extract access through existing BW/Power BI first. If that is insufficient, SFS IT should confirm the approved fallback: CDS/OData, scheduled export, SLT, SFTP or Azure Blob drop.

### 3.2 Growthbook

Growthbook is critical for Field Performance, Activity Analytics, Dealer Profiles, Sales Coaching and Churn.

| Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|
| Field activity export with event id, employee/TBM/MGO id, dealer id, timestamp, activity type, visit outcome, scheme participation, notes metadata and status | Activity event | At least 12 months | Dealer code mapped to SAP dealer, employee code mapped to SAP/TBM hierarchy | Growthbook admin/product owner |

**Specific validation question:** does Growthbook actually capture secondary sales, liquidation or PoG data today? If yes, share the schema. If no, treat secondary sales/liquidation as net-new capture, not Wave 1 base data.

### 3.3 Saathi app

Saathi matters for Dealer Profiles, Activity Analytics, Sales Coaching, Scheme Chatbot and Churn.

| Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|
| Dealer profile export, engagement events, last visit timestamp, visit notes, issue logs, intervention logs, chatbot query logs if live, voice/call capture status and consent metadata | Dealer x event or dealer profile row | 12 months if live; otherwise current schema | Dealer code, employee/TBM code, timestamp, interaction id | Saathi app owner plus legal/compliance |

**Specific validation questions:**

1. Is Saathi live in production for SFS, or is it planned?
2. Are dealer notes structured, semi-structured or free text?
3. Is voice capture live, planned or outside Saathi?
4. If voice/call recording exists, is consent captured and legally cleared for analytics/classification?

### 3.4 Concur

Concur is explicitly named by SFS for expenses and is not integrated into SAP in the current state.

| Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|
| Expense export with expense id, amount, category, employee, cost centre, date, approval status, business unit and territory if available | Expense line | 24 to 36 months | Employee code, cost centre, territory/BU mapping | Concur owner plus finance/field ops |

**Why needed:** field performance, SG&A context and procurement spend analysis cannot be complete without the Concur expense mapping.

### 3.5 Complinity

Complinity is explicitly named by SFS for vendor license/compliance and is not integrated into SAP in the current state.

| Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|
| Vendor compliance export with vendor license status, validity date, vendor id, PAN, GSTIN, compliance document type and update date | Vendor x license/compliance record | Current snapshot plus 24 months if available | SAP vendor code, PAN, GSTIN | Complinity owner plus procurement/vendor master |

**Why needed:** Historical Spend and Vendor Credit/Fraud need vendor compliance context and vendor-master matching.

### 3.6 Ariba

Ariba appears relevant for vendor identification, RFQ workflow, onboarding and vendor risk. We need to confirm whether it is live, in rollout or planned.

| Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|
| Supplier onboarding status, RFQ trigger events, supplier shortlist, bids, awarded supplier, contract references and supplier-to-SAP vendor mapping | Supplier/RFQ event | 12 to 24 months if live | Supplier id, SAP vendor code, PAN/GSTIN, material/category | Ariba owner plus procurement |

**Specific validation question:** if Ariba is not live, which system currently holds RFQ, vendor discovery and onboarding workflow status?

### 3.7 Scheme, target and policy documents

These are critical for Field Performance, Enterprise Assistant, Scheme Chatbot and Dealer Profiles.

| Exact data ask | Minimum grain | History | Join keys needed | SFS owner |
|---|---|---|---|---|
| Sales target files by period, TBM/MGO/RBM/ZBM, SKU/product, dealer/territory and BU | Target row | 24 to 36 months | Employee code, dealer code, material code, territory, period | Sales Ops / Field Excellence |
| Scheme circular repository, active scheme list, scheme eligibility rules, credit policy, commercial terms and archived circulars | Document plus structured metadata | Active plus 24 months archive | Scheme id, product/material, dealer tier/classification, region, period | Scheme owner plus Sales Ops |
| Historical business review decks and KPI packs | Document plus metadata | Last 12 to 24 months | Period, business unit, metric names | CFO/Controller office plus Sales Ops |

**Specific validation question:** which source is the legal/commercial source of truth for scheme eligibility: SAP pricing master, scheme circulars, Excel trackers, claims workflow or another system?

### 3.8 External-data posture

For import, negotiation, should-cost and vendor-risk use cases, SFS does not need to provide these fields directly if there is no existing subscription. SFS does need to name the contracting and legal owners.

| External source | Exact ask | Use cases affected | Owner needed |
|---|---|---|---|
| EXIM/customs data | Confirm whether SFS already subscribes to an EXIM data provider. If yes, share provider name, coverage, latency and allowed use. If no, nominate owner to approve provider shortlist. | Import Analysis, Negotiation Prep, Should-Cost, Vendor ID | External-data contracting owner plus procurement |
| Commodity and macro data | Confirm existing subscriptions for commodity indices, crude/diesel, FX, MSP/agri indices, labour benchmarks and utility rates | Historical Spend, Negotiation Prep, Should-Cost | External-data contracting owner |
| GST/GSP, MCA21, credit bureau, litigation/court data | Confirm existing subscriptions or approve sourcing path and legal use constraints | Vendor Credit/Fraud, Vendor ID, Churn optional enrichment | Legal/compliance plus external-data contracting |

### 3.9 Logistics systems

Logistics is a separate buy-and-customise track, not the first AI/data-build wave. Still, we need a light inventory.

| Exact ask | Why | Owner |
|---|---|---|
| Confirm current TMS/logistics vendors, if any, and whether FreightTiger, Shipsy, FarEye, Locus, Project44 or Roambee are already under consideration | Prevents us from proposing a custom build where vendor selection is the right answer | Logistics owner |
| Provide 3 to 6 months sample shipment/lane/POD/carrier data if readily available | Helps fit-gap vendor selection and later integration planning | Logistics plus IT |

### 3.10 Field coverage from the data-access asks

The 146 fields split into two kinds of discovery:

1. **Source/provider discovery:** confirm whether the field exists, where it sits, who owns it, how it can be extracted and what join keys are preserved.
2. **Definition discovery:** confirm the business rule for computed fields that Conformal will create in the semantic layer.

The Section 3 data-access asks cover **88 of the 146 fields** directly through systems, files or external providers. The remaining **58 fields** are computed/derived fields. They are not raw extracts from SFS systems; they are closed through the business-definition workshops in Section 6.

Legend used below: EA = Enterprise Assistant; FF = Field Force; Proc = Procurement.

| Section 3 ask | Unique fields covered | Use cases advanced out of 15 | What counts as "discovered" |
|---|---:|---|---|
| SAP BW / Power BI and SAP S/4HANA | 40 | All 15 mapped use cases | SAP owner, extract route, sample/schema, grain, join keys and refresh cadence confirmed |
| Growthbook | 2 | EA #1; FF #1, #3, #4, #5, #6, #8 | Event schema, history, dealer/employee IDs and secondary-sales/liquidation status confirmed |
| Saathi app | 8 | FF #1, #2, #3, #4, #5, #8 | Live status, export/API route, notes/visit schema, voice/call status and consent fields confirmed |
| Concur | 2 | Proc #1; field expense context for FF #1 | Expense export route, employee/cost-centre mapping and history confirmed |
| Complinity | 2 | Proc #1; vendor-compliance context for Proc #5 | Vendor licence/compliance export route and SAP vendor mapping confirmed |
| Ariba | 2 | Proc #4, #5 | Live/planned status, RFQ/onboarding export route and supplier-to-SAP mapping confirmed |
| Scheme, target and policy repositories | 3 | EA #1; FF #1, #3 | Target files, scheme circulars/docs and official source of truth confirmed |
| External data providers | 27 | Proc #1, #2, #3, #4, #5, #6; FF #8 | Provider availability, contracting owner, legal posture, identifiers and refresh cadence confirmed |
| Logistics/TMS feeder fields | 2 | FF #7 | Current TMS/vendor source and sample shipment/warehouse feeder fields confirmed |
| **Source/provider subtotal** | **88** | **All 15 mapped use cases have at least one source/provider dependency covered** | These are the fields for which SFS must confirm source truth or provider route |
| Computed/derived semantic-layer fields | 58 | All 15 mapped use cases | Business owner, formula/definition, examples and validation test confirmed |
| **Total 146-field map** | **146** | **All 15 mapped use cases** | Every field either has a source route or a definition route |

If SFS provides the Section 3 data-access asks in order, source/provider discovery progresses like this:

| Data-access milestone | New fields covered | Cumulative source/provider fields | Cumulative out of 146 | Use cases advanced |
|---|---:|---:|---:|---|
| SAP BW / Power BI and S/4 extracts validated | 40 | 40 / 88 | 40 / 146 | All 15 mapped use cases get their SAP base checked |
| Growthbook schema/export validated | 2 | 42 / 88 | 42 / 146 | EA #1; FF #1, #3, #4, #5, #6, #8 |
| Saathi schema/export validated | 8 | 50 / 88 | 50 / 146 | FF #1, #2, #3, #4, #5, #8 |
| Concur export validated | 2 | 52 / 88 | 52 / 146 | Proc #1; field expense context for FF #1 |
| Complinity export validated | 2 | 54 / 88 | 54 / 146 | Proc #1; vendor-compliance context for Proc #5 |
| Ariba status/export validated | 2 | 56 / 88 | 56 / 146 | Proc #4, #5 |
| Targets, schemes and document sources validated | 3 | 59 / 88 | 59 / 146 | EA #1; FF #1, #3 |
| External data posture validated | 27 | 86 / 88 | 86 / 146 | Proc #1, #2, #3, #4, #5, #6; FF #8 |
| Logistics/TMS feeder fields validated | 2 | 88 / 88 | 88 / 146 | FF #7 |
| Business-definition workshops completed | 58 | 88 / 88 | 146 / 146 | All 15 mapped use cases get their computed-field rules dispositioned |

## 4. Exact system privilege asks

### 4.1 Discovery sprint privileges

For the first 2 to 3 weeks, request:

| Privilege | Exact ask | Notes |
|---|---|---|
| Data export permission | Permission for SFS owners to share masked sample extracts with Conformal | No production credentials required |
| SAP BW / Power BI read export | Read-only export from approved BW query, Power BI dataset/dataflow or semantic model | Preferred path for SAP data |
| Secure file transfer | Approved mechanism: SFTP, Azure Blob, SharePoint/OneDrive folder, or encrypted email for small samples | SFS IT to choose |
| Data dictionary access | Schema, column descriptions, refresh cadence, grain and key definitions | Needed as much as the data itself |
| API documentation access | For Growthbook, Saathi, Concur, Complinity and Ariba, where APIs exist | Export files are acceptable first |
| Meeting access | Working sessions with functional owners and system admins | Needed to interpret data correctly |

### 4.2 Pilot privileges

Once discovery confirms sources, request:

| Privilege | Exact ask | Notes |
|---|---|---|
| Read-only service account | Service account or scheduled export identity for agreed source systems | No write permissions |
| Scheduled extract job | Daily/weekly export into SFS-approved landing zone | Can start as files before full APIs |
| Azure landing zone | Storage account/container, network rules, managed identity or approved equivalent | Only if SFS wants the pilot inside its tenant |
| Entra ID / SSO group | Named user group for Conformal and SFS pilot users | Needed for role-aware access |
| Secret management | Key Vault or SFS-approved secret store for API credentials | No secrets in code or files |
| Audit logging | Access logs for data pulls, agent queries and tool calls | Needed for enterprise trust |

### 4.3 Production privileges

Do not ask for these until the production scope is approved:

| Privilege | Exact ask | Notes |
|---|---|---|
| Production integration route | Approved connector pattern for SAP, internal apps and external providers | To be finalized after discovery |
| Network allowlisting/VPN/private endpoint | SFS-approved connectivity path | Depends on deployment model |
| Model gateway approval | Approved LLM/model provider path, logging policy and data retention stance | Needed before production agents |
| Role-based access control | Business-role to data-view mapping | Controls which teams can see which data |
| Monitoring and incident process | Owners, alerts, runbooks and support SLAs | Required for handover |

## 5. People access: named owners we need

This is the most important ask. Without named owners, the data work will become a generic IT request and stall.

| SFS owner needed | Why we need them | Exact ask from them | Use cases blocked without them |
|---|---|---|---|
| Executive sponsor | Cross-functional prioritisation and mandate | Confirm this discovery is approved and ask each function to nominate owners | All |
| Amit / Project Leap business owner | Coordination and decision routing | Own the working-session calendar and unblock missing stakeholders | All |
| SFS IT lead | Overall access path and system constraints | Confirm data-sharing route, environments, security gates and source-system contacts | All |
| SAP Basis / BW / Power BI owner | SAP extract route | Confirm whether SAP BW / Power BI can expose the needed read-only extracts and schemas | Enterprise, Field Performance, Dealer Profiles, Procurement, Stock |
| SAP SD owner | Sales, billing, pricing and dealer/customer master | Validate sales/billing, dealer master and pricing/scheme data availability | Enterprise, Field #1, #3, #4, #6, #8 |
| SAP MM owner | Purchase register, material, vendor and inventory | Validate PO-line, vendor, material, HSN and stock data availability | Procurement #1, #2, #3, #4, #5, #6, Field #7 |
| SAP FI/CO owner | Receivables, collections, GL/P&L, finance metric definitions | Validate receivables, collections, ageing and finance extracts | Enterprise, Field #1, Dealer Profiles, Churn |
| Master Data / Data Governance owner | Dealer/vendor/material/employee/HSN crosswalks and product hierarchy | Own the ID matching problem across SAP, Growthbook, Saathi, Concur and external data | Almost every joined use case |
| Growthbook admin/product owner | Field activity data | Confirm event schema, history, dealer/employee IDs and whether secondary sales/liquidation is captured | Field #1, #2, #4, #5, #8 |
| Saathi app owner | Dealer engagement, notes, visits and voice capture | Confirm live schema, export/API path, notes structure, voice/call status and intervention logs | Field #2, #4, #5, #8, Scheme Chatbot |
| Field Excellence / Sales Ops lead | Targets, schemes, dealer tiers and field workflows | Provide target files, scheme process, dealer classification and activity workflow context | Field #1, #3, #4, #5, #6, #8 |
| Procurement head | Procurement prioritisation and spend taxonomy | Confirm procurement wave priorities, category owners and BPV/spend taxonomy workshop | Procurement #1 to #6 |
| Procurement category managers | Category rules, should-cost and negotiation context | Define categories, commodities, negotiation outcome capture and should-cost assumptions | Procurement #1, #3, #4, #6 |
| Ariba owner | Supplier/RFQ/onboarding workflow | Confirm live/planned status and export/API path | Procurement #3, #4, #5 |
| Concur owner | Expense connector | Provide expense schema, export/API route and mapping to employee/cost centre/territory | Field Performance and Historical Spend |
| Complinity owner | Vendor license/compliance connector | Provide vendor compliance schema, export/API route and mapping to SAP vendor master | Historical Spend and Vendor Credit/Fraud |
| External-data contracting owner | EXIM, commodity, GST, MCA, credit and litigation subscriptions | Confirm existing providers or approve shortlist/contracting path | Procurement #2, #3, #5, #6 |
| Legal / Compliance / Data Privacy | External risk data, voice/call capture, retention and consent | Approve posture for GST/MCA/credit/litigation data and dealer voice/call recording/classification | Vendor Credit/Fraud, Dealer Profiles, Sales Coaching |
| Azure / Security owner | Tenant, SSO, logging, data residency and model gateway | Confirm where pilot runs and what security controls are mandatory | All production pilots |
| Logistics owner | Vendor-led logistics track | Confirm current logistics systems, vendors and fit-gap process | Logistics #1 to #5 |

## 6. Meetings and workshops to schedule

The meeting plan should show SFS how the 146-field map gets closed progressively. "Completed discovery" does not mean the field is production-integrated. It means one of three things is true:

- For source-system fields: source owner, extraction route, sample/schema, grain and join keys are confirmed.
- For external-provider fields: provider route, contracting owner, legal posture, identifiers and refresh cadence are confirmed.
- For computed/derived fields: business owner, definition/formula, examples and validation tests are confirmed.

| Meeting | New fields dispositioned | Cumulative fields dispositioned | Use cases advanced out of 15 | What gets closed |
|---|---:|---:|---|---|
| 1. Executive alignment and kickoff | 0 | 0 / 146 | All 15 at owner/calendar level | No field-level discovery yet; owner mandate and calendar for all 146 fields |
| 2. IT, SAP and security access design | 0 | 0 / 146 | All 15 at access-route level | Access route for the 88 source/provider fields; field count starts once samples/schemas are reviewed |
| 3. SAP data working session | 40 | 40 / 146 | All 15, because every mapped use case has at least one SAP dependency | SAP sales, dealer/customer, finance, purchase, vendor, material and stock fields |
| 4. Field-force systems working session | 44 | 84 / 146 | EA #1; FF #1 to #8; Proc #1 for Concur expense context | 15 Growthbook/Saathi/Concur/target/scheme/document source fields plus 29 field-force computed-field definitions |
| 5. Procurement systems working session | 46 | 130 / 146 | Proc #1 to #6; EA #1 for spend/procurement metrics | 20 procurement/source/provider fields plus 26 procurement computed-field definitions |
| 6. Finance and metric dictionary workshop | 3 | 133 / 146 | EA #1; also standardises metric language reused by FF #1, FF #6, FF #8 and Proc #1 | Enterprise Assistant computed fields: metric dictionary, query log/digest logic and golden-question definitions |
| 7. Master-data and crosswalk workshop | 0 | 133 / 146 | All 15, because dealer/vendor/material/employee/HSN crosswalks govern joins across the full map | No new unique fields; validates the crosswalks that make SAP, Growthbook, Saathi, Concur, Ariba and external data joinable |
| 8. Legal, compliance and privacy review | 13 | 146 / 146 | Proc #4, #5; FF #8; plus voice/call governance for FF #4 and FF #5 | External risk/compliance fields: GST/GSP, MCA21, credit bureau and litigation, plus voice/call governance already counted in field-force fields |
| 9. Wave triage and scope readout | 0 | 146 / 146 | All 15 classified into build, discovery, external-data or new-capture tracks | All 146 fields are classified into ready, definition-led, external-data gated, net-new-capture or out-of-scope |

The highest-value point to make to SFS: by the end of Meetings 3 and 4, we should have dispositioned **84 of 146 fields**, including the data base for Enterprise Assistant, Field Performance and Dealer Profiles. That is enough to validate the Wave 1 build path while the remaining procurement, external-data and legal items continue in parallel.

### Meeting 1: Executive alignment and working-session kickoff

**Duration:** 60 minutes
**Attendees:** Amit, executive sponsor, SFS IT lead, field force lead, procurement lead, finance lead, Conformal
**Purpose:** confirm mandate, owners, priority use cases and data-sharing path.

**Outputs required:**

- Named source owners.
- Agreement that discovery starts with masked samples.
- Confirmation of Wave 1 focus: Enterprise Assistant, Field Performance, Dealer Profiles.
- Agreement on data-room or transfer mechanism.

### Meeting 2: IT, SAP and security access design

**Duration:** 90 minutes
**Attendees:** SFS IT, SAP Basis/BW, Power BI owner, SAP SD/MM/FI owners, Azure/security owner, Conformal
**Purpose:** decide extraction path and security model.

**Exact agenda:**

1. Confirm SAP landscape and whether SFS is on one S/4HANA instance for SD/MM/FI/stock.
2. Confirm existing SAP BW / Power BI datasets for sales, purchase, finance and inventory.
3. Confirm whether line-level extracts are possible from BW/Power BI.
4. If not, choose fallback: CDS/OData, SLT, flat-file job, SFTP, Azure Blob or other route.
5. Confirm masking/anonymisation policy for discovery data.
6. Confirm pilot environment options: SFS Azure tenant vs Conformal controlled environment.

**Outputs required:**

- Extraction route decision.
- Data transfer mechanism.
- Security constraints.
- Owner for each SAP extract.

### Meeting 3: SAP data working session

**Duration:** 2 hours
**Attendees:** SAP SD, MM, FI/CO, inventory, BW/Power BI, master-data owners, Conformal
**Purpose:** validate SAP fields and join keys.

**Exact agenda:**

1. SD sales/billing extract.
2. Customer/dealer master.
3. FI receivables and collections.
4. MM purchase register.
5. Vendor master.
6. Material master and HSN mapping.
7. Stock/inventory snapshots.
8. Crosswalks: dealer, vendor, material, employee, HSN.

**Outputs required:**

- Sample extract list and due date.
- Data dictionary owners.
- Join-key confirmation.
- Known data-quality gaps.

### Meeting 4: Field force systems working session

**Duration:** 2 hours
**Attendees:** Field Excellence/Sales Ops, Growthbook owner, Saathi owner, SAP SD owner, Concur owner, Legal if voice/call data is discussed, Conformal
**Purpose:** validate Growthbook, Saathi, targets, schemes, dealer profiles and field expenditure.

**Exact agenda:**

1. Growthbook event schema and whether IDs match SAP.
2. Whether secondary sales/liquidation/PoG is captured anywhere today.
3. Saathi live status, dealer notes, visit logs and voice/call capture status.
4. Target files and field hierarchy.
5. Scheme participation and scheme circular source of truth.
6. Concur field expense mapping.

**Outputs required:**

- Growthbook and Saathi sample exports.
- Target and scheme sample files.
- Decision on secondary sales/liquidation capture.
- Legal follow-up if voice/call recording is in scope.

### Meeting 5: Procurement systems working session

**Duration:** 2 hours
**Attendees:** Procurement head, category managers, SAP MM, Ariba owner, Complinity owner, external-data contracting owner, Conformal
**Purpose:** validate procurement data and external dependencies.

**Exact agenda:**

1. Purchase register and vendor/material master coverage.
2. Spend taxonomy and category hierarchy.
3. BPV and anomaly definitions.
4. Complinity vendor license data.
5. Ariba live/planned status and RFQ/onboarding data.
6. EXIM, commodity and should-cost provider posture.
7. Vendor risk sources: GST, MCA, credit bureau, litigation.

**Outputs required:**

- PO-line and vendor compliance samples.
- Procurement category owner list.
- External data provider decision path.
- Spend taxonomy workshop date.

### Meeting 6: Finance and metric dictionary workshop

**Duration:** 90 to 120 minutes
**Attendees:** CFO/controller office, SAP FI/CO owner, Sales Ops, Procurement, Conformal
**Purpose:** define trusted metrics for the Enterprise Assistant and dashboards.

**Exact agenda:**

1. Revenue, margin, PBDIT, DSO and working-capital definitions.
2. Target-attainment and variance definitions.
3. Finance data grain and approved visibility.
4. Official metric owners.
5. Golden questions leadership wants the assistant to answer.

**Outputs required:**

- First metric dictionary.
- Golden-question list.
- Finance extract approval path.

### Meeting 7: Master-data and crosswalk workshop

**Duration:** 90 minutes
**Attendees:** Master Data/Data Governance, SAP SD/MM, Growthbook, Saathi, Concur, Ariba, Conformal
**Purpose:** solve the real integration blocker: IDs.

**Exact agenda:**

1. Dealer/customer ID across SAP, Growthbook and Saathi.
2. Employee/TBM/MGO ID across SAP, Growthbook, Saathi and Concur.
3. Vendor ID across SAP, Complinity, Ariba and external data.
4. Material/SKU/HSN mapping across SAP and EXIM.
5. Product hierarchy and cross-BU hierarchy.

**Outputs required:**

- Owner for each crosswalk.
- Sample crosswalk file.
- Data-quality risks.
- Decision process for hierarchy corrections.

### Meeting 8: Legal, compliance and privacy review

**Duration:** 60 to 90 minutes
**Attendees:** Legal, compliance, data privacy, SFS IT/security, Saathi owner, external-data contracting, Conformal
**Purpose:** approve boundaries for external risk data and voice/call capture.

**Exact agenda:**

1. GST, MCA, credit bureau and litigation data use.
2. Dealer voice notes and call recording/classification.
3. Consent, retention and access policy.
4. PII masking for discovery.
5. Model provider and data-retention restrictions.

**Outputs required:**

- Permitted data categories.
- Red lines.
- Consent/retention requirements.
- Required contract clauses for external providers.

### Meeting 9: Wave triage and scope readout

**Duration:** 60 minutes
**Attendees:** Amit, executive sponsor, IT, function leads, Conformal
**Purpose:** convert discovery findings into Wave 1 and Wave 2 scope.

**Outputs required:**

- Confirm Wave 1 scope.
- Confirm blocked use cases and blockers.
- Confirm data foundation build plan.
- Confirm proposal structure and commercial next step.

## 7. Minimum discovery data pack

If SFS wants a single checklist to circulate internally, use this.

| # | Data pack item | Source owner |
|---:|---|---|
| 1 | 36 months SAP purchase register at PO-line grain | SAP MM |
| 2 | 36 months SAP sales and billing at invoice-line or order-line grain | SAP SD |
| 3 | 24 to 36 months collections and receivables ageing | SAP FI/CO |
| 4 | Current material master with hierarchy, HSN, UoM and active flag | SAP MM / Master Data |
| 5 | Current vendor master with GSTIN, PAN, legal name, region, category and active flag | SAP MM / Vendor Master |
| 6 | Current customer/dealer master with territory, credit terms, credit limit, onboarding date and assigned field owner | SAP SD / Customer Master |
| 7 | Field hierarchy mapping: ZBM, RBM, TBM, MGO and territories | Sales Ops |
| 8 | Growthbook activity export for at least 12 months with SAP-matching dealer and employee IDs | Growthbook owner |
| 9 | Saathi dealer profile, visit and notes schema, plus export if live | Saathi owner |
| 10 | Target and incentive files by period, field role, SKU/product and territory | Sales Ops |
| 11 | Scheme circular repository, active scheme list, eligibility rules and credit policy/commercial terms | Scheme owner |
| 12 | Inventory snapshot by plant, storage location, SKU, batch and expiry if available | SAP Inventory/MM |
| 13 | Concur expense export with employee, category, amount, cost centre and date | Concur owner |
| 14 | Complinity vendor licence/compliance export with vendor ID, PAN/GSTIN, status and validity | Complinity owner |
| 15 | Ariba supplier/RFQ/onboarding export if live, or current source of RFQ/onboarding data if not | Ariba/procurement owner |
| 16 | External provider inventory: EXIM, commodity, GST/GSP, MCA21, credit bureau, litigation/court, labour/utility | External-data contracting |
| 17 | Historical review decks/KPI packs and standard business-reporting templates | CFO/Controller office |

## 8. Specific unresolved questions SFS should answer

These are the questions that most directly affect feasibility and sequencing.

1. Can Conformal receive read-only extracts from the existing SAP BW / Power BI layer?
2. If BW/Power BI cannot expose line-level data, what is the approved fallback route: CDS/OData, scheduled flat file, SLT, SFTP or Azure Blob?
3. Are SD, MM, FI/CO and inventory in one SAP S/4HANA instance or multiple systems?
4. Does Growthbook capture only activities, or does it also capture secondary sales, liquidation and PoG?
5. Is Saathi live for SFS? If yes, what data is structured versus free text?
6. Is voice or call recording live, planned or not approved?
7. Where is scheme eligibility officially defined: SAP pricing, scheme circulars, Excel trackers, claims process or another system?
8. Are sales targets maintained in Excel, SAP, Power BI, Growthbook or another source?
9. Who owns the dealer/vendor/material/employee/HSN crosswalks?
10. Is Ariba live, in rollout or planned? If not live, where is supplier/RFQ/onboarding workflow captured?
11. Which EXIM, commodity, GST/GSP, MCA21, credit and litigation data providers does SFS already subscribe to?
12. What is the approved legal posture for storing and analyzing external vendor-risk data?
13. Is dealer churn currently defined and labelled anywhere?
14. Are intervention logs captured after a churn risk or sales decline action?
15. What is the SFS-approved deployment path: SFS Azure tenant, Conformal-hosted VPC, or another environment?

## 9. Recommended sequencing of asks

### Within 3 business days

SFS confirms:

- Executive sponsor and Amit-led coordination path.
- Named owners for SAP, Growthbook, Saathi, Concur, Complinity, Ariba, master data, legal, security, field force and procurement.
- Approved data-sharing mechanism for masked samples.
- Dates for the first four working sessions: IT/SAP/security, SAP data, field force systems, procurement systems.

### Within 7 to 10 business days

SFS shares:

- SAP BW/Power BI dataset inventory and available schemas.
- Masked sample extracts for SAP sales, purchase, finance, master data and inventory.
- Growthbook and Saathi schemas/samples.
- Target, scheme and circular samples.
- Concur and Complinity sample exports.
- Ariba status and sample export if live.

### Within 2 to 3 weeks

SFS and Conformal complete:

- Metric dictionary workshop.
- Spend taxonomy and BPV workshop.
- Master-data crosswalk workshop.
- Field-force workflow and secondary-sales/liquidation validation.
- External-data and legal posture review.
- Wave 1/Wave 2 triage readout.

## 10. What Conformal will do with these asks

Once SFS provides the owners and first data pack, Conformal will:

1. Profile each extract for grain, completeness, history, duplicates, nulls and join keys.
2. Build the first raw and standardised columnar tables.
3. Create dealer, vendor, material, employee and HSN crosswalks.
4. Build the first gold marts for Enterprise Assistant, Field Performance and Dealer 360.
5. Run a small set of golden questions on real SFS data.
6. Classify each use case as extraction-led, definition-led, external-data gated or new-capture required.
7. Return a validated Wave 1 scope with data risks, blockers, owners and implementation plan.

## 11. Short version to send Amit

Hi Amit,

As a next step, we would like to run a focused data-readiness sprint with the SFS team. The objective is not to ask for full production credentials upfront. We want to validate the source-system truth underneath the Project Leap use cases using masked extracts, schemas and short working sessions with the right owners.

The core asks from SFS are:

1. Confirm the SAP extraction route, ideally read-only extracts from the existing SAP BW / Power BI layer for sales, purchase, finance, master data and inventory.
2. Share masked sample extracts for SAP SD, MM, FI/CO, inventory, dealer/vendor/material masters, Growthbook, Saathi, Concur, Complinity and scheme/target files.
3. Nominate owners from SAP, IT/security, finance, field force, procurement, master data, Growthbook, Saathi, Concur, Complinity, Ariba, legal/compliance and external-data contracting.
4. Schedule working sessions on SAP access, field-force systems, procurement systems, finance metrics, master-data crosswalks, legal/privacy and use-case triage.
5. Confirm open items: secondary sales/liquidation/PoG capture, Saathi voice/call capture, Ariba rollout status, external provider subscriptions and the approved pilot environment.

With this, Conformal can validate which use cases are ready to build first, which require business definitions, and which need new data capture. Our recommendation is to use this sprint to confirm Wave 1 around Enterprise Assistant, Field Performance and Dealer Profiles while building the shared data foundation that later procurement, churn, scheme and visibility use cases reuse.
