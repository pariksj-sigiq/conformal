import type { ChartPayload, ChatEvent } from "@/lib/agent-types";

const axis = { labelColor: "#5f5a55", titleColor: "#3c3835", gridColor: "#ebe5dd" };
const config = {
  background: "transparent",
  font: "IBM Plex Sans, ui-sans-serif, system-ui",
  axis,
  view: { stroke: null },
  legend: { labelColor: "#4d4742", titleColor: "#302c29" },
};

function chart(id: string, title: string, narrative: string, sql: string, spec: ChartPayload["spec"], span: ChartPayload["span"] = 2): ChartPayload {
  return { id, title, narrative, sql, spec: { ...spec, config }, span };
}

export const heroQuestions = [
  "How is the field force tracking this quarter?",
  "Show me procurement savings vs target by category.",
  "What's happening with farmer NPS across regions?",
  "Status of Wave 1 micro-battles.",
  "Channel partners at churn risk in North zone.",
  "What's moving in commodity markets today?",
];

export function scriptedEvents(prompt: string): ChatEvent[] {
  const lower = prompt.toLowerCase();
  if (lower.includes("field force")) return fieldForceEvents();
  if (lower.includes("procurement")) return procurementEvents();
  if (lower.includes("nps")) return npsEvents();
  if (lower.includes("micro")) return microbattleEvents();
  if (lower.includes("churn") || lower.includes("channel")) return churnEvents();
  if (lower.includes("commodity") || lower.includes("markets")) return commodityEvents();
  return genericEvents();
}

function baseTrace(table: string): ChatEvent[] {
  return [
    { type: "tool_start", id: `list-${table}`, tool: "list_tables", status: "running", label: "Inspecting available SFS tables" },
    { type: "tool_end", id: `list-${table}`, tool: "list_tables", status: "complete", label: "Found 8 business tables", durationMs: 82 },
    { type: "tool_start", id: `desc-${table}`, tool: "describe_table", status: "running", label: `Reading schema for ${table}` },
    { type: "tool_end", id: `desc-${table}`, tool: "describe_table", status: "complete", label: `Schema and sample rows loaded`, durationMs: 124 },
  ];
}

function fieldForceEvents(): ChatEvent[] {
  const charts = [
    chart(
      "field-coverage",
      "Field force coverage by region, current quarter",
      "Coverage is strongest in South and West. North is the clear execution gap despite meaningful order volume.",
      "-- hero:field_force_coverage\nSELECT region, SUM(visits_done)::DOUBLE / SUM(visits_planned) AS coverage, SUM(orders_booked) AS orders FROM field_force_activity WHERE date >= '2026-04-01' GROUP BY region ORDER BY coverage DESC LIMIT 10",
      {
        data: { name: "data" },
        mark: { type: "bar", cornerRadiusEnd: 5, tooltip: true },
        encoding: {
          x: { field: "coverage", type: "quantitative", axis: { format: ".0%" } },
          y: { field: "region", type: "nominal", sort: "-x" },
          color: { condition: { test: "datum.coverage < .8", value: "#B8232E" }, value: "#2F6F73" },
        },
      },
    ),
    chart(
      "field-trend",
      "Weekly visits: planned vs delivered",
      "The delivery gap narrowed in the latest weeks, but the quarter still shows persistent under-delivery versus plan.",
      "-- hero:field_force_trend\nSELECT week_starting, SUM(visits_done) AS done, SUM(visits_planned) AS planned FROM field_force_activity WHERE date >= '2026-02-01' GROUP BY 1 ORDER BY 1 LIMIT 20",
      {
        data: { name: "data" },
        transform: [{ fold: ["planned", "done"], as: ["series", "visits"] }],
        mark: { type: "line", point: true, tooltip: true },
        encoding: {
          x: { field: "week", type: "temporal" },
          y: { field: "visits", type: "quantitative" },
          color: { field: "series", type: "nominal", scale: { range: ["#B8A36A", "#B8232E"] } },
        },
      },
    ),
    chart(
      "mgo-leaderboard",
      "Top MGOs by orders booked",
      "The top performers are concentrated outside North, which suggests the gap is more operating rhythm than demand.",
      "-- hero:mgo_leaderboard\nSELECT mgo_id, region, SUM(orders_booked) AS orders FROM field_force_activity WHERE date >= '2026-04-01' GROUP BY 1,2 ORDER BY orders DESC LIMIT 10",
      {
        data: { name: "data" },
        mark: { type: "bar", tooltip: true },
        encoding: {
          x: { field: "orders", type: "quantitative" },
          y: { field: "mgo_id", type: "nominal", sort: "-x" },
          color: { field: "region", type: "nominal", scale: { range: ["#B8232E", "#2F6F73", "#6E7F4F", "#C08A3E", "#5C6670"] } },
        },
      },
    ),
  ];
  return [...baseTrace("field_force_activity"), ...charts.map((chart) => ({ type: "chart" as const, chart })), { type: "final", text: "Field execution is broadly healthy, but North is holding back the quarter. I would treat this as a focused operating cadence issue: inspect North MGO visit completion, protect the high performers, and use the next two weeks to close the planned-versus-done gap." }];
}

function procurementEvents(): ChatEvent[] {
  const charts = [
    chart("procurement-savings", "Procurement savings vs target by category", "Logistics and Raw Material are carrying the savings pool; Media and IT need sharper intervention.", "-- hero:procurement_savings\nSELECT category, SUM(savings_vs_baseline) AS savings, 10000000 AS target FROM procurement_spend WHERE month >= '2026-01-01' GROUP BY category ORDER BY savings DESC LIMIT 12", {
    data: { name: "data" },
    layer: [
      { mark: { type: "bar", cornerRadiusEnd: 4, tooltip: true }, encoding: { x: { field: "savings", type: "quantitative" }, y: { field: "category", type: "nominal", sort: "-x" }, color: { condition: { test: "datum.savings >= datum.target", value: "#2F6F73" }, value: "#B8232E" } } },
      { mark: { type: "rule", color: "#1f1b18", strokeDash: [4, 4] }, encoding: { x: { field: "target", type: "quantitative" } } },
    ],
  }, 3),
    chart("procurement-trend", "Savings run-rate over the last six months", "The run-rate is improving, but it is uneven by category, which is where governance should focus.", "-- hero:procurement_trend\nSELECT month, category, savings_vs_baseline FROM procurement_spend WHERE month >= '2025-11-01' ORDER BY month, category LIMIT 80", {
      data: { name: "data" },
      mark: { type: "line", point: true, tooltip: true },
      encoding: {
        x: { field: "month", type: "temporal" },
        y: { field: "savings_vs_baseline", type: "quantitative" },
        color: { field: "category", type: "nominal" },
      },
    }, 3),
  ];
  return [...baseTrace("procurement_spend"), ...charts.map((chart) => ({ type: "chart" as const, chart })), { type: "final", text: "The savings program is ahead where supplier concentration gives leverage, especially Logistics. The executive action is to move the under-target categories into weekly negotiation governance rather than wait for month-end variance review." }];
}

function npsEvents(): ChatEvent[] {
  const charts = [
    chart("nps-trend", "Farmer NPS trend by region", "NPS is improving overall, but North remains structurally below the system average while South is creating the benchmark.", "-- hero:farmer_nps_trend\nSELECT quarter, region, nps, sample_size FROM farmer_nps ORDER BY quarter, region LIMIT 60", {
    data: { name: "data" },
    mark: { type: "line", point: true, tooltip: true },
    encoding: {
      x: { field: "quarter", type: "ordinal" },
      y: { field: "nps", type: "quantitative" },
      color: { field: "region", type: "nominal", scale: { range: ["#B8232E", "#2F6F73", "#6E7F4F", "#C08A3E", "#5C6670"] } },
      facet: { field: "region", columns: 3 },
    },
  }, 4),
    chart("farmer-engagement-now", "Current digital engagement by region", "South pairs the best NPS with the strongest app engagement; North needs service recovery and digital activation together.", "-- hero:farmer_engagement_now\nSELECT week, region, app_dau, calls_handled, nps FROM farmer_engagement QUALIFY week = MAX(week) OVER () ORDER BY app_dau DESC LIMIT 10", {
      data: { name: "data" },
      mark: { type: "circle", size: 220, opacity: 0.82, tooltip: true },
      encoding: {
        x: { field: "app_dau", type: "quantitative" },
        y: { field: "nps", type: "quantitative" },
        size: { field: "calls_handled", type: "quantitative" },
        color: { field: "region", type: "nominal" },
      },
    }, 2),
  ];
  return [...baseTrace("farmer_nps"), ...charts.map((chart) => ({ type: "chart" as const, chart })), { type: "final", text: "Farmer sentiment is moving in the right direction, but the regional spread is too wide for comfort. North needs closed-loop recovery on the top service issues while South's operating playbook should be copied into West and Central." }];
}

function microbattleEvents(): ChatEvent[] {
  const charts = [
    chart("microbattle-status", "Wave 1 micro-battle status", "Most Wave 1 bets are moving, but two watch items and one blocked item need leadership unblockers.", "-- hero:microbattle_status\nSELECT name, owner_function, status, percent_complete, target_date, blockers FROM wave1_microbattles ORDER BY percent_complete DESC LIMIT 20", {
    data: { name: "data" },
    mark: { type: "rect", tooltip: true },
    encoding: {
      x: { field: "owner_function", type: "nominal" },
      y: { field: "name", type: "nominal", sort: "-color" },
      color: { field: "percent_complete", type: "quantitative", scale: { range: ["#F3D7D9", "#B8232E"] } },
    },
  }, 4),
    chart("microbattle-completion", "Completion by micro-battle", "The blocked leakage audit is now the bottom of the execution stack and should be the first unblock.", "-- hero:microbattle_completion\nSELECT name, status, percent_complete FROM wave1_microbattles ORDER BY percent_complete ASC LIMIT 20", {
      data: { name: "data" },
      mark: { type: "bar", tooltip: true },
      encoding: {
        x: { field: "percent_complete", type: "quantitative", axis: { format: ".0%" } },
        y: { field: "name", type: "nominal", sort: "x" },
        color: { field: "status", type: "nominal", scale: { range: ["#2F6F73", "#C08A3E", "#B8232E"] } },
      },
    }, 3),
  ];
  return [...baseTrace("wave1_microbattles"), ...charts.map((chart) => ({ type: "chart" as const, chart })), { type: "final", text: "Wave 1 is not a red program, but it has three visible pressure points. The CEO cockpit should use this view in every steerco: each watch or blocked micro-battle needs a named unblocker and a next checkpoint." }];
}

function churnEvents(): ChatEvent[] {
  const charts = [
    chart("north-churn", "North zone channel partners at churn risk", "The highest-risk partners are mostly lower tiers with high DSO and weak scheme attachment.", "-- hero:north_churn_risk\nSELECT dealer_id, tier, ytd_sales, payment_dso, churn_risk FROM channel_partners WHERE region = 'North' ORDER BY churn_risk DESC LIMIT 12", {
    data: { name: "data" },
    mark: { type: "bar", tooltip: true },
    encoding: {
      x: { field: "churn_risk", type: "quantitative", axis: { format: ".0%" } },
      y: { field: "dealer_id", type: "nominal", sort: "-x" },
      color: { field: "tier", type: "nominal", scale: { range: ["#B8232E", "#C08A3E", "#6E7F4F", "#2F6F73"] } },
    },
  }, 3),
    chart("north-churn-dso", "North risk by DSO and YTD sales", "The most urgent accounts combine high churn risk with slow payment behavior, so the recovery motion should include credit cleanup.", "-- hero:north_churn_dso\nSELECT dealer_id, tier, ytd_sales, payment_dso, churn_risk FROM channel_partners WHERE region = 'North' ORDER BY payment_dso DESC LIMIT 18", {
      data: { name: "data" },
      mark: { type: "circle", opacity: 0.82, tooltip: true },
      encoding: {
        x: { field: "payment_dso", type: "quantitative" },
        y: { field: "churn_risk", type: "quantitative", axis: { format: ".0%" } },
        size: { field: "ytd_sales", type: "quantitative" },
        color: { field: "tier", type: "nominal" },
      },
    }, 2),
  ];
  return [...baseTrace("channel_partners"), ...charts.map((chart) => ({ type: "chart" as const, chart })), { type: "final", text: "North churn risk is concentrated enough to action. Start with the top twelve dealers, split interventions between credit cleanup and scheme attachment, and make the regional head accountable for weekly recovery." }];
}

function commodityEvents(): ChatEvent[] {
  const charts = [
    chart("commodity-today", "Commodity moves today", "Urea and DAP are the current watch items; the direction matters more than the absolute price today.", "-- hero:commodity_today\nSELECT commodity, price_inr, dod_change_pct FROM commodity_prices QUALIFY date = MAX(date) OVER () ORDER BY dod_change_pct DESC LIMIT 10", {
      data: { name: "data" },
      mark: { type: "bar", tooltip: true },
      encoding: { x: { field: "dod_change_pct", type: "quantitative", axis: { format: "+.1%" } }, y: { field: "commodity", type: "nominal", sort: "-x" }, color: { condition: { test: "datum.dod_change_pct > 0", value: "#B8232E" }, value: "#2F6F73" } },
    }),
    chart("commodity-spark", "Commodity price sparklines", "The live simulator will tick this chart as market rows mutate.", "-- hero:commodity_sparkline\nSELECT date, commodity, price_inr FROM commodity_prices WHERE date >= '2026-03-15' ORDER BY date LIMIT 500", {
      data: { name: "data" },
      mark: { type: "line", tooltip: true },
      encoding: { x: { field: "date", type: "temporal" }, y: { field: "price_inr", type: "quantitative" }, color: { field: "commodity", type: "nominal" } },
    }, 4),
  ];
  return [...baseTrace("commodity_prices"), ...charts.map((chart) => ({ type: "chart" as const, chart })), { type: "final", text: "Commodity markets are moving enough to keep procurement alert, especially on fertilizer-linked inputs. Turn Live on and this cockpit will re-query the subscribed charts as the underlying market table changes." }];
}

function genericEvents(): ChatEvent[] {
  const payload = chart("sales-region", "Secondary sales by region, latest quarter", "The agent used the broadest sales table as a starting point and found North lagging the pack.", "-- hero:sales_by_region\nSELECT region, SUM(revenue_inr) AS revenue_inr, SUM(units) AS units FROM secondary_sales WHERE date >= '2026-04-01' GROUP BY region ORDER BY revenue_inr DESC LIMIT 10", {
    data: { name: "data" },
    mark: { type: "bar", tooltip: true },
    encoding: { x: { field: "revenue_inr", type: "quantitative" }, y: { field: "region", type: "nominal", sort: "-x" }, color: { value: "#B8232E" } },
  }, 3);
  return [...baseTrace("secondary_sales"), { type: "chart", chart: payload }, { type: "final", text: "I started from secondary sales because it is the broadest executive signal in the warehouse. Ask a sharper follow-up by region, product, field-force execution, NPS, procurement, or commodity exposure and I will compose a more specific view." }];
}
