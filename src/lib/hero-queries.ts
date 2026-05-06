import type { ChartPayload, ChatEvent } from "@/lib/agent-types";

const axis = { labelColor: "#6f6b66", titleColor: "#3c3835", gridColor: "#ebe5dd", domain: false, ticks: false };
const config = {
  background: "transparent",
  font: "var(--font-sans), ui-sans-serif, system-ui",
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

function finalResponse(insight: string, chartObservations: string[], watchOut?: string): ChatEvent {
  return {
    type: "final",
    text: [
      `Insight: ${insight}`,
      `Chart observations:\n${chartObservations.map((observation) => `- ${observation}`).join("\n")}`,
      watchOut ? `Watch-out: ${watchOut}` : "",
    ]
      .filter(Boolean)
      .join("\n\n"),
  };
}

function fieldForceEvents(): ChatEvent[] {
  const charts = [
    chart(
      "field-trend",
      "Weekly visits: planned vs actual",
      "The week-9 recovery confirms the Allahabad TBM intervention is holding. FY28 trajectory stays intact if East sustains this pace through March.",
      "-- hero:field_force_trend\nSELECT week_starting, SUM(visits_done) AS actual, SUM(visits_planned) AS planned FROM field_force_activity WHERE date >= '2026-02-01' GROUP BY 1 ORDER BY 1 LIMIT 11",
      {
        data: { name: "data" },
        layer: [
          {
            mark: { type: "area", color: "#B8232E", opacity: 0.08, interpolate: "monotone" },
            encoding: {
              x: { field: "week_starting", type: "temporal", axis: { title: null, format: "W%-U" } },
              y: { field: "actual", type: "quantitative", axis: { title: null } },
            },
          },
          {
            mark: { type: "line", stroke: "#7a756f", strokeDash: [5, 4], strokeWidth: 2, tooltip: true },
            encoding: {
              x: { field: "week_starting", type: "temporal" },
              y: { field: "planned", type: "quantitative" },
            },
          },
          {
            mark: { type: "line", color: "#B8232E", point: { filled: true, size: 60 }, strokeWidth: 3, tooltip: true },
            encoding: {
              x: { field: "week_starting", type: "temporal" },
              y: { field: "actual", type: "quantitative" },
            },
          },
          {
            mark: { type: "text", text: "dip W5", dx: 26, dy: -18, color: "#77716b", fontSize: 13 },
            transform: [{ window: [{ op: "row_number", as: "rowNumber" }] }, { filter: "datum.rowNumber == 5" }],
            encoding: {
              x: { field: "week_starting", type: "temporal" },
              y: { field: "actual", type: "quantitative" },
            },
          },
        ],
        resolve: { scale: { color: "independent" } },
      },
      3,
    ),
    chart(
      "north-churn-inline",
      "Churn risk",
      "LKO and PAT sit above the intervention line; BPL should be managed through amber governance while JPR and AMD remain stable.",
      "-- hero:north_churn_inline\nSELECT dealer_id, churn_risk FROM channel_partners WHERE region = 'North' ORDER BY churn_risk DESC LIMIT 5",
      {
        data: { name: "data" },
        layer: [
          {
            mark: { type: "bar", cornerRadiusEnd: 3, tooltip: true },
            encoding: {
              x: { field: "churn_risk", type: "quantitative", axis: null, scale: { domain: [0, 1] } },
              y: { field: "dealer_id", type: "nominal", sort: "-x", axis: { title: null } },
              color: {
                condition: [
                  { test: "datum.churn_risk >= 0.7", value: "#B8232E" },
                  { test: "datum.churn_risk >= 0.45", value: "#BA7517" },
                ],
                value: "#1D9E75",
              },
            },
          },
          {
            mark: { type: "text", align: "left", dx: 5, baseline: "middle", fontSize: 12 },
            encoding: {
              x: { field: "churn_risk", type: "quantitative" },
              y: { field: "dealer_id", type: "nominal", sort: "-x" },
              text: { field: "churn_risk", type: "quantitative", format: ".2f" },
              color: {
                condition: [
                  { test: "datum.churn_risk >= 0.7", value: "#B8232E" },
                  { test: "datum.churn_risk >= 0.45", value: "#BA7517" },
                ],
                value: "#1D9E75",
              },
            },
          },
        ],
      },
      1,
    ),
  ];
  return [
    ...baseTrace("field_force_activity"),
    ...charts.map((chart) => ({ type: "chart" as const, chart })),
    finalResponse(
      "North is still the strongest field-force zone at about 86% coverage, while East is the concern at about 61%, its weakest quarter since Q1 FY24. The recovery after week 9 suggests the Allahabad TBM intervention is working, but East needs sustained visit discipline through March before we can call it fixed.",
      [
        "The visits chart compares planned versus actual weekly visits; actuals dip around week 5, then recover and track much closer to plan by the end of the period.",
        "The churn-risk bar view shows the near-term channel risk concentration: LKO and PAT are above the intervention line, while BPL sits in amber governance territory.",
      ],
      "Keep East on a weekly recovery cadence and pair field coverage with dealer-risk follow-up, not just visit completion.",
    ),
  ];
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
  return [
    ...baseTrace("procurement_spend"),
    ...charts.map((chart) => ({ type: "chart" as const, chart })),
    finalResponse(
      "Procurement savings are ahead in categories where supplier concentration gives SFS leverage, especially Logistics and Raw Material. The gap is not a broad program failure; it is concentrated in under-target categories that need tighter negotiation governance before month-end variance reviews.",
      [
        "The savings-versus-target chart ranks categories against a target rule, making it clear which categories are creating the savings pool and which are still below threshold.",
        "The six-month run-rate chart shows improvement over time, but the slope is uneven by category, so averages hide where intervention is still needed.",
      ],
      "Move the lagging categories into weekly governance with named owners and a supplier-specific action list.",
    ),
  ];
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
  return [
    ...baseTrace("farmer_nps"),
    ...charts.map((chart) => ({ type: "chart" as const, chart })),
    finalResponse(
      "Farmer sentiment is improving overall, but the regional spread is too wide to treat this as a system-wide win. South is creating the benchmark, while North remains structurally below the system average and needs service recovery plus digital activation together.",
      [
        "The NPS trend chart shows regional lines moving up, but North stays below the pack across quarters rather than showing a one-quarter dip.",
        "The engagement scatter links app activity, support volume, and NPS; South combines stronger engagement with better sentiment, while North needs a closed-loop recovery motion.",
      ],
      "Use South's operating playbook as the replication case and give North a separate service-issue backlog.",
    ),
  ];
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
  return [
    ...baseTrace("wave1_microbattles"),
    ...charts.map((chart) => ({ type: "chart" as const, chart })),
    finalResponse(
      "Wave 1 is not a red program, but it has three visible pressure points that need leadership attention. Most bets are moving, while the blocked leakage audit and two watch items need named unblockers rather than another status review.",
      [
        "The status heatmap shows progress by owner function and micro-battle, making the blocked and watch items visually obvious.",
        "The completion chart orders the micro-battles from lowest to highest completion, so the bottom of the execution stack is clear rather than buried in a table.",
      ],
      "Use this view in every steerco until each watch or blocked item has an owner, unblocker, and next checkpoint.",
    ),
  ];
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
  return [
    ...baseTrace("channel_partners"),
    ...charts.map((chart) => ({ type: "chart" as const, chart })),
    finalResponse(
      "North churn risk is concentrated enough to action rather than monitor passively. The highest-risk partners tend to combine weaker tier quality, high DSO, and weak scheme attachment, so the intervention should mix commercial recovery with credit cleanup.",
      [
        "The ranked churn chart shows the top risk accounts first and colors the bar by tier, which separates structural partner quality from temporary sales softness.",
        "The DSO-versus-risk scatter shows that the most urgent accounts are not only churn risks; several also carry slow payment behavior, increasing recovery complexity.",
      ],
      "Start with the top twelve dealers and make the regional head accountable for weekly progress on both credit and scheme attachment.",
    ),
  ];
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
  return [
    ...baseTrace("commodity_prices"),
    ...charts.map((chart) => ({ type: "chart" as const, chart })),
    finalResponse(
      "Commodity markets are moving enough to keep procurement alert, especially on fertilizer-linked inputs where price direction can quickly change buying posture. The immediate read is not that every commodity needs action, but that current watch items should stay in the procurement war-room cadence.",
      [
        "The daily-move chart ranks commodities by latest percentage change, so the current watch list is visible without scanning every price series.",
        "The sparkline chart shows whether the latest move is part of a trend or just a one-day fluctuation across the commodity basket.",
      ],
      "Use live refresh for this view when procurement is actively negotiating or deciding whether to hold volumes flat.",
    ),
  ];
}

function genericEvents(): ChatEvent[] {
  const payload = chart("sales-region", "Secondary sales by region, latest quarter", "The agent used the broadest sales table as a starting point and found North lagging the pack.", "-- hero:sales_by_region\nSELECT region, SUM(revenue_inr) AS revenue_inr, SUM(units) AS units FROM secondary_sales WHERE date >= '2026-04-01' GROUP BY region ORDER BY revenue_inr DESC LIMIT 10", {
    data: { name: "data" },
    mark: { type: "bar", tooltip: true },
    encoding: { x: { field: "revenue_inr", type: "quantitative" }, y: { field: "region", type: "nominal", sort: "-x" }, color: { value: "#B8232E" } },
  }, 3);
  return [
    ...baseTrace("secondary_sales"),
    { type: "chart", chart: payload },
    finalResponse(
      "I started from secondary sales because it is the broadest executive signal in the current demo warehouse. The first scan suggests North is lagging the pack, so the next useful cut is to separate whether this is a region issue, a product mix issue, or a field execution issue.",
      [
        "The regional sales chart ranks latest-quarter revenue by region, giving a quick view of where the demand signal is strongest and weakest.",
        "Because this is an aggregate view, it should be treated as a triage chart rather than a root-cause answer.",
      ],
      "Ask a sharper follow-up by region, product, field-force execution, NPS, procurement, or commodity exposure for a more diagnostic answer.",
    ),
  ];
}
