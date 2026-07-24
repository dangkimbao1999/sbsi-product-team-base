# Business Requirements Document — Watchlist

**Product**: SBSI Research Hub
**Feature**: Watchlist
**Status**: Draft — for stakeholder review
**Version**: 0.1
**Date**: 2026-07-24
**Author**: Claude Code (drafted on request; needs product/business owner review before approval)

---

## 1. Document Control

| Field | Value |
|---|---|
| Document owner | *<assign — Research Hub product owner>* |
| Reviewers | *<Product, Compliance, Engineering lead — TBD>* |
| Approval status | Not yet approved |
| Related docs | `apps/research-hub/CLAUDE.md` (project context & domain model) |

> This BRD is a first draft generated from the existing project context in
> `apps/research-hub/CLAUDE.md` (working entity chain: `User -> Portfolio/Watchlist
> -> Alert`). It has **not** been validated against real user research, a
> finalized domain schema, or compliance review. Sections marked
> **[OPEN QUESTION]** must be resolved before this BRD is approved for
> build.

---

## 2. Purpose

Define the business requirements for a **Watchlist** feature within SBSI
Research Hub, enabling individual investors, analysts, and traders to track
a personal, curated list of Vietnam-market tickers (equities and ETFs) they
are monitoring or considering for investment.

The Watchlist is a core retention and engagement mechanic for Research
Hub's stated strategic role: Research Hub is **not** a standalone product —
it is SBSI's top-of-funnel acquisition surface, designed to attract retail
investors with research content and convert them into SBSI trading
customers.

---

## 3. Background & Business Context

Research Hub aggregates crowdsourced stock analysis, quant ratings,
earnings data, and market news for the Vietnam market. Today, a visitor can
read this content but has no persistent, personalized way to track tickers
they care about across sessions, nor to be notified of relevant activity
(new articles, price moves, earnings, rating changes) on those tickers.

A Watchlist closes this gap:

- It gives users a reason to create an account (registration gate) and
  return regularly (habit loop), increasing session frequency and
  time-on-platform.
- It is the natural surface to attach **Alerts** (per the domain model:
  `User -> Portfolio/Watchlist -> Alert`), which drive re-engagement
  notifications.
- It is a high-intent signal: a user watchlisting a ticker is a strong
  conversion trigger for a "Trade this idea" / "Open an account" call to
  action into SBSI's trading products.

---

## 4. Business Objectives

| # | Objective | Rationale |
|---|---|---|
| O1 | Increase registered-user retention (D7/D30 return rate) | Watchlists are a classic engagement hook — users return to check tracked tickers |
| O2 | Increase account-creation conversion from anonymous visitors | Gate watchlist creation behind sign-up to convert top-of-funnel traffic |
| O3 | Increase click-through to SBSI trading products | Surface trade CTAs contextually against watchlisted tickers |
| O4 | Establish the foundation for Alerts | Watchlist is the entity Alerts attach to; sequencing this first unblocks that roadmap item |

### Success Metrics **[OPEN QUESTION — needs business/product sign-off]**

- % of registered users who create at least one watchlist within 7 days of
  sign-up
- Average tickers per active watchlist
- D7/D30 retention delta: watchlist users vs. non-watchlist users
- Click-through rate from a watchlisted ticker to a trading-account CTA
- *<Add specific numeric targets once baseline data or benchmarks exist>*

---

## 5. Scope

### 5.1 In Scope (proposed)

- Registered users can create, rename, and delete one or more watchlists.
- Users can add/remove Vietnam-market equities and ETFs to/from a
  watchlist by ticker search.
- Each watchlist item displays, at minimum: ticker symbol, company name,
  last price, day change (%/absolute), and Quant Rating (per the existing
  domain model's factor-grading system).
- Users can reorder or sort watchlist items (e.g., by ticker, % change,
  quant rating).
- Watchlist is accessible from both the web and mobile experience (see
  **Open Question 8.3** — mobile scope/timeline is not yet decided).
- A watchlisted ticker surfaces a contextual CTA toward SBSI's trading
  product (e.g., "Trade [TICKER]").
- Empty-state and onboarding guidance for first-time watchlist users.

### 5.2 Out of Scope (proposed, for this iteration)

- Real-time push/email/SMS **Alerts** on watchlist items — tracked as a
  separate, dependent feature (see Dependencies, §7).
- Social/sharing features (e.g., publishing a watchlist publicly, following
  another user's watchlist).
- Advanced portfolio accounting (cost basis, P&L tracking, tax lots) — this
  is a *watchlist* (intent to track), not a *portfolio* (actual holdings).
  Confirm this distinction with product before merging the two concepts.
- Anonymous/guest watchlists (local-storage-only, no account) — **[OPEN
  QUESTION]**, see §8.1.
- ADR coverage — inherited open question from the parent domain model;
  confirm VN-only scope applies to Watchlist tickers too.

---

## 6. Stakeholders & Personas

### 6.1 Stakeholders **[OPEN QUESTION — names/roles TBD]**

| Role | Interest |
|---|---|
| Research Hub Product Owner | Feature scope, prioritization, success metrics |
| SBSI Trading/Brokerage Product | Conversion funnel from Watchlist into trading accounts |
| Compliance/Legal | Any suitability/advice-adjacent framing near a "watch" or "trade" action |
| Engineering Lead | Technical feasibility, data/quote-feed dependencies |
| Contributors/Analysts (indirect) | Increased distribution if watchlisted tickers surface their content |

### 6.2 Personas (from existing project context)

- **Individual retail investor** — wants to track a shortlist of VN stocks
  they're researching before committing capital.
- **Analyst/trader** — wants to monitor names they've published ideas on,
  or names competitors have covered.
- **Prospective SBSI customer** — arrives via research content, has no
  brokerage account yet; watchlist is a low-commitment first action.

---

## 7. Dependencies

- **Ticker/Security master data** — the watchlist depends on the same
  Ticker/Security entity referenced elsewhere in Research Hub's domain
  model (articles, Quant Ratings, earnings data). No separate ticker list
  should be built for this feature.
- **Quant Rating data** — if displayed on watchlist rows, depends on
  whether Quant Rating is computed at runtime or cached on a schedule —
  this is an existing **unresolved** question in
  `apps/research-hub/CLAUDE.md` and affects watchlist row load performance.
- **Market data / quote feed** — real-time or delayed price + day-change
  data requires a market-data source; none is confirmed yet in the tech
  stack (tech stack for Research Hub is undecided as of this writing).
- **Alerts** — a natural extension of Watchlist per the domain model
  (`Watchlist -> Alert`), but explicitly out of scope for this iteration;
  sequencing/roadmap dependency only.
- **SBSI trading account system** — the "Trade this idea" CTA depends on
  a confirmed handoff/deep-link point into SBSI's customer trading
  platform, which is flagged as an open question in the parent CLAUDE.md
  and is **not yet built** in this monorepo.

---

## 8. Open Questions **[MUST be resolved before build]**

1. **Anonymous vs. registered-only watchlists** — should an anonymous
   visitor be able to start a watchlist (e.g., browser-local storage) and
   be prompted to register only to persist/sync it, or is registration
   required up front? This materially affects the conversion funnel design
   (Objective O2).
2. **Watchlist cardinality** — can a user have multiple named watchlists,
   or exactly one? Multiple watchlists add complexity (naming, switching
   UI) but may better match how analysts organize ideas by theme/sector.
3. **Mobile scope and timeline** — Research Hub's tech stack (including
   mobile) is undecided; confirm whether Watchlist ships web-first with
   mobile deferred, or must launch on both simultaneously.
4. **VN-only ticker scope** — confirm ADRs are excluded from watchlist-able
   securities, consistent with the platform's VN-only positioning (existing
   open question inherited from the parent domain model).
5. **Compliance framing** — does displaying a "Trade this idea" CTA next to
   a watchlisted ticker (which may sit alongside crowdsourced
   buy/sell-thesis content) trigger any suitability, advice, or disclosure
   obligation under Vietnamese securities regulation (SSC/UBCKNN)? Flagged
   for legal/compliance review per the parent domain model's existing
   compliance caveat on contributor content.
6. **Data freshness requirement** — is delayed (e.g., 15-minute) market
   data acceptable for watchlist price display, or is real-time required?
   This has direct cost/vendor implications given no market-data source is
   confirmed yet.
7. **Watchlist size limit** — is there a maximum number of tickers per
   watchlist (for both UX and backend load reasons)?
8. **Relationship to Screener** — the domain model separately lists a
   Screener (`User -> Screener`, saved filter over Ticker + Quant Rating).
   Should users be able to bulk-add screener results to a watchlist?
   Confirm whether this integration is in scope now or a later iteration.

---

## 9. Assumptions

- Research Hub already has (or will have, ahead of this feature) a
  registered-user account system; Watchlist does not itself define
  authentication.
- Ticker/Security reference data (symbol, company name) already exists or
  is being built as shared infrastructure across Research Hub features,
  not exclusively for Watchlist.
- This BRD assumes VN equities and ETFs only, consistent with the
  platform's stated VN-only market focus; any ADR inclusion requires a
  scope change.

---

## 10. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Market-data vendor cost/licensing undetermined | Could block or delay real-time price display | Resolve tech-stack/market-data-source decision before committing to a launch date |
| Compliance exposure from "watch + trade" CTA next to crowdsourced content | Regulatory/legal risk | Route through Compliance review before build (§8, Q5) |
| Scope creep into full portfolio/P&L tracking | Delays MVP, blurs product line between Watchlist and future Portfolio feature | Explicitly exclude portfolio accounting (§5.2) and hold the line in backlog grooming |
| Quant Rating compute cost on every watchlist load | Performance/cost risk if computed at runtime for many users x many tickers | Resolve the computed-vs-cached decision (inherited open question) before finalizing NFRs |

---

## 11. Non-Functional Considerations (preliminary — not final NFRs)

- **Performance**: Watchlist view should load without perceptibly blocking
  on live quote/rating data (define target latency once market-data source
  is chosen).
- **Consistency**: Ticker/company data shown on Watchlist rows must match
  what's shown elsewhere in Research Hub (article pages, screener) — no
  divergent data sources for the same entity.
- **Auditability**: Not currently identified as a requirement (Watchlist is
  not a transactional/trading record), but revisit if compliance (§8, Q5)
  determines otherwise.

---

## 12. Glossary

| Term | Definition |
|---|---|
| Watchlist | A user-curated list of tickers being monitored, without implying ownership or a trade |
| Ticker/Security | A VN equity or ETF, per Research Hub's shared reference data |
| Quant Rating | Factor-based score (value, growth, profitability, momentum, earnings revisions) per the existing Research Hub domain model |
| Portfolio | *Distinct from Watchlist* — implies actual held positions; out of scope here (§5.2) |
| Alert | A notification triggered by activity on a watched ticker; separate, dependent feature (§7) |

---

## 13. Next Steps

1. Circulate this draft to the stakeholders in §6.1 for input.
2. Resolve all **[OPEN QUESTION]** items in §8 — these block a stable
   scope.
3. Once scope is stable, hand off to a PRD / technical design covering UI
   flows, data model, and API contract (tech-stack-dependent — currently
   undecided per `apps/research-hub/CLAUDE.md`).
4. Track this work in Linear under team **Iambao**, project *"Stock
   Research Hub - SBSI"* per the project's issue-tracking convention.
