# SBSI Research Hub

> One of the product team's tracked projects — see the root `../../CLAUDE.md`
> for the parent brokerage context and repo-wide rules (this file inherits
> all of them: TDD, no-fallbacks, git workflow, etc.). This file only
> documents what is specific to Research Hub. **This folder holds knowledge,
> not code** — Research Hub's actual codebase (once built) lives in its own
> repo; see `../README.md` for the convention.

## Project Context

SBSI Research Hub is a crowdsourced financial-markets platform and
investment-research hub for individual investors, analysts, and traders,
**focused on the Vietnam market only**. Rather than relying solely on
in-house publications or automated feeds, it is primarily an
open-contributor ecosystem: independent financial analysts, industry
experts, money managers, and day traders publish stock analyses, investment
ideas, and macro commentary.

Strategically, this is **not** a standalone product — it is SBSI's
top-of-funnel acquisition surface. Its job is to attract retail investors
with research content and convert them into SBSI trading customers (see
root `CLAUDE.md` for the brokerage's trading systems this funnels into).

### Key aspects

- **Crowdsourced stock analysis & long/short ideas** — articles covering
  Vietnam equities and ETFs (the source description also mentions ADRs,
  which is a Seeking-Alpha-shaped carryover; confirm with product whether
  ADR coverage is actually in scope for a VN-only platform before building
  against it). Contributors publish thesis pieces from deep fundamental
  analysis to short arguments, giving multiple perspectives per ticker.
- **Earnings data & transcripts** — tracking for upcoming earnings,
  historical financials, and full earnings-call transcripts paired with
  analytical highlights.
- **Quantitative ratings & factor grading** — a Quant Rating system scoring
  stocks across value, growth, profitability, momentum, and earnings
  revisions, to benchmark ideas objectively alongside qualitative articles.
- **Market news & real-time catalysts** — curated breaking news, analyst
  upgrades/downgrades ("Notable Calls"), macro trends, and sector updates.
- **Portfolio management & screening tools** — user portfolio tracking,
  customizable alerts, and stock/ETF screeners filtering on dividend yield,
  market cap, valuation multiples, and quant scores.

## Tech Stack

<Not decided yet — fill in once chosen. Placeholder, same shape as root
CLAUDE.md:>

- **Language**: <TypeScript / Python / Go / ...>
- **Package manager**: <...>
- **Runtime**: <...>
- **Server framework**: <...>
- **Database**: <...>
- **Frontend**: <...>
- **Mobile**: <...>

## Domain Model

<Placeholder — fill in once real schema/API contracts exist. Do not invent
table names; this is a first pass at the entity vocabulary from the product
description above, to be corrected against the real schema.>

Working entity chain (content side): Contributor -> Article/Idea (long or
short thesis, tied to one or more Tickers) -> Ticker/Security (VN equity or
ETF) -> Quant Rating (factor scores: value, growth, profitability,
momentum, earnings revisions) -> Earnings Report/Transcript (tied to a
Ticker). Separately, on the user side: User -> Portfolio/Watchlist -> Alert,
and User -> Screener (saved filter over Ticker + Quant Rating fields).

Open questions to resolve against the real schema when it exists:
- Is a Quant Rating computed at runtime or cached/recomputed on a schedule?
  (Root CLAUDE.md's domain-model.md flags this same computed-vs-cached
  question for trading balances — same discipline applies here.)
- How does an Article/Idea relate to Contributor reputation/verification
  status (compliance may care about this — crowdsourced financial content
  in Vietnam may carry disclosure/registration obligations; check with
  legal/compliance before treating any contributor content as advice).
- What is the actual conversion/handoff point into SBSI's trading systems
  (e.g. a "Trade this idea" CTA deep-linking into the customer trading app)?

## Issue Tracking

Tracked in Linear under team **Iambao**, project **"Stock Research Hub -
SBSI"** (https://linear.app/iambao/project/stock-research-hub-sbsi-a05bf11a905c).
See root `.claude/rules/linear.md` for the MCP-based workflow — same rules
apply here, no separate setup needed.
