# SBSI Research Hub

> One of the product team's tracked projects — see the root `../../CLAUDE.md`
> for the parent brokerage context and repo-wide rules (this file inherits
> all of them: TDD, no-fallbacks, git workflow, etc.). This file only
> documents what is specific to Research Hub. **This folder holds knowledge,
> not code** — Research Hub's actual codebase (once built) lives in its own
> repo; see `../README.md` for the convention.

## Project Context

> **Status**: product-definition stage. This is background context for
> future product tasks, not an approved functional specification. Specific
> features, scope, user flows, architecture, roadmap, and prioritization
> are defined separately per task — don't infer any of those from this
> section.

### 1. Project Background

The Research Hub is a digital product being developed within the ecosystem
of a securities company in Vietnam.

The product is intended to become a central destination where investors
can access, understand, and interact with investment-related information.
It will sit between the company's research capabilities, market and
product data, customer understanding, and trading ecosystem.

The initial reference points for the product include platforms such as
Investing.com, Seeking Alpha, and research platforms operated by
securities companies. However, the objective is not to replicate any
single existing platform. The Research Hub should be designed according to
the company's own business model, customer base, data capabilities,
regulatory requirements, and long-term product strategy.

The project is still in the product-definition stage. Specific features,
detailed scope, user flows, technical architecture, roadmap, and
prioritization will be defined separately for each future task.

### 2. Product Purpose

The purpose of the Research Hub is to help investors better understand the
market, investment products, and information relevant to their investment
decisions.

The product should reduce the gap between:
- Receiving investment information.
- Understanding what the information means.
- Determining whether the information is relevant to a particular investor.
- Connecting that understanding with the broader brokerage and investment
  ecosystem.

The Research Hub should not be considered only as a news portal, report
library, content website, or marketing channel. It should be viewed as a
broader investment research and decision-support environment that can
gradually connect research, customer context, investment products,
portfolio information, and brokerage services.

### 3. Strategic Role Within the Company

The Research Hub is expected to serve several strategic roles for the
securities company.

- **Research distribution channel** — it provides a structured environment
  for distributing the company's research, analysis, market insights,
  educational content, and product information.
- **Customer acquisition channel** — the platform can attract users who
  are interested in investment information but do not yet have a trading
  account with the company, establishing a relationship before they become
  brokerage customers.
- **Customer engagement channel** — for existing customers, the Research
  Hub can create more frequent and meaningful interactions beyond trading
  activities, so customers engage as part of their ongoing
  investment-research process, not only when placing orders.
- **Connection between research and trading** — the platform can connect
  the research journey with the brokerage journey: users may begin by
  reading or exploring information and later proceed to account opening,
  portfolio connection, product consideration, or trading through the
  company's secured brokerage environment.
- **Customer-understanding layer** — over time, the Research Hub may help
  the company better understand investors through their declared
  interests, research behavior, investment context, and relationship with
  the company's products, which may later support more relevant
  experiences across the wider ecosystem.

### 4. Product Positioning

The Research Hub combines elements from several types of investment
platforms.

- **Public market-information platform** — may serve users broadly
  interested in financial markets, investment information, listed
  companies, sectors, products, and market developments, increasing reach,
  brand visibility, and investor awareness.
- **Investment research platform** — should provide an environment where
  users can explore and understand investment-related content with
  greater depth and structure than a general news platform, reflecting the
  standards, expertise, and credibility expected from a securities company.
- **Brokerage-integrated platform** — unlike an independent content
  platform, the Research Hub belongs to a securities-company ecosystem and
  may therefore connect research with customer accounts, investment
  products, portfolios, and transactions when appropriate.
- **Personalized investment environment** — the long-term direction is for
  the platform to become increasingly relevant to each user rather than
  presenting the same experience to everyone. Personalization should be
  understood broadly: considering the user's context, interests,
  objectives, behavior, and investment relationship when presenting
  information or support. The detailed personalization model has not yet
  been finalized and should be designed separately in later stages.

### 5. Target User Context

The Research Hub may serve both users who already have a relationship with
the securities company and users who do not.

- **Prospective investors** — interested in investing, financial markets,
  or investment knowledge but may not yet have a brokerage account with
  the company. The platform should let them start using the Research Hub
  without first becoming trading customers.
- **Existing brokerage customers** — may already hold a trading account,
  portfolio, or investment products within the company's ecosystem. Their
  Research Hub experience may later be connected with their brokerage
  relationship, subject to consent, security, compliance, and
  product-design decisions.
- **Less experienced investors** — may require clearer explanations,
  stronger guidance, and a simpler way to understand complex market
  information.
- **Experienced and self-directed investors** — may expect deeper
  research, more control, richer data, and the ability to explore
  information independently.

The product should not assume that all users have the same level of
knowledge, investment objectives, or preferred way of consuming
information.

### 6. Identity and Account Context

The Research Hub should be accessible without requiring users to initially
log in with a brokerage trading account. Users may begin with common
authentication methods such as Google, Facebook, email/password, or other
commonly supported login methods. The platform may then request
phone-number verification through OTP. This reduces the entry barrier for
users who are not yet brokerage customers and allows the Research Hub to
operate as an independent acquisition and engagement channel.

There are two important account states:

- **Research Hub account without a trading connection** — a user may have
  an identity within the Research Hub without having a trading account or
  without linking an existing one. At this stage, the Research Hub manages
  the user's basic profile and platform relationship. Editable information
  should generally remain limited to basic, non-trading information: name,
  phone number, preferred language, avatar, basic platform preferences.
- **Research Hub account linked to a trading account** — a user who
  already has a brokerage account may connect it to the Research Hub; a
  user who does not yet have one may later complete account-opening and
  establish the connection. Once the Research Hub identity is linked to a
  trading identity, **the brokerage system should become the authoritative
  identity system** — this is necessary because the connected account
  relates to financial assets, customer verification, transactions, and
  regulated activities. Authentication, security controls, customer
  information, and sensitive profile management should therefore follow
  the brokerage platform's framework after linking.

The detailed linking mechanism, account hierarchy, synchronization rules,
and migration logic will be defined in a separate identity-related task.

### 7. Relationship With the Trading Platform

The Research Hub and the trading platform should be considered separate
but connected product environments. The Research Hub focuses on
information, research, understanding, exploration, and decision support.
The trading platform remains responsible for brokerage-account management,
customer verification, financial assets, orders and transactions, trading
security, product eligibility, and regulated brokerage processes.

The Research Hub may support the journey leading to a transaction, but it
should not replace or bypass the brokerage platform's controls. Where
users move from research to trading, the transition should be clear,
secure, and consistent with the company's regulatory and security
requirements.

### 8. Personalization Context

Personalization is an important long-term direction, but its detailed
implementation has not yet been defined. The underlying principle: the
same market event, product, report, or investment idea has different
relevance depending on a user's investment objectives, investment horizon,
risk characteristics, interests, existing portfolio, knowledge/experience,
relationship with the company, and previous behavior on the platform.

Personalization must remain:
- Explainable.
- Controllable by the user.
- Consistent with consent and privacy requirements.
- Separate from mandatory compliance and suitability controls.
- Careful not to treat inferred behavior as unquestionable fact.
- Appropriate for the financial and regulatory context.

The specific data model, scoring model, recommendation logic, and
user-profile structure will be defined in future tasks.

### 9. Research and Content Context

The Research Hub is expected to work with multiple forms of
investment-related information — internally produced, licensed external
sources, market data, company information, product information, analyst
views, educational materials, and other approved content.

Content should be treated not merely as isolated articles or reports, but
as structured information connected to relevant entities: companies,
securities, sectors, markets, investment themes, financial products,
events, authors/analysts, and customer interests. A strong taxonomy and
metadata structure will matter for search, organization, discovery,
personalization, analytics, and future AI use cases.

The detailed content model, publishing workflow, editorial process, and
information architecture will be handled separately.

### 10. AI Context

AI may become an important component, particularly in helping users
understand and navigate large amounts of investment information —
summarization, information retrieval, explanation, synthesis, user
interaction, or contextual support. The project should not assume AI is
automatically appropriate for every part of the product.

Any AI capability used within the Research Hub must account for:
hallucination risk, outdated information, unsupported conclusions, source
traceability, data privacy, confidential customer information, regulatory
boundaries, user misunderstanding, accountability for generated content,
and the distinction between information, research, recommendation, and
regulated advice.

AI should support the investment-research experience, but must not bypass
required controls or present uncertain information as guaranteed fact. The
exact AI scope, architecture, model selection, governance, and user
experience will be defined separately.

### 11. Data Context

The Research Hub may eventually interact with several broad data
categories, which should **not** automatically be treated as
interchangeable — access, ownership, use, retention, sharing, and security
should be defined according to the sensitivity and purpose of each:

- **Public and market data** — market information, company data,
  securities data, product data, news, corporate events, and other
  externally available or licensed information.
- **Research and content data** — internal reports, analysis, commentary,
  educational content, metadata, and publishing information.
- **User-declared data** — information users intentionally provide to the
  Research Hub.
- **Behavioral data** — generated when users search, read, follow, save,
  view, dismiss, or otherwise interact with the platform.
- **Brokerage and portfolio data** — made available after an appropriate
  connection with the trading platform, subject to authorization, consent,
  security, and regulatory controls.

The project should follow the company's data-governance,
personal-data-protection, information-security, and audit requirements.

### 12. Regulatory and Governance Context

Because the Research Hub belongs to a securities company, it must be
developed within a regulated financial environment, considering
requirements related to: securities activities, customer information,
personal-data protection, cybersecurity, information security, electronic
transactions, content approval, investment research, product distribution,
customer suitability, record retention, auditability, third-party service
providers, and AI/automated processing where applicable.

The Research Hub may contain a combination of public information, company
research, personalized content, product information, and customer-specific
context — legal and compliance treatment may therefore vary by capability.
**Regulatory interpretation should be performed at the level of each
future feature or workflow**, not assumed to be one common rule for the
entire platform.

### 13. Core Product Principles

- **User value before feature volume** — help users understand what is
  useful, relevant, and trustworthy, not build the largest possible
  collection of information or features.
- **Research credibility** — information distributed should reflect the
  standards expected from a securities company; sources, authorship,
  publication time, data freshness, and material assumptions should be
  transparent where appropriate.
- **Progressive product relationship** — users should get value before
  opening or linking a brokerage account; the relationship deepens over
  time as users choose to provide more information or connect services.
- **Clear boundary between research and trading** — support the investment
  journey while preserving the trading platform's controls and
  responsibilities.
- **Explainability** — where the platform personalizes, ranks, summarizes,
  or generates information, users should be able to understand the basis
  of important outputs.
- **User control** — users retain appropriate control over their profile,
  permissions, preferences, linked accounts, and communication settings.
- **Security by design** — incorporated from the beginning, especially
  once connected to brokerage or portfolio data.
- **Compliance by design** — regulatory and suitability considerations
  considered during product definition and workflow design, not added
  after a feature is completed.
- **Modular development** — structured so research, identity,
  personalization, AI, content, data, and brokerage integration can evolve
  without requiring the entire platform to be redesigned each time.

### 14. Current Project Boundaries

At this stage, the following are intentionally **not yet fixed**: final
feature list, MVP scope, detailed user journeys, functional requirements,
prioritization, delivery roadmap, monetization model, content categories,
recommendation methodology, investment-profile model, AI functionality,
portfolio-analysis scope, product taxonomy, technical architecture, vendor
selection, integration design, detailed operating model, team structure,
success metrics, and detailed compliance treatment for individual use
cases. These will be defined task by task as the project progresses.

### 15. Working Definition

The Research Hub can currently be defined as: *a digital investment
research and information platform within a securities-company ecosystem,
designed to serve both prospective and existing investors, connect
research with broader customer and brokerage contexts, and gradually
provide a more relevant and understandable investment experience.*

Its long-term strategic direction: *to become the central research and
investment-understanding layer between the investor, the securities
company's knowledge and data, investment products, customer context, and
the secured trading environment.*

### Note on the earlier crowdsourced/Seeking-Alpha-shaped draft below

The "Key aspects" list below was an earlier working draft, shaped directly
around Seeking-Alpha-style reference platforms (crowdsourced
contributor articles, Quant Ratings, earnings transcripts). Section 1
above explicitly says those platforms are reference points only, **not**
a target to replicate — treat the crowdsourced-contributor model as one
possible direction to reconcile against the canonical context above (esp.
§3 strategic roles, §9 research/content context, §13 principles), not as
confirmed scope. Confirm with product before building against it.

### Key aspects (earlier draft — see note above)

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
