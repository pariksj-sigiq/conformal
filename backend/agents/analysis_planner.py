"""Agent 2: AnalysisPlanner.

Decomposes an interpreted question into 1-4 analyses. Sees the full schema and
the analysis pattern library so it can produce concrete, type-tagged specs that
the QueryExecutor can turn into SQL.
"""
from __future__ import annotations

from backend.contracts import Analysis, Plan
from backend.llm import complete_json
from backend.prompts import load_doc, load_prompt, render


def plan(interpreted_question: str, implicit_assumptions: list[str] | None = None) -> Plan:
    deterministic = _deterministic_demo_plan(interpreted_question)
    if deterministic:
        return deterministic

    template = load_prompt("planner")
    system = render(
        template,
        schema=load_doc("SCHEMA.md"),
        analysis_patterns=load_doc("ANALYSIS_PATTERNS.md"),
    )
    user = (
        "INTERPRETED QUESTION:\n"
        f"{interpreted_question}\n\n"
        "IMPLICIT ASSUMPTIONS:\n"
        f"{chr(10).join('- ' + a for a in (implicit_assumptions or [])) or '(none)'}\n\n"
        "Decompose into 1-4 analyses. Return only the JSON described in the system prompt."
    )
    try:
        raw = complete_json(system, user, max_tokens=2048)
    except Exception as exc:
        if _can_use_local_fallback(exc):
            return _local_plan(interpreted_question)
        raise
    return Plan.model_validate(raw)


def _deterministic_demo_plan(interpreted_question: str) -> Plan | None:
    lower = interpreted_question.lower()
    asks_fy26_close = "fy26" in lower and any(token in lower for token in ("closing", "close", "vs plan", "where are we"))
    if asks_fy26_close:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="fy26_close_1",
                    purpose="Revenue actuals vs targets by BU and region for full FY26, showing achievement percentage and absolute variance",
                    type="comparison",
                    tables_needed=["fact_targets"],
                    filters={"fiscal_year": "FY26"},
                    measures=[
                        "SUM(actual_net_value_inr) / 10000000 AS actual_revenue_cr",
                        "SUM(target_net_value_inr) / 10000000 AS target_revenue_cr",
                        "SUM(actual_net_value_inr - target_net_value_inr) / 10000000 AS revenue_variance_cr",
                        "SUM(actual_net_value_inr) / NULLIF(SUM(target_net_value_inr), 0) * 100 AS achievement_pct",
                    ],
                    dimensions=["category", "region"],
                    expected_output_shape="BU-region rows with actual revenue, target revenue, variance, and achievement percentage",
                ),
                Analysis(
                    analysis_id="fy26_close_2",
                    purpose="EBITDA actuals vs budget by BU for full FY26, with revenue and gross margin context to understand drivers of any shortfall or beat",
                    type="comparison",
                    tables_needed=["fact_finance_pl"],
                    filters={"fiscal_year": "FY26"},
                    measures=[
                        "SUM(revenue_inr) / 10000000 AS actual_revenue_cr",
                        "SUM(revenue_budget_inr) / 10000000 AS budget_revenue_cr",
                        "SUM(revenue_variance_inr) / 10000000 AS revenue_variance_cr",
                        "SUM(gross_margin_inr) / 10000000 AS actual_gm_cr",
                        "SUM(ebitda_inr) / 10000000 AS actual_ebitda_cr",
                        "SUM(ebitda_budget_inr) / 10000000 AS budget_ebitda_cr",
                        "SUM(ebitda_variance_inr) / 10000000 AS ebitda_variance_cr",
                    ],
                    dimensions=["business_unit"],
                    expected_output_shape="BU rows with revenue, gross margin, EBITDA actuals, budgets, variance, and margin percentages",
                ),
                Analysis(
                    analysis_id="fy26_close_3",
                    purpose="Q4 FY26 close assessment by BU, comparing revenue vs target and EBITDA vs budget to identify which BUs need a final push",
                    type="comparison",
                    tables_needed=["fact_targets", "fact_finance_pl"],
                    filters={"fiscal_year": "FY26", "fiscal_quarter": "Q4"},
                    measures=[
                        "SUM(target_net_value_inr) / 10000000 AS q4_target_revenue_cr",
                        "SUM(actual_net_value_inr) / 10000000 AS q4_actual_revenue_cr",
                        "SUM(actual_net_value_inr) / NULLIF(SUM(target_net_value_inr), 0) * 100 AS q4_achievement_pct",
                        "SUM(ebitda_inr) / 10000000 AS q4_actual_ebitda_cr",
                        "SUM(ebitda_budget_inr) / 10000000 AS q4_budget_ebitda_cr",
                    ],
                    dimensions=["business_unit"],
                    expected_output_shape="BU rows for Q4 with target revenue, actual revenue, achievement percentage, actual EBITDA, budget EBITDA, and EBITDA variance",
                ),
                Analysis(
                    analysis_id="fy26_close_4",
                    purpose="Quarterly revenue trend across all four quarters of FY26 by BU to show whether performance improved or deteriorated through the year",
                    type="trend",
                    tables_needed=["fact_targets"],
                    filters={"fiscal_year": "FY26"},
                    measures=[
                        "SUM(actual_net_value_inr) / 10000000 AS actual_revenue_cr",
                        "SUM(target_net_value_inr) / 10000000 AS target_revenue_cr",
                        "SUM(actual_net_value_inr) / NULLIF(SUM(target_net_value_inr), 0) * 100 AS achievement_pct",
                    ],
                    dimensions=["fiscal_quarter", "category"],
                    expected_output_shape="Quarter-BU rows with actual revenue, target revenue, variance, and achievement percentage",
                ),
            ],
            plan_rationale=(
                "A comprehensive FY26 performance vs plan view needs four complementary lenses: "
                "revenue achievement by BU and region, full P&L context, Q4 close risk, and quarterly trajectory."
            ),
        )

    rich = _rich_demo_plan(interpreted_question)
    if rich:
        return rich

    return None


def _can_use_local_fallback(error: Exception) -> bool:
    message = str(error).lower()
    return (
        "content_filter" in message
        or "too many requests" in message
        or "429" in message
        or "timed out" in message
        or "timeout" in message
    )


def _rich_demo_plan(interpreted_question: str) -> Plan | None:
    lower = interpreted_question.lower()
    asks_revenue = any(token in lower for token in ("revenue", "sales", "topline", "turnover"))
    asks_ebitda = any(token in lower for token in ("ebitda", "pbdt", "profit", "margin"))
    asks_time = any(token in lower for token in ("time series", "trend", "month", "monthly", "over time", "last 12 months"))
    asks_last_two_quarters = "last two quarter" in lower or "last 2 quarter" in lower
    asks_procurement = any(token in lower for token in ("procurement", "supplier", "purchase", "raw material", "above market", "savings", "premium vs market"))
    asks_distributor = any(token in lower for token in ("distributor", "dealer", "paying late", "selling slow", "dso"))
    asks_field_force = any(token in lower for token in ("field force", "mgo", "visit", "coverage"))
    asks_regulatory = any(token in lower for token in ("regulatory", "registration", "pipeline", "molecule", "regulator"))
    asks_ebitda_variance = "ebitda" in lower and any(token in lower for token in ("miss", "variance", "budget", "bridge", "why"))

    if asks_procurement:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="procurement_1",
                    purpose="Rank FY26 market-linked procurement categories by spend, savings versus spot, and premium percentage",
                    type="ranking",
                    tables_needed=["fact_procurement"],
                    filters={"fiscal_year": "FY26", "commodity_link": "NOT NULL"},
                    measures=[
                        "SUM(total_value_inr) / 10000000 AS spend_cr",
                        "SUM((market_spot_price_inr - contracted_price_inr) * qty) / 10000000 AS savings_vs_market_cr",
                        "AVG(premium_vs_market_pct) AS premium_vs_market_pct",
                        "COUNT(*) AS po_count",
                    ],
                    dimensions=["material_category"],
                    expected_output_shape="Material-category rows ordered by market premium and opportunity size",
                ),
                Analysis(
                    analysis_id="procurement_2",
                    purpose="Show whether procurement premium versus market is structural across FY26 months and materials",
                    type="trend",
                    tables_needed=["fact_procurement"],
                    filters={"fiscal_year": "FY26", "commodity_link": "NOT NULL"},
                    measures=[
                        "AVG(premium_vs_market_pct) AS premium_vs_market_pct",
                        "SUM(total_value_inr) / 10000000 AS spend_cr",
                    ],
                    dimensions=["month", "material_category"],
                    expected_output_shape="Month-material rows with average premium percentage and spend",
                ),
                Analysis(
                    analysis_id="procurement_3",
                    purpose="Identify suppliers and countries behind the largest procurement market premiums",
                    type="breakdown",
                    tables_needed=["fact_procurement", "dim_supplier"],
                    filters={"fiscal_year": "FY26", "commodity_link": "NOT NULL"},
                    measures=[
                        "SUM(total_value_inr) / 10000000 AS spend_cr",
                        "SUM((contracted_price_inr - market_spot_price_inr) * qty) / 10000000 AS premium_paid_cr",
                        "AVG(premium_vs_market_pct) AS premium_vs_market_pct",
                    ],
                    dimensions=["supplier_name", "country"],
                    expected_output_shape="Supplier-country rows ranked by premium paid in crores",
                ),
            ],
            plan_rationale=(
                "Procurement questions need a market-premium answer, a time-series check to separate structural issues from one-off buys, "
                "and supplier concentration so the renegotiation lever is visible."
            ),
        )

    if asks_distributor:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="distributor_risk_1",
                    purpose="Rank distributors by combined buying decline, late-payment DSO, and slow sell-through risk",
                    type="composite_score",
                    tables_needed=["fact_primary_sales", "fact_secondary_sales", "fact_collections", "fact_inventory", "dim_distributor"],
                    filters={"fiscal_year": "FY26"},
                    measures=[
                        "FY26 revenue versus FY25 revenue",
                        "AVG(actual_payment_days) AS avg_dso_days",
                        "sell_out_value_inr / net_value_inr AS sell_through_pct",
                        "AVG(days_aging) AS avg_inventory_age_days",
                    ],
                    dimensions=["distributor_id"],
                    expected_output_shape="Distributor risk rows with revenue decline, DSO, sell-through, inventory age, and risk score",
                ),
                Analysis(
                    analysis_id="distributor_risk_2",
                    purpose="Show geographic and crop-belt concentration of distributors with the highest risk scores",
                    type="breakdown",
                    tables_needed=["fact_primary_sales", "fact_collections", "fact_inventory", "dim_distributor"],
                    filters={"risk_score": "top cohort"},
                    measures=[
                        "COUNT(*) AS distributor_count",
                        "SUM(revenue_at_risk_cr) AS revenue_at_risk_cr",
                        "AVG(avg_dso_days) AS avg_dso_days",
                    ],
                    dimensions=["region", "agri_belt"],
                    expected_output_shape="Region and agri-belt rows for the at-risk distributor cohort",
                ),
                Analysis(
                    analysis_id="distributor_risk_3",
                    purpose="Compare healthy versus at-risk distributors on DSO, sell-through, and inventory age",
                    type="comparison",
                    tables_needed=["fact_primary_sales", "fact_secondary_sales", "fact_collections", "fact_inventory"],
                    filters={"cohort": "risk cohorts"},
                    measures=[
                        "AVG(avg_dso_days) AS avg_dso_days",
                        "AVG(sell_through_pct) AS sell_through_pct",
                        "AVG(avg_inventory_age_days) AS avg_inventory_age_days",
                    ],
                    dimensions=["risk_cohort"],
                    expected_output_shape="Risk cohort comparison rows with payment, sell-through, and inventory metrics",
                ),
            ],
            plan_rationale=(
                "Distributor-health questions need an entity ranking, a geography concentration view, and a healthy-versus-risky benchmark "
                "so the answer is actionable rather than just a list."
            ),
        )

    if asks_field_force:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="field_force_1",
                    purpose="Summarise Q4 FY26 field-force visit outcomes and conversion into orders",
                    type="breakdown",
                    tables_needed=["fact_field_visits"],
                    filters={"date_range": "2026-01-01..2026-03-31"},
                    measures=["COUNT(*) AS visits", "AVG(duration_min) AS avg_duration_min"],
                    dimensions=["visit_outcome"],
                    expected_output_shape="Visit-outcome rows with count, share, and average duration",
                ),
                Analysis(
                    analysis_id="field_force_2",
                    purpose="Compare field-force coverage and order conversion by region in Q4 FY26",
                    type="comparison",
                    tables_needed=["fact_field_visits", "dim_distributor"],
                    filters={"date_range": "2026-01-01..2026-03-31"},
                    measures=[
                        "COUNT(*) AS visits",
                        "COUNT(DISTINCT distributor_id) AS distributors_touched",
                        "order placed visits / visits AS order_conversion_pct",
                    ],
                    dimensions=["region"],
                    expected_output_shape="Region rows with visits, coverage, order conversion, and average duration",
                ),
                Analysis(
                    analysis_id="field_force_3",
                    purpose="Identify top and bottom MGO productivity in Q4 FY26 by visit volume and order conversion",
                    type="ranking",
                    tables_needed=["fact_field_visits", "dim_employee"],
                    filters={"date_range": "2026-01-01..2026-03-31"},
                    measures=[
                        "COUNT(*) AS visits",
                        "order placed visits / visits AS order_conversion_pct",
                        "COUNT(DISTINCT distributor_id) AS distributors_touched",
                    ],
                    dimensions=["mgo_id", "name"],
                    expected_output_shape="MGO rows ranked by visit volume and conversion",
                ),
            ],
            plan_rationale=(
                "Field-force questions need outcome mix, regional coverage, and MGO productivity together; otherwise the answer cannot distinguish activity from quality."
            ),
        )

    if asks_regulatory:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="regulatory_pipeline_1",
                    purpose="Establish headline regulatory pipeline value and registration count by active status",
                    type="kpi_lookup",
                    tables_needed=["fact_regulatory_pipeline"],
                    filters={"status": "Filed|Under Review"},
                    measures=[
                        "SUM(expected_revenue_uplift_inr_cr_y1) AS pipeline_value_cr",
                        "COUNT(*) AS registrations",
                    ],
                    dimensions=["status"],
                    expected_output_shape="Status rows with in-flight Y1 uplift and registration count",
                ),
                Analysis(
                    analysis_id="regulatory_pipeline_2",
                    purpose="Show pipeline value concentration by country and filing status",
                    type="breakdown",
                    tables_needed=["fact_regulatory_pipeline"],
                    filters={"status": "Filed|Under Review"},
                    measures=["SUM(expected_revenue_uplift_inr_cr_y1) AS pipeline_value_cr", "COUNT(*) AS registrations"],
                    dimensions=["country", "status"],
                    expected_output_shape="Country-status rows with pipeline value and registration count",
                ),
                Analysis(
                    analysis_id="regulatory_pipeline_3",
                    purpose="Rank molecules and markets with the largest Y1 revenue uplift still in flight",
                    type="ranking",
                    tables_needed=["fact_regulatory_pipeline"],
                    filters={"status": "Filed|Under Review"},
                    measures=["expected_revenue_uplift_inr_cr_y1 AS pipeline_value_cr"],
                    dimensions=["molecule", "trade_name", "country", "regulator", "status"],
                    expected_output_shape="Top in-flight molecule-country rows by Y1 uplift",
                ),
            ],
            plan_rationale=(
                "Regulatory-pipeline questions need a headline value, country-status concentration, and molecule-level table so strategic markets and blockers are visible."
            ),
        )

    if asks_ebitda_variance:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="ebitda_variance_1",
                    purpose="Establish Q2 FY26 EBITDA actual, budget, and variance",
                    type="kpi_lookup",
                    tables_needed=["fact_finance_pl"],
                    filters={"fiscal_year": "FY26", "fiscal_quarter": "Q2"},
                    measures=[
                        "SUM(ebitda_inr) / 10000000 AS ebitda_cr",
                        "SUM(ebitda_budget_inr) / 10000000 AS ebitda_budget_cr",
                        "SUM(ebitda_variance_inr) / 10000000 AS ebitda_variance_cr",
                    ],
                    dimensions=[],
                    expected_output_shape="Single row with Q2 FY26 EBITDA actual, budget, and variance",
                ),
                Analysis(
                    analysis_id="ebitda_variance_2",
                    purpose="Decompose Q2 FY26 EBITDA variance into revenue, COGS, and opex effects",
                    type="decomposition",
                    tables_needed=["fact_finance_pl"],
                    filters={"fiscal_year": "FY26", "fiscal_quarter": "Q2"},
                    measures=[
                        "SUM(revenue_variance_inr) / 10000000 AS revenue_effect_cr",
                        "SUM(cogs_budget_inr - cogs_inr) / 10000000 AS cogs_effect_cr",
                        "SUM(opex_budget_inr - opex_inr) / 10000000 AS opex_effect_cr",
                    ],
                    dimensions=["variance_component"],
                    expected_output_shape="Bridge rows for revenue, COGS, and opex effects",
                ),
                Analysis(
                    analysis_id="ebitda_variance_3",
                    purpose="Identify which BU drove the Q2 FY26 EBITDA miss",
                    type="breakdown",
                    tables_needed=["fact_finance_pl"],
                    filters={"fiscal_year": "FY26", "fiscal_quarter": "Q2"},
                    measures=[
                        "SUM(revenue_variance_inr) / 10000000 AS revenue_variance_cr",
                        "SUM(ebitda_inr) / 10000000 AS ebitda_cr",
                        "SUM(ebitda_budget_inr) / 10000000 AS ebitda_budget_cr",
                        "SUM(ebitda_variance_inr) / 10000000 AS ebitda_variance_cr",
                    ],
                    dimensions=["business_unit"],
                    expected_output_shape="BU rows with Q2 revenue and EBITDA variances",
                ),
                Analysis(
                    analysis_id="ebitda_variance_4",
                    purpose="Compare EBITDA variance across FY26 quarters to show whether Q2 was isolated or part of a trend",
                    type="trend",
                    tables_needed=["fact_finance_pl"],
                    filters={"fiscal_year": "FY26"},
                    measures=["SUM(ebitda_variance_inr) / 10000000 AS ebitda_variance_cr"],
                    dimensions=["fiscal_quarter"],
                    expected_output_shape="Quarter rows with FY26 EBITDA variance in crores",
                ),
            ],
            plan_rationale=(
                "EBITDA-miss questions need the headline, a driver bridge, BU ownership, and quarter context; a single variance table is too shallow."
            ),
        )

    if asks_revenue or asks_ebitda or asks_time or asks_last_two_quarters:
        finance_filters = {"fiscal_year": "FY26", "fiscal_quarter": "Q3|Q4"} if asks_last_two_quarters else {"fiscal_year": "FY26"}
        period_label = "Q3-Q4 FY26" if asks_last_two_quarters else "FY26"
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="finance_trend_1",
                    purpose=f"Show {period_label} revenue, EBITDA, and EBITDA margin trajectory",
                    type="trend",
                    tables_needed=["fact_finance_pl"],
                    filters=finance_filters,
                    measures=[
                        "SUM(revenue_inr) / 10000000 AS revenue_cr",
                        "SUM(ebitda_inr) / 10000000 AS ebitda_cr",
                        "SUM(ebitda_inr) / NULLIF(SUM(revenue_inr), 0) * 100 AS ebitda_margin_pct",
                    ],
                    dimensions=["month"],
                    expected_output_shape="Monthly FY26 rows with revenue, EBITDA, and EBITDA margin",
                ),
                Analysis(
                    analysis_id="finance_trend_2",
                    purpose=f"Break {period_label} revenue and EBITDA performance down by business unit",
                    type="breakdown",
                    tables_needed=["fact_finance_pl"],
                    filters=finance_filters,
                    measures=[
                        "SUM(revenue_inr) / 10000000 AS revenue_cr",
                        "SUM(ebitda_inr) / 10000000 AS ebitda_cr",
                        "SUM(ebitda_inr) / NULLIF(SUM(revenue_inr), 0) * 100 AS ebitda_margin_pct",
                    ],
                    dimensions=["business_unit"],
                    expected_output_shape="BU rows with FY26 revenue, EBITDA, and EBITDA margin",
                ),
                Analysis(
                    analysis_id="finance_trend_3",
                    purpose=f"Compare {period_label} quarter-level revenue and EBITDA to highlight the exit-rate problem",
                    type="comparison",
                    tables_needed=["fact_finance_pl"],
                    filters=finance_filters,
                    measures=[
                        "SUM(revenue_inr) / 10000000 AS revenue_cr",
                        "SUM(ebitda_inr) / 10000000 AS ebitda_cr",
                        "SUM(ebitda_inr) / NULLIF(SUM(revenue_inr), 0) * 100 AS ebitda_margin_pct",
                    ],
                    dimensions=["fiscal_quarter"],
                    expected_output_shape="Quarter rows with revenue, EBITDA, and margin",
                ),
            ],
            plan_rationale=(
                "Finance trend questions need movement over time, BU contribution, and quarter-level context so the answer explains both trajectory and ownership."
            ),
        )

    return None


def _local_plan(interpreted_question: str) -> Plan:
    rich = _rich_demo_plan(interpreted_question)
    if rich:
        return rich

    lower = interpreted_question.lower()
    asks_revenue = any(token in lower for token in ("revenue", "sales", "topline", "turnover"))
    asks_ebitda = any(token in lower for token in ("ebitda", "pbdt", "profit", "margin"))
    asks_time = any(token in lower for token in ("time series", "trend", "month", "monthly", "over time"))
    asks_last_two_quarters = "last two quarter" in lower or "last 2 quarter" in lower
    asks_procurement = any(token in lower for token in ("procurement", "supplier", "purchase", "po ", "savings", "premium vs market"))
    asks_fy26_ytd = any(token in lower for token in ("fy26 year-to-date", "fy26 ytd", "year-to-date", "ytd"))
    asks_distributor = any(token in lower for token in ("distributor", "dealer", "paying late", "selling slow", "dso"))
    asks_field_force = any(token in lower for token in ("field force", "mgo", "visit", "coverage"))
    asks_regulatory = any(token in lower for token in ("regulatory", "registration", "pipeline", "molecule", "regulator"))
    asks_ebitda_variance = "ebitda" in lower and any(token in lower for token in ("miss", "variance", "budget", "bridge"))

    if asks_procurement:
        filters = {"fiscal_year": "FY26"} if asks_fy26_ytd or "fy26" in lower else {}
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="procurement_1",
                    purpose="Compare procurement value and savings against market price by material category",
                    type="breakdown",
                    tables_needed=["fact_procurement"],
                    filters=filters,
                    measures=[
                        "SUM(total_value_inr) / 10000000 AS spend_cr",
                        "SUM((market_spot_price_inr - contracted_price_inr) * qty) / 10000000 AS savings_vs_market_cr",
                        "AVG(premium_vs_market_pct) AS premium_vs_market_pct",
                    ],
                    dimensions=["material_category"],
                    expected_output_shape="Material-category rows with spend, savings against market, and average premium percentage",
                )
            ],
            plan_rationale="Used the local procurement planning fallback after the LLM provider rejected or under-specified a safe business prompt.",
        )

    if asks_ebitda_variance:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="ebitda_variance_1",
                    purpose="Break down Q2 FY26 EBITDA variance against budget by business unit",
                    type="breakdown",
                    tables_needed=["fact_finance_pl"],
                    filters={"fiscal_year": "FY26", "fiscal_quarter": "Q2"},
                    measures=[
                        "SUM(ebitda_inr) / 10000000 AS ebitda_cr",
                        "SUM(ebitda_budget_inr) / 10000000 AS ebitda_budget_cr",
                        "SUM(ebitda_variance_inr) / 10000000 AS ebitda_variance_cr",
                    ],
                    dimensions=["business_unit"],
                    expected_output_shape="Business-unit rows with actual EBITDA, budget EBITDA, and variance in crores",
                )
            ],
            plan_rationale="Used the local EBITDA variance fallback after the LLM provider rejected or under-specified a safe business prompt.",
        )

    if asks_distributor:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="distributor_risk_1",
                    purpose="Rank distributors by late-payment exposure and DSO",
                    type="ranking",
                    tables_needed=["fact_collections"],
                    filters={"status": "Paid"},
                    measures=[
                        "SUM(invoice_value_inr) / 10000000 AS paid_revenue_cr",
                        "AVG(actual_payment_days) AS avg_dso_days",
                        "SUM(days_overdue) AS overdue_days",
                    ],
                    dimensions=["distributor_id"],
                    expected_output_shape="Distributor rows with paid revenue, average DSO, and overdue-day load",
                )
            ],
            plan_rationale="Used the local distributor-risk fallback after the LLM provider rejected or under-specified a safe business prompt.",
        )

    if asks_field_force:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="field_force_1",
                    purpose="Summarise field-force activity by visit outcome",
                    type="breakdown",
                    tables_needed=["fact_field_visits"],
                    filters={},
                    measures=[
                        "COUNT(*) AS visits",
                        "AVG(duration_min) AS avg_duration_min",
                    ],
                    dimensions=["visit_outcome"],
                    expected_output_shape="Visit-outcome rows with visit counts and average duration",
                )
            ],
            plan_rationale="Used the local field-force fallback after the LLM provider rejected or under-specified a safe business prompt.",
        )

    if asks_regulatory:
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="regulatory_pipeline_1",
                    purpose="Summarise in-flight regulatory pipeline value by country and status",
                    type="breakdown",
                    tables_needed=["fact_regulatory_pipeline"],
                    filters={"status": "Filed|Under Review"},
                    measures=[
                        "SUM(expected_revenue_uplift_inr_cr_y1) AS pipeline_value_cr",
                        "COUNT(*) AS registrations",
                    ],
                    dimensions=["country", "status"],
                    expected_output_shape="Country and status rows with pipeline value and registration count",
                )
            ],
            plan_rationale="Used the local regulatory-pipeline fallback after the LLM provider rejected or under-specified a safe business prompt.",
        )

    if asks_revenue or asks_ebitda or asks_last_two_quarters:
        measures = []
        if asks_revenue or asks_last_two_quarters:
            measures.append("SUM(revenue_inr) / 10000000 AS revenue_cr")
        if asks_ebitda or asks_last_two_quarters:
            measures.append("SUM(ebitda_inr) / 10000000 AS ebitda_cr")
            measures.append("CASE WHEN SUM(revenue_inr) = 0 THEN NULL ELSE SUM(ebitda_inr) / SUM(revenue_inr) * 100 END AS ebitda_margin_pct")

        dimensions = ["month"] if asks_time else ["fiscal_year", "fiscal_quarter"]
        filters = {"fiscal_year": "FY26", "fiscal_quarter": "Q3|Q4"} if asks_last_two_quarters else {}
        return Plan(
            analyses=[
                Analysis(
                    analysis_id="finance_1",
                    purpose="Answer the finance performance question from the monthly P&L table",
                    type="trend" if asks_time or asks_last_two_quarters else "kpi_lookup",
                    tables_needed=["fact_finance_pl"],
                    filters=filters,
                    measures=measures or ["SUM(revenue_inr) / 10000000 AS revenue_cr"],
                    dimensions=dimensions,
                    expected_output_shape="Rows grouped by the requested period with finance metrics in crores",
                )
            ],
            plan_rationale="Used the local finance planning fallback after the LLM provider rejected a safe business prompt.",
        )

    return Plan(
        analyses=[
            Analysis(
                analysis_id="sales_1",
                purpose="Summarise booked revenue by region and category",
                type="breakdown",
                tables_needed=["sales_enriched"],
                filters={},
                measures=["SUM(net_value_inr) / 10000000 AS booked_revenue_cr"],
                dimensions=["region", "category"],
                expected_output_shape="Regional/category revenue rows in crores",
            )
        ],
        plan_rationale="Used the local sales planning fallback after the LLM provider rejected a safe business prompt.",
    )
