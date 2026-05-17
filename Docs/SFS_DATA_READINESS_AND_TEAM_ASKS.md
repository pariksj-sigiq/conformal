# SFS Project Leap - Data Readiness and Team Asks

Last updated: May 17, 2026

> Update: this document was created from the earlier 50-field data export. For the latest analysis based on `conformal/notion-data-fields-full-db-complete.json` with 146 fields, use `Docs/SFS_FULL_DB_READINESS_REANALYSIS.md`.

## Why This Exists

The current Conformal cockpit is a demo built on an assumed enterprise data model. It proves the product motion: a leader asks a natural-language question, the system chooses data, writes SQL, renders a chart, and gives a traceable answer.

Production is a different problem. Before we price or commit scope, we need SFS to confirm what data exists, where it lives, how much history is available, how often it refreshes, and which data is not captured today.

This document converts the 21 Project Leap use cases into a practical technical ask pack for the SFS team.

## The Message To SFS

We have gone through all 21 use cases. Our next step is a technical discovery sprint where we validate data availability and source ownership. We are not asking SFS to replace SAP, Ariba, Growthbook, Concur, ByteEdge, or logistics systems. We are asking for read-only access, sample extracts, system owners, and metric definitions so we can build the AI decision layer on top.

## What We Have Today

### Their Inputs

- `conformal/Use Cases details_SFS_Project LEAP.ods`: the 21 use cases, current state, target state, costs, key activities.
- `conformal/Conformal_AI Transformation for SFS_May 2026.pdf`: the intro deck we presented, including the Enterprise Cockpit demo, platform thesis, diagnose/build/drive model, and next steps.
- `conformal/notion-data-fields-selected.json`: 50 field-level data notes mapped mainly to procurement, enterprise assistant, and some field-force use cases.

### Our Demo Data

The demo database in `src/lib/workbook-data.json` contains assumed data across 14 tables:

- Geography, product, distributor, supplier dimensions.
- Primary sales, secondary sales, inventory, targets, collections.
- Field visits, commodity prices, procurement, finance P&L, regulatory pipeline.

This is useful as a target schema prototype, but it is not proof that SFS has all of this data in this shape.

### Data Field Export Readiness

The Notion-style data field export has 50 fields. It maps to only 12 of the 21 use cases, which means 9 use cases still need fresh discovery. Even within those 12, many capture mechanisms are blank.

Important examples:

| Area | Fields mapped | Available | Partial | Unavailable | What it means |
|---|---:|---:|---:|---:|---|
| Historical Spend | 26 | 11 | 6 | 9 | Strong SAP base, but taxonomy, BPV, anomaly rules, and category hierarchy are missing. |
| EXIM Analysis | 16 | 3 | 2 | 11 | Needs third-party EXIM provider and HSN mapping. |
| Negotiation Prep | 21 | 5 | 3 | 13 | Needs external feeds plus new outcome logging. |
| Vendor Risk | 6 | 2 | 1 | 3 | SAP vendor master exists, but MCA/litigation/credit signals must be sourced. |
| Vendor ID | 11 | 5 | 3 | 3 | Internal history exists; market/vendor discovery is external or uncaptured. |
| Should-Cost | 10 | 4 | 2 | 4 | Needs cost model assumptions and macro/commodity feeds. |
| Field/Stock/Visibility | Few fields | Mixed | Mixed | Mixed | Current export is too thin; needs Growthbook/SAP discovery. |

## Program-Level Technical Asks

### Ask 1: Source-System Access Map

For each system, we need the owner, available extraction method, history depth, refresh frequency, data dictionary, and sample masked extract.

| Source | Likely owner | What we need |
|---|---|---|
| SAP S/4HANA SD | Sales/commercial IT | Sales orders, billing, invoices, schemes, customer/dealer master, pricing conditions. |
| SAP S/4HANA MM | Procurement/Supply Chain IT | Purchase orders, GRN, material master, vendor master, inventory movements. |
| SAP FI-AR | Finance IT | Receivables, collections, credit limits, overdue ageing, payment history. |
| SAP FI/CO | Finance/controller | P&L, cost centers, GL lines, budgets, variance definitions. |
| SAP WM/EWM or inventory module | Supply chain/logistics IT | Warehouse stock, batch/lot, plant/storage location, ATP, in-transit where available. |
| Ariba | Procurement transformation owner | Vendor onboarding, RFQs, contracts, supplier performance, sourcing workflow status. |
| Growthbook | Sales ops/field excellence | MGO/TBM activity logs, visit plans, visit outcomes, dealer interactions, location/time stamps. |
| ByteEdge | Training/field capability | Training content, completions, quizzes, skill gaps, course metadata. |
| Concur | Finance/admin | Expense categories, SG&A spend, cost centers, claim history. |
| Complinity | Compliance/procurement | Vendor license status, validity dates, compliance exceptions. |
| Scheme/circular repository | Sales ops/marketing | Policy PDFs, scheme circulars, pricing rules, eligibility, effective dates. |
| Logistics/TMS/transport vendors | Logistics | Freight rates, shipments, POD, GPS events, carrier SLAs, route plans. |
| External data providers | Procurement/legal | EXIM, commodity prices, MCA21, GST, credit bureau, litigation, diesel/toll indices. |

### Ask 2: Minimum Data Pack For A Two-Week Discovery Sprint

Masked samples are enough for discovery. We do not need production credentials on day one.

1. 36 months of SAP purchase register at PO-line grain.
2. 36 months of SAP primary sales and billing at invoice-line grain.
3. 24-36 months of collections and receivables ageing.
4. Current material master with product hierarchy, HSN, UoM, active/inactive flag.
5. Current vendor master with GSTIN, legal name, region, category, active/inactive flag.
6. Current customer/dealer master with territory, credit limit, dealer tier, onboarding date.
7. Current field hierarchy: ZBM/RBM/TBM/MGO mapping.
8. Growthbook activity/event export for at least 12 months.
9. Current target files and incentive logic for MGO/TBM/RBM.
10. Current scheme circulars and pricing-policy repository.
11. Inventory snapshot extract by plant/storage location/SKU.
12. Any existing logistics lane/rate/shipment tracker.

### Ask 3: Named SFS Counterparts

| Role needed | Why |
|---|---|
| Executive sponsor | Prioritization and cross-functional unblock. |
| SFS IT lead | System access, data extraction, deployment constraints. |
| SAP Basis/Integration lead | RFC/OData/CDS/BW/extract route, auth, scheduling. |
| SAP SD functional owner | Sales, billing, pricing, dealer/customer master. |
| SAP MM functional owner | PO, GRN, material master, vendor master, inventory. |
| SAP FI/CO owner | P&L, receivables, cost centers, GL, budgets. |
| Growthbook admin | Field activity/event export and user hierarchy. |
| Ariba owner | Sourcing/vendor workflow status and API/export options. |
| Procurement category managers | Spend taxonomy, BPV, should-cost assumptions, negotiation rules. |
| Field excellence/sales ops lead | Field dashboard, schemes, coaching, dealer workflows. |
| Logistics lead | TMS fit-gap, freight, route, POD, shipment tracking. |
| Security/Azure/infra owner | VPC, SSO, data residency, model provider, logging, approvals. |

## What Parikshit/Sidd Should Learn

You do not need to become SAP implementation consultants. You need to understand data objects, extraction paths, and buyer language.

### SAP/Data Basics

- SAP S/4HANA SD: sales order, delivery, billing document, customer/dealer master, pricing conditions.
- SAP S/4HANA MM: purchase requisition, purchase order, GRN, material document, vendor master, material master.
- SAP FI-AR/FI-CO: receivables, payment clearing, credit exposure, GL, cost centers, profit centers, budgets.
- SAP WM/EWM/inventory: plant, storage location, batch, stock, movements, ATP/in-transit.
- Extraction routes: CDS views, OData APIs, SAP BW/ODP, SLT/replication, scheduled flat-file extracts, data lake landing.
- SAP security basics: read-only roles, row/field authorization, audit logs, service users.

### Procurement Tools

- SAP Ariba Sourcing, Supplier Lifecycle and Performance, Contracts, Buying/Invoicing.
- Ariba integration options: exports, APIs, supplier IDs, RFQ trigger points.
- Vendor data sources: GST, MCA21, credit bureau, litigation, EXIM providers, commodity price feeds.

### Data/AI Platform

- Azure landing zone, Entra ID/SSO, Key Vault, Private Link/VNet, storage accounts.
- Databricks/Fabric/Synapse patterns for lakehouse and semantic layer.
- Data quality, lineage, freshness, and observability.
- Agent evals: golden questions, expected SQL/result, regression tests, hallucination checks.
- Model gateway and audit: prompt/tool traces, role-aware access, cost/latency logs.

## Use-Case Deep Dive

### 1. Enterprise Chat Assistant

**Production read:** This is Wave 1. It is the production version of the demo cockpit over real SFS data.

**Likely sources:** SAP SD, SAP FI-AR, SAP FI/CO, SAP MM, SAP inventory, Growthbook, scheme repository, historical review decks.

**Data asks:** 24-36 months of sales, collections, targets, P&L, inventory, procurement, product, dealer, vendor, and field hierarchy data. We also need the official metric dictionary: revenue, gross margin, PBDIT/EBITDA, DSO, receivables, target achievement, sell-in, sell-out, stock ageing.

**Missing capture/schema:** Enterprise metric definitions are not a system table today. Create `metric_definition(metric_id, metric_name, formula, source_table, grain, owner, approved_by, effective_from, notes)`.

**First proof:** 20 leadership questions answered end-to-end with source citations, SQL trace, chart, and data freshness badge.

**Team asks:** CFO/controller, sales ops, SFS IT, SAP SD/MM/FI owners, Azure/security owner.

### 2. Historical Spend Analysis and Price Insights

**Production read:** Spend cube and anomaly analytics first; chatbot second.

**Likely sources:** SAP MM purchase register, vendor master, material master, Ariba if live, Complinity, Concur.

**Data asks:** 36 months of PO-line data with vendor, material, plant/region, UoM, quantity, unit price, line value, PO date, GRN status. Also vendor master, material master, tax/HSN, and cost center if SG&A is included.

**Missing capture/schema:** Spend category, sub-category, BPV, price variance, strategic classification, anomaly flag. Create `spend_taxonomy(material_code, category, sub_category, strategic_class, owner, confidence, effective_from)` and `spend_anomaly(po_line_id, anomaly_type, threshold, observed_value, severity, status, reviewed_by)`.

**First proof:** Category x vendor x SKU x region x month spend cube with top 20 BPV leakages.

**Team asks:** Procurement head, category managers, SAP MM owner, vendor master owner, Concur/Complinity owners.

### 3. Real-Time Import Data Analysis

**Production read:** Market intelligence and benchmarking product. The hard part is EXIM provider selection and HSN-to-SKU mapping.

**Likely sources:** EXIM/customs data provider, SAP purchase register, SAP material master, commodity indices.

**Data asks:** Priority commodity/SKU list, HSN coverage report, last purchase prices by HSN/material, preferred EXIM provider or permission to evaluate vendors.

**Missing capture/schema:** Create `hsn_sku_map(hsn_code, material_code, material_name, grade_spec, mapping_confidence, validated_by)` and `exim_transaction(provider_id, hsn_code, transaction_date, importer, exporter, origin_country, quantity, uom, cif_value, landed_cost_estimate, port)`.

**First proof:** For 10 priority HSNs, show SFS purchase price versus EXIM landed-cost benchmark and top source countries.

**Team asks:** Procurement category owners, legal/procurement for provider contracting, SAP MM/material owner.

### 4. AI-Driven Preparation Material For Negotiations

**Production read:** A negotiation brief generator. It needs internal purchase history, external benchmarks, and a new outcome logging workflow.

**Likely sources:** SAP purchase register, vendor master, EXIM data, commodity indices, buyer notes/contracts, Ariba RFQ/contract history.

**Data asks:** 36 months of PO history by commodity/vendor, vendor performance data, historical negotiation material if any, category playbooks, contract/RFQ history.

**Missing capture/schema:** Negotiation outcomes are not captured today. Create `negotiation_brief(brief_id, vendor_id, material_code, generated_at, benchmark_price, target_price_low, target_price_high, recommended_anchor, confidence, source_snapshot_id)` and `negotiation_outcome(brief_id, opening_quote, final_price, quantity_committed, concessions, outcome_status, buyer_notes, logged_by, logged_at)`.

**First proof:** Generate 5 negotiation packs for priority commodities with target price range, vendor pattern, EXIM benchmark, and suggested talking points.

**Team asks:** Category managers, sourcing buyers, SAP MM owner, Ariba owner, external-data owner.

### 5. AI-Led Vendor Identification and Recommendation

**Production read:** Vendor discovery plus vendor scoring. It should feed Ariba RFQ/onboarding, not replace it.

**Likely sources:** SAP vendor master, PO/GRN history, quality/rejection data if present, Ariba supplier lifecycle, EXIM exporter/importer data, external vendor databases.

**Data asks:** Vendor master, purchase history, delivery performance, quality/rejection records, current onboarding process, Ariba status, approved/preferred vendor rules.

**Missing capture/schema:** Create `vendor_score(vendor_id, material_code, price_score, delivery_score, quality_score, risk_score, capacity_signal, total_score, explanation, refreshed_at)` and `market_vendor_candidate(candidate_id, source, legal_name, country, hsn_or_material, evidence_url, onboarding_status)`.

**First proof:** Ranked vendor list for 5 materials with evidence, risk flags, and suggested RFQ action.

**Team asks:** Procurement, quality, SAP MM/vendor master owner, Ariba owner, legal/compliance.

### 6. Vendor Creditworthiness and Fraud Check

**Production read:** Vendor risk intelligence, mostly sourced from external signals and entity resolution.

**Likely sources:** SAP vendor master, Complinity, MCA21, GST, litigation/court databases, credit bureau, payment/dispute history.

**Data asks:** Vendor legal name, GSTIN, PAN/CIN if available, onboarding date, active status, payment/dispute flags, blocked vendor list.

**Missing capture/schema:** Create `vendor_risk_signal(vendor_id, signal_type, source, severity, evidence, observed_at, expiry_at, resolution_status)` and `beneficial_owner_edge(entity_id, director_or_owner_id, relationship_type, effective_from, source)`.

**First proof:** Risk profile for current top 50 vendors, including duplicates, director/entity links, GST/MCA status, litigation hits, and risk explanation.

**Team asks:** Procurement compliance, vendor master owner, legal, data privacy/security.

### 7. AI-Driven Should-Cost Analysis

**Production read:** Cost model for top 5-10 products/materials. This is not a generic LLM use case; it needs category-specific cost assumptions.

**Likely sources:** SAP PO history, material master, EXIM/commodity feeds, FX, diesel/crude, MSP/agri indices, BOM/specification inputs from category teams.

**Data asks:** Priority materials, standard specs/grades, purchase history, UoM conversions, input cost drivers, logistics assumptions, margin/processing assumptions.

**Missing capture/schema:** Create `should_cost_model(model_id, material_code, version, owner, valid_from, assumptions_json, confidence, approved_by)` and `should_cost_component(model_id, component_name, component_type, source, quantity_per_unit, rate, cost_per_unit, sensitivity_band)`.

**First proof:** Should-cost model for 3-5 priority SKUs with sensitivity to FX, EXIM price, commodity index, and freight.

**Team asks:** Category managers, finance/procurement analytics, SAP MM owner, external-data owner.

### 8. Field Performance Tracking Dashboard

**Production read:** Sales-performance data product with a field-facing assistant layer.

**Likely sources:** SAP SD sales/billing, FI-AR collections, targets/incentive files, Growthbook activity logs, dealer master, product master.

**Data asks:** MGO/TBM/RBM hierarchy, targets by period/territory/product, sales at dealer x SKU x month, collections, Growthbook activity logs, incentive logic.

**Missing capture/schema:** Activity outcomes need to tie to business results. Create `field_activity_outcome(activity_id, dealer_id, mgo_id, activity_type, outcome, linked_order_id, next_action, conversion_value, notes)`.

**First proof:** MGO/TBM/RBM dashboard showing target, actual, collection risk, visit intensity, and top dealer actions.

**Team asks:** Sales ops, Growthbook admin, SAP SD/FI owner, field leadership.

### 9. Activity Analytics (Growthbook + SAP)

**Production read:** This is only valuable if activity events can be linked to orders, collections, and dealer movement.

**Likely sources:** Growthbook events, SAP sales, collections, dealer master, MGO hierarchy.

**Data asks:** Raw Growthbook event export, event taxonomy, location/time fields, visit purpose, visit outcome, MGO/dealer IDs, SAP order linkage if any.

**Missing capture/schema:** Create `field_activity_event(event_id, event_time, mgo_id, dealer_id, event_type, planned_flag, geo_lat, geo_lon, duration_min, outcome_code, source)` and maintain a crosswalk to SAP dealer IDs.

**First proof:** Activity-to-conversion analysis: visits per dealer, visits before order, no-order visits, and regions with high activity but low sales lift.

**Team asks:** Growthbook admin, sales ops, SAP SD owner.

### 10. Pricing, Policy and Scheme Dissemination Chatbot

**Production read:** A field-facing retrieval and rules agent for schemes. The risk is unstructured circulars and uncodified eligibility logic.

**Likely sources:** SAP pricing conditions, scheme circulars/PDFs/images, WhatsApp/email distribution archives, dealer tiers, region/product master.

**Data asks:** Last 12-24 months of scheme circulars, active scheme list, eligibility rules, approval owners, pricing-condition extract, dealer tier/region/product mappings.

**Missing capture/schema:** Create `scheme_master(scheme_id, name, start_date, end_date, product_scope, region_scope, dealer_scope, approval_status, source_doc_id)` and `scheme_rule(rule_id, scheme_id, condition_type, field_name, operator, value, benefit_type, benefit_value)`.

**First proof:** TBM asks "Which schemes apply to dealer X for SKU Y in district Z today?" and receives answer with cited circular and eligibility logic.

**Team asks:** Sales ops, marketing/trade schemes owner, SAP SD pricing owner, field leadership.

### 11. Dealer Profiles and Field-Visit Conversation Inputs (Saathi)

**Production read:** Dealer 360 plus structured visit capture. The value is in combining SAP facts with current field notes.

**Likely sources:** SAP customer/dealer master, sales, collections, inventory/secondary sales if available, Growthbook visit logs, complaints/service logs.

**Data asks:** Dealer master, sales and collections history, dealer tier, credit limit, product mix, visit history, existing notes format, field workflow constraints.

**Missing capture/schema:** Create `dealer_profile_snapshot(dealer_id, period, revenue, growth, collection_status, product_mix_json, risk_flags_json, recommended_next_action)` and `visit_conversation_note(note_id, visit_id, dealer_id, mgo_id, captured_at, transcript_text, structured_topics_json, sentiment, follow_up_due_date)`.

**First proof:** Mobile-first dealer profile for top 20 dealers in one territory, with next-best action before each visit.

**Team asks:** Sales ops, Growthbook admin, SAP SD/FI owner, TBM/MGO pilot users.

### 12. AI-Enabled Sales Coaching

**Production read:** Coaching assistant grounded in SFS product knowledge, objections, schemes, and field performance.

**Likely sources:** ByteEdge, product manuals, scheme circulars, FAQs, objection-handling decks, field visit outcomes, sales performance data.

**Data asks:** Training content, product FAQs, common objection lists, ByteEdge completion data, role/territory mapping, product priority list.

**Missing capture/schema:** Create `coaching_content_chunk(chunk_id, source_doc_id, product_code, topic, audience_role, text, approved_by, effective_from)` and `coaching_interaction(interaction_id, user_id, query, response_id, feedback, linked_product, created_at)`.

**First proof:** MGO asks product/scheme objection questions in the field and receives approved answers with source references.

**Team asks:** Training/ByteEdge owner, product marketing, sales ops, field pilot users.

### 13. Unified Product and Partner-Level Visibility

**Production read:** Partner scorecard and drilldown. This is a semantic-layer problem more than an AI problem.

**Likely sources:** SAP SD, FI-AR, product master, dealer master, targets, Growthbook, secondary sales/inventory if available.

**Data asks:** Partner hierarchy, targets, sales, collection, product mix, credit limit, dealer tier, geography, visit activity, secondary sales if captured.

**Missing capture/schema:** Create `partner_scorecard_snapshot(partner_id, period, revenue, target_achievement, collection_health, product_mix_score, visit_health, growth_classification, next_action)`.

**First proof:** National to RBM to TBM to dealer drilldown with a standardized partner scorecard.

**Team asks:** Sales ops, finance, SAP SD/FI owner, Growthbook admin.

### 14. Real-Time Warehouse Stock Visibility

**Production read:** Queryable stock/ATP layer for field teams. Vendor warehouse stock is the likely gap.

**Likely sources:** SAP inventory/WM/EWM, plant/storage location stock, open orders, in-transit records, vendor warehouse feeds, logistics/TMS.

**Data asks:** Stock by SKU x plant/storage location, refresh frequency, ATP/open-order logic, in-transit records, warehouse mapping to territory/dealer, vendor warehouse process.

**Missing capture/schema:** Create `stock_snapshot(snapshot_time, sku, plant, storage_location, available_qty, blocked_qty, in_transit_qty, batch, expiry_date, source)` and `vendor_stock_feed(vendor_id, warehouse_id, sku, quantity, feed_time, ingestion_status)`.

**First proof:** TBM searches SKU and sees available stock, nearest location, substitute SKUs, and freshness timestamp.

**Team asks:** Supply chain, SAP MM/WM owner, logistics, vendor warehouse owner.

### 15. Early Warning For Sales Performance and Dealer Churn Risk

**Production read:** Predictive risk model plus intervention workflow. It fails without a churn definition and action logging.

**Likely sources:** SAP sales, collections, schemes, dealer master, Growthbook visits, complaints, secondary sales/inventory if available.

**Data asks:** 36 months of dealer sales/collections, scheme participation, visit frequency, product mix, credit exposure, churn/decline examples, seasonal exclusions.

**Missing capture/schema:** Create `dealer_churn_label(dealer_id, label_period, churn_definition, label, reason_code, validated_by)` and `churn_intervention(intervention_id, dealer_id, owner_id, risk_score, action_taken, action_date, outcome_after_30d, notes)`.

**First proof:** Monthly ranked risk list with top contributing factors and intervention suggestions for one pilot region.

**Team asks:** Sales ops, finance/collections, TBM/RBM pilot users, SAP SD/FI owner.

### 16. Freight Price Discovery

**Production read:** Buy-and-customize. Conformal should lead vendor evaluation, data model, integration, and AI layer on top.

**Likely sources:** TMS candidates such as FreightTiger/Shipsy/FarEye/Locus, SAP shipment/order data, freight invoices, lane masters, vendor rate cards, diesel/toll indices.

**Data asks:** Lane history, current vendor list, freight invoices, vehicle types, service levels, route/lane definitions, current RFQ process, rate cards.

**Missing capture/schema:** Create `freight_lane_rate(rate_id, lane_id, vendor_id, vehicle_type, rate_type, quoted_rate, effective_from, effective_to, fuel_index, source)` and `freight_quote_event(quote_id, lane_id, vendor_id, requested_at, response_at, quoted_rate, accepted_flag)`.

**First proof:** Vendor/TMS fit-gap and one lane-rate benchmark dashboard.

**Team asks:** Logistics lead, procurement, SAP SD/MM owner, shortlisted TMS vendors.

### 17. Optimal Route and Pickup/Drop Recommendation

**Production read:** TMS optimization module, not custom AI from scratch.

**Likely sources:** Orders/deliveries from SAP, inventory, vehicle capacity, dealer locations, plant/warehouse locations, historical trips, TMS route engine.

**Data asks:** Delivery addresses/geocodes, order priorities, vehicle types/capacity, dispatch constraints, route plans, actual trip data, direct-dispatch rules.

**Missing capture/schema:** Create `route_plan(plan_id, run_date, source_system, objective, total_distance_km, estimated_cost, status)` and `route_stop(plan_id, stop_sequence, location_id, order_id, planned_eta, actual_arrival, delivered_qty, exception_code)`.

**First proof:** Run one week of historical orders through vendor/TMS optimizer and compare planned versus actual distance/cost.

**Team asks:** Logistics operations, TMS vendor, SAP order/delivery owner.

### 18. E-Proof of Delivery (E-PoD) Execution

**Production read:** Mobile workflow and SAP/TMS integration. Minimal agentic value; should be vendor-led.

**Likely sources:** TMS/mobile POD vendor, SAP delivery/invoice, dealer master, QR/barcode data if used.

**Data asks:** Current POD process, delivery document fields, invoice linkage, exception reasons, required evidence, dealer confirmation workflow.

**Missing capture/schema:** Create `epod_event(pod_id, delivery_id, dealer_id, captured_at, geo_lat, geo_lon, signature_blob_ref, photo_refs_json, condition_status, exception_code, sap_posting_status)`.

**First proof:** Fit-gap against one vendor product and integration design for SAP posting.

**Team asks:** Logistics, SAP SD/delivery owner, dealer/channel ops, TMS/POD vendor.

### 19. Real-Time Consignment Monitoring

**Production read:** Shipment visibility. Buy vendor tracking, then integrate visibility into SFS surfaces.

**Likely sources:** TMS, GPS provider, carrier APIs, e-waybill data, SAP shipment/order data, dealer/customer master.

**Data asks:** Shipment IDs, carrier/vendor list, GPS availability, tracking update frequency, dealer visibility needs, exception workflow.

**Missing capture/schema:** Create `consignment_event(consignment_id, event_time, event_type, lat, lon, source, eta, delay_reason, exception_status)` and `shipment_order_link(consignment_id, order_id, invoice_id, dealer_id, carrier_id)`.

**First proof:** Live/near-live tracker for a small set of consignments with ETA and delay alerts.

**Team asks:** Logistics, carriers/TMS vendors, SAP delivery owner, dealer service owner.

### 20. Ocean Freight Tracking and Optimization

**Production read:** Use Project44-style or forwarder-portal aggregation. Do not build carrier tracking in-house.

**Likely sources:** Freight forwarders, container tracking providers, TMS/global visibility platform, SAP import POs, EXIM/customs data.

**Data asks:** Import PO list, forwarder list, container numbers, booking data, port of loading/discharge, inland movement tracking, demurrage/detention data.

**Missing capture/schema:** Create `ocean_shipment(shipment_id, po_id, container_no, carrier, origin_port, destination_port, etd, eta, forwarder, current_status)` and `ocean_event(shipment_id, event_time, event_type, port_or_location, source, delay_reason)`.

**First proof:** Compare 2-3 visibility vendors and demonstrate unified container status for historical/import shipments.

**Team asks:** Import procurement, logistics, forwarders, finance if demurrage impact is measured.

### 21. Technology and Infrastructure Setup

**Production read:** Mandatory foundation. This is how we avoid building 21 disconnected pilots.

**Likely sources:** All systems above plus identity, security, CI/CD, logging, model provider, data platform.

**Data asks:** Azure tenant/subscription status, network/security constraints, preferred model provider, SSO/Entra setup, data residency rules, SAP connectivity path, existing warehouse/lake/BI stack.

**Missing capture/schema:** Create platform metadata tables: `data_asset_registry(asset_id, source, owner, grain, refresh_frequency, sensitivity, quality_sla)`, `dq_check_result(check_id, asset_id, run_time, status, failed_rows, severity)`, `agent_eval_result(eval_id, use_case, question, expected_behavior, actual_result, pass_fail, reviewed_by)`, `agent_audit_log(session_id, user_id, tool_calls_json, source_rows, model, latency_ms, cost, created_at)`.

**First proof:** Production architecture and one read-only SAP extract flowing into a governed semantic layer, queried by the assistant with audit trace.

**Team asks:** SFS IT, Azure/security, SAP Basis, data/BI owner, legal/security approver.

## Cross-Use-Case Data Gaps We Should Be Honest About

1. **Taxonomy is not data plumbing.** Spend category, product hierarchy, and strategic classification need business workshops and governance.
2. **EXIM is not "real time" by default.** Provider lag, licensing, HSN mapping, and grade/spec matching will define accuracy.
3. **Field-force AI depends on capture discipline.** Dealer notes, visit outcomes, churn interventions, and negotiation outcomes must be logged or the system cannot learn.
4. **Logistics is not a custom AI build.** The right move is vendor selection plus integration and analytics on top.
5. **Enterprise assistant requires a metric dictionary.** Without one, the assistant will reproduce existing definition conflicts.
6. **Secondary sales and dealer inventory may be incomplete.** If not systematically captured, we should treat those as future data-capture workstreams.

## Suggested 30-Day Technical Plan

### Week 1: Data Access and Owner Alignment

- Get named owners for SAP SD, MM, FI/CO, Growthbook, Ariba, schemes, logistics, Azure/security.
- Receive masked sample extracts for the 12 minimum data-pack items.
- Confirm data history, grain, refresh, and extraction method per source.
- Agree top 5-6 use cases for detailed discovery.

### Week 2: Data Profiling and Feasibility Matrix

- Profile extract completeness, join keys, duplicate IDs, missing tags, date coverage, and row counts.
- Build a source-system map and data-readiness heatmap.
- Identify fields that are available, partial, unavailable, or need external vendor.
- Draft missing-capture schemas and workflow changes.

### Week 3: Prototype Real Source Slice

- Load one SAP sales/collections slice and one procurement slice into a governed dev lakehouse.
- Build semantic definitions for 10-15 executive metrics.
- Run 20 golden leadership questions and 10 procurement questions.
- Start EXIM/provider and logistics/TMS vendor shortlist.

### Week 4: Proposal-Ready Architecture and SOW

- Produce wave plan with dependencies, data access assumptions, and build scope.
- Define Wave 1 success metrics and acceptance tests.
- Price the production assistant and platform foundation separately from later waves.
- Capture explicit exclusions: E-PoD custom build, ocean freight build-from-scratch, uncaptured secondary sales if SFS cannot provide it.

## First Message To Send The Team

We have completed a first technical read of all 21 use cases across the SFS/Bain sheet, our demo data model, and the available field-level data notes. The main conclusion is that the demo proves the AI experience, but production depends on validating source-system access and data capture.

For the next working session, we would like to align on four things:

1. Which SAP/Ariba/Growthbook/Concur/ByteEdge/logistics systems currently hold the required data.
2. How much history exists, at what grain, and how it can be extracted read-only.
3. Which fields are not captured today and need new workflow/schema design.
4. Which 5-6 use cases should enter detailed discovery first.

Our recommendation is to start with Platform + Enterprise Assistant, then fold Field Force and Procurement into two integrated suites rather than treating the sheet as 21 separate builds.
