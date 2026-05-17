import json, collections, re, html
from pathlib import Path
from datetime import date

ROOT = Path('/Users/pariksj/Desktop/Projects/dcmsriram')
rows = json.load(open(ROOT/'conformal/notion-data-fields-full-db-selected.json'))
project = json.load(open(ROOT/'conformal/notion-project-leap-full-dataset.json'))
meta = {u['Name']: u for u in project['useCases']}
by = collections.defaultdict(list)
for r in rows:
    for uc in r['relatedUseCases']:
        by[uc].append(r)

ORDER = [
'Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)',
'Field Force #1 - Field Performance Tracking Dashboard',
'Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)',
'Procurement #1 - Historical Spend Analysis & Price Insights',
'Field Force #6 - Unified Product & Partner-Level Visibility',
'Field Force #7 - Real-Time Warehouse Stock Visibility',
'Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot',
'Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk',
'Procurement #4 - AI-Led Vendor Identification & Recommendation',
'Procurement #3 - AI-Driven Preparation Material for Negotiations',
'Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products)',
'Procurement #2 - Real-Time Import Data Analysis',
'Procurement #5 - Vendor Creditworthiness & Fraud Check',
'Field Force #5 - AI-Enabled Sales Coaching',
'Field Force #2 - Activity Analytics (Growthbook + SAP)',
]

TIER_LABELS = {
    'easy': 'Fast start', 'pilot': 'Strong pilot', 'moderate': 'Moderate integration',
    'external': 'External-data gated', 'workshop': 'Workshop-heavy', 'assumption': 'Discovery-only'
}

# Convert typographic punctuation and symbols to ASCII so client artifacts do not contain em dashes.
def clean(s):
    if s is None:
        return ''
    s = str(s)
    replacements = {
        '\u2014': '-', '\u2013': '-', '\u2212': '-', '\u2192': '->', '\u00d7': 'x',
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u00a0': ' ',
        '\u2022': '-', '\u2026': '...', '\u20b9': 'INR ', '\u2265': '>=', '\u2264': '<=',
        '\u00b7': '-', '\u2011': '-', '\u00ad': '', '\u2122': ''
    }
    for a, b in replacements.items():
        s = s.replace(a, b)
    s = s.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'\s+', ' ', s).strip()

def esc(s):
    return html.escape(clean(s), quote=True)

def md(s):
    return clean(s).replace('|', '\\|')

def route(system, group):
    system = clean(system); group = clean(group)
    if group == 'SAP':
        if 'Sales' in system or 'Customer' in system:
            return 'Primary route: SAP BW / Power BI extract. Fallback: S/4 CDS/OData or scheduled SD/customer-master export.'
        if 'Purchase' in system or 'Vendor' in system or 'Material' in system:
            return 'Primary route: SAP BW / Power BI or MM extract. Fallback: S/4 CDS/OData or scheduled PO/vendor/material export.'
        if 'Stock' in system or 'Inventory' in system:
            return 'Primary route: BW inventory cube or scheduled stock snapshot by plant, warehouse, SKU and date.'
        if 'Financial' in system:
            return 'Primary route: SAP BW / FI-CO extract or controlled receivables and GL export at approved grain.'
        return 'Primary route: SAP BW / Power BI. Fallback: read-only S/4 CDS/OData or scheduled controlled export.'
    if system == 'Concur':
        return 'Concur API or scheduled expense export; map employee, cost centre, category and date to SAP dimensions.'
    if system == 'Complinity':
        return 'Complinity API or scheduled vendor-compliance export; map vendor ID, PAN/GSTIN and validity dates.'
    if system == 'Growthbook':
        return 'Growthbook event export/API with employee, dealer, activity type, timestamp and outcome mapped to SAP IDs.'
    if system == 'Saathi App':
        return 'Saathi DB/API/export; confirm dealer profile, visit notes, voice capture, intervention logs and consent controls.'
    if system == 'Excel - Targets / Schemes':
        return 'Controlled file repository or SharePoint/Drive drop; standardise owner, version, period and upload cadence.'
    if 'Internal Docs' in system:
        return 'Central circular/PDF repository; ingest with metadata, version, applicability and owner.'
    if system == 'Ariba':
        return 'Ariba export/API for supplier onboarding, RFQs and contracts; map supplier IDs to SAP vendor IDs.'
    if 'EXIM' in system:
        return 'External EXIM/customs provider; ingest by HSN, importer/exporter, date, quantity, CIF/landed cost and origin.'
    if system in ['GST Portal (via GSP)', 'MCA21', 'Credit Bureau', 'Court / Litigation Records']:
        return 'Approved external risk provider/API; requires legal sign-off and entity-resolution keys.'
    if group.startswith('External'):
        return 'External provider API/export; confirm provider, terms, refresh, identifiers and history.'
    if group == 'Computed / Derived':
        return 'Computed by Conformal in the semantic layer after base data lands; requires definition owner and examples.'
    if group == 'Logistics':
        return 'TMS/vendor export or fit-gap track; do not custom-build until source system/vendor is selected.'
    return 'Confirm source owner, export route, history, grain and refresh cadence.'

def ask_for(r):
    a = r['availability']; g = r['sourceGroup']
    if a == 'Available':
        return 'Provide masked sample extract, schema/data dictionary, history range, join keys and refresh cadence.'
    if a == 'Partial':
        return 'Confirm owner and integration gap; provide sample export plus mapping rules needed to make it usable.'
    if g == 'Computed / Derived':
        return 'No raw-field ask. Confirm definition, formula, owner and examples; Conformal computes it.'
    if g.startswith('External'):
        return 'Confirm existing provider or nominate contracting owner and approve provider shortlist.'
    if g == 'Internal Apps':
        return 'Confirm whether workflow is live; if not, approve net-new capture and name owner.'
    if g == 'SAP':
        return 'Confirm whether field exists in SAP master/transaction layer; if not, name master-data owner or alternate source.'
    return 'Confirm source and capture mechanism with owner.'

def counts_for(uc):
    c = collections.Counter(r['availability'] for r in by[uc])
    return len(by[uc]), c.get('Available',0), c.get('Partial',0), c.get('Unavailable',0)

def decision_for(uc):
    if uc in ORDER[:3]:
        return 'Wave 1 build candidate'
    if uc == 'Procurement #1 - Historical Spend Analysis & Price Insights':
        return 'Wave 1 discovery, Wave 2 build candidate'
    tier = meta.get(uc, {}).get('Readiness Tier', '')
    if tier == 'pilot': return 'Wave 2 build candidate after foundation'
    if tier == 'moderate': return 'Wave 2 after source-owner validation'
    if tier == 'external': return 'External-data discovery before build claim'
    if tier == 'workshop': return 'Workshop-heavy; do not anchor Wave 1'
    if tier == 'assumption': return 'Discovery-only; no build claim yet'
    return 'Triage after source validation'

# Source summary
availability = collections.Counter(r['availability'] for r in rows)
source_group_counts = collections.defaultdict(collections.Counter)
for r in rows:
    source_group_counts[r['sourceGroup']][r['availability']] += 1
external = [r for r in rows if r['sourceGroup'].startswith('External')]
netnew = [r for r in rows if r['availability'] == 'Unavailable' and r['sourceGroup'] in ['Internal Apps','SAP','Logistics']]
computed = [r for r in rows if r['availability'] == 'Unavailable' and r['sourceGroup'] == 'Computed / Derived']

# ------------------ client markdown ------------------
md_lines = []
md_lines += [
'# SFS Project Leap - Data Deep-Dive, Integration Vision and Working Session Asks',
'',
'Prepared for Shriram Farm Solutions',
'Prepared by Conformal',
'Last updated: May 18, 2026',
'',
'## 1. Purpose',
'',
'SFS shared the Project Leap use-case document with Conformal. We reviewed those use cases and decomposed the 15 custom-build use cases into the individual data fields needed to move from prototype to production. We then mapped each field to the likely source system, assessed whether it is available, partially available, computed, externally sourced or net-new capture, and converted that into a concrete ask pack for the next SFS working session.',
'',
'This document is not a final scope or commercial proposal. It is a data-readiness working paper. Its purpose is to help SFS and Conformal validate source-system truth quickly, agree the right owners, and begin the first discovery sprint with specific, low-risk data asks.',
'',
'## 2. Executive summary',
'',
'- We mapped 146 fields across 15 custom-build use cases. Logistics is treated separately as a buy-and-customise vendor/TMS track.',
'- The headline readiness split is 33 Available, 19 Partial and 94 Unavailable.',
'- The 94 Unavailable fields should not be read as 94 blockers. 58 are computed by Conformal once base data lands, 27 are external feeds that Conformal can source, and roughly 9 require SFS workflow or master-data capture decisions.',
'- The first build should start with reusable foundations: SAP BW / Power BI sales and finance extracts, Growthbook/Saathi field activity, SAP MM procurement extracts, and master-data crosswalks.',
'- Recommended Wave 1: Enterprise Assistant, Field Performance Tracking Dashboard and Dealer Profiles. These create the data spine for later field-force, procurement, churn, scheme and enterprise assistant use cases.',
'',
'## 3. How to read the field analysis',
'',
'We worked from the SFS-provided use-case document. For each use case, we asked four practical questions:',
'',
'1. What data fields would this need in production?',
'2. Which source system is most likely to hold each field?',
'3. Is the field available today, partially available, computed, externally sourced, or not captured?',
'4. What exact owner, extract or decision is needed from SFS to validate it?',
'',
'Because this is derived from the use-case document and referenced systems, every finding should be validated with SFS source owners before final pricing or production scope.',
'',
'## 4. Readiness snapshot',
'',
'| Readiness bucket | Count | Practical meaning |',
'|---|---:|---|',
 f'| Available | {availability["Available"]} | Likely exists in an SFS-owned system, mostly SAP. Discovery asks for masked extracts and schemas. |',
 f'| Partial | {availability["Partial"]} | Exists but needs integration, cleanup, mapping or scope confirmation. |',
 f'| Unavailable | {availability["Unavailable"]} | Not a direct field today. It may still be computed by Conformal or sourced externally. |',
 f'| Total | {len(rows)} | Field-level data map across 15 mapped build use cases. |',
'',
'The Unavailable fields split as follows:',
'',
'| Gap type | Count | Primary action |',
'|---|---:|---|',
 f'| Computed / derived | {len(computed)} | Conformal computes these in the semantic layer after base data lands. SFS provides definitions and examples, not raw data. |',
 f'| Externally sourced | {len(external)} | Conformal integrates external providers such as EXIM, GST/GSP, MCA21, credit, commodity, FX, labour and utilities. SFS confirms provider posture and contracting owner. |',
 f'| Net-new SFS capture or governance | {len(netnew)} | SFS confirms whether the workflow or master-data field exists. If not, SFS names the owner and approves capture. |',
'',
'## 5. Recommended sequencing',
'',
'| Sequence | Use cases | Why this comes here | Reusable foundation created |',
'|---|---|---|---|',
'| Wave 0: foundation | Shared data layer | Required for trust, speed and re-use | Raw landing, standard columnar layer, ID crosswalks, metric dictionary, access control, audit trail |',
'| Wave 1 build | Enterprise Assistant, Field Performance, Dealer Profiles | Strong SFS-owned data base and direct ROI alignment | Enterprise KPI mart, field performance mart, dealer 360, semantic SQL/chart/retrieval tools |',
'| Wave 1 discovery / Wave 2 build | Historical Spend | SAP purchase base is strong, but taxonomy and BPV require procurement sign-off | Spend cube, vendor/material dimensions, variance and anomaly framework |',
'| Wave 2 build | Product/Partner Visibility, Warehouse Stock, Scheme Chatbot, Churn Risk, Vendor ID | Mostly owned data, but requires definitions and source-owner validation | Product/partner mart, stock mart, scheme eligibility, churn labels, vendor scoring |',
'| External-data discovery | Negotiation Prep, Should-Cost, Import Analysis, Vendor Credit/Fraud | Depends on EXIM, commodity, GST, MCA, credit or litigation providers | External connector layer and provider governance |',
'| Discovery-only | Activity Analytics | SFS document gives a name but no detail. Field map is inferred and must be scoped with SFS. | Activity taxonomy and field workflow definition |',
'| Separate track | Logistics use cases | Buy-and-customise vendor/TMS track, not a custom AI build | Vendor fit-gap, shipment/POD/lane integration if SFS proceeds |',
'',
'## 6. Integration vision',
'',
'The architecture should make source-system access a shared foundation, not a one-off integration per use case.',
'',
'1. Source read access: SAP BW / Power BI, SAP SD/MM/FI/Inventory, Growthbook, Saathi, Concur, Complinity, Ariba and approved external data providers.',
'2. Raw landing: store extracts exactly as received, partitioned by source and date, with run metadata.',
'3. Standard columnar layer: typed tables, data quality checks, ID crosswalks and refresh timestamps.',
'4. Gold semantic marts: dealer 360, field performance, enterprise KPIs, spend cube, stock visibility, vendor score, scheme eligibility and churn risk.',
'5. Governed agent tools: SQL over semantic views, retrieval over policy/circular documents, chart/report generation, audit logs and evaluation sets.',
'',
'Agents should query governed semantic views. They should not connect directly to SAP, Concur, Saathi, Ariba or other source systems.',
'',
'## 7. How we propose to extract data',
'',
'| System | Preferred route | First ask | Owner needed |',
'|---|---|---|---|',
'| SAP BW / Power BI | Read-only extract from existing BW queries, Power BI semantic model or dataflow | Dataset inventory, data dictionary, sample export, refresh cadence and preserved join keys | SAP Basis/BW and Power BI owner |',
'| SAP SD | Existing BW sales/billing cube; fallback to S/4 CDS/OData or scheduled SD export | Sales/billing line extract with dealer, material, territory, date, quantity, value and pricing/scheme refs | SAP SD owner |',
'| SAP MM | Existing BW purchasing cube; fallback to S/4 CDS/OData or scheduled MM export | PO line extract with vendor, material, HSN, UoM, quantity, price, currency and GRN status | SAP MM owner |',
'| SAP FI/CO | Existing BW/Power BI finance model; fallback to controlled FI/CO export | Receivables, collections, ageing, GL/P&L and budget/target metrics at approved grain | Finance FI/CO owner |',
'| SAP Stock / Inventory | BW inventory cube or scheduled stock snapshot | On-hand stock, open orders, ATP if available and plant/warehouse mapping | SAP inventory/MM owner |',
'| Growthbook | API or event export | 12-month activity event export with employee ID, dealer ID, timestamp, activity type and outcome | Growthbook owner |',
'| Saathi | API/export from app DB | Dealer profile, visit notes, voice/call capture status, intervention logs and chatbot logs | Saathi owner plus legal/compliance |',
'| Concur | Concur API or scheduled expense export | Expense entries with amount, category, employee, cost centre, date and approval status | Concur owner |',
'| Complinity | API or scheduled vendor-compliance export | Vendor licence status, validity date, vendor ID and PAN/GSTIN if available | Complinity owner |',
'| Ariba | Ariba API/export | Supplier onboarding status, RFQ events, contracts and supplier-to-SAP-vendor mapping | Ariba owner |',
'| External data | Provider API/export | Existing subscriptions, provider shortlist, permitted use and contracting owner | External-data contracting plus legal |',
'| Logistics/TMS | Vendor/TMS export once source is known | Lane rates, shipment examples, POD examples and carrier status data | Logistics owner |',
'',
'## 8. Exact first ask pack',
'',
'| Owner | What they unblock | Exact ask for the working session | Use cases blocked until present |',
'|---|---|---|---|',
'| Executive sponsor | Cross-functional priority and decisions | Confirm the working-session mandate and nominate source owners | All |',
'| SFS IT lead | Access pattern and deployment constraints | Confirm target environment, security path and data-sharing mechanism | All |',
'| SAP Basis / BW / Power BI | SAP extraction route | Confirm read-only extract access off the existing SAP BW / Power BI layer | Enterprise, field, procurement and stock use cases |',
'| SAP SD owner | Sales, billing, dealer master and pricing | Provide masked sales/billing sample and pricing-condition availability | Field #1, #3, #4, #6, #8 and Enterprise |',
'| SAP MM owner | PO lines, vendor, material and inventory | Provide masked PO-line, vendor, material and stock samples | Procurement #1, #3, #4, #6 and Field #7 |',
'| SAP FI/CO owner | Receivables, collections and metric definitions | Provide collections/receivables sample and official metric definitions | Enterprise, Field #1 and Field #8 |',
'| Master Data / Governance | Crosswalks and hierarchies | Provide dealer/vendor/material/employee/HSN crosswalk ownership and product hierarchy decision process | Joined marts, Product/Partner Visibility, EXIM and Vendor ID |',
'| Growthbook / Saathi owners | Field activity and dealer interactions | Provide schemas, 12-month exports and voice/call capture status | Field #1, #2, #4, #5 and #8 |',
'| Concur / Complinity owners | Expense and vendor licence connectors | Provide export/API options and mapping owners | Procurement #1 and field expense views |',
'| Ariba owner | Supplier and RFQ workflow | Confirm rollout status, exports/APIs and supplier ID mapping | Procurement #3, #4 and #5 |',
'| External-data contracting | EXIM, commodity, GST, MCA, credit and litigation | Confirm existing subscriptions or approve provider selection | Procurement #2, #3, #5 and #6 |',
'| Legal / compliance | Risk data, voice capture and call recording | Confirm approval stance, consent, retention and classification rules | Procurement #5, Field #4 and Field #5 |',
'| Azure / security | VPC, SSO, audit, data residency and model gateway | Confirm approved tenant, logging, access groups and model path | All production agents |',
'',
'## 9. Initial masked data pack',
'',
'The first discovery sprint does not require production credentials. Masked samples are sufficient to validate schema, grain, data quality and join keys.',
'',
'1. 36 months SAP purchase register at PO-line grain.',
'2. 36 months SAP primary sales and billing at invoice-line grain.',
'3. 24 to 36 months collections and receivables ageing.',
'4. Current material master, including hierarchy, HSN, UoM and active flag.',
'5. Current vendor master, including GSTIN, legal name, region, category and active flag.',
'6. Current customer/dealer master, including territory, credit terms, onboarding date and assigned field owner.',
'7. Field hierarchy: ZBM, RBM, TBM and MGO mapping.',
'8. Growthbook activity export for at least 12 months with SAP-matching dealer and employee IDs.',
'9. Target and incentive files by period and field role.',
'10. Scheme circular repository and active scheme list.',
'11. Inventory snapshot by plant, storage location and SKU.',
'12. Concur SG&A export and Complinity vendor-licence export.',
'',
'## 10. Definition workshops required',
'',
'Computed fields need business definitions before they can become trusted metrics. These are decision workshops, not integration work.',
'',
'| Workshop | SFS owner needed | Defines | Unblocks |',
'|---|---|---|---|',
'| Enterprise metric dictionary | CFO/Controller plus Sales Ops | Revenue, margin, PBDIT, DSO, target attainment and metric ownership | Enterprise Assistant and every dashboard |',
'| Spend taxonomy and BPV rules | Procurement head and category managers | Category hierarchy, strategic classification, BPV logic and anomaly thresholds | Historical Spend, Vendor ID and Should-Cost |',
'| Product hierarchy | Master Data plus category owners | Unified cross-BU product hierarchy | Product/Partner Visibility and Enterprise Assistant |',
'| Partner scorecard and dealer tier | Sales Ops plus Field leadership | Dealer tier logic, scorecard formula and cross-sell rules | Field Performance, Dealer Profiles, Product Visibility and Churn |',
'| Churn and intervention logic | Sales Ops plus Finance/Collections | Churn definition, labels, intervention workflow and success criteria | Dealer Churn Risk |',
'| Scheme eligibility logic | Sales Ops plus scheme owner | Eligibility rules, source of truth and approval process | Scheme Chatbot |',
'| Negotiation outcome capture | Procurement category managers | Outcome logging workflow and learning loop | Negotiation Prep |',
'',
'## 11. Use-case readiness table',
'',
'| Use case | Fields | Available | Partial | Unavailable | Proposed treatment |',
'|---|---:|---:|---:|---:|---|',
]
for uc in ORDER:
    total, a, p, u = counts_for(uc)
    md_lines.append(f'| {md(uc)} | {total} | {a} | {p} | {u} | {md(decision_for(uc))} |')

md_lines += [
'',
'## 12. Detailed appendix: field-level asks',
'',
'The tables below list every assumed field, its readiness status, likely source system, extraction route and concrete ask. Computed fields should not be requested from SFS as raw data. They need definitions and validation examples, after which Conformal computes them in the semantic layer.',
]

av_order = {'Available':0, 'Partial':1, 'Unavailable':2}
for uc in ORDER:
    total, a, p, u = counts_for(uc)
    md_lines += ['', f'### {md(uc)}', '', f'Fields: {total}. Available: {a}. Partial: {p}. Unavailable: {u}. Treatment: {md(decision_for(uc))}.', '', '| Field | Status | Source system | Route | Ask |', '|---|---|---|---|---|']
    for r in sorted(by[uc], key=lambda x: (av_order.get(x['availability'], 9), x['sourceGroup'], x['sourceSystem'], x['fieldName'])):
        md_lines.append(f'| {md(r["fieldName"])} | {md(r["availability"])} | {md(r["sourceSystem"])} | {md(route(r["sourceSystem"], r["sourceGroup"]))} | {md(ask_for(r))} |')

client_md = '\n'.join(md_lines) + '\n'
(ROOT/'deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.md').write_text(client_md)

# ------------------ client HTML/PDF source ------------------
def table_rows_md_to_html(lines):
    return ''

def simple_table(headers, rows_list, cls=''):
    out = [f'<table class="{cls}"><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead><tbody>']
    for row in rows_list:
        out.append('<tr>' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>')
    out.append('</tbody></table>')
    return '\n'.join(out)

usecase_rows = []
for uc in ORDER:
    total, a, p, u = counts_for(uc)
    usecase_rows.append([esc(uc), str(total), str(a), str(p), str(u), esc(decision_for(uc))])

system_rows = [
['SAP BW / Power BI','Read-only extract from existing BW queries, Power BI semantic model or dataflows','Dataset inventory, data dictionary, sample export, refresh cadence and preserved join keys','SAP Basis/BW and Power BI owner'],
['SAP SD','Existing BW sales/billing cube; fallback to S/4 CDS/OData or scheduled SD export','Sales/billing line extract with dealer, material, territory, date, quantity, value and pricing/scheme refs','SAP SD owner'],
['SAP MM','Existing BW purchasing cube; fallback to S/4 CDS/OData or scheduled MM export','PO line extract with vendor, material, HSN, UoM, quantity, price, currency and GRN status','SAP MM owner'],
['SAP FI/CO','Existing BW/Power BI finance model; fallback to controlled FI/CO export','Receivables, collections, ageing, GL/P&L and budget/target metrics at approved grain','Finance FI/CO owner'],
['Growthbook','API or event export','12-month activity event export with employee ID, dealer ID, timestamp, activity type and outcome','Growthbook owner'],
['Saathi','API/export from app DB','Dealer profile, visit notes, voice/call capture status, intervention logs and chatbot logs','Saathi owner plus legal/compliance'],
['Concur','Concur API or scheduled expense export','Expense entries with amount, category, employee, cost centre, date and approval status','Concur owner'],
['Complinity','API or scheduled vendor-compliance export','Vendor licence status, validity date, vendor ID and PAN/GSTIN if available','Complinity owner'],
['Ariba','Ariba API/export','Supplier onboarding status, RFQ events, contracts and supplier-to-SAP-vendor mapping','Ariba owner'],
['External data','Provider API/export','Existing subscriptions, provider shortlist, permitted use and contracting owner','External-data contracting plus legal']
]

owner_rows = [
['Executive sponsor','Confirm mandate and nominate owners','All'],
['SFS IT lead','Confirm target environment, security path and data-sharing mechanism','All'],
['SAP Basis / BW / Power BI','Confirm read-only extract access off existing SAP BW / Power BI layer','Enterprise, field, procurement and stock'],
['SAP SD owner','Provide masked sales/billing sample and pricing-condition availability','Field #1, #3, #4, #6, #8 and Enterprise'],
['SAP MM owner','Provide masked PO-line, vendor, material and stock samples','Procurement #1, #3, #4, #6 and Field #7'],
['SAP FI/CO owner','Provide collections/receivables sample and official metric definitions','Enterprise, Field #1 and Field #8'],
['Master Data / Governance','Own dealer/vendor/material/employee/HSN crosswalks and product hierarchy','Joined marts, Product/Partner Visibility, EXIM and Vendor ID'],
['Growthbook / Saathi','Provide schemas, 12-month exports and voice/call capture status','Field #1, #2, #4, #5 and #8'],
['Concur / Complinity','Provide export/API options and mapping owners','Procurement #1 and field expense views'],
['External-data contracting','Confirm subscriptions or approve provider selection','Procurement #2, #3, #5 and #6'],
['Legal / compliance','Confirm risk data, voice capture and call recording posture','Procurement #5, Field #4 and Field #5']
]

appendix_html = []
for uc in ORDER:
    total, a, p, u = counts_for(uc)
    appendix_html.append(f'<section class="appendix-usecase"><h3>{esc(uc)}</h3><p class="meta">{total} fields. {a} available, {p} partial, {u} unavailable. {esc(decision_for(uc))}.</p>')
    appendix_html.append('<table class="field-table"><thead><tr><th>Field</th><th>Status</th><th>Source</th><th>Route and ask</th></tr></thead><tbody>')
    for r in sorted(by[uc], key=lambda x: (av_order.get(x['availability'], 9), x['sourceGroup'], x['sourceSystem'], x['fieldName'])):
        status = clean(r['availability'])
        appendix_html.append(f'<tr><td>{esc(r["fieldName"])}</td><td><span class="status {status}">{status}</span></td><td>{esc(r["sourceSystem"])}<br><span class="group">{esc(r["sourceGroup"])}</span></td><td>{esc(route(r["sourceSystem"], r["sourceGroup"]))}<br><b>Ask:</b> {esc(ask_for(r))}</td></tr>')
    appendix_html.append('</tbody></table></section>')

client_html = f'''<!doctype html>
<html><head><meta charset="utf-8"><title>Conformal SFS Data Deep-Dive and Asks</title>
<style>
@page {{ size: Letter; margin: 0.72in 0.7in 0.72in 0.7in; }}
* {{ box-sizing: border-box; }}
body {{ margin:0; font-family: Arial, Helvetica, sans-serif; color:#171917; background:white; font-size:10.5pt; line-height:1.45; }}
h1,h2,h3 {{ margin:0; line-height:1.15; color:#172019; }}
h1 {{ font-family: Georgia, 'Times New Roman', serif; font-size:31pt; font-weight:500; letter-spacing:-0.2pt; }}
h2 {{ font-size:15pt; margin-top:28px; padding-top:6px; border-top:1px solid #d9d8d3; }}
h3 {{ font-size:12pt; margin-top:20px; }}
p {{ margin:8px 0; }}
ul,ol {{ margin:8px 0 8px 22px; padding:0; }}
li {{ margin:3px 0; }}
.cover {{ height:9.4in; display:flex; flex-direction:column; justify-content:space-between; page-break-after:always; }}
.brand {{ color:#1f5b42; font-weight:700; letter-spacing:0.04em; text-transform:uppercase; font-size:9pt; }}
.cover-title {{ margin-top:1.3in; max-width:6.5in; }}
.subtitle {{ margin-top:18px; max-width:6.3in; color:#5e625f; font-size:12.5pt; line-height:1.5; }}
.cover-meta {{ border-top:1px solid #d9d8d3; padding-top:18px; color:#5e625f; }}
.callout {{ border-left:4px solid #b8232e; background:#fbf1f2; padding:11px 13px; margin:14px 0; color:#3b2528; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin:14px 0; }}
.stat {{ border:1px solid #d9d8d3; padding:12px; background:#fafaf8; min-height:86px; }}
.stat b {{ display:block; font-family:Georgia,serif; font-size:26pt; line-height:1; color:#1f5b42; }}
.stat span {{ display:block; margin-top:5px; font-size:8.5pt; color:#5e625f; text-transform:uppercase; letter-spacing:.04em; }}
table {{ width:100%; border-collapse:collapse; margin:10px 0 16px; page-break-inside:auto; }}
th {{ background:#f0efeb; color:#5e625f; font-size:7.8pt; text-transform:uppercase; letter-spacing:.04em; text-align:left; padding:6px 7px; border:1px solid #d9d8d3; }}
td {{ vertical-align:top; padding:6px 7px; border:1px solid #d9d8d3; font-size:8.7pt; }}
.compact td {{ font-size:8.2pt; }}
.field-table td {{ font-size:7.7pt; line-height:1.33; }}
.field-table th {{ font-size:7.2pt; }}
.status {{ font-weight:700; }} .Available {{ color:#177245; }} .Partial {{ color:#946012; }} .Unavailable {{ color:#b8232e; }}
.group {{ color:#777; font-size:7.2pt; }}
.section-break {{ page-break-before:always; }}
.appendix-usecase {{ page-break-before:always; }}
.meta {{ color:#5e625f; font-size:9pt; }}
.footer-note {{ margin-top:16px; font-size:8.5pt; color:#6a6e69; }}
.no-break {{ page-break-inside:avoid; }}
</style></head><body>
<section class="cover">
  <div><div class="brand">Conformal</div><div class="cover-title"><h1>SFS Project Leap<br>Data Deep-Dive, Integration Vision and Working Session Asks</h1><p class="subtitle">A field-level analysis of the SFS Project Leap use-case document, translated into source-system readiness, integration routes and concrete asks for the next working session.</p></div></div>
  <div class="cover-meta"><p><b>Prepared for:</b> Shriram Farm Solutions</p><p><b>Prepared by:</b> Conformal</p><p><b>Date:</b> May 18, 2026</p></div>
</section>
<h2>1. Purpose</h2><p>SFS shared the Project Leap use-case document with Conformal. We decomposed the 15 custom-build use cases into the individual fields needed to move from prototype to production, mapped those fields to likely source systems, and translated the result into integration routes and working-session asks.</p><div class="callout"><b>Important:</b> this is a data-readiness working paper, not a final scope or commercial proposal. The first SFS working session should validate owners, extracts, schemas, join keys and data quality before production scope is committed.</div>
<h2>2. Executive summary</h2><ul><li>We mapped <b>146 fields</b> across <b>15 custom-build use cases</b>. Logistics remains a separate buy-and-customise vendor/TMS track.</li><li>The readiness split is <b>33 Available</b>, <b>19 Partial</b> and <b>94 Unavailable</b>.</li><li>The 94 Unavailable fields are not 94 blockers. <b>58</b> are computed by Conformal, <b>27</b> are external feeds Conformal can source, and roughly <b>9</b> require SFS workflow or master-data decisions.</li><li>Recommended Wave 1: Enterprise Assistant, Field Performance Tracking Dashboard and Dealer Profiles.</li></ul>
<div class="grid3"><div class="stat"><b>146</b><span>Fields mapped</span></div><div class="stat"><b>58</b><span>Computed by Conformal</span></div><div class="stat"><b>27</b><span>External provider fields</span></div></div>
<h2>3. Recommended sequencing</h2>{simple_table(['Sequence','Use cases','Why this comes here','Foundation created'], [[esc('Wave 0: foundation'),esc('Shared data layer'),esc('Required for trust, speed and re-use'),esc('Raw landing, standard columnar layer, ID crosswalks, metric dictionary, access control and audit trail')],[esc('Wave 1 build'),esc('Enterprise Assistant, Field Performance, Dealer Profiles'),esc('Strong SFS-owned data base and direct ROI alignment'),esc('Enterprise KPI mart, field performance mart, dealer 360 and semantic agent tools')],[esc('Wave 1 discovery / Wave 2 build'),esc('Historical Spend'),esc('SAP purchase base is strong, taxonomy and BPV require procurement sign-off'),esc('Spend cube, vendor/material dimensions, variance and anomaly framework')],[esc('Wave 2 build'),esc('Product/Partner Visibility, Warehouse Stock, Scheme Chatbot, Churn Risk, Vendor ID'),esc('Mostly owned data, but requires definitions and source-owner validation'),esc('Product/partner mart, stock mart, scheme eligibility, churn labels and vendor scoring')],[esc('External-data discovery'),esc('Negotiation Prep, Should-Cost, Import Analysis, Vendor Credit/Fraud'),esc('Depends on EXIM, commodity, GST, MCA, credit or litigation providers'),esc('External connector layer and provider governance')],[esc('Discovery-only'),esc('Activity Analytics'),esc('SFS document gives a name but no detail'),esc('Activity taxonomy and field workflow definition')]], 'compact')}
<h2>4. Integration vision</h2><p>The architecture should make source-system access a shared foundation, not a one-off integration per use case. Data lands from SAP BW / Power BI, SAP modules, Growthbook, Saathi, Concur, Complinity, Ariba and external providers into a raw landing zone, then into typed columnar tables, then into governed semantic marts. Agents query the governed marts, not the operational source systems.</p>
<h2>5. How we propose to extract data</h2>{simple_table(['System','Preferred route','First ask','Owner needed'], [[esc(x) for x in row] for row in system_rows], 'compact')}
<h2>6. Exact first ask pack</h2>{simple_table(['Owner','Exact ask','Use cases blocked until present'], [[esc(r[0]), esc(r[1]), esc(r[2])] for r in owner_rows], 'compact')}
<h2>7. Initial masked data pack</h2><ol><li>36 months SAP purchase register at PO-line grain.</li><li>36 months SAP primary sales and billing at invoice-line grain.</li><li>24 to 36 months collections and receivables ageing.</li><li>Material, vendor and customer/dealer masters.</li><li>Field hierarchy and Growthbook activity export with SAP-matching dealer and employee IDs.</li><li>Target and incentive files, scheme circulars, inventory snapshot, Concur SG&A export and Complinity vendor-licence export.</li></ol>
<h2>8. Use-case readiness table</h2>{simple_table(['Use case','Fields','Available','Partial','Unavailable','Treatment'], usecase_rows, 'compact')}
<section class="section-break"><h2>9. Detailed field appendix</h2><p class="meta">Every assumed field is listed below with its status, likely source system, route and ask. Computed fields should not be requested as raw data from SFS.</p>{''.join(appendix_html)}</section>
</body></html>'''
(ROOT/'deliverables/Conformal_SFS_Data_Deep_Dive_and_Asks.html').write_text(client_html)

# ------------------ improved deck ------------------
def count_row(uc):
    t,a,p,u = counts_for(uc); return f'{t} fields: {a} A / {p} P / {u} U'

deck = f'''<!doctype html><html><head><meta charset="utf-8"><title>Conformal SFS Data Deep-Dive Deck</title>
<style>
@page {{ size: 1280px 720px; margin: 0; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#e7e5df; color:#171917; font-family: Arial, Helvetica, sans-serif; }}
.slide {{ width:1280px; height:720px; background:#f8f6f0; page-break-after:always; position:relative; overflow:hidden; }}
.slide.dark {{ background:#1f5b42; color:white; }}
.pad {{ position:absolute; inset:0; padding:54px 64px; }}
.brand {{ position:absolute; left:64px; bottom:32px; font-size:14px; color:#1f5b42; font-weight:700; }}
.dark .brand {{ color:white; }}
.page {{ position:absolute; right:64px; bottom:34px; font-size:11px; letter-spacing:.12em; color:#777a75; }}
.dark .page {{ color:rgba(255,255,255,.7); }}
.eyebrow {{ color:#b8232e; font-size:12px; text-transform:uppercase; letter-spacing:.14em; font-weight:800; margin-bottom:16px; }}
.dark .eyebrow {{ color:#f2d8d2; }}
h1 {{ font-family: Georgia, 'Times New Roman', serif; font-weight:500; line-height:1.08; letter-spacing:-.015em; margin:0; font-size:52px; max-width:980px; }}
h1.large {{ font-size:67px; max-width:950px; }}
h1 em {{ color:#b8232e; font-style:italic; }}
.dark h1 em {{ color:#f2d8d2; }}
.lead {{ color:#656a64; font-size:17px; line-height:1.55; max-width:820px; margin-top:20px; }}
.dark .lead {{ color:rgba(255,255,255,.82); }}
.meta {{ position:absolute; right:64px; top:58px; font-size:13px; letter-spacing:.1em; text-transform:uppercase; color:rgba(255,255,255,.78); }}
.rule {{ position:absolute; left:64px; right:64px; height:1px; background:#d9d4c8; }}
.dark .rule {{ background:rgba(255,255,255,.24); }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:22px; margin-top:34px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; margin-top:34px; }}
.grid4 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-top:30px; }}
.card {{ background:white; border:1px solid #ded9cf; border-radius:10px; padding:22px; min-height:142px; }}
.card h3 {{ margin:0 0 10px; font-family:Georgia,serif; font-size:22px; font-weight:500; }}
.card p {{ margin:0; color:#666b65; font-size:14px; line-height:1.52; }}
.stat {{ background:white; border:1px solid #ded9cf; border-radius:10px; padding:22px; min-height:176px; }}
.stat .n {{ font-family:Georgia,serif; font-size:58px; line-height:1; color:#1f5b42; }}
.stat .n.red {{ color:#b8232e; }}
.stat .label {{ margin-top:10px; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:#69706a; font-weight:800; }}
.stat p {{ margin:10px 0 0; font-size:13.5px; line-height:1.45; color:#666b65; }}
table {{ width:100%; border-collapse:collapse; margin-top:28px; font-size:14px; }}
th {{ text-align:left; background:#eeeae1; color:#667069; font-size:11px; text-transform:uppercase; letter-spacing:.08em; padding:10px 12px; }}
td {{ padding:12px; border-bottom:1px solid #ded9cf; vertical-align:top; line-height:1.42; }}
td.muted {{ color:#666b65; font-size:13.5px; }}
.flow {{ display:grid; grid-template-columns:1.05fr .9fr .9fr 1fr .9fr; gap:12px; margin-top:42px; }}
.step {{ background:white; border:1px solid #ded9cf; border-radius:10px; padding:18px 16px; min-height:150px; }}
.step b {{ display:block; color:#1f5b42; font-size:12px; text-transform:uppercase; letter-spacing:.08em; margin-bottom:9px; }}
.step span {{ color:#666b65; font-size:13px; line-height:1.45; }}
.checks {{ list-style:none; padding:0; margin:28px 0 0; max-width:980px; }}
.checks li {{ padding:13px 0 13px 28px; border-bottom:1px solid #ded9cf; position:relative; font-size:17px; line-height:1.4; }}
.checks li:before {{ content:''; width:8px; height:8px; border-radius:50%; background:#1f5b42; position:absolute; left:4px; top:21px; }}
.checks span {{ color:#666b65; font-size:14px; }}
.band {{ position:absolute; left:0; right:0; bottom:0; height:88px; background:#1f5b42; color:white; display:flex; align-items:center; padding:0 64px; font-size:20px; font-family:Georgia,serif; }}
.small {{ font-size:13px; color:#666b65; line-height:1.45; }}
</style></head><body>
<section class="slide dark"><div class="pad"><div class="meta">May 2026</div><div class="eyebrow">Project Leap follow-up</div><h1 class="large">Data deep-dive, integration vision and working-session asks</h1><p class="lead">A field-level translation of the SFS Project Leap use-case document into source systems, readiness, sequencing and the exact inputs needed to begin.</p><div class="rule" style="bottom:98px"></div><div class="brand">Conformal</div><div class="page">01</div></div></section>
<section class="slide"><div class="pad"><div class="eyebrow">What changed since the demo</div><h1>We moved from prototype thinking to the data contract behind production.</h1><div class="grid3"><div class="card"><h3>Input from SFS</h3><p>The Project Leap use-case file, covering 21 use cases across enterprise, procurement, field force, logistics and infrastructure.</p></div><div class="card"><h3>Our decomposition</h3><p>We translated the 15 custom-build use cases into 146 assumed fields and mapped each to likely source systems.</p></div><div class="card"><h3>Output now</h3><p>A concrete ask pack: source owners, extraction routes, masked data samples, definition workshops and sequencing.</p></div></div></div><div class="brand">Conformal</div><div class="page">02</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Readiness snapshot</div><h1>146 fields, mapped and assessed.</h1><div class="grid3"><div class="stat"><div class="n">33</div><div class="label">Available</div><p>Likely exists in an owned system, mostly SAP. Extraction-led.</p></div><div class="stat"><div class="n">19</div><div class="label">Partial</div><p>Exists but needs cleanup, integration, mapping or scope confirmation.</p></div><div class="stat"><div class="n red">94</div><div class="label">Unavailable</div><p>Not a direct field today. This is the number that needs interpretation.</p></div></div><p class="lead">The key is what those 94 actually represent, not the headline count alone.</p></div><div class="brand">Conformal</div><div class="page">03</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">The central finding</div><h1>The real data gap is much smaller than it first appears.</h1><div class="grid3"><div class="stat"><div class="n">58</div><div class="label">Conformal computes</div><p>Derived metrics such as target attainment, BPV, churn risk and scorecards. These need definitions, not raw SFS fields.</p></div><div class="stat"><div class="n">27</div><div class="label">Conformal sources</div><p>EXIM, commodity, GST/GSP, MCA21, credit, litigation, labour and utility benchmarks.</p></div><div class="stat"><div class="n red">~9</div><div class="label">SFS capture decisions</div><p>Voice capture, intervention logs, RFQ triggers, product hierarchy and similar workflow or master-data gaps.</p></div></div><div class="band">The ask is mostly read-only access, source owners and definitions. It is not 94 new fields for SFS to create.</div></div><div class="page">04</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Architecture principle</div><h1>The use cases are not separate builds. They are queries over one foundation.</h1><div class="grid2"><div class="card"><h3>Shared facts and dimensions</h3><p>Dealer, product, vendor, employee, territory, plant and time. Sales, collections, PO lines, inventory, activity, targets and schemes.</p></div><div class="card"><h3>The linking layer</h3><p>Dealer, vendor, material, employee and HSN crosswalks are the join layer between SAP, field apps and external sources. This is where trust is won or lost.</p></div></div><p class="lead">Build this foundation once. Enterprise, field-force and procurement use cases all reuse it.</p></div><div class="brand">Conformal</div><div class="page">05</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Integration model</div><h1>One governed data pipe into AI agents.</h1><div class="flow"><div class="step"><b>Sources</b><span>SAP BW / Power BI, SAP modules, Growthbook, Saathi, Concur, Complinity, Ariba, documents and external feeds.</span></div><div class="step"><b>Raw landing</b><span>Extracts stored exactly as received, with source, run and date metadata.</span></div><div class="step"><b>Standard layer</b><span>Typed, deduplicated tables with ID crosswalks and quality checks.</span></div><div class="step"><b>Gold marts</b><span>Dealer 360, field performance, spend cube, enterprise KPIs, stock and vendor scoring.</span></div><div class="step"><b>Agent tools</b><span>SQL, retrieval, charts and reports over governed views only.</span></div></div><p class="lead">We are not replacing SAP, Ariba, Growthbook, Concur, Complinity or logistics systems. We build the governed AI and data layer above them.</p></div><div class="brand">Conformal</div><div class="page">06</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Where to start</div><h1>Start with the data slices that unlock later use cases.</h1><div class="grid4"><div class="card"><h3>SAP sales base</h3><p>Feeds Enterprise Assistant, Field Performance, Dealer Profiles, Product Visibility, Churn and Scheme answers.</p></div><div class="card"><h3>Growthbook + Saathi</h3><p>Feeds visits, dealer context, activity analytics, coaching, intervention tracking and relationship intelligence.</p></div><div class="card"><h3>SAP MM purchase base</h3><p>Feeds Historical Spend, Vendor ID, Negotiation Prep, Should-Cost and EXIM mapping.</p></div><div class="card"><h3>Master-data crosswalks</h3><p>Dealer, vendor, material, employee and HSN IDs make the entire programme joinable and trustworthy.</p></div></div></div><div class="brand">Conformal</div><div class="page">07</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Recommended sequencing</div><h1>Wave 1 should be ROI-aligned and data-realistic.</h1><table><tr><th>Sequence</th><th>Use cases</th><th>Why here</th></tr><tr><td><b>Wave 1 build</b></td><td class="muted">Enterprise Assistant, Field Performance, Dealer Profiles</td><td class="muted">Strong owned-data base, limited external dependency and direct reuse of the demo foundation.</td></tr><tr><td><b>Wave 1 discovery</b></td><td class="muted">Historical Spend</td><td class="muted">SAP purchase base is strong. Spend taxonomy and BPV rules need procurement sign-off.</td></tr><tr><td><b>Wave 2 build</b></td><td class="muted">Product Visibility, Stock, Scheme, Churn, Vendor ID</td><td class="muted">Mostly owned data, but definitions and source-owner validation are required.</td></tr><tr><td><b>External-data discovery</b></td><td class="muted">Negotiation, Should-Cost, Import, Vendor Credit</td><td class="muted">High value, but gated by EXIM, commodity, GST, MCA, credit or litigation providers.</td></tr><tr><td><b>Separate track</b></td><td class="muted">Logistics</td><td class="muted">Buy-and-customise vendor/TMS track, not a custom AI build.</td></tr></table></div><div class="brand">Conformal</div><div class="page">08</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Wave 1 recommendation</div><h1>Enterprise Assistant plus Field Performance is the clean first move.</h1><div class="grid3"><div class="card"><h3>Enterprise Assistant</h3><p>{count_row('Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)')}. Strong pilot if scoped to confirmed SAP BW / Power BI metrics and a metric dictionary.</p></div><div class="card"><h3>Field Performance</h3><p>{count_row('Field Force #1 - Field Performance Tracking Dashboard')}. SFS's highest-impact field-force use case and the strongest data start.</p></div><div class="card"><h3>Dealer Profiles</h3><p>{count_row('Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)')}. Builds dealer 360 and the field-facing context layer for later use cases.</p></div></div><p class="lead">The same first extracts power all three: SAP sales/dealer/targets, Growthbook/Saathi activity and the enterprise metric dictionary.</p></div><div class="brand">Conformal</div><div class="page">09</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">What we need from SFS</div><h1>Specific owners and masked extracts, not production access.</h1><div class="grid2"><div class="card"><h3>Named owners</h3><p>Executive sponsor, SFS IT, SAP Basis/BW/Power BI, SAP SD/MM/FI, Master Data, Growthbook, Saathi, Concur, Complinity, Ariba, legal, external-data contracting and security.</p></div><div class="card"><h3>Initial data pack</h3><p>Masked samples: 36 months PO line, 36 months sales/billing, collections/ageing, material/vendor/dealer masters, field hierarchy, Growthbook activity, targets, schemes, inventory, Concur and Complinity exports.</p></div></div><ul class="checks"><li>Confirm read-only extract access off existing SAP BW / Power BI.</li><li>Confirm which unavailable fields are computed, sourced externally or require new capture.</li><li>Book the definition workshops before scope is locked.</li></ul></div><div class="brand">Conformal</div><div class="page">10</div></section>
<section class="slide"><div class="pad"><div class="eyebrow">Scope reassurance</div><h1>What we are not asking for.</h1><ul class="checks"><li><b>No production credentials to begin.</b> <span>Masked extracts are enough for discovery.</span></li><li><b>No source-system replacement.</b> <span>SAP, Ariba, Growthbook, Concur, Complinity and logistics remain systems of record.</span></li><li><b>No full-programme commitment before validation.</b> <span>The first sprint de-risks scope, data friction and sequencing.</span></li><li><b>No assumption that all 21 use cases are custom builds.</b> <span>Logistics stays a vendor/TMS fit-gap track.</span></li></ul></div><div class="brand">Conformal</div><div class="page">11</div></section>
<section class="slide dark"><div class="pad"><div class="eyebrow">Proposed next step</div><h1>A 60 to 90 minute working session, then a validated plan on real data.</h1><div class="grid2"><div class="card"><h3>In the session</h3><p>Walk the field map, confirm source systems, assign owners, agree masked extracts and book definition workshops.</p></div><div class="card"><h3>After the session</h3><p>Profile sample data, stand up the first governed layer, run golden questions and return with evidence-backed sequencing and scope.</p></div></div><p class="lead">This moves the engagement from a demo and use-case list to a production path grounded in SFS source-system truth.</p><div class="brand">Conformal</div><div class="page">12</div></div></section>
</body></html>'''
(ROOT/'presentation/sfs_datadeepdive_deck.html').write_text(deck)

print('Wrote client markdown/html and deck html')
