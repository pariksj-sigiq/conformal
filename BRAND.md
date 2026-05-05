# DCM Shriram / SFS — Brand, Voice & Design Inspiration

Distilled from `dcmshriram.com`, `shriramfarmsolutions.com`, and the May 2025 corporate presentation. This file is for design, copy, and visual decisions. The agent should read it before tuning the system prompt's narrative voice and before authoring the Vega theme.

---

## The brand promise in one paragraph

DCM Shriram is a 130-year Indian industrial conglomerate (founded 1889 as Delhi Cloth Mills by Sir Shri Ram, restructured into its present form in 1990) that has grown into a ₹12,080 Cr group across agri-rural, chemicals & vinyl, and value-added businesses. Their public identity centres on **trust, heritage, and quiet competence** — not flash, not "innovation theatre." Their tagline is "Growing with Trust." Their vision is "Vibrant Growth with Trust, Energised Employees & Delighted Customers." Every customer-facing touchpoint reinforces longevity, reliability, and a deep relationship with rural India. Shriram Farm Solutions (SFS) — the demo audience — extends this into agriculture: 50 years of partnership with Indian farmers, 3,000+ dealers, science-backed inputs, and a "from farmer to agri-preneur" positioning.

The product we are building must feel like it belongs to this family — not like a tech startup demo bolted onto an enterprise.

---

## Visual identity

### Color

| Role | Hex | Use |
|---|---|---|
| **Primary brand red** | `#B8232E` | Headlines, primary CTAs, single-series chart strokes, the live pulse, focused state outlines |
| **Site chrome teal** | `#0090C9` | Used on dcmshriram.com as theme color. Reserve as a *secondary* accent — useful for "Live" status pills and informational badges where red would be too loud |
| **Ink / foreground** | `#0E0E0E` (light), `#FAFAFA` (dark) | Body text, axis labels |
| **Surface / canvas** | `#FAFAFA` (light), `#0B0B0C` (dark) | Page background |
| **Card / muted** | `#F4F4F5` (light), `#18181B` (dark) | Card backgrounds, dividers, gridlines |
| **Earth accent** (optional) | `#8B6F47` | A muted warm brown for soil/agriculture associations — only if a chart's narrative is explicitly agronomic |
| **Series palette for multi-series charts** | red `#B8232E` → teal `#0090C9` → ochre `#C9A227` → forest `#2E7D5B` → slate `#475569` | Use in this order. Do not introduce purples, fluorescent greens, or pastels |

**Rule:** red carries weight. One red element per visual frame, maximum two. If everything is red, nothing is.

### Typography

The website uses generic sans-serif body type (Open Sans / system stack). We deliberately upgrade for the cockpit, since this is an executive product:

- **Display** (page titles, chart titles, hero numbers): a **serif with gravitas** — Fraunces, GT Sectra, Playfair Display, or Source Serif 4. The serif evokes heritage and seriousness; it differentiates the product from generic "AI dashboard" aesthetics that all use sans-serif geometric type.
- **Body & UI** (chat messages, labels, table cells): **Geist** or **IBM Plex Sans**. Both feel modern but considered. Avoid Inter — it's the default of every AI product and reads as generic.
- **Numeric & code** (SQL blocks, KPI values): **Geist Mono** or **IBM Plex Mono**. Tabular numerals on for KPI tiles so digits don't shift width during value tweens.

### Imagery (for marketing pages, splash screens, demo intro)

The DCM Shriram website is dense with photography of three kinds:
1. **Wide field shots** — green crop rows, golden harvest light, often with a single farmer figure in frame
2. **Manufacturing interiors** — industrial scale, clean composition, controlled light
3. **R&D environments** — labs, microscopes, hands handling seeds or chemicals

If the cockpit needs imagery (login screen, empty state hero, demo welcome screen), match this style: documentary, warm, human. Avoid stock-photo "people in a meeting room pointing at laptops" — every AI product uses those.

### Logo treatment

DCM Shriram uses a triangular three-peak geometric mark with the wordmark "DCM SHRIRAM" and "Growing with trust" beneath. For our app:

- The cockpit is for SFS specifically, so **lead with the SFS lockup** in the sidebar header
- Show "Project Leap" as a small caps label below the SFS mark — frames the product as part of the strategic transformation, not a vendor pitch
- In `?client=sfs` mode, render the actual SFS logo from `public/sfs-logo.svg`
- In neutral mode, use a simple geometric monogram so the demo can be repurposed

---

## Voice & language

### The trust through-line

The word **trust** appears explicitly on the homepage, in the tagline, and in the corporate vision. The agent's narrative voice should occasionally land on language that echoes this — not as branding, but as natural register. The agent is the analyst who has earned the executive's trust over years of being right.

### Words and phrases to mirror (their actual corporate vocabulary)

These appear repeatedly across their materials. Using them makes the agent sound like an insider:

- **Strategic Business Units** (SBUs) — how they refer to BUs internally
- **Cane command area** — sugar industry-specific term
- **Adjacencies** — their preferred word for new business areas
- **Self-sustaining businesses** — their model description
- **Financial discipline / financial prudence** — recurring framing
- **Scale, integration, innovation, circular economy** — the strategic pillars
- **Resilient operating environment / resilient during a tough operating environment** — their boilerplate during downturns
- **Channel partners** — preferred term for dealers + distributors
- **Field force** — preferred term for MGOs/TBMs/RBMs collectively
- **Khushali** (Hindi: prosperity / wellbeing) — used as the umbrella for all CSR programs (Khushali Sehat, Khushali Shiksha, Khushali Swachhata, Khushali Rozgaar, Khushali Paryavaran). Reference this if a question touches CSR or community impact.

### Words to avoid

- **AI**, **ML**, **GenAI**, **agentic** — never mention the technology in user-facing copy. The product *is* AI; saying so is unsophisticated. Executives don't want to be told they're using AI; they want answers.
- **Leverage**, **synergy**, **best-in-class**, **paradigm** — corporate filler.
- **Just**, **simply**, **basically** — diminish the message.
- **I'm an AI**, **As a language model**, **Based on the data** — chatbot tells.
- **Disrupt**, **revolutionize**, **transform** — startup vocabulary that doesn't fit this brand.

### Tone in three registers

| Surface | Register |
|---|---|
| Agent's narrative response (CEO is reading) | Senior analyst writing a CEO briefing memo. Two to three sentences. Direct, declarative, surfaces the non-obvious finding, calls out implications for the FY28 trajectory when relevant. No hedging. No offer to help further. |
| UI labels, buttons, empty states | Clear, dignified, light. "Ask anything about the business" — not "What can I help you with today?" |
| Error messages | Honest and short. "Query failed — the table `xyz` is unavailable." Not "Oops! Something went wrong." |

---

## Heritage threads to weave into the product

These are real DCM Shriram details, scraped from the site. Threading them into copy makes the product feel native rather than generic.

### "It's about trust"
The literal headline on the About Us page. Use as the **empty-state hero on the chat panel**, set in the serif display face. Below it: "Ask anything about the business." Don't theme the entire app around the word — just plant it where it lands once.

### 130+ years of sustained entrepreneurship
Reference point for time-series queries. When the agent answers a 5-year revenue question, the narrative might end with: "*The trajectory continues a 130-year pattern of compounding through cycles.*" Used sparingly, this is the kind of line that makes a CEO look up.

### Sir Shri Ram (1884–1963)
The founder. A figure of real gravitas — first Chairman of the Industrial Finance Corporation of India, founder of Lady Shri Ram College, founding board member of the RBI. The founder image and quote could appear in a **"/about" subtle attribution page** — not the main UX, but a touch of polish if you want one.

### The Khushali integrated development model
Five sub-brands: *Khushali Sehat* (health), *Khushali Shiksha* (education), *Khushali Swachhata* (sanitation), *Khushali Rozgaar* (livelihood), *Khushali Paryavaran* (environment). If the agent ever surfaces a CSR / ESG / community impact question, it should reference these by name — that's the language SFS leadership themselves use.

### "From farmer to agri-preneur"
SFS's positioning line. Surfaces well when answering questions about farmer engagement, advisory programs, or product adoption.

### Awards and recognitions to drop in narratives
- S&P Global CSA 2024: Top 7% of global chemical companies on sustainability
- KPMG ESG Excellence Award 2024 (Mid/Small Cap)
- EcoVadis Bronze 2024
- FICCI HR Innovation Award 2024 — Technology at Workplace

The agent shouldn't recite these unprompted, but if asked about ESG performance or workplace tech, these are the references.

---

## Specific design inspirations for the cockpit

### From the corporate presentation
The May 2025 deck uses a clean grid system, generous white space, and reserves red for accent only — never for backgrounds. **Mirror this discipline** in the cockpit: the canvas is mostly neutral; red shows up to mean "look here."

### From the website's section pattern
DCM's site uses small-caps eyebrows above section headers ("OUR BUSINESSES" → "Agri-Rural Business" → body). Adopt this for chart titles in the canvas: a thin small-caps eyebrow naming the data domain ("FIELD FORCE") above the actual chart title in serif display ("Coverage by region, current quarter"). Costs nothing, looks deliberate.

### From the SFS site's interactive map
The shriramfarmsolutions.com landing page has an interactive India map where each pin opens a farmer testimonial. We don't need this in the cockpit, but it tells us SFS leadership thinks geographically. **Geography-first views in the cockpit (region/state filters in the sidebar, choropleth options in chart kebab menus) will resonate.**

### From the "It's about trust" headline treatment
On the About Us page, "**trust**" is set heavier than the surrounding words ("It's about **trust**"). Echo this typographic move on chart titles where one word matters more than the rest — bold the *operative* word, not the chart name. Example: "Coverage *down* in West, recovery in East." This is editorial typography, and it reads as expensively designed.

### From the milestone timeline
Their site organises history into decades: "Decade Post Trifurcation 1990–2000," "Scale & New Businesses 2001–2010," etc. Mirror this idea in the empty-state chat panel: a faint horizontal timeline at the bottom showing 1990 → 2000 → 2010 → 2020 → "2026 (you are here)." Subtle, contextual, places the product in continuity with the company's own way of describing itself.

---

## Anti-patterns — what would feel "off" for this brand

- **Glassmorphism, neon, Mac OS-style traffic lights, gradients on cards** — too startup, breaks the heritage register
- **Emoji in narratives or empty states** — wrong register entirely
- **"Powered by Claude" / "AI-powered" badges anywhere visible** — never reveal the technology to the executive user
- **Overly bright greens** — nominally agricultural but reads as fake-ag-tech
- **Meeting-room stock photography** — every B2B AI product uses these
- **Dark mode that's pure black** — too "developer tool"; use `#0B0B0C` so it feels considered
- **Charts with rainbow color scales** — only the curated 5-color palette above
- **Pie charts** — almost never the right answer; horizontal bar or stacked bar nearly always wins. The system prompt should explicitly forbid pie charts unless the question literally asks for share-of-whole on ≤4 categories.
- **Buttons labeled "Submit" or "Go"** — use verbs that match the action: "Ask," "Pin," "Share."
