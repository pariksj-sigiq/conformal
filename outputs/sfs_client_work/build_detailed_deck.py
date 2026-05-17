import collections
import html
import json
import re
from pathlib import Path


ROOT = Path("/Users/pariksj/Desktop/Projects/dcmsriram")
ROWS = json.loads((ROOT / "conformal/notion-data-fields-full-db-selected.json").read_text())


def clean(value):
    if value is None:
        return ""
    text = str(value)
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2212": "-",
        "\u2192": "->",
        "\u00d7": "x",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00a0": " ",
        "\u2022": "-",
        "\u2026": "...",
        "\u20b9": "INR ",
        "\u2265": ">=",
        "\u2264": "<=",
        "\u00b7": "-",
        "\u2011": "-",
        "\u2122": "",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = text.encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text).strip()


def esc(value):
    return html.escape(clean(value), quote=True)


def availability_counts(rows):
    counts = collections.Counter(row["availability"] for row in rows)
    return {
        "available": counts.get("Available", 0),
        "partial": counts.get("Partial", 0),
        "unavailable": counts.get("Unavailable", 0),
        "total": len(rows),
    }


BY_UC = collections.defaultdict(list)
for row in ROWS:
    for uc in row["relatedUseCases"]:
        BY_UC[clean(uc)].append(row)


ORDER = [
    "Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)",
    "Field Force #1 - Field Performance Tracking Dashboard",
    "Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)",
    "Procurement #1 - Historical Spend Analysis & Price Insights",
    "Field Force #6 - Unified Product & Partner-Level Visibility",
    "Field Force #7 - Real-Time Warehouse Stock Visibility",
    "Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot",
    "Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk",
    "Procurement #4 - AI-Led Vendor Identification & Recommendation",
    "Procurement #3 - AI-Driven Preparation Material for Negotiations",
    "Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products)",
    "Procurement #2 - Real-Time Import Data Analysis",
    "Procurement #5 - Vendor Creditworthiness & Fraud Check",
    "Field Force #5 - AI-Enabled Sales Coaching",
    "Field Force #2 - Activity Analytics (Growthbook + SAP)",
]


def uc_counts(uc):
    return availability_counts(BY_UC[uc])


def simple_name(uc):
    name = clean(uc)
    replacements = {
        "Enterprise Assistant #1 - ": "Enterprise #1: ",
        "Field Force #": "FF #",
        "Procurement #": "Proc #",
        " - ": ": ",
        "AI-Driven ": "",
        "AI-Led ": "",
        "AI-Enabled ": "",
        " (Growthbook + SAP)": "",
        " (Saathi app)": "",
        " (across the top 5-10 products)": "",
    }
    for source, target in replacements.items():
        name = name.replace(source, target)
    return name


def bar(counts):
    total = max(counts["total"], 1)
    parts = [
        ("Available", counts["available"], "#1f6a49"),
        ("Partial", counts["partial"], "#b4812f"),
        ("Unavailable", counts["unavailable"], "#b8232e"),
    ]
    spans = []
    for label, value, color in parts:
        width = 100 * value / total
        spans.append(f'<span title="{label}: {value}" style="width:{width:.2f}%; background:{color}"></span>')
    return f'<div class="stackbar">{"".join(spans)}</div>'


def route_for(system, group):
    system = clean(system)
    group = clean(group)
    if group == "SAP":
        if "Sales" in system or "Customer" in system:
            return "SAP BW / Power BI first; fallback S/4 CDS/OData or scheduled SD/customer export"
        if "Purchase" in system or "Vendor" in system or "Material" in system:
            return "SAP BW / MM extract first; fallback S/4 CDS/OData or scheduled PO/vendor/material export"
        if "Stock" in system or "Inventory" in system:
            return "BW inventory cube or scheduled stock snapshot by plant, warehouse, SKU and date"
        if "Financial" in system:
            return "SAP BW / FI-CO extract or controlled receivables and GL export"
        return "SAP BW / Power BI first; fallback read-only S/4 extract"
    if system == "Growthbook":
        return "Event export or API with SAP-matching dealer and employee IDs"
    if system == "Saathi App":
        return "DB/API export for dealer profile, visit notes, voice status and intervention logs"
    if system == "Concur":
        return "Concur API or scheduled expense export mapped to employee and cost centre"
    if system == "Complinity":
        return "API or scheduled vendor-compliance export mapped to SAP vendor ID, PAN or GSTIN"
    if system == "Ariba":
        return "Supplier, RFQ and contract export mapped to SAP vendor master"
    if group.startswith("External"):
        return "Provider API/export after SFS confirms subscription and permitted use"
    if group == "Computed / Derived":
        return "Computed in Conformal semantic layer after SFS confirms definitions"
    if group == "Logistics":
        return "TMS/vendor route after vendor selection"
    return "Confirm source owner, extract route and join keys"


def mini_uc_table(usecases):
    rows = []
    for uc in usecases:
        counts = uc_counts(uc)
        rows.append(
            f"""
            <tr>
              <td><b>{esc(simple_name(uc))}</b></td>
              <td>{counts['total']}</td>
              <td class="green">{counts['available']}</td>
              <td class="amber">{counts['partial']}</td>
              <td class="red">{counts['unavailable']}</td>
              <td>{bar(counts)}</td>
            </tr>
            """
        )
    return '<table class="mini"><thead><tr><th>Use case</th><th>Fields</th><th>A</th><th>P</th><th>U</th><th>Readiness</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"


def field_rows(uc, limit=12):
    priority = {"Available": 0, "Partial": 1, "Unavailable": 2}
    rows = sorted(BY_UC[uc], key=lambda r: (priority.get(r["availability"], 3), clean(r["sourceGroup"]), clean(r["fieldName"])))
    out = []
    for row in rows[:limit]:
        status = row["availability"]
        css = "ok" if status == "Available" else "mid" if status == "Partial" else "gap"
        out.append(
            f"""
            <tr>
              <td>{esc(row['fieldName'])}</td>
              <td><span class="pill {css}">{esc(status)}</span></td>
              <td>{esc(row['sourceSystem'])}</td>
              <td>{esc(route_for(row['sourceSystem'], row['sourceGroup']))}</td>
            </tr>
            """
        )
    return "".join(out)


SYSTEM_PRIORITY = [
    "SAP - Sales & Distribution",
    "SAP - Customer / Dealer Master",
    "SAP - Purchase Register",
    "SAP - Material Master",
    "SAP - Stock / Inventory",
    "SAP - Financials (GL/P&L)",
    "Growthbook",
    "Saathi App",
    "Concur",
    "Complinity",
    "Ariba",
    "EXIM Data Provider",
    "GST Portal (via GSP)",
    "MCA21",
    "Credit Bureau",
]


def system_table():
    by_system = collections.defaultdict(list)
    for row in ROWS:
        by_system[clean(row["sourceSystem"])].append(row)
    rows = []
    for system in SYSTEM_PRIORITY:
        if system not in by_system:
            continue
        counts = availability_counts(by_system[system])
        group = clean(by_system[system][0]["sourceGroup"])
        rows.append(
            f"""
            <tr>
              <td><b>{esc(system)}</b><br><span>{esc(group)}</span></td>
              <td>{counts['total']}</td>
              <td class="green">{counts['available']}</td>
              <td class="amber">{counts['partial']}</td>
              <td class="red">{counts['unavailable']}</td>
              <td>{esc(route_for(system, group))}</td>
            </tr>
            """
        )
    return '<table class="source-table"><thead><tr><th>Source</th><th>Fields</th><th>A</th><th>P</th><th>U</th><th>Extraction route</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table>"


def source_bundle(label, systems, route, owner, ask, accent="green"):
    fields = [row for row in ROWS if clean(row["sourceSystem"]) in systems or clean(row["sourceGroup"]) in systems]
    counts = availability_counts(fields)
    chips = "".join(f"<span>{esc(system)}</span>" for system in systems[:3])
    return f"""
    <div class="source-card {accent}">
      <div class="source-card-top">
        <h3>{esc(label)}</h3>
        <div class="source-count"><b>{counts['total']}</b><span>fields</span></div>
      </div>
      <div class="source-mini">{chips}</div>
      <div class="source-readiness"><b class="green">{counts['available']} A</b><b class="amber">{counts['partial']} P</b><b class="red">{counts['unavailable']} U</b></div>
      {bar(counts)}
      <p><b>Route:</b> {esc(route)}</p>
      <p><b>Owner:</b> {esc(owner)}</p>
      <p><b>First ask:</b> {esc(ask)}</p>
    </div>
    """


def source_cards():
    return "".join(
        [
            source_bundle(
                "SAP reporting and core modules",
                [
                    "SAP - Sales & Distribution",
                    "SAP - Customer / Dealer Master",
                    "SAP - Purchase Register",
                    "SAP - Material Master",
                    "SAP - Stock / Inventory",
                    "SAP - Financials (GL/P&L)",
                ],
                "Confirm read-only extract from SAP BW / Power BI first, then fallback to S/4 CDS/OData or scheduled exports.",
                "SAP Basis/BW + SD/MM/FI owners",
                "Dataset inventory, sample exports, join keys and refresh cadence.",
            ),
            source_bundle(
                "Field apps",
                ["Growthbook", "Saathi App"],
                "API or controlled DB/file export with dealer, employee, timestamp, activity and interaction metadata.",
                "Growthbook + Saathi owners",
                "12-month activity export, Saathi schema and voice/call capture status.",
            ),
            source_bundle(
                "Finance and compliance apps",
                ["Concur", "Complinity"],
                "Scheduled export or API mapped back to SAP employee, cost-centre, vendor, PAN/GSTIN.",
                "Concur + Complinity owners",
                "SG&A expense sample and vendor licence/status export.",
                "amber",
            ),
            source_bundle(
                "Procurement workflow",
                ["Ariba"],
                "Supplier, RFQ and onboarding exports mapped to SAP vendor master.",
                "Ariba/procurement systems owner",
                "Confirm whether Ariba is live, in rollout or planned.",
                "red",
            ),
            source_bundle(
                "External market feeds",
                ["External (Market Data)"],
                "Provider API/export for EXIM, commodity, FX, labour and utility benchmarks.",
                "External-data contracting owner",
                "Existing subscriptions or provider shortlist approval.",
                "amber",
            ),
            source_bundle(
                "External risk feeds",
                ["External (Risk/Compliance)"],
                "Provider API/export for GST/GSP, MCA21, credit and litigation records.",
                "Legal + external-data contracting",
                "Permitted-use approval and entity-resolution rules.",
                "red",
            ),
        ]
    )


def product_card(title, uc, promise, sources, base):
    counts = uc_counts(uc)
    chips = "".join(f"<span>{esc(source)}</span>" for source in sources)
    return f"""
    <div class="product-card">
      <div class="product-head">
        <h3>{esc(title)}</h3>
        <div class="source-count"><b>{counts['total']}</b><span>fields</span></div>
      </div>
      <div class="source-readiness"><b class="green">{counts['available']} available</b><b class="amber">{counts['partial']} partial</b><b class="red">{counts['unavailable']} unavailable</b></div>
      {bar(counts)}
      <p>{esc(promise)}</p>
      <div class="chip-row">{chips}</div>
      <div class="base-note">{esc(base)}</div>
    </div>
    """


def source_mix_cards(uc):
    rows = BY_UC[uc]
    by_source = collections.defaultdict(list)
    for row in rows:
        by_source[clean(row["sourceSystem"])].append(row)
    top = sorted(by_source.items(), key=lambda item: (-len(item[1]), item[0]))[:5]
    cards = []
    for source, source_rows in top:
        counts = availability_counts(source_rows)
        cards.append(
            f"""
            <div class="mix-card">
              <b>{esc(source)}</b>
              <span>{counts['total']} fields</span>
              <div class="source-readiness mini-read"><b class="green">{counts['available']}</b><b class="amber">{counts['partial']}</b><b class="red">{counts['unavailable']}</b></div>
              {bar(counts)}
            </div>
            """
        )
    return "".join(cards)


def field_chips(uc, limit=10):
    priority = {"Available": 0, "Partial": 1, "Unavailable": 2}
    rows = sorted(BY_UC[uc], key=lambda r: (priority.get(r["availability"], 3), clean(r["sourceGroup"]), clean(r["fieldName"])))
    chips = []
    for row in rows[:limit]:
        status = row["availability"]
        css = "ok" if status == "Available" else "mid" if status == "Partial" else "gap"
        chips.append(f'<div class="field-chip {css}"><b>{esc(row["fieldName"])}</b><span>{esc(row["sourceSystem"])}</span></div>')
    return "".join(chips)


def matrix_cells():
    buckets = [
        ("Start now", ["Field Force #1 - Field Performance Tracking Dashboard", "Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)", "Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)"]),
        ("Define next", ["Procurement #1 - Historical Spend Analysis & Price Insights", "Field Force #6 - Unified Product & Partner-Level Visibility", "Field Force #7 - Real-Time Warehouse Stock Visibility", "Procurement #4 - AI-Led Vendor Identification & Recommendation"]),
        ("External gated", ["Procurement #2 - Real-Time Import Data Analysis", "Procurement #3 - AI-Driven Preparation Material for Negotiations", "Procurement #5 - Vendor Creditworthiness & Fraud Check", "Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products)"]),
        ("Discovery only", ["Field Force #2 - Activity Analytics (Growthbook + SAP)", "Field Force #3 - Pricing, Policy & Scheme Dissemination Chatbot", "Field Force #5 - AI-Enabled Sales Coaching", "Field Force #8 - Early Warning for Sales Performance & Dealer Churn Risk"]),
    ]
    html_rows = []
    for label, ucs in buckets:
        cards = []
        for uc in ucs:
            counts = uc_counts(uc)
            cards.append(
                f"""
                <div class="uc-chip">
                  <b>{esc(simple_name(uc))}</b>
                  <span>{counts['available']}A / {counts['partial']}P / {counts['unavailable']}U</span>
                  {bar(counts)}
                </div>
                """
            )
        html_rows.append(f'<div class="matrix-col"><h3>{esc(label)}</h3>{"".join(cards)}</div>')
    return "".join(html_rows)


availability = availability_counts(ROWS)
computed = [r for r in ROWS if r["availability"] == "Unavailable" and clean(r["sourceGroup"]) == "Computed / Derived"]
external = [r for r in ROWS if clean(r["sourceGroup"]).startswith("External")]
netnew = [
    r
    for r in ROWS
    if r["availability"] == "Unavailable" and clean(r["sourceGroup"]) in {"Internal Apps", "SAP", "Logistics"}
]


css = """
@page { size: 1280px 720px; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; background:#e7e2d5; color:#171917; font-family: Arial, Helvetica, sans-serif; }
.slide { width:1280px; height:720px; position:relative; overflow:hidden; page-break-after:always; background:#f7f3ea; }
.slide.dark { background:#145b40; color:white; }
.slide.split { background:linear-gradient(90deg,#145b40 0 38%,#f7f3ea 38% 100%); }
.pad { position:absolute; inset:0; padding:46px 58px 42px; }
.brand { position:absolute; left:58px; bottom:28px; font-size:13px; font-weight:800; color:#145b40; }
.dark .brand, .split .brand { color:white; }
.page { position:absolute; right:58px; bottom:30px; color:#7b7d77; font-size:11px; letter-spacing:.12em; }
.dark .page { color:rgba(255,255,255,.75); }
.eyebrow { color:#b8232e; text-transform:uppercase; letter-spacing:.14em; font-size:11px; font-weight:900; margin-bottom:12px; }
.dark .eyebrow { color:#f1d4ce; }
h1 { margin:0; max-width:950px; font-family: Georgia, 'Times New Roman', serif; font-weight:500; line-height:1.05; letter-spacing:-.01em; font-size:48px; }
.dark h1 { max-width:840px; }
h2 { margin:0; font-size:21px; font-family:Georgia,serif; font-weight:500; }
h3 { margin:0; font-family:Georgia,serif; font-size:19px; font-weight:500; }
p { margin:0; }
.lead { margin-top:16px; max-width:790px; color:#626760; font-size:16px; line-height:1.48; }
.dark .lead { color:rgba(255,255,255,.82); }
.small { color:#626760; font-size:12.5px; line-height:1.42; }
.dark .small { color:rgba(255,255,255,.76); }
.kicker { font-size:12px; text-transform:uppercase; letter-spacing:.1em; font-weight:900; color:#69716a; }
.dark .kicker { color:rgba(255,255,255,.7); }
.grid { display:grid; gap:14px; }
.g2 { grid-template-columns:1fr 1fr; }
.g3 { grid-template-columns:repeat(3,1fr); }
.g4 { grid-template-columns:repeat(4,1fr); }
.g5 { grid-template-columns:repeat(5,1fr); }
.panel { background:#fffdf8; border:1px solid #ddd6c9; padding:18px; border-radius:4px; }
.panel.green { background:#155b41; color:white; border-color:#155b41; }
.panel.red { background:#fff3f3; border-color:#e0bab8; }
.panel h3 { margin-bottom:9px; }
.panel p { color:#626760; font-size:13.5px; line-height:1.45; }
.panel.green p { color:rgba(255,255,255,.78); }
.statline { display:flex; gap:10px; margin-top:28px; }
.stat { flex:1; background:#fffdf8; border-top:4px solid #155b41; padding:15px 16px; min-height:126px; box-shadow:0 1px 0 rgba(0,0,0,.04); }
.stat.red { border-color:#b8232e; }
.stat b { display:block; font-family:Georgia,serif; font-size:46px; line-height:.95; color:#155b41; font-weight:500; }
.stat.red b { color:#b8232e; }
.stat span { display:block; margin-top:6px; color:#69716a; font-size:11px; text-transform:uppercase; letter-spacing:.08em; font-weight:900; }
.stat p { margin-top:8px; color:#666a64; font-size:12.5px; line-height:1.35; }
.rule { height:1px; background:#d9d2c5; margin:22px 0; }
.note { border-left:3px solid #155b41; padding:9px 0 9px 14px; background:transparent; color:#4f5851; font-size:13px; line-height:1.42; }
.note b { color:#155b41; }
.split-left { position:absolute; left:58px; top:48px; width:390px; color:white; }
.split-right { position:absolute; left:530px; right:58px; top:48px; bottom:48px; }
.artifact { position:absolute; right:58px; top:78px; width:420px; height:430px; border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.06); padding:18px; }
.artifact-grid { display:grid; grid-template-columns:repeat(8,1fr); gap:6px; }
.artifact-grid span { height:27px; border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.08); }
.artifact-grid span.hot { background:#b8232e; border-color:#e9b0a9; }
.artifact-grid span.ok { background:#d7efe1; border-color:#d7efe1; }
.timeline { display:grid; grid-template-columns:repeat(3,1fr); gap:0; margin-top:32px; border:1px solid #d9d2c5; }
.timeline .step { padding:22px; border-right:1px solid #d9d2c5; min-height:220px; background:#fffdf8; }
.timeline .step:last-child { border-right:0; }
.num { font-family:Georgia,serif; font-size:45px; line-height:1; color:#155b41; }
.caption { color:#626760; font-size:13px; line-height:1.42; }
.breakdown { display:grid; grid-template-columns: 1.2fr 1fr; gap:28px; margin-top:24px; align-items:start; }
.barwrap { background:#fffdf8; border:1px solid #ddd6c9; padding:22px; }
.bigbar { height:70px; display:flex; border-radius:2px; overflow:hidden; border:1px solid #ddd6c9; }
.bigbar div { display:flex; align-items:center; justify-content:center; color:white; font-weight:900; font-size:20px; }
.bigbar .ok { background:#1f6a49; width:22.6%; }
.bigbar .mid { background:#b4812f; width:13%; }
.bigbar .gap { background:#b8232e; width:64.4%; }
.subbar { margin-top:20px; height:52px; display:flex; overflow:hidden; border:1px solid #ddd6c9; }
.subbar div { display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:900; }
.subbar .comp { background:#d7efe1; color:#145b40; width:61.7%; }
.subbar .ext { background:#f2d7a8; color:#4b3b19; width:28.7%; }
.subbar .new { background:#f2c9c7; color:#6b1d21; width:9.6%; }
.legend { display:flex; gap:14px; margin-top:12px; color:#646a63; font-size:12px; }
.legend i { width:9px; height:9px; display:inline-block; margin-right:5px; }
.source-map { display:grid; grid-template-columns:1fr 1fr 1fr 1fr 1fr; gap:12px; margin-top:30px; }
.source-map .node { border:1px solid #d9d2c5; background:#fffdf8; min-height:154px; padding:15px; }
.source-map .node.darknode { background:#155b41; color:white; border-color:#155b41; }
.source-map .node b { display:block; color:#155b41; font-size:12px; text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px; }
.source-map .node.darknode b { color:#f1d4ce; }
.source-map .node span { display:block; color:#656a64; font-size:12px; line-height:1.4; }
.source-map .node.darknode span { color:rgba(255,255,255,.78); }
table { width:100%; border-collapse:collapse; }
th { text-align:left; background:#ebe5da; color:#69716a; font-size:10px; text-transform:uppercase; letter-spacing:.07em; padding:8px 9px; border:1px solid #d9d2c5; }
td { padding:8px 9px; border:1px solid #d9d2c5; vertical-align:top; font-size:12px; line-height:1.32; background:#fffdf8; }
td span { color:#747a73; font-size:10.5px; }
.source-table td { font-size:10px; padding:5px 7px; line-height:1.18; }
.source-table th { font-size:8.5px; padding:5px 7px; }
.source-card-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:24px; }
.source-card { background:#fffdf8; border:1px solid #d9d2c5; border-top:5px solid #155b41; padding:15px; min-height:202px; box-shadow:0 1px 0 rgba(0,0,0,.04); }
.source-card.amber { border-top-color:#b4812f; }
.source-card.red { border-top-color:#b8232e; }
.source-card-top { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; }
.source-card h3 { font-size:20px; line-height:1.08; max-width:220px; }
.source-count { text-align:right; min-width:58px; }
.source-count b { display:block; font-family:Georgia,serif; color:#155b41; font-size:32px; line-height:.95; font-weight:500; }
.source-count span { display:block; color:#747a73; font-size:9px; text-transform:uppercase; letter-spacing:.08em; font-weight:900; margin-top:3px; }
.source-mini { display:flex; flex-wrap:wrap; gap:5px; margin:10px 0 9px; min-height:20px; }
.source-mini span, .chip-row span { display:inline-block; color:#4f5750; background:#f0ebe0; border:1px solid #ded5c8; padding:4px 7px; font-size:9.5px; font-weight:800; }
.source-readiness { display:flex; gap:10px; align-items:center; font-size:11px; margin:8px 0; }
.source-card p { margin-top:8px; color:#60665f; font-size:11.5px; line-height:1.32; }
.product-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-top:28px; }
.product-card { background:#fffdf8; border:1px solid #d9d2c5; border-top:5px solid #155b41; padding:18px; min-height:365px; display:flex; flex-direction:column; }
.product-head { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; }
.product-card h3 { font-size:25px; line-height:1.08; max-width:240px; }
.product-card p { color:#5e665e; font-size:13px; line-height:1.44; margin:14px 0 12px; }
.chip-row { display:flex; flex-wrap:wrap; gap:6px; margin-top:auto; }
.base-note { margin-top:12px; padding-top:12px; border-top:1px solid #e2dbcf; color:#155b41; font-size:12px; line-height:1.35; font-weight:800; }
.mix-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:9px; margin-top:14px; }
.mix-card { background:#fffdf8; border:1px solid #d9d2c5; padding:9px; min-height:86px; }
.mix-card b { display:block; font-size:11px; line-height:1.2; min-height:28px; }
.mix-card span { display:block; color:#69716a; font-size:9.5px; margin:4px 0 5px; text-transform:uppercase; letter-spacing:.04em; }
.mini-read { gap:7px; margin:3px 0 6px; }
.field-chip-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-top:12px; }
.field-chip { border:1px solid #d9d2c5; background:#fffdf8; padding:8px 10px; min-height:48px; border-left:4px solid #176a49; }
.field-chip.mid { border-left-color:#b4812f; }
.field-chip.gap { border-left-color:#b8232e; }
.field-chip b { display:block; font-size:11.3px; line-height:1.18; }
.field-chip span { display:block; color:#737971; font-size:9.5px; margin-top:4px; line-height:1.2; }
.ask-strip { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:13px; }
.ask-strip div { background:#155b41; color:white; padding:12px; min-height:72px; }
.ask-strip b { display:block; font-size:12px; margin-bottom:5px; }
.ask-strip span { display:block; color:rgba(255,255,255,.76); font-size:10.5px; line-height:1.28; }
.route-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:24px; }
.route-card { background:#fffdf8; border:1px solid #d9d2c5; border-top:5px solid #155b41; padding:15px; min-height:215px; }
.route-card b { display:block; font-family:Georgia,serif; font-size:22px; line-height:1.05; margin-bottom:10px; }
.route-card p { color:#5f665f; font-size:12.2px; line-height:1.4; margin-bottom:10px; }
.route-card span { display:block; color:#155b41; font-size:10px; text-transform:uppercase; letter-spacing:.07em; font-weight:900; margin-top:8px; }
.mini th { font-size:9.2px; }
.mini td { font-size:11.2px; padding:7px 8px; }
.green { color:#176a49; font-weight:900; }
.amber { color:#9d6b20; font-weight:900; }
.red { color:#b8232e; font-weight:900; }
.stackbar { width:100%; height:8px; display:flex; background:#eee7dc; overflow:hidden; }
.stackbar span { display:block; height:100%; }
.matrix { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:24px; }
.matrix-col { background:#fffdf8; border:1px solid #d9d2c5; padding:13px; min-height:420px; }
.matrix-col h3 { font-size:18px; padding-bottom:9px; border-bottom:1px solid #d9d2c5; margin-bottom:10px; }
.uc-chip { padding:10px; border-bottom:1px solid #ebe4d8; }
.uc-chip b { font-size:11.8px; line-height:1.24; display:block; }
.uc-chip span { display:block; margin:5px 0 7px; color:#69716a; font-size:10px; font-weight:800; }
.lane { display:grid; grid-template-columns: 1fr 1fr 1fr; gap:14px; margin-top:26px; }
.lane .box { background:#fffdf8; border:1px solid #d9d2c5; padding:15px; min-height:320px; }
.box ul { margin:12px 0 0; padding-left:17px; color:#626760; font-size:12.5px; line-height:1.5; }
.box li { margin-bottom:6px; }
.field-table th { font-size:9px; }
.field-table td { font-size:10.4px; line-height:1.28; padding:6px 7px; }
.pill { display:inline-block; padding:3px 7px; border-radius:20px; color:white; font-size:9px; font-weight:900; }
.pill.ok { background:#176a49; }
.pill.mid { background:#b4812f; }
.pill.gap { background:#b8232e; }
.deep { display:grid; grid-template-columns: 330px 1fr; gap:18px; margin-top:24px; }
.deep-left { background:#155b41; color:white; padding:20px; min-height:435px; }
.deep-left h2 { font-size:29px; line-height:1.08; margin-bottom:18px; }
.deep-left .score { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:16px 0; }
.deep-left .score div { background:rgba(255,255,255,.11); padding:10px; }
.deep-left .score b { display:block; font-family:Georgia,serif; font-size:28px; }
.deep-left .score span { color:rgba(255,255,255,.72); font-size:9px; text-transform:uppercase; letter-spacing:.08em; }
.deep-left p { color:rgba(255,255,255,.8); font-size:13px; line-height:1.45; }
.ask-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:24px; }
.ask-card { background:#fffdf8; border:1px solid #d9d2c5; border-top:4px solid #155b41; padding:14px; min-height:150px; }
.ask-card b { display:block; font-family:Georgia,serif; font-size:18px; margin-bottom:8px; }
.ask-card p { color:#626760; font-size:12.5px; line-height:1.42; }
.ask-card ul { margin:8px 0 0; padding-left:15px; color:#626760; font-size:11.5px; line-height:1.36; }
.ask-card li { margin-bottom:4px; }
.block-label { color:#b8232e; font-size:9px; text-transform:uppercase; letter-spacing:.08em; font-weight:900; margin-top:8px; display:block; }
.pack-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:25px; }
.pack-card { background:#fffdf8; border:1px solid #d9d2c5; border-top:5px solid #155b41; padding:15px; min-height:240px; }
.pack-card h3 { font-size:22px; line-height:1.05; margin-bottom:12px; }
.pack-card ul { margin:0; padding-left:16px; color:#5f665f; font-size:12.2px; line-height:1.42; }
.pack-card li { margin-bottom:8px; }
.pack-card span { display:inline-block; margin-bottom:11px; color:#155b41; font-size:10px; font-weight:900; text-transform:uppercase; letter-spacing:.07em; }
.dayplan { display:grid; grid-template-columns:repeat(4,1fr); gap:13px; margin-top:28px; }
.day { background:#fffdf8; border:1px solid #d9d2c5; padding:16px; min-height:350px; position:relative; }
.day:before { content:''; position:absolute; left:16px; right:16px; top:62px; height:3px; background:#155b41; }
.day .num { font-size:36px; margin-bottom:26px; }
.day ul { margin:0; padding-left:16px; color:#626760; font-size:12.4px; line-height:1.46; }
.closing { position:absolute; inset:0; display:grid; grid-template-columns:41% 59%; }
.closing .left { background:#155b41; padding:58px; color:white; }
.closing .right { padding:58px; }
.closing .left .lead { color:rgba(255,255,255,.78); }
.closing .left .eyebrow { color:#f1d4ce; }
.quote { font-family:Georgia,serif; font-size:30px; line-height:1.18; color:#171917; max-width:640px; }
"""


slides = []


def slide(body, dark=False, cls=""):
    page = len(slides) + 1
    mode = " dark" if dark else ""
    if cls:
        mode += f" {cls}"
    slides.append(
        f'<section class="slide{mode}"><div class="pad">{body}</div><div class="brand">Conformal</div><div class="page">{page:02d}</div></section>'
    )


slide(
    """
    <div class="eyebrow">Project Leap follow-up</div>
    <h1 style="max-width:650px">Data readiness, integration plan and working-session asks</h1>
    <p class="lead">A richer client-facing follow-up to the demo: what the SFS use-case file implies at field level, which systems need to be touched, and what we need from the team to move from prototype to production.</p>
    <div class="statline" style="max-width:680px">
      <div class="stat"><b>146</b><span>assumed fields</span><p>Derived from the SFS use-case document across 15 custom-build use cases.</p></div>
      <div class="stat"><b>15</b><span>mapped use cases</span><p>Logistics remains a vendor/TMS selection and customization track.</p></div>
      <div class="stat red"><b>~9</b><span>true net-new capture</span><p>The rest is owned, partial, computed or externally sourced.</p></div>
    </div>
    <div class="artifact">
      <div class="kicker" style="color:rgba(255,255,255,.72); margin-bottom:14px">Field map artifact</div>
      <div class="artifact-grid">
        """ + "".join(f'<span class="{"hot" if i % 7 == 0 else "ok" if i % 5 == 0 else ""}"></span>' for i in range(96)) + """
      </div>
      <p class="small" style="margin-top:15px">Each cell represents a field-level assumption that now needs source-owner validation.</p>
    </div>
    """,
    dark=True,
)

slide(
    """
    <div class="eyebrow">The story to tell SFS</div>
    <h1>SFS gave us use cases. We turned them into a data contract.</h1>
    <div class="timeline">
      <div class="step"><div class="num">01</div><h3>SFS source</h3><p class="caption">Project Leap use-case document with business ambition, expected impact and named systems such as SAP BW + Power BI, Growthbook, Saathi, Concur and Complinity.</p></div>
      <div class="step"><div class="num">02</div><h3>Conformal decomposition</h3><p class="caption">Each custom-build use case translated into assumed production fields, likely source systems, availability and integration route.</p></div>
      <div class="step"><div class="num">03</div><h3>Working-session output</h3><p class="caption">Concrete owners, masked extracts, definition workshops and sequencing. This validates the AI product scope on real SFS data.</p></div>
    </div>
    <div class="note" style="margin-top:22px"><b>Positioning:</b> this is not a final implementation scope. It is the fastest path to validate what is easy, what is definition-gated and what requires new capture.</div>
    """
)

slide(
    f"""
    <div class="eyebrow">Executive readout</div>
    <h1>The programme is smaller and more structured than 21 separate builds.</h1>
    <div class="statline">
      <div class="stat"><b>{availability['total']}</b><span>fields mapped</span><p>Across the 15 custom-build use cases that need a data/AI product layer.</p></div>
      <div class="stat"><b>{availability['available']}</b><span>available</span><p>Mostly SAP-owned fields. The work is extraction, joins and quality checks.</p></div>
      <div class="stat"><b>{availability['partial']}</b><span>partial</span><p>Exists somewhere, but needs cleanup, connector work or scope confirmation.</p></div>
      <div class="stat red"><b>{availability['unavailable']}</b><span>unavailable</span><p>Misleading as a single bucket. Most of it is computed or externally sourced.</p></div>
    </div>
    <div class="rule"></div>
    <div class="grid g3">
      <div class="panel"><h3>15 mapped</h3><p>Enterprise, Procurement and Field Force have a field-level readiness map.</p></div>
      <div class="panel"><h3>5 logistics</h3><p>Freight, route, E-PoD, consignment and ocean tracking should stay buy-and-customize.</p></div>
      <div class="panel"><h3>1 foundation</h3><p>Technology and infrastructure is the mandatory shared layer beneath all waves.</p></div>
    </div>
    """
)

slide(
    f"""
    <div class="eyebrow">What the gap really means</div>
    <h1>The 94 unavailable fields are not 94 fields SFS must create.</h1>
    <div class="breakdown">
      <div class="barwrap">
        <div class="kicker">Headline readiness</div>
        <div class="bigbar"><div class="ok">{availability['available']} A</div><div class="mid">{availability['partial']} P</div><div class="gap">{availability['unavailable']} U</div></div>
        <div class="legend"><span><i style="background:#1f6a49"></i>Available</span><span><i style="background:#b4812f"></i>Partial</span><span><i style="background:#b8232e"></i>Unavailable</span></div>
        <div class="rule"></div>
        <div class="kicker">Unavailable split</div>
        <div class="subbar"><div class="comp">{len(computed)} computed</div><div class="ext">{len(external)} external</div><div class="new">{len(netnew)} net-new</div></div>
      </div>
      <div class="grid" style="gap:12px">
        <div class="panel"><h3>{len(computed)} computed by Conformal</h3><p>Target attainment, dealer tier, BPV, variance, risk score, opportunity score and other semantic metrics.</p></div>
        <div class="panel"><h3>{len(external)} sourced externally</h3><p>EXIM, GST/GSP, MCA21, credit, litigation, commodity, FX, labour and utility benchmarks.</p></div>
        <div class="panel red"><h3>{len(netnew)} SFS decisions</h3><p>Voice capture, intervention logs, Ariba triggers, product hierarchy and SKU substitution style gaps.</p></div>
      </div>
    </div>
    """
)

slide(
    """
    <div class="eyebrow">Integration vision</div>
    <h1>One governed data pipe, then many AI products.</h1>
    <div class="source-map">
      <div class="node"><b>Sources</b><span>SAP BW / Power BI<br>SAP SD, MM, FI, Inventory<br>Growthbook, Saathi<br>Concur, Complinity, Ariba<br>External providers</span></div>
      <div class="node"><b>Raw landing</b><span>Append-only extracts with source, date, run ID, grain and lineage preserved.</span></div>
      <div class="node"><b>Standard layer</b><span>Typed columnar tables, dedupe, validation and ID crosswalks.</span></div>
      <div class="node"><b>Gold marts</b><span>Dealer 360, field performance, spend cube, stock, schemes, enterprise KPIs.</span></div>
      <div class="node darknode"><b>Agent tools</b><span>SQL, retrieval, charts, reports, audits and evals over governed views.</span></div>
    </div>
    <div class="note" style="margin-top:26px"><b>Important:</b> agents should not connect directly to SAP, Concur, Saathi, Ariba or other systems of record. They query governed semantic views with access control and traceability.</div>
    """
)

slide(
    """
    <div class="eyebrow">SAP route</div>
    <h1>The SAP ask is a confirmation path, not an open-ended discovery.</h1>
    <div class="grid g2" style="margin-top:28px">
      <div class="panel green"><h3>SFS's own document names SAP BW + Power BI</h3><p>That means the first route should be read-only extraction from the existing BW/Power BI reporting layer, preserving line-level keys wherever the semantic model allows it.</p></div>
      <div class="panel"><h3>Fallback if line-level fields are missing</h3><p>Use read-only S/4 CDS/OData views or scheduled flat-file exports for SD billing, MM PO lines, FI/AR and inventory snapshots.</p></div>
    </div>
    <div class="route-grid">
      <div class="route-card"><b>SD / Sales</b><p>Sales and billing line with dealer, material, date, territory, quantity and value.</p><span>Owner: SAP SD + BW</span><p>Feeds Field Performance, Dealer Profiles, Churn and Enterprise Assistant.</p></div>
      <div class="route-card"><b>MM / Procurement</b><p>PO line with vendor, material, HSN, UoM, quantity, price, currency and GRN.</p><span>Owner: SAP MM + BW</span><p>Feeds Historical Spend, Vendor ID, Should-Cost and Negotiation.</p></div>
      <div class="route-card"><b>FI / Collections</b><p>Receivables, ageing, collections and approved GL/P&L metrics at agreed grain.</p><span>Owner: FI/CO + Finance</span><p>Feeds enterprise metrics, dealer health and working-capital views.</p></div>
      <div class="route-card"><b>Inventory</b><p>Stock snapshot by plant, storage location, SKU, batch and freshness timestamp.</p><span>Owner: Inventory/MM</span><p>Feeds warehouse stock visibility and product availability.</p></div>
    </div>
    """
)

slide(
    f"""
    <div class="eyebrow">Source-system readiness</div>
    <h1 style="font-size:42px">Source-system readiness by extraction route.</h1>
    <div class="source-card-grid">{source_cards()}</div>
    """
)

slide(
    f"""
    <div class="eyebrow">Use-case triage</div>
    <h1>Pick first use cases that also build the base for later ones.</h1>
    <div class="matrix">{matrix_cells()}</div>
    """
)

slide(
    f"""
    <div class="eyebrow">Wave 1 design</div>
    <h1>Wave 1 should be a foundation build, not three isolated apps.</h1>
    <div class="product-grid">
      {product_card("Enterprise Assistant", ORDER[0], "Productionise the demo around confirmed SAP BW / Power BI metrics, governed SQL, document retrieval and a first metrics dictionary.", ["SAP BW / Power BI", "FI/CO", "schemes", "agent evals"], "Base created: enterprise metric dictionary and governed agent access layer.")}
      {product_card("Field Performance", ORDER[1], "Start with the strongest field-force data base and SFS's highest-impact revenue use case.", ["SAP SD", "dealer master", "targets", "Growthbook"], "Base created: field performance mart, territory hierarchy and sales target spine.")}
      {product_card("Dealer Profiles", ORDER[2], "Build the dealer 360 layer that later powers churn, coaching, product visibility and scheme answers.", ["SAP dealer", "Saathi", "Growthbook", "legal"], "Base created: dealer 360, dealer ID crosswalk and relationship context layer.")}
    </div>
    """
)

for uc, label, why, base in [
    (
        "Field Force #1 - Field Performance Tracking Dashboard",
        "Field Performance",
        "Fastest field-force data start. The descriptive base is mostly owned by SFS; the intelligence layer comes after definitions and capture validation.",
        "Creates fact_sales, fact_target, dim_dealer, dim_employee and territory hierarchy for later field use cases.",
    ),
    (
        "Enterprise Assistant #1 - Enterprise Chat Assistant (Supply & Sales)",
        "Enterprise Assistant",
        "Strong pilot because the demo already exists and the SFS document points to SAP BW + Power BI as the reporting layer.",
        "Creates the enterprise metric dictionary, governed SQL tool, charting path and evaluation set.",
    ),
    (
        "Field Force #4 - Dealer Profiles & Field-Visit Conversation Inputs (Saathi app)",
        "Dealer Profiles",
        "Strong SAP dealer base plus Saathi enrichment. Voice and relationship intelligence need SFS confirmation and legal posture.",
        "Creates dealer_360 and the dealer ID crosswalk reused by churn, coaching, visibility and enterprise questions.",
    ),
]:
    counts = uc_counts(uc)
    ask_sets = {
        "Field Performance": [
            ("SAP sales extract", "36 months invoice/sales line with dealer, material, territory and value."),
            ("Targets and hierarchy", "TBM/RBM/MGO mapping plus target and incentive files."),
            ("Activity mapping", "Growthbook/Saathi events with SAP-matching dealer and employee IDs."),
        ],
        "Enterprise Assistant": [
            ("SAP BW / Power BI", "Confirm read-only extractable datasets and preserved join keys."),
            ("Metric dictionary", "Agree official KPI definitions, owner and refresh cadence."),
            ("Golden questions", "Pick 20-30 executive questions to evaluate answers and SQL traces."),
        ],
        "Dealer Profiles": [
            ("Dealer master", "Dealer code, GSTIN, credit terms, territory, onboarding and geo fields."),
            ("Saathi schema", "Dealer profile, visit logs, notes, key contacts and voice capture status."),
            ("Legal posture", "Confirm whether call/voice capture and classification are permitted."),
        ],
    }
    ask_html = "".join(
        f"<div><b>{esc(title)}</b><span>{esc(text)}</span></div>"
        for title, text in ask_sets[label]
    )
    slide(
        f"""
        <div class="eyebrow">Wave 1 deep dive</div>
        <h1 style="font-size:42px">{esc(label)}: source fields, route and first asks.</h1>
        <div class="deep">
          <div class="deep-left">
            <h2>{esc(simple_name(uc))}</h2>
            <div class="score"><div><b>{counts['available']}</b><span>available</span></div><div><b>{counts['partial']}</b><span>partial</span></div><div><b>{counts['unavailable']}</b><span>unavailable</span></div></div>
            <p><b>Why first:</b> {esc(why)}</p>
            <p style="margin-top:16px"><b>Base created:</b> {esc(base)}</p>
          </div>
          <div>
            <h3>Source mix</h3>
            <div class="mix-grid">{source_mix_cards(uc)}</div>
            <h3 style="margin-top:16px">First fields to validate</h3>
            <div class="field-chip-grid">{field_chips(uc, 6)}</div>
            <div class="ask-strip">{ask_html}</div>
          </div>
        </div>
        """
    )

slide(
    f"""
    <div class="eyebrow">Procurement path</div>
    <h1>Procurement is valuable, but the first move is spend foundation.</h1>
    <div class="grid g2" style="margin-top:24px">
      <div>{mini_uc_table([
        "Procurement #1 - Historical Spend Analysis & Price Insights",
        "Procurement #4 - AI-Led Vendor Identification & Recommendation",
        "Procurement #3 - AI-Driven Preparation Material for Negotiations",
        "Procurement #6 - AI-Driven Should-Cost Analysis (across the top 5-10 products)",
        "Procurement #2 - Real-Time Import Data Analysis",
        "Procurement #5 - Vendor Creditworthiness & Fraud Check",
      ])}</div>
      <div class="grid" style="gap:12px">
        <div class="panel green"><h3>Start with Historical Spend</h3><p>SAP PO-line data is the anchor. Once material, vendor, HSN and category mapping are stable, later procurement copilots become much easier.</p></div>
        <div class="panel"><h3>Then add external connectors</h3><p>Import, negotiation, should-cost and fraud require EXIM, commodity, GST/GSP, MCA21, credit and litigation feeds.</p></div>
        <div class="panel red"><h3>Do not over-promise smart procurement in Wave 1</h3><p>Negotiation and should-cost have the same external-data profile as real-time import. They need provider decisions and category workshops first.</p></div>
      </div>
    </div>
    """
)

slide(
    """
    <div class="eyebrow">External data and net-new capture</div>
    <h1>Separate what Conformal can source from what SFS must start capturing.</h1>
    <div class="grid g2" style="margin-top:26px">
      <div class="panel">
        <h3>27 external-provider fields</h3>
        <table class="mini" style="margin-top:12px">
          <thead><tr><th>Provider class</th><th>Unblocks</th><th>SFS decision</th></tr></thead>
          <tbody>
            <tr><td>EXIM/customs</td><td>Import, Negotiation, Vendor ID, Should-Cost</td><td>Existing subscription or new provider approval</td></tr>
            <tr><td>GST/GSP, MCA21, credit, litigation</td><td>Vendor Credit/Fraud, Churn risk signals</td><td>Legal posture and permitted use</td></tr>
            <tr><td>Commodity, FX, labour, utility</td><td>Negotiation and Should-Cost models</td><td>Provider shortlist and refresh cadence</td></tr>
          </tbody>
        </table>
      </div>
      <div class="panel red">
        <h3>~9 SFS workflow or governance fields</h3>
        <table class="mini" style="margin-top:12px">
          <thead><tr><th>Gap</th><th>Likely owner</th><th>Use cases blocked</th></tr></thead>
          <tbody>
            <tr><td>Dealer voice capture, call classification, intervention logs</td><td>Saathi + legal</td><td>Dealer Profiles, Coaching, Churn</td></tr>
            <tr><td>Product hierarchy, SKU substitution, HSN mapping</td><td>Master Data</td><td>Product Visibility, Stock, Procurement</td></tr>
            <tr><td>RFQ trigger, onboarding workflow status</td><td>Ariba / procurement</td><td>Vendor ID, Credit/Fraud</td></tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="note" style="margin-top:20px"><b>Cross-cutting caveat:</b> secondary sales, inventory liquidation and PoG are not confirmed as collected. Descriptive field views can start fast, but sell-out completeness needs an explicit SFS capture decision.</div>
    """
)

slide(
    """
    <div class="eyebrow">Named owners</div>
    <h1>The next meeting should be organized around source ownership.</h1>
    <div class="ask-grid">
      <div class="ask-card"><b>SAP Basis / BW / Power BI</b><p>Confirm read-only access and the fastest extract route.</p><ul><li>Dataset inventory</li><li>Data dictionary</li><li>Refresh cadence</li></ul><span class="block-label">Blocks: all SAP-backed waves</span></div>
      <div class="ask-card"><b>SAP SD, MM, FI/CO</b><p>Validate business grain and functional meaning.</p><ul><li>Sales/billing line</li><li>PO-line and GRN</li><li>Receivables and ageing</li></ul><span class="block-label">Blocks: enterprise, field, procurement</span></div>
      <div class="ask-card"><b>Master Data / Governance</b><p>Own the crosswalks that make systems joinable.</p><ul><li>Dealer/vendor IDs</li><li>Material and HSN</li><li>Employee and territory</li></ul><span class="block-label">Blocks: cross-BU visibility</span></div>
      <div class="ask-card"><b>Growthbook + Saathi</b><p>Validate field activity and dealer context.</p><ul><li>Activity event schema</li><li>Dealer interaction logs</li><li>Voice/call capture status</li></ul><span class="block-label">Blocks: dealer, coaching, churn</span></div>
      <div class="ask-card"><b>Concur + Complinity + Ariba</b><p>Confirm non-SAP connector paths.</p><ul><li>SG&A export</li><li>Vendor licence export</li><li>RFQ/onboarding status</li></ul><span class="block-label">Blocks: spend and vendor risk</span></div>
      <div class="ask-card"><b>Legal + External Contracting</b><p>Approve sensitive and third-party data posture.</p><ul><li>GST/MCA/credit/litigation</li><li>Voice recording</li><li>Provider shortlist</li></ul><span class="block-label">Blocks: fraud, coaching, external feeds</span></div>
    </div>
    """
)

slide(
    """
    <div class="eyebrow">Masked data pack</div>
    <h1>We can begin with controlled samples, not production credentials.</h1>
    <div class="pack-grid">
      <div class="pack-card"><span>SAP transactions</span><h3>Line-level extracts</h3><ul><li>36 months PO line</li><li>36 months sales/billing line</li><li>24 to 36 months collections and ageing</li></ul></div>
      <div class="pack-card"><span>SAP masters</span><h3>Join keys</h3><ul><li>Material master and HSN</li><li>Vendor master</li><li>Customer/dealer master</li><li>Employee and field hierarchy</li></ul></div>
      <div class="pack-card"><span>Field apps</span><h3>Activity context</h3><ul><li>Growthbook activity export</li><li>Saathi dealer profile</li><li>Visit and interaction logs</li><li>Voice/call capture status</li></ul></div>
      <div class="pack-card"><span>Controls</span><h3>Commercial files</h3><ul><li>Target and incentive files</li><li>Scheme circulars</li><li>Inventory snapshot</li><li>Concur and Complinity exports</li></ul></div>
    </div>
    <div class="note" style="margin-top:20px"><b>Discovery sprint rule:</b> start with masked samples and schema dictionaries. Production access is a later security and deployment conversation.</div>
    """
)

slide(
    """
    <div class="eyebrow">30-day execution plan</div>
    <h1>What happens after SFS names owners and shares samples.</h1>
    <div class="dayplan">
      <div class="day"><div class="num">0-5</div><h3>Source validation</h3><ul><li>Owner kickoff</li><li>Schema inventory</li><li>Extract routes confirmed</li><li>Security and masking agreed</li></ul></div>
      <div class="day"><div class="num">6-12</div><h3>Data profiling</h3><ul><li>Load sample extracts</li><li>Join-key audit</li><li>Freshness and null checks</li><li>Field map validation</li></ul></div>
      <div class="day"><div class="num">13-21</div><h3>Semantic layer</h3><ul><li>Dealer and material crosswalks</li><li>Gold marts for Wave 1</li><li>Metric dictionary draft</li><li>Golden questions defined</li></ul></div>
      <div class="day"><div class="num">22-30</div><h3>Proof on real data</h3><ul><li>Run Wave 1 questions</li><li>Show traceable answers</li><li>Document gaps</li><li>Return validated wave plan</li></ul></div>
    </div>
    """
)

slide(
    """
    <div class="closing">
      <div class="left">
        <div class="eyebrow">Recommended ask</div>
        <h1 style="font-size:46px">A 60 to 90 minute source-owner working session.</h1>
        <p class="lead">The goal is to validate source truth, not debate AI interfaces. Once the data spine is real, the agent experience becomes much easier to scope.</p>
      </div>
      <div class="right">
        <p class="quote">"Give us source owners, masked extracts and definition workshops. We will convert the use-case list into a validated build plan on real SFS data."</p>
        <div class="rule"></div>
        <div class="grid g2">
          <div class="panel"><h3>In the room</h3><p>SFS IT, SAP BW/Power BI, SD, MM, FI/CO, Master Data, Growthbook, Saathi, Concur, Complinity, Ariba, Legal and External Data.</p></div>
          <div class="panel"><h3>Output</h3><p>Validated field map, source route, data gaps, Wave 1 scope and a credible integration path for the full programme.</p></div>
        </div>
      </div>
    </div>
    """,
    cls="no-pad",
)


html_doc = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Conformal SFS Data Deep-Dive Deck</title>
  <style>{css}</style>
</head>
<body>
{''.join(slides)}
</body>
</html>
"""

out = ROOT / "presentation/sfs_datadeepdive_deck.html"
out.write_text(html_doc)
print(f"wrote {out} ({len(slides)} slides)")
