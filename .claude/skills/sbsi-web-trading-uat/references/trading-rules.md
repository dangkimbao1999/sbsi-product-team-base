# SBSI Web Trading (Maris / Core FLEX) — Trading rules reference

> **Unverified.** Ported from the Antigravity `sbsi-web-trading-tester`
> skill's `test_guidelines.md`. Confirm each rule against HDSD
> (`01_FLEX_BackOffice`, `02_SBSI_Web_App`) or current exchange regulation
> before citing it as the reason for a Fail. If they disagree, trust the
> source document and flag the mismatch to the user.

## 1. Price bands & price steps (stocks)

| Exchange | Band vs. reference (TC) | Price step |
| :--- | :--- | :--- |
| HOSE | ±7% | < 10,000đ: 10đ · 10,000–49,950đ: 50đ · ≥ 50,000đ: 100đ |
| HNX | ±10% | 100đ |
| UPCOM | ±15% | 100đ |

Maris displays prices ÷1,000 (20,950đ is entered as `20.95`). Always read the
live Trần/Sàn from the screen. Bands can differ (e.g. first trading day,
ex-rights dates), so don't compute them from the table alone.

## 2. Lot sizes

- Board lot: multiples of 100 shares.
- Odd lot: 1–99 shares. Only `LO` is allowed. `ATO`, `ATC`, `MTL`, `MOK`,
  `MAK` must be rejected/locked for odd lots. Volume is shown exactly, with
  no rounding.

## 3. Buying power (sub-account 06 — margin)

- Buy order value = price (as entered) × volume × 1,000.
- Buying power after placing = before − order value − margin fee (if any).
- Cancelling an open order must restore buying power immediately and
  in full.

## 4. Order statuses in Sổ lệnh

1. `Chờ gửi`: queued to the exchange, or outside trading hours.
2. `Chờ khớp` (Open): accepted by the exchange, waiting for a match.
3. `Khớp một phần` (Partially filled).
4. `Khớp hết` (Filled).
5. `Đã hủy` (Cancelled): by the user or the system (MOK/MAK).
6. `Từ chối` (Rejected): by Core or the exchange for a rule violation.
