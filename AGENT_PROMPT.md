# Coding Agent Prompt — Project Leap Executive Cockpit

---

## What you are building

An **agentic executive intelligence cockpit** for Shriram Farm Solutions (SFS). Built around one interaction: a leader types a business question in plain English, and an AI agent — visibly reasoning in real time — explores the data, writes its own SQL, composes a unique visualization for the result, and streams it back. Charts on screen stay live: when underlying data shifts, every visible chart silently re-runs its query and animates to the new values.

This is the "Enterprise CEO Chatbot" Bain & Company specified as Wave 1 Priority 1 of Project Leap. You are building the production-quality version that will be demoed to SFS leadership.

---

## The user journey (what makes this work)

This is what a viewer sees, in order, when the demo presenter types `"How is the field force tracking this quarter?"`:

1. The input bar dims; a thin red pulse runs along its bottom edge.
2. A "Trace" rail appears below the message, listing tool calls as they happen — `list_tables ✓ 12ms` → `describe_table(field_force_activity) ✓ 8ms` → `run_sql ⏳` (with the SQL streaming in character-by-character in a syntax-highlighted block) → `✓ 142ms · 47 rows`.
3. While the trace is still running, a chart skeleton appears in the canvas to the right.
4. The skeleton resolves into a finished chart with a brief enter animation. Title above, narrative caption below.
5. The agent calls `run_sql` again, and a second chart appears beside the first.
6. After the third chart, a 2–3 sentence executive summary fades in below the canvas.
7. A subtle "live" pulse stays on each chart. Thirty seconds later, with the simulator running, one of the values ticks — the bar visibly grows, the number tweens.

That sequence is the product. Everything in this document serves it. If a build decision doesn't make that sequence feel better, it's wrong.

---

## Files to read before you start

Four files in the repo root. Read all four end-to-end before writing code.

1. **`PLAN.md`** — Full architecture, agent loop design, EC2 deployment runbook, acceptance criteria. This is the authoritative spec.
2. **`company-context.json`** — Real DCM Shriram financials (FY2025 revenue ₹12,080 Cr, SFS ₹1,450 Cr at 20% PBDT, FY28 target ₹2,400 Cr), 13 real states, 4 real regions, real product lines (Seeds/SPN/Crop Protection/Urea), real field force roles (MGO/TBM/RBM), real existing systems (Growth Book, ByteEdge, SAP). Use these for seed data, system prompt context, and the `describe_table` tool.
3. **`INSIGHTS.md`** — Where each scraped insight goes in the codebase. Pay attention to the **margin punch-above-weight story** (SFS = 12% revenue but 17% PBDIT) — make sure that insight is reachable through normal natural-language questions, because surfacing it unprompted is the demo's wow moment.
4. **`BRAND.md`** — Visual identity, voice, language patterns, heritage threads, design inspirations all distilled from DCM Shriram's actual public materials. This is what makes the cockpit feel like it belongs to a 130-year-old industrial conglomerate rather than a generic AI dashboard. Read it before authoring the Vega theme, the system prompt's narrative voice, the empty states, or any UI copy.

---

## Locked-in technical decisions

| Layer | Choice | Why |
|---|---|---|
| Framework | Next.js 15 App Router + TypeScript | Streaming, RSC, route handlers |
| UI components | shadcn/ui + shadcn blocks (`https://ui.shadcn.com/blocks` — vendor `sidebar-07`, `dashboard-01`) | User requirement |
| Charts | **Vega-Lite** via `react-vega` | Per-query chart composition. Not Recharts, not shadcn `<Chart>`, not Chart.js |
| SQL engine | **DuckDB-WASM** (in-browser) | Zero-backend SQL. Not Postgres, not SQLite |
| LLM | Claude Sonnet 4 (`claude-sonnet-4-20250514`) with tool use | Reliable structured tool calling |
| Streaming | Custom SSE event format from `/api/chat` | Standard `useChat` libraries don't handle our 4-tool agent loop |
| Animation | Motion (formerly Framer Motion) | Numeric value tweens on data updates |
| Deploy | EC2 (Ubuntu 22.04) + Nginx + Certbot + PM2 | Self-hosted. Not Vercel |

The full PLAN.md has the rationale for each. Do not substitute these for "more familiar" alternatives.

---

## Build phases — reordered for visual progress

The agent works best when something is rendering by end of day 1. Phases are ordered to get a working visual shell up first, then progressively give it intelligence.

### Phase 0 — Foundation (1 hour)
Next.js repo, Tailwind, App Router, src dir. `shadcn init`. Add the components listed in PLAN.md §8 Phase 0. Install: `@duckdb/duckdb-wasm`, `react-vega`, `vega`, `vega-lite`, `motion`, `@anthropic-ai/sdk`, `@tanstack/react-query`, `@dnd-kit/core`, `zod`. Vendor `sidebar-07` and `dashboard-01` blocks into `src/components/blocks/`.

### Phase 1 — Visual shell (½ day) — must look like the final product
Build the layout based on `sidebar-07`. Left rail with placeholder logo, "New Chat" button, conversation list (empty state for now), Pinned Dashboard link. Top bar with a "Live" toggle pill (non-functional), a theme toggle, and a `Cmd+K` search trigger. Main area: split pane with chat thread (~36%) on the left and chart canvas (~64%) on the right. Light/dark themes both wired and intentional.

Drop two static placeholder `<Card>` elements in the canvas — one tall, one wide — so the layout reads correctly empty. The chat thread shows a welcome state with the 6 hero query chips as suggestions.

**At end of Phase 1, the app should look like the finished product with no functionality.** This is the visual contract; everything later just animates content into this shell.

### Phase 2 — Data foundation (1 day)
Write `scripts/generate-seed.ts` — a Node script that emits 24 months (April 2023 – March 2025) of Parquet files to `public/data/`, using the exact geographies, products, roles, and financial magnitudes from `company-context.json`. Tables and columns are listed in `PLAN.md §4`.

Seed with deliberate patterns the agent can find:
- North region beats plan on revenue but has the worst payment DSO
- Either UP or Rajasthan shows a declining NPS trend
- Crop Protection is growing faster YoY than Seeds
- Two Gold-tier dealers in East show rising churn risk
- Procurement OTIF dipped in Q3 FY24 then recovered
- Glyphosate Technical price spiked Jan 2024
- Wave 1 micro-battles: 2 On Track, 1 At Risk, 1 Delayed
- `group_financials` mirrors the real FY2025 numbers exactly

Bootstrap DuckDB-WASM in `src/providers/duckdb-provider.tsx`. Implement `src/lib/duckdb-store.ts` with `mutate`, `subscribe`, `tablesReferencedBy`. Build the simulator (`src/lib/data-simulator.ts`) and wire to the Live toggle.

**Build a `/dev/sql` page** — a raw SQL textarea that runs through DuckDB and shows results. This is your test harness for the rest of the build. Don't skip it.

### Phase 3 — LiveChart component (1 day) — the rendering pipeline
Build `<LiveChart sql spec title narrative span />`. On mount: run SQL, inject results into the spec's `data.values`, render via `<VegaLite>`. Subscribe to `store.subscribe(tablesReferencedBy(sql), rerun)`. On rerun: re-execute SQL, tween numeric values via Motion's `useSpring`, update spec data.

Build `src/lib/vega-theme.ts` — a Vega config object that pulls from shadcn CSS vars (`--background`, `--foreground`, `--muted`, `--primary`). Apply it as the default config wrapper around every spec the agent emits. **This is the single most important file for visual cohesion** — every chart inherits this theme, so individual specs don't need styling boilerplate and they all feel like the same product.

Build a `/dev/charts` page that hardcodes 4 sample `<LiveChart>` components with varied SQL and varied Vega-Lite specs (one trend, one ranking, one comparison, one status). Turn the simulator on. Confirm all four animate values smoothly when data ticks. **This phase is done when the rendering pipeline is provably working without any agent involvement.**

### Phase 4 — Agent tools + streaming loop (1.5 days)
Implement `src/lib/agent-tools.ts` exposing `listTables`, `describeTable`, `runSql` against DuckDB. `describeTable` merges the live DuckDB schema with the rich descriptions from `company-context.json` and includes 3 sample rows. `render_chart` is not a function — it's a UI side-effect emitted by the server.

Server route `src/app/api/chat/route.ts` calls Anthropic with the four tools and streams a custom event format: `{ type: "text" | "tool_use" | "tool_result_request" | "render_chart" | "done", payload }`. Tool calls that need DuckDB (`list_tables`, `describe_table`, `run_sql`) come back to the client as `tool_result_request`; the client executes locally and POSTs results back to continue the loop. `render_chart` is a pure UI side-effect emitted directly to the canvas.

Client `src/hooks/use-chat.ts` orchestrates the round-trip and streams text + tool traces + charts into the current turn as they arrive. Chat UI: messages list, the trace rail (collapsible, default open while streaming, auto-collapses 1s after `done`), widget grid driven by `span`, narrative below.

### Phase 5 — System prompt tuning (1 day) — getting the agent to feel like an analyst
Use the `system_prompt_context_paragraph` from `company-context.json` as the prompt opener. Add the four-tool process, the SQL rules, the Vega-Lite rules, the narrative rules from `PLAN.md §3`. Include 4 few-shot examples — one each for trend, ranking, comparison, status query types. Each few-shot shows the full tool-call sequence and a complete Vega-Lite spec.

**Iterate on this phase until all 6 hero queries produce great output every time.** Tune the prompt, not the chart components. If a chart looks wrong, the fix is almost always in the few-shots or the Vega rules — not the renderer.

### Phase 6 — Pinned dashboard, demo mode, polish (1 day)
- `/dashboard` route loading pinned `{sql, spec, title}` from `localStorage`, draggable grid via `@dnd-kit/core`, every pinned chart still subscribed to live data
- Skeletons sized to chart spans, error boundary per chart (failed chart shows "Query failed" with the SQL visible — never crashes the page)
- **Demo mode**: hidden `Cmd+Shift+D` cycles all 6 hero queries with realistic 40ms-per-character typing. Pre-cache the agent's full tool-call trace + Vega-Lite specs for each in `src/data/demo-cache.json`. If a live LLM call exceeds 10s or fails, replay the cached trace at realistic speed. The audience cannot tell.
- Lighthouse: ≥ 95 performance, ≥ 90 accessibility before Phase 7.

### Phase 7 — EC2 deployment (1 day)
Follow `PLAN.md §8 Phase 7` exactly. The two settings most demos get wrong, both critical for streaming: **`proxy_buffering off`** and **`proxy_read_timeout 300s`** in the Nginx location block. Without them the trace rail freezes mid-stream. `ANTHROPIC_API_KEY` lives in `/etc/leap.env` with `chmod 600` — never in the repo, never client-side. Run `certbot renew --dry-run` before signing off.

---

## The quality bar — what "great" means for this product

`BRAND.md` is the source of truth for visual and tonal decisions. The points below are the operational tests that prove BRAND.md was actually read and followed.

**Visual cohesion.** Every chart looks like it belongs to the same product. The Vega theme config implements `BRAND.md`'s color and typography rules — serif display for titles, the curated 5-color series palette, red used as accent only. If a chart looks "off," the fix is in the theme, not the spec.

**Chart variety.** No two charts in the same demo session use the same encoding. A trend question gets a layered line. A ranking gets a horizontal bar sorted descending. A regional comparison gets faceted small multiples. A status check gets a custom rect grid. Pie charts are forbidden except for share-of-whole questions on ≤4 categories. The system prompt enforces this explicitly.

**Narrative voice.** The agent talks like a senior analyst writing a CEO briefing memo, exactly as `BRAND.md` describes. Two or three sentences. No "based on the data," no "I'm an AI," no offer to help further. Mirrors the SFS corporate vocabulary (channel partners, field force, adjacencies, financial discipline, FY28 trajectory). Surfaces non-obvious findings unprompted.

**Streaming feel.** The trace rail, SQL, and charts arrive progressively. The user reads the agent's reasoning while the answer assembles. The streaming itself is part of the demo.

**Live aliveness.** When the simulator is on, charts breathe. Values tween, never snap. The pulse on the Live pill matches the rhythm of incoming mutations.

**Reference quality.** Linear, Vercel, Stripe Sigma — paired with the heritage gravitas described in `BRAND.md`. Not Streamlit, not Metabase, not a hackathon project, not a generic "AI dashboard."

**No technology tells.** "AI," "Claude," "agent," "GenAI," "powered by" — none of these words appear in any user-facing copy. Per `BRAND.md`, the product *is* the technology; saying so is unsophisticated.

---

## Error handling and degradation

- DuckDB query fails → chart shows "Query error" with the SQL visible and a retry button. Other charts unaffected.
- LLM call times out at 30s → fallback to the demo-cache version of that query if it exists; otherwise show "Connection issue. Please try again."
- Parquet file fails to load on app boot → show a full-page error with the missing file name. Do not partially boot.
- Streaming disconnects mid-response → show the partial result, mark the trace incomplete, surface a "Resume" affordance.
- Live mutation arrives for a table no chart references → silently ignored.

---

## Dev tooling the agent must build along the way

- `/dev/sql` — raw SQL textarea against DuckDB (Phase 2)
- `/dev/charts` — hardcoded LiveCharts to verify the rendering pipeline (Phase 3)
- `/dev/prompt` — paste a question, see the system prompt + few-shots that would be sent, plus a "Send to live API" button (Phase 5)

These are not user-facing. They speed up iteration enormously and stay in the repo, gated by `NODE_ENV !== 'production'`.

---

## Acceptance criteria — every box must be checked

- [ ] All 6 hero queries produce ≥ 2 charts + narrative + visible trace within 8 seconds on the deployed URL
- [ ] Live toggle on → at least one chart updates with an animated value tween within 30 seconds
- [ ] Pinning a chart and navigating to `/dashboard` keeps it live and updating there
- [ ] Across a single demo session, no two charts use identical encodings
- [ ] Demo mode cycles all 6 hero queries with no empty frames, no layout shifts, no jank
- [ ] On a flight-mode laptop, demo mode still works via the pre-cache
- [ ] Streaming is smooth: trace rail and SQL appear progressively during a live call, not as one block at the end (this verifies Nginx is configured correctly)
- [ ] Lighthouse: ≥ 95 performance, ≥ 90 accessibility
- [ ] `certbot renew --dry-run` passes
- [ ] No console errors on any of the 6 hero queries

---

## What NOT to do

- Do not add a backend database. DuckDB-WASM is the database.
- Do not add auth, accounts, or multi-tenancy.
- Do not use Recharts, Chart.js, or shadcn `<Chart>` for the agent's output. Those are for fixed UI; the agent uses Vega-Lite.
- Do not invent SFS data that contradicts `company-context.json`.
- Do not collapse the client/server tool round-trip into a single server call — DuckDB is in the browser, the round-trip is what makes it work.
- Do not expose `ANTHROPIC_API_KEY` anywhere reachable from the client.
- Do not skip the dev pages (`/dev/sql`, `/dev/charts`, `/dev/prompt`). They save more time than they cost.
- Do not ask clarifying questions about scope or design. This document plus the three referenced files are the scope. Build it.
