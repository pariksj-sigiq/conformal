import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

type Region = "North" | "East" | "West" | "South" | "Central";
type Product =
  | "Urea"
  | "DAP"
  | "NPK 20-20"
  | "NPK 12-32-16"
  | "BioGro"
  | "CropShield"
  | "Specialty Zinc";

type TableName =
  | "secondary_sales"
  | "field_force_activity"
  | "channel_partners"
  | "farmer_engagement"
  | "procurement_spend"
  | "wave1_microbattles"
  | "commodity_prices"
  | "farmer_nps";

type JsonRow = Record<string, string | number | boolean | null>;

const outDir = join(process.cwd(), "public", "data");
const dictionaryPath = join(process.cwd(), "public", "data-dictionary.json");

const regions: Region[] = ["North", "East", "West", "South", "Central"];
const products: Product[] = [
  "Urea",
  "DAP",
  "NPK 20-20",
  "NPK 12-32-16",
  "BioGro",
  "CropShield",
  "Specialty Zinc",
];
const channels = ["Retailer", "Distributor", "Co-op", "Agri clinic"] as const;
const crops = ["Wheat", "Paddy", "Sugarcane", "Cotton", "Mustard", "Maize"] as const;
const commodities = ["Natural Gas", "Phosphoric Acid", "Ammonia", "Sulphur", "Potash"] as const;

const monthKeys = Array.from({ length: 24 }, (_, index) => {
  const date = new Date(Date.UTC(2024, 4 + index, 1));
  return date.toISOString().slice(0, 10);
});

function seededRandom(seed: number) {
  let state = seed >>> 0;
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 2 ** 32;
  };
}

const random = seededRandom(20260505);

function pick<T>(items: readonly T[]) {
  return items[Math.floor(random() * items.length)] as T;
}

function round(value: number, digits = 2) {
  const multiplier = 10 ** digits;
  return Math.round(value * multiplier) / multiplier;
}

function monthNumber(date: string) {
  return Number(date.slice(5, 7));
}

function seasonality(date: string) {
  const month = monthNumber(date);
  if ([6, 7, 10, 11].includes(month)) return 1.28;
  if ([2, 3, 8, 9].includes(month)) return 1.08;
  if ([4, 5, 12].includes(month)) return 0.9;
  return 0.98;
}

function regionDrag(region: Region) {
  if (region === "North") return 0.78;
  if (region === "East") return 0.82;
  if (region === "West") return 1.13;
  if (region === "South") return 1.08;
  return 1;
}

function productHeat(product: Product, monthIndex: number) {
  if (product === "BioGro") return monthIndex > 7 ? 1.62 : 1.2;
  if (product === "CropShield") return 1.22;
  if (product === "Specialty Zinc") return 1.1;
  if (product === "Urea") return 0.96;
  return 1;
}

function dealerHealth(monthIndex: number, dealerCohort: string) {
  if (dealerCohort !== "At-risk FY24 cohort") return 1;
  return monthIndex < 8 ? 0.96 : Math.max(0.44, 0.96 - (monthIndex - 7) * 0.035);
}

function makeSecondarySales() {
  const rows: JsonRow[] = [];
  monthKeys.forEach((date, monthIndex) => {
    regions.forEach((region) => {
      products.forEach((product) => {
        channels.forEach((channel) => {
          const dealerCohort =
            channel === "Distributor" && ["North", "East"].includes(region)
              ? "At-risk FY24 cohort"
              : random() > 0.72
                ? "New growth cohort"
                : "Stable core";
          const base = 450 + products.indexOf(product) * 38 + regions.indexOf(region) * 27;
          const units = Math.max(
            18,
            Math.round(
              base *
                seasonality(date) *
                regionDrag(region) *
                productHeat(product, monthIndex) *
                dealerHealth(monthIndex, dealerCohort) *
                (0.86 + random() * 0.28),
            ),
          );
          const price = 820 + products.indexOf(product) * 145 + (channel === "Retailer" ? 42 : 0);
          rows.push({
            month: date,
            region,
            state: stateForRegion(region),
            product,
            product_family: product.includes("NPK") ? "Complex fertiliser" : product === "BioGro" ? "Bio-stimulant" : "Core fertiliser",
            channel,
            dealer_cohort: dealerCohort,
            units_mt: units,
            net_revenue_lakh: round((units * price) / 100000),
            gross_margin_pct: round(13.5 + productHeat(product, monthIndex) * 2.4 + random() * 3 - (region === "East" ? 2.1 : 0), 1),
            discount_pct: round((dealerCohort === "At-risk FY24 cohort" ? 5.4 : 3.1) + random() * 2, 1),
          });
        });
      });
    });
  });
  return rows;
}

function makeFieldForceActivity() {
  const rows: JsonRow[] = [];
  monthKeys.forEach((date, monthIndex) => {
    regions.forEach((region) => {
      const drag = regionDrag(region);
      const reps = region === "North" || region === "East" ? 38 : 45;
      rows.push({
        month: date,
        region,
        active_reps: reps,
        planned_visits: Math.round(reps * 56),
        completed_visits: Math.round(reps * 56 * drag * (0.87 + random() * 0.14)),
        dealer_visits: Math.round(reps * 25 * drag * (0.85 + random() * 0.18)),
        farmer_meetings: Math.round(reps * 9 * seasonality(date) * drag * (0.82 + random() * 0.18)),
        demo_plots_started: Math.round((18 + monthIndex * 0.7) * drag * (region === "South" ? 1.15 : 1)),
        app_checkins_pct: round(61 + monthIndex * 1.1 + (region === "East" ? -8 : 0) + random() * 6, 1),
      });
    });
  });
  return rows;
}

function makeChannelPartners() {
  const rows: JsonRow[] = [];
  regions.forEach((region) => {
    Array.from({ length: 80 }, (_, index) => {
      const cohort = index < 18 && ["North", "East"].includes(region) ? "At-risk FY24 cohort" : index > 62 ? "New growth cohort" : "Stable core";
      const risk = cohort === "At-risk FY24 cohort" ? 72 + random() * 21 : cohort === "New growth cohort" ? 22 + random() * 25 : 36 + random() * 22;
      rows.push({
        partner_id: `${region.slice(0, 2).toUpperCase()}-${String(index + 1).padStart(3, "0")}`,
        region,
        state: stateForRegion(region),
        partner_type: pick(channels),
        cohort,
        onboarded_month: monthKeys[Math.max(0, Math.floor(random() * 18))],
        credit_limit_lakh: round(18 + random() * 120, 1),
        current_outstanding_lakh: round(8 + risk * 0.42 + random() * 32, 1),
        fill_rate_pct: round(94 - risk * 0.18 + random() * 5, 1),
        churn_risk_score: round(risk, 1),
        status: risk > 82 ? "Watchlist" : risk > 68 ? "Intervention" : "Active",
      });
    });
  });
  return rows;
}

function makeFarmerEngagement() {
  const rows: JsonRow[] = [];
  monthKeys.forEach((date, monthIndex) => {
    regions.forEach((region) => {
      crops.forEach((crop) => {
        const digitalBoost = monthIndex > 10 ? 1.22 : 1;
        rows.push({
          month: date,
          region,
          crop,
          farmers_reached: Math.round(1200 * seasonality(date) * regionDrag(region) * digitalBoost * (0.86 + random() * 0.24)),
          demo_attendance: Math.round(180 * seasonality(date) * regionDrag(region) * (0.82 + random() * 0.28)),
          soil_tests: Math.round(95 * regionDrag(region) * (monthIndex > 9 ? 1.35 : 1) * (0.8 + random() * 0.3)),
          whatsapp_optins: Math.round(420 * regionDrag(region) * digitalBoost * (0.82 + random() * 0.26)),
          sample_conversion_pct: round(8.8 + productHeat("BioGro", monthIndex) * 1.8 + (region === "North" ? -2.2 : 0) + random() * 2.2, 1),
        });
      });
    });
  });
  return rows;
}

function makeProcurementSpend() {
  const rows: JsonRow[] = [];
  monthKeys.forEach((date, monthIndex) => {
    commodities.forEach((commodity) => {
      const base = 45 + commodities.indexOf(commodity) * 12;
      const shock = commodity === "Natural Gas" && monthIndex > 13 && monthIndex < 18 ? 1.32 : 1;
      const tick = 1 + Math.sin(monthIndex / 2.7) * 0.08 + (random() - 0.5) * 0.06;
      rows.push({
        month: date,
        commodity,
        supplier_region: pick(["Gulf", "Domestic", "Southeast Asia", "North Africa"]),
        contracted_volume_kt: round((85 + random() * 130) * (commodity === "Natural Gas" ? 1.9 : 1), 1),
        landed_cost_index: round(base * tick * shock, 2),
        spend_crore: round((base * tick * shock * (80 + random() * 90)) / 10, 2),
        hedge_cover_pct: round(28 + monthIndex * 0.7 + random() * 18, 1),
      });
    });
  });
  return rows;
}

function makeWave1Microbattles() {
  const names = [
    "North/East dealer recovery",
    "BioGro hot product scale-up",
    "Distributor churn save desk",
    "Kharif demand sensing",
    "Commodity margin cockpit",
    "Field-force visit quality",
    "Farmer NPS closed loop",
    "Working-capital discipline",
  ];
  return names.flatMap((name, index) =>
    monthKeys.map((date, monthIndex) => {
      const status =
        monthIndex < 5 ? "Mobilising" : monthIndex < 12 ? (index % 3 === 0 ? "At risk" : "In flight") : index === 0 ? "At risk" : index === 2 ? "Recovering" : "Scaling";
      return {
        month: date,
        microbattle_id: `W1-${String(index + 1).padStart(2, "0")}`,
        microbattle: name,
        owner: pick(["Sales Ops", "Commercial", "Procurement", "Marketing", "Transformation Office"]),
        region_focus: index === 0 || index === 2 ? "North/East" : index === 1 ? "All India" : pick(regions),
        status,
        confidence_pct: round(status === "At risk" ? 48 + random() * 13 : status === "Scaling" ? 78 + random() * 12 : 61 + random() * 16, 1),
        target_delta_crore: round(8 + index * 2.7 + monthIndex * 0.18, 1),
        realised_delta_crore: round((status === "At risk" ? 2.5 : 5.5) + monthIndex * (status === "Scaling" ? 0.65 : 0.34) + random() * 2, 1),
        next_gate: monthIndex % 6 === 0 ? "SteerCo review" : monthIndex % 3 === 0 ? "Sprint demo" : "Weekly standup",
      };
    }),
  );
}

function makeCommodityPrices() {
  const rows: JsonRow[] = [];
  commodities.forEach((commodity) => {
    let price = 100 + commodities.indexOf(commodity) * 18;
    monthKeys.forEach((date, monthIndex) => {
      const eventShock = commodity === "Ammonia" && monthIndex === 16 ? 14 : commodity === "Potash" && monthIndex > 18 ? -5 : 0;
      price = price * (0.985 + random() * 0.04) + eventShock;
      rows.push({
        month: date,
        commodity,
        spot_index: round(price, 2),
        mom_change_pct: round((random() - 0.45) * 6 + eventShock / 6, 2),
        volatility_30d: round(9 + random() * 18 + Math.abs(eventShock) / 2, 2),
        fx_usdinr: round(82.8 + monthIndex * 0.055 + random() * 0.8, 2),
      });
    });
  });
  return rows;
}

function makeFarmerNps() {
  const rows: JsonRow[] = [];
  monthKeys.forEach((date, monthIndex) => {
    regions.forEach((region) => {
      crops.forEach((crop) => {
        const base = 42 + monthIndex * 0.45 + (region === "North" ? -9 : region === "East" ? -7 : 3);
        rows.push({
          month: date,
          region,
          crop,
          survey_responses: Math.round(170 + random() * 210),
          nps_score: round(base + random() * 8, 1),
          detractor_pct: round(31 - base * 0.22 + random() * 4, 1),
          promoter_pct: round(39 + base * 0.25 + random() * 5, 1),
          top_pain_point: region === "North" || region === "East" ? pick(["Delayed supply", "Dealer availability", "Price communication"]) : pick(["Advisory depth", "Credit terms", "Demo follow-up"]),
        });
      });
    });
  });
  return rows;
}

function stateForRegion(region: Region) {
  const states: Record<Region, string[]> = {
    North: ["Punjab", "Haryana", "Uttar Pradesh"],
    East: ["Bihar", "West Bengal", "Odisha"],
    West: ["Rajasthan", "Gujarat", "Maharashtra"],
    South: ["Telangana", "Andhra Pradesh", "Karnataka"],
    Central: ["Madhya Pradesh", "Chhattisgarh"],
  };
  return pick(states[region]);
}

function toCsv(rows: JsonRow[]) {
  const headers = Object.keys(rows[0] ?? {});
  const escape = (value: JsonRow[string]) => {
    if (value === null) return "";
    const text = String(value);
    return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
  };
  return [headers.join(","), ...rows.map((row) => headers.map((header) => escape(row[header])).join(","))].join("\n");
}

const tables: Record<TableName, JsonRow[]> = {
  secondary_sales: makeSecondarySales(),
  field_force_activity: makeFieldForceActivity(),
  channel_partners: makeChannelPartners(),
  farmer_engagement: makeFarmerEngagement(),
  procurement_spend: makeProcurementSpend(),
  wave1_microbattles: makeWave1Microbattles(),
  commodity_prices: makeCommodityPrices(),
  farmer_nps: makeFarmerNps(),
};

const dictionary = {
  generated_at: new Date("2026-05-05T00:00:00.000Z").toISOString(),
  grain: "Synthetic monthly SFS cockpit demo data covering May 2024 through April 2026.",
  deliberate_patterns: [
    "North and East underperform on sales, activity completion, partner health, and farmer NPS.",
    "BioGro is the hot product and accelerates after the first eight months.",
    "North/East distributor cohort churn risk worsens after FY24.",
    "Kharif and rabi seasonality lifts agri sales and engagement around sowing windows.",
    "Commodity prices include tick-level movement, volatility, and a natural-gas shock.",
    "Wave 1 microbattles include status progression, at-risk items, confidence, and gate cadence.",
  ],
  tables: Object.fromEntries(
    Object.entries(tables).map(([name, rows]) => [
      name,
      {
        row_count: rows.length,
        columns: Object.keys(rows[0] ?? {}).map((column) => ({
          name: column,
          type: typeof rows[0]?.[column] === "number" ? "number" : typeof rows[0]?.[column] === "boolean" ? "boolean" : "string",
        })),
      },
    ]),
  ),
};

mkdirSync(outDir, { recursive: true });
Object.entries(tables).forEach(([name, rows]) => {
  writeFileSync(join(outDir, `${name}.json`), `${JSON.stringify(rows, null, 2)}\n`);
  writeFileSync(join(outDir, `${name}.csv`), `${toCsv(rows)}\n`);
});
writeFileSync(dictionaryPath, `${JSON.stringify(dictionary, null, 2)}\n`);

console.log(`Generated ${Object.keys(tables).length} tables in ${outDir}`);
