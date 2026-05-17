# SFS Project Leap: 21 Use Cases Technical Deep Dive

Last updated: May 15, 2026

## Purpose

This document converts the SFS / Bain use-case sheet into a technical delivery view for Conformal. It separates what the SFS document asks for from what actually has to be built, integrated, bought, governed, and validated.

The current DCM Shriram cockpit is a strong demo vertical slice. It proves that an executive can ask a cross-functional question and receive an answer with a trace, SQL, narrative, and chart. Production is a different problem: real source access, identity, permissions, data quality, refresh, semantic definitions, evals, audit trails, deployment, and support.

## Recommended Program Shape

### Wave 0: Technical Discovery

Duration: 1-2 weeks.

Outputs:
- Source-system map across SAP S4HANA, Growthbook, Ariba, Concur, ByteEdge, scheme repositories, logistics systems, and external data providers.
- Data availability matrix by use case.
- Security and deployment architecture for Azure / VPC / on-prem constraints.
- Feasibility ranking of all 21 use cases.
- Shortlist of Wave 1 and Wave 2 production builds.
- Clarification questions and assumptions for commercial proposal.

### Wave 1: Platform Foundation + Enterprise Assistant

Build the reusable production foundation and productionize the existing cockpit into an enterprise assistant. This should be the anchor.

### Wave 2: Field Force Agent Suite

Collapse Field Performance Dashboard, Scheme Chatbot, Dealer Profiles, Sales Coaching, Partner Visibility, Stock Visibility, and Churn Risk into a coherent field-force product suite. Do not sell eight disconnected apps.

### Wave 3: Procurement Copilot Suite

Collapse Historical Spend, EXIM Intelligence, Negotiation Prep, Vendor ID, Vendor Risk, and Should-Cost into one procurement decision product.

### Wave 4: Logistics Vendor Selection And Integration

Treat logistics as buy-and-customize. Conformal can lead vendor evaluation, architecture, fit-gap, and integration PMO. Avoid custom-building TMS, E-PoD, ocean tracking, or route optimization from scratch.

## Shared Technical Foundation Needed Across Most Use Cases

### Source Connectors

Likely sources:
- SAP S4HANA: sales, collections, purchase register, vendor master, customer master, inventory, targets, P&L, GL, shipment/order objects.
- Growthbook: field activity logs, visit logs, field hierarchy, farmer/dealer interactions.
- Ariba: vendor onboarding, RFQs, contracts, sourcing workflows.
- Concur: field expense and SG&A data where relevant.
- ByteEdge: training modules and field-force learning activity.
- Scheme/circular repositories: PDFs, images, WhatsApp/email exports, pricing masters.
- External data: EXIM/customs, commodity indices, GST, MCA21, credit bureau, court/litigation sources, logistics market-rate feeds.

### Data Platform

Minimum production architecture:
- Landing zone for raw extracts and APIs.
- Curated data lakehouse / warehouse.
- Entity resolution for dealers, vendors, products, employees, territories, warehouses, and SKUs.
- Semantic layer for metrics and business definitions.
- Refresh orchestration with freshness indicators.
- Data quality checks, lineage, and failure alerts.

### Agent Platform

Reusable components:
- Intent router and clarification flow.
- Tool layer for SQL, retrieval, chart generation, report generation, document parsing, and workflow actions.
- Role-aware permissions.
- Trace rail: prompts, tools, SQL, result shape, citations, model, latency, cost.
- Eval harness with golden questions and expected outputs.
- Human feedback loop and regression testing.

### App Surfaces

Likely surfaces:
- Executive web cockpit for leadership.
- TBM/RBM/MGO mobile-first web or embedded app surface.
- Procurement copilot web app.
- Admin console for data refresh, evals, logs, and access.
- Optional Teams/WhatsApp/email alert channels after the core app works.

## Use Case Deep Dives

## 1. Enterprise Assistant: Enterprise Chat Assistant

### What This Really Is

A production version of the current demo: a governed executive analytics agent over sales, supply, finance, collections, targets, inventory, and later other functions.

### What Needs To Be Done

Data work:
- Connect SAP S4HANA extracts or APIs for sales, collections, targets, inventory, purchase, finance, and working-capital data.
- Define the enterprise metrics dictionary: revenue, gross margin, EBITDA/PBDIT, collections, DSO, inventory ageing, sell-in, sell-out, target achievement.
- Harmonize product, dealer, region, and fiscal-calendar dimensions.
- Ingest historical leadership decks and recurring review questions to build the intent library.

Product work:
- Convert the demo cockpit into a role-aware leadership assistant.
- Add follow-up context, saved/pinned answers, export to PPT/PDF, and source citations.
- Add weekly "what changed" digest for top metric movements and anomalies.
- Add admin controls for data freshness, failed queries, and eval outcomes.

AI work:
- Production SQL agent with semantic schema context and refusal behavior.
- Chart and narrative generation bounded by verified result rows.
- Eval suite for leadership questions: FY closing, distributor risk, procurement premium, regulatory pipeline, EBITDA variance, collections, inventory, target misses.

Integrations:
- SAP / Power BI / warehouse source.
- Azure AD / SSO.
- Model gateway through Azure OpenAI or approved provider.

Main risks:
- Metric-definition drift across Finance/Sales.
- Users asking questions the data cannot answer yet.
- SAP access delays.
- Over-promising "enterprise-wide" before the semantic layer is mature.

Conformal stance:
- Lead this as Wave 1. It is the cleanest conversion from demo to production.

## 2. Procurement: Historical Spend Analysis & Price Insights

### What This Really Is

A spend intelligence data product with an optional natural-language layer. The core is not LLM magic; it is data modeling, taxonomy, anomaly rules, and dashboards.

### What Needs To Be Done

Data work:
- Three-year SAP purchase register at PO line-item grain.
- Vendor master cleansing and deduplication.
- SKU/product taxonomy: category, sub-category, strategic class, HSN where relevant.
- Region/site/plant mapping if procurement varies by location.
- Optional Concur and Complinity integration for SG&A/license spend if included.

Product work:
- Spend cube: category x vendor x SKU x region x time.
- BPV leakage view: same/similar products bought at different prices.
- Price variance alerts, concentration alerts, and maverick spend flags.
- Monthly leadership report generation.
- Self-serve filters and exportable review packs.

AI work:
- NL query interface over the spend cube.
- Narrative explanation of anomalies.
- Optional anomaly summarizer that explains "why this price looks odd."

Integrations:
- SAP procurement and vendor master.
- Ariba later, if sourcing workflow is live.
- Email/Teams alerts after dashboard reliability is proven.

Main risks:
- Poor material descriptions and no category taxonomy.
- "Same product" matching may require manual master-data work.
- Savings claims depend on procurement acting on surfaced leakage.

Conformal stance:
- Build as part of a Procurement Copilot suite, not as a standalone chatbot.

## 3. Procurement: Real-Time Import Data Analysis

### What This Really Is

An external market-intelligence and benchmarking product. It needs EXIM data licensing/feeds and HSN-to-SKU mapping more than an AI interface.

### What Needs To Be Done

Data work:
- Select EXIM/customs data provider and clarify refresh frequency.
- Build HSN-to-SFS-SKU mapping.
- Normalize import prices into comparable landed-cost benchmarks.
- Link SAP purchase prices to HSN/product families.
- Capture country of origin, importer, supplier, quantity, price, date, and port where available.

Product work:
- Import intelligence dashboard by product/HSN.
- SFS purchase price vs import parity view.
- Top source countries and top importers view.
- Weekly alerts for price drops, large competitor imports, and SFS premium over benchmark.

AI work:
- Summarize market movement and suggest sourcing implications.
- Feed EXIM facts into negotiation packs.
- Clarify when EXIM benchmark is not a true comparable due to grade, formulation, freight, duties, or timing.

Integrations:
- EXIM provider API/files.
- SAP purchase register.
- Commodity price feeds where relevant.

Main risks:
- EXIM data quality and lag.
- HSN mapping ambiguity.
- Overstating benchmark accuracy where grade/spec differs.

Conformal stance:
- Include as a data module under Procurement Copilot.

## 4. Procurement: AI-Driven Preparation Material For Negotiations

### What This Really Is

A procurement agent that generates negotiation briefs from internal purchase history, external benchmarks, vendor history, and category rules.

### What Needs To Be Done

Data work:
- SAP purchase history by SKU/vendor/category.
- EXIM benchmark and commodity price history.
- Vendor performance: delivery, quality, rejections, credit, disputes.
- Historical contracts and negotiation outcomes if available.
- Category playbooks and buyer notes.

Product work:
- Negotiation brief generator by commodity and vendor.
- Recommended target price, walk-away range, opening anchor, and counter-arguments.
- Vendor history page: quote behavior, delivery reliability, quality issues, share of wallet.
- Exportable pack for buyer meetings.

AI work:
- RAG over vendor/category documents.
- Structured brief generation with citations.
- Scenario generation: vendor says X, buyer responds Y.
- Guardrails to avoid unsupported recommendations.

Integrations:
- SAP and external pricing modules.
- Ariba/RFQ workflow if available.
- Document repository for contracts and vendor submissions.

Main risks:
- Negotiation recommendations can become commercially sensitive and must be auditable.
- Buyers may distrust generated scripts unless they see source evidence.
- "Target price" must come from a transparent model, not just an LLM.

Conformal stance:
- High-value agentic use case. Build after spend and benchmark foundations exist.

## 5. Procurement: AI-Led Vendor Identification & Recommendation

### What This Really Is

A vendor discovery and scoring system. It combines internal vendor performance, external supplier discovery, risk signals, and RFQ workflow.

### What Needs To Be Done

Data work:
- SAP vendor master, PO history, GRN, delivery timeliness, rejection/quality records.
- Ariba supplier/RFQ data if live.
- External supplier databases by commodity/category.
- Certifications, location, capacity, and compliance attributes where available.

Product work:
- Vendor profile page for existing and candidate vendors.
- Multi-factor vendor scoring: price, quality, delivery, capacity, risk, geography, certifications.
- Recommendation UI for vendor shortlist and vendor mix.
- New vendor onboarding handoff to risk/fraud checks.
- RFQ trigger into Ariba where feasible.

AI work:
- Entity matching across external vendor databases and internal master.
- Summarization of vendor fit and evidence.
- Explainable recommendation reasons.

Integrations:
- SAP vendor and procurement.
- Ariba onboarding/RFQ.
- External supplier databases.
- Vendor risk module.

Main risks:
- External supplier data may be incomplete or paid.
- Vendor scoring can become politically sensitive.
- Capacity and quality signals may be weak unless captured systematically.

Conformal stance:
- Useful, but should come after spend analytics and vendor risk. Do not lead with this.

## 6. Procurement: Vendor Creditworthiness & Fraud Check

### What This Really Is

A vendor risk scoring and monitoring system. This is more compliance/data integration than generative AI.

### What Needs To Be Done

Data work:
- SAP vendor master and annual spend.
- GSTIN, PAN, bank account, MCA CIN, address, directors where applicable.
- GST filing/default signals, MCA filings, credit bureau data, litigation/court data, insolvency data.
- Internal delivery, dispute, rejection, and payment issue history.

Product work:
- Vendor risk score with green/amber/red tiers.
- Risk explanation view by signal: GST, MCA, credit, litigation, duplicate entity, delivery behavior.
- New vendor onboarding check.
- Monthly monitoring alerts for active vendors.
- Spend-at-risk dashboard.

AI work:
- Document extraction from vendor onboarding packs.
- Risk narrative summarization.
- Entity-resolution assistance for duplicate/shell-company detection.

Integrations:
- Ariba onboarding if in use.
- SAP vendor master.
- External APIs: GST, MCA21, credit bureau, litigation/court providers.

Main risks:
- API availability and legal/compliance constraints.
- False positives can block legitimate suppliers.
- Credit bureau data may require separate commercial agreement.

Conformal stance:
- Build as a deterministic scoring product with AI for extraction/explanation only.

## 7. Procurement: AI-Driven Should-Cost Analysis

### What This Really Is

A category-specific cost-modeling product. It is closer to pricing science and procurement analytics than generic AI.

### What Needs To Be Done

Data work:
- Select top 5-10 categories/products where should-cost is feasible.
- Gather component cost drivers: raw materials, conversion, labor, packaging, logistics, working capital, margin assumptions.
- Commodity indices, MSP/government notifications, crude/freight indices where relevant.
- Vendor cost sheets and historical contracts.

Product work:
- Category-specific cost trees.
- Scenario sliders for commodity/labor/logistics assumptions.
- Should-cost vs last contracted price comparison.
- Vendor cost-sheet upload and variance explanation.
- Exportable negotiation appendix.

AI work:
- Extract vendor cost sheets from PDFs/Excel.
- Explain deviations from benchmark.
- Generate negotiation talking points tied to model outputs.

Integrations:
- SAP purchase history.
- External commodity/index feeds.
- Document ingestion for vendor submissions.

Main risks:
- Should-cost credibility depends on category expertise and data quality.
- Not all products will have reliable external benchmarks.
- Cost models should be reviewed by procurement SMEs before use in negotiation.

Conformal stance:
- Strong use case, but start with 2-3 categories before claiming top 10.

## 8. Field Force: Field Performance Tracking Dashboard

### What This Really Is

The anchor field-force data product. It creates the unified performance layer that many other field-force use cases depend on.

### What Needs To Be Done

Data work:
- Growthbook activity logs.
- SAP primary sales, collections, targets, dealer/product hierarchy.
- Manual Excel targets at RO/TBM/RBM level.
- MGO incentive logic and payout rules.
- Concur expenses if field-expense ROI is included.
- Master mapping between SAP dealer IDs, Growthbook dealer IDs, territories, and employee hierarchy.

Product work:
- Mobile/laptop dashboards for TBM, RBM, HO.
- Sales vs target, collections, activity completion, underperforming dealers, incentive progress.
- Natural-language query on performance analytics.
- Auto-generated weekly insight cards.
- Review-pack export.

AI work:
- NL analytics over field KPIs.
- Root-cause hypotheses grounded in actual features: fewer visits, scheme misses, product mix, collection issues.
- Insight generation for "what should this RBM/TBM do next?"

Integrations:
- SAP, Growthbook, target files, Concur.
- SSO and role hierarchy.

Main risks:
- Dealer and territory master mismatch.
- Activity data may measure effort but not outcome.
- Target files may be messy and not centrally governed.

Conformal stance:
- Make this the Field Force Wave 2 anchor.

## 9. Field Force: Activity Analytics

### What This Really Is

In the sheet this row is effectively a stub. Technically, it should be treated as a sub-module inside the Field Performance Dashboard.

### What Needs To Be Done

Data work:
- Growthbook activity logs: visits, meetings, demo events, attendance, outcomes.
- SAP sales and collection data by dealer/territory/time.
- Farmer/dealer segmentation where available.
- Campaign/scheme calendar.

Product work:
- Activity-to-outcome analysis: which activity types correlate with revenue, collections, scheme uptake, and product mix.
- MGO productivity and coverage metrics.
- Visit quality indicators, not just visit count.
- Cohort comparisons across territory, crop, dealer tier, and product category.

AI work:
- Summarize activity patterns and recommend next best actions.
- Detect weak activity signals: high visits but low conversion, low coverage of high-potential dealers.

Integrations:
- Growthbook and SAP semantic layer.

Main risks:
- Attribution is hard: activity may not cause sales in a clean way.
- If outcomes are not tagged, only directional analytics will be possible.

Conformal stance:
- Do not sell as a standalone use case. Fold into Field Performance.

## 10. Field Force: Pricing, Policy & Scheme Dissemination Chatbot

### What This Really Is

A governed scheme/pricing knowledge assistant and rules engine for field teams.

### What Needs To Be Done

Data work:
- Historical and active scheme circulars: PDFs, emails, WhatsApp images, price lists.
- SAP pricing master with effective dates.
- Dealer/customer master with region, tier, crop, eligibility tags.
- Scheme calendar and approval workflow.

Product work:
- Central scheme repository with versioning.
- Chatbot for scheme/pricing/policy questions.
- Eligibility resolver: product x region x dealer tier x period.
- Linked source circular for every answer.
- Push alerts for expiring schemes and under-participating eligible dealers.
- Query analytics for Commercial team to see confusing schemes.

AI work:
- OCR/document ingestion.
- RAG over circulars plus structured rules.
- Ambiguity handling when schemes overlap.
- Vernacular/transliteration support if field users need it.

Integrations:
- SAP pricing and customer master.
- Growthbook/field app push channel.
- Optional WhatsApp/Teams later.

Main risks:
- Unstructured circulars will conflict unless Commercial owns a structured scheme master.
- Wrong answers create dealer disputes, so every answer needs citations and effective dates.

Conformal stance:
- High-priority Field Force module. It is practical and visibly useful.

## 11. Field Force: Dealer Profiles & Field-Visit Conversation Inputs

### What This Really Is

A 360-degree dealer brief plus visit-note capture and action-item system. This is one of the most agentic field-force cases.

### What Needs To Be Done

Data work:
- SAP dealer master, sales, collections, outstanding, credit notes, commercial disputes.
- Scheme participation history.
- Growthbook visit logs and free-text notes.
- Dealer segmentation and product mix.
- Optional voice recordings with consent and policy.

Product work:
- One-page dealer brief before every visit.
- Recommended talking points and visit objectives.
- Last-visit action items and closure status.
- Voice-note capture during/after visit.
- Auto-summary, tagged action items, next follow-ups.
- Similar-dealer recommendations for cross-sell inspiration.

AI work:
- Dealer-brief generation.
- Speech-to-text, multilingual if needed.
- Structured extraction from visit conversations.
- Recommendation engine for talking points.

Integrations:
- SAP, Growthbook, field app surface.
- Calendar/task system if follow-ups are assigned.

Main risks:
- Consent/privacy for recording conversations.
- Speech quality and local-language accuracy.
- Field adoption: the app must reduce prep burden, not add admin work.

Conformal stance:
- Strong differentiator. Build after the field data foundation exists.

## 12. Field Force: AI-Enabled Sales Coaching

### What This Really Is

A vernacular coaching and roleplay assistant for MGOs/TBMs. This is closer to training enablement than core analytics.

### What Needs To Be Done

Data work:
- Product literature, safety sheets, agronomy guides, pitch decks.
- ByteEdge modules and training taxonomy.
- Objection-handling scripts and best-practice recordings.
- Field survey notes and common farmer/dealer objections.

Product work:
- Voice-first coaching assistant.
- Pre-meeting audio briefs by product, crop, region, and season.
- Roleplay scenarios with scoring.
- Feedback rubric: product accuracy, objection handling, clarity, compliance/safety.
- Progress dashboard for managers.

AI work:
- RAG over product and training material.
- Voice input/output.
- Roleplay simulation.
- Scoring with rubric and cited feedback.

Integrations:
- ByteEdge, product document repository, field app.

Main risks:
- Voice quality and local language support.
- Coaching score must be perceived as helpful, not punitive.
- Product advice must be accurate and compliant.

Conformal stance:
- Valuable, but not the first field-force build. Put after scheme/dealer/profile foundations.

## 13. Field Force: Unified Product & Partner-Level Visibility

### What This Really Is

A partner/product scorecard and hierarchy dashboard. This is mostly BI/semantic-layer work.

### What Needs To Be Done

Data work:
- SAP product master, customer/dealer master, sales, collections, targets.
- Territory and employee hierarchy.
- Product-category mapping and partner segmentation.
- PoG/inventory liquidation data if available.

Product work:
- National to RBM to TBM to dealer drill path.
- Product mix depth, target vs actual, collections ageing, partner scorecard.
- Partner classification: star, growth, maintain, turnaround.
- Monthly review pack generation.

AI work:
- NL query and narrative explanation.
- Suggested next actions based on scorecard class.

Integrations:
- SAP and target files.
- Field dashboard surface.

Main risks:
- Scorecard definitions must be accepted by Sales/Finance.
- If liquidation data is not available, avoid implying sell-out precision.

Conformal stance:
- Fold into Field Performance Dashboard rather than separate build.

## 14. Field Force: Real-Time Warehouse Stock Visibility

### What This Really Is

A stock availability and fulfilment visibility product. It is integration-heavy and not inherently AI.

### What Needs To Be Done

Data work:
- SAP own-warehouse stock with near-real-time refresh.
- Vendor-managed warehouse stock feeds via API/CSV/manual upload.
- In-transit stock from logistics/SAP.
- Product substitute mapping and warehouse/service-region mapping.

Product work:
- SKU stock search for TBMs/RBMs.
- Warehouse-level availability, freshness/staleness indicator, in-transit visibility.
- Substitute suggestions.
- Low-stock and stock-out alerts by territory/product.
- Order confirmation support or handoff.

AI work:
- Minimal. Optional natural-language stock query and substitute explanation.

Integrations:
- SAP inventory.
- Vendor warehouse systems.
- Logistics/TMS if present.

Main risks:
- "Real-time" may be impossible for vendor warehouses.
- Wrong stock visibility can damage dealer trust.
- This can become a supply-chain integration project outside Conformal's sweet spot.

Conformal stance:
- Treat as enabling data product inside Field Force only if SFS can provide reliable feeds.

## 15. Field Force: Early Warning For Sales Performance & Dealer Churn Risk

### What This Really Is

A predictive dealer-risk model with explainable alerts and intervention workflow.

### What Needs To Be Done

Data work:
- Three-year SAP dealer sales history.
- Collections, DSO, outstanding exposure.
- Scheme participation.
- Product-mix breadth/narrowing.
- Visit frequency and issue logs.
- Churn definition agreed with Sales and Finance.
- Historical labels for back-testing.

Product work:
- Monthly ranked at-risk dealer list by TBM territory.
- Risk score and top contributing factors.
- Finance view filtered by credit exposure.
- Suggested intervention playbooks.
- Outcome capture: what action was taken and whether dealer recovered.

AI/ML work:
- Feature engineering: offtake trend, order frequency, collection delay, scheme skip, product concentration, visit gaps.
- Gradient boosting / ensemble model with explainability.
- Drift monitoring and back-testing.
- LLM-generated explanation for TBM, grounded in feature attribution.

Integrations:
- SAP, Growthbook, alert channel.

Main risks:
- No agreed churn label means no credible model.
- Seasonal business can create false positives.
- Alerts are useless without intervention ownership.

Conformal stance:
- Good Wave 2/3 field module after data foundation and adoption exist.

## 16. Logistics: Freight Price Discovery

### What This Really Is

A transport management / freight marketplace capability. SFS correctly frames this as buy-and-customize.

### What Needs To Be Done

Vendor work:
- Shortlist FreightTiger, Shipsy, FarEye, Locus, or similar India-relevant vendors.
- Run fit-gap demos against SFS lanes, vehicle types, vendors, rate cards, and quote workflows.
- Compare subscription vs transaction pricing, SLAs, data ownership, exit terms.

Data/integration work:
- Historical freight rate data by lane, vehicle, vendor, route, date.
- SAP orders, shipments, invoices, vendors, customers, plants.
- Route codes, vehicle types, lane master cleanup.
- Diesel/toll index feed if benchmarking is required.

Product work:
- Rate comparison by lane/mode/vehicle.
- RFQ dispatch and quote collation.
- Vendor performance and rate history.
- Weekly rate movement alerts.

AI work:
- Optional negotiation brief and rate anomaly explanation.

Main risks:
- Custom build is not worth it.
- Freight savings depend on vendor network liquidity and operational compliance.

Conformal stance:
- Advisory/vendor-selection role, not custom product build.

## 17. Logistics: Optimal Route & Pickup/Drop Recommendation

### What This Really Is

A route optimization engine. This is a mature operations research / TMS capability, not a custom LLM use case.

### What Needs To Be Done

Vendor work:
- Validate whether shortlisted TMS vendors support route optimization, vehicle loading, direct dispatch vs warehouse routing, and plan-vs-actual analytics.

Data/integration work:
- Orders, delivery points, inventory, vehicle capacity, delivery windows, route restrictions.
- Warehouse/vendor location master.
- Historical transit time and cost by lane.

Product work:
- Daily dispatch plan generation.
- Vehicle load optimization and pickup/drop sequencing.
- Direct-dispatch vs warehouse-routing recommendation.
- Plan vs actual review.

AI work:
- Minimal. LLM can explain recommendations but should not optimize routes.

Main risks:
- Requires high-quality operational constraints.
- Route optimization fails if planners ignore recommendations due to local realities not captured in data.

Conformal stance:
- Buy through TMS vendor. Conformal can define requirements and integration architecture.

## 18. Logistics: E-Proof Of Delivery Execution

### What This Really Is

A mobile logistics workflow app integrated with SAP/TMS. This is not an AI use case.

### What Needs To Be Done

Vendor work:
- Confirm TMS/E-PoD vendor capability for driver app, dealer signature, photo, geo-tag, exception capture, and SAP update.

Data/integration work:
- Order, invoice, shipment, consignment, dealer, driver, vehicle data.
- SAP goods issue/delivery confirmation update.
- QR code feasibility if product-level scan is required.

Product work:
- Driver/dealer delivery confirmation.
- Photo and geo-tag evidence.
- Partial/damaged delivery exception workflow.
- Dealer SMS/WhatsApp confirmation.
- Invoice-to-PoD linkage.

AI work:
- Minimal. Optional damage photo classification later, but not core.

Main risks:
- Field operations rollout complexity.
- Driver/dealer adoption.
- SAP writeback and exception handling can be messy.

Conformal stance:
- Scope out of custom AI build. Recommend vendor product.

## 19. Logistics: Real-Time Consignment Monitoring

### What This Really Is

Shipment tracking / visibility from TMS or tracking providers. This is buy/integrate.

### What Needs To Be Done

Vendor work:
- Evaluate tracking vendors for GPS/cellular tracking, carrier integrations, dealer visibility, ETA alerts, and route deviation alerts.

Data/integration work:
- Consignment IDs, orders, invoices, vehicles, drivers, dealer delivery points.
- Tracking provider APIs.
- Historical transit time baselines.

Product work:
- Dealer/TBM/RBM tracking view.
- ETA and exception alerts.
- Route deviation and delay notifications.
- Historical transit performance analytics.

AI work:
- Optional delay explanation and exception summarization.

Main risks:
- Tracking depends on vendor/carrier adoption.
- GPS and phone-based tracking quality can vary.
- Real-time dealer visibility creates expectation pressure.

Conformal stance:
- Vendor-led. Conformal can help with integration and executive visibility layer.

## 20. Logistics: Ocean Freight Tracking & Optimization

### What This Really Is

Ocean freight visibility and rate intelligence. Mature products already exist.

### What Needs To Be Done

Vendor work:
- Evaluate Project44, FourKites, GoComet, Shipsy, or freight-forwarder platforms.
- Check India import workflows, container tracking, port congestion, ocean rate benchmarks, and inland leg integration.

Data/integration work:
- Purchase/import orders, container numbers, BL/AWB, freight forwarders, ports, expected arrival, plant/warehouse demand.
- Forwarder/carrier tracking APIs.
- Ocean freight rate benchmarks.

Product work:
- Unified container dashboard.
- ETA and exception alerts.
- Carrier/route/timing recommendation if vendor supports it.
- Import planning handoff to procurement/production.

AI work:
- Optional narrative summary of delayed containers and production risk.

Main risks:
- Carrier/forwarder data fragmentation.
- Optimization claims may be limited if SFS volume is small.
- Project44-style products may already cover most needs.

Conformal stance:
- Do not build. Advise vendor selection and integration.

## 21. Technology & Infrastructure Setup

### What This Really Is

The shared production foundation. This is mandatory for any serious multi-use-case program. The SFS sheet underestimates it by excluding Azure engineers and license costs.

### What Needs To Be Done

Cloud and DevOps:
- Azure subscription, billing, environments, networking, private endpoints, secrets, CI/CD.
- Dev, staging, production separation.
- Monitoring, logging, alerting, cost tracking.

Data platform:
- Data lakehouse/warehouse.
- Raw, curated, and serving layers.
- SAP integration pattern: APIs, extracts, BW, CDS views, or batch files.
- External-source ingestion framework.
- Data quality checks and lineage.

Enterprise integration:
- API gateway and secure integration layer.
- Connectors for SAP, Growthbook, Ariba, Concur, external APIs.
- Event/batch orchestration.

GenAI platform:
- Model gateway.
- Prompt/version registry.
- Tool-call framework.
- RAG/document indexing.
- Guardrails and refusal policies.
- Eval harness and regression suite.
- Trace/audit store.

Security and governance:
- SSO/RBAC.
- Data-access policies by role/function.
- Audit logs.
- DPIA/DPA/security review packet.
- Data retention policy.

Operating model:
- Ownership between Conformal, SFS IT, business SMEs, and vendors.
- Release cadence.
- Support model.
- Incident process.
- Model/data quality review rhythm.

Main risks:
- Becoming a full system-integrator program.
- Infra timelines blocking use-case momentum.
- Undefined internal ownership on SFS side.

Conformal stance:
- Architect and build the AI/data foundation needed for the first waves. Avoid owning broad enterprise data warehouse transformation beyond the use-case scope.

## Cross-Use-Case Dependency Map

### Must Exist Before Serious Production

- SSO/RBAC.
- SAP data access.
- Data lakehouse/semantic layer.
- Entity mapping: dealer, vendor, product, employee, territory, warehouse.
- Audit trace and eval harness.
- Security review and deployment model.

### Field Force Dependencies

- Dealer master and territory hierarchy.
- SAP sales/collections/targets.
- Growthbook activity logs.
- Scheme repository/pricing master.
- Field app surface and alert channel.

### Procurement Dependencies

- SAP purchase register.
- Vendor master.
- Product/category/HSN taxonomy.
- External EXIM and commodity feeds.
- Ariba/RFQ/onboarding details.
- Vendor risk data providers.

### Logistics Dependencies

- TMS/vendor choice.
- Shipment/order/invoice integration.
- Lane/route/vehicle master.
- Dealer delivery point master.
- Tracking provider APIs.

## Commercially Important Clarifications For SFS

Ask these before committing a proposal:

1. Are the cost numbers in the sheet an approved budget, Bain estimate, or internal reference?
2. What source systems are accessible in the next 30 days?
3. Does SFS have an Azure tenant and preferred deployment architecture?
4. What is the status of Ariba implementation?
5. What is the status and ownership of Growthbook data?
6. Is Concur in scope for field force and SG&A analytics?
7. Which business owner signs off on each theme?
8. Is Bain still involved in sequencing or vendor selection?
9. Is SFS expecting a written proposal, deck, or formal RFP response?
10. Can Conformal run a 1-2 week paid discovery before final pricing?

## Recommended Conformal Position

Lead with this:

"The demo shows the interaction model. The next step is to productionize it around real SFS data, permissions, refresh, auditability, and evals. We recommend a short technical discovery, then Wave 1 around the Enterprise Assistant and shared platform foundation, followed by a field-force suite. Procurement should follow once SAP/Ariba/vendor-data foundations are clear. Logistics should be handled through vendor selection and integration, not custom AI build."
