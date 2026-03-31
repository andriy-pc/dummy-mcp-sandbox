# Implementation Plan: Hedging Tool

## Overview

Add a Hedging Tool card to both the Long and Short panels. The card lets a trader configure a main position and an opposing hedge, then drag a single shared price slider to see per-leg PnL, liquidation markers, and combined net PnL in real time. All changes are confined to `app.html`, `calc.js`, `style.css`, and `tests.js`.

## Tasks

- [x] 1. Add pure calculation helpers to `calc.js`
  - [x] 1.1 Implement `hdgLiqPrice(type, entry, leverage)`
    - Returns `entry × (1 − 1/leverage)` for `'long'`, `entry × (1 + 1/leverage)` for `'short'`
    - Place under a new `/* ─── Hedging Tool ───… */` section banner
    - _Requirements: 7.1, 7.2, 9.1_

  - [ ]* 1.2 Write unit tests for `hdgLiqPrice`
    - Mirror the function verbatim at the top of `tests.js`
    - Suite: `hdgLiqPrice` — cover long below entry, short above entry, formula values, higher leverage brings liq closer to entry
    - _Requirements: 9.1_

  - [x] 1.3 Implement `hdgLegPnl(type, simPrice, entryPrice, collateral, leverage)`
    - Long: `(simPrice − entryPrice) / entryPrice × leverage × collateral`
    - Short: negation of the above
    - _Requirements: 6.1, 6.2, 9.2_

  - [ ]* 1.4 Write unit tests for `hdgLegPnl`
    - Mirror the function verbatim in `tests.js`
    - Suite: `hdgLegPnl` — at-entry returns 0 (both directions), long profits on up-move, short profits on down-move, scales linearly with collateral and leverage
    - _Requirements: 9.2, 9.5_

  - [x] 1.5 Implement `hdgNetPnl(mainPnl, hedgePnl)`
    - Returns `mainPnl + hedgePnl`
    - _Requirements: 8.1, 9.3_

  - [x] 1.6 Implement `hdgNetPnlPct(netPnl, mainCollateral, hedgeCollateral)`
    - Returns `netPnl / (mainCollateral + hedgeCollateral) × 100`; returns `0` when sum of collaterals is zero
    - _Requirements: 8.2, 9.4_

  - [ ]* 1.7 Write unit tests for `hdgNetPnl` and `hdgNetPnlPct`
    - Mirror both functions verbatim in `tests.js`
    - Suite `hdgNetPnl`: sum of two values, zero when both zero, sign correctness
    - Suite `hdgNetPnlPct`: typical value, zero-collateral guard, percentage formula
    - Also test the symmetric hedge cancellation property: `hdgNetPnl(hdgLegPnl('long', p, e, c, l), hdgLegPnl('short', p, e, c, l)) === 0` for any valid `p, e, c, l`
    - _Requirements: 9.3, 9.4, 9.6_

- [x] 2. Add `.slider-liq-tick--hedge` CSS modifier to `style.css`
  - Add the modifier class after the existing `.slider-liq-tick` rule; use a distinct colour (e.g. `var(--short)` orange) so the hedge liq tick is visually different from the main liq tick
  - _Requirements: 7.5_

- [x] 3. Add Hedging Tool card markup to `app.html`
  - [x] 3.1 Add the Long panel card inside `#panel-long`
    - Card header: title "Hedging Tool", `card-badge--long` badge "Hedge simulator", help button `onclick="openModal('hdg-long')"`
    - Main position row (`field-grid--3`): `l-hdg-entry` (Entry price), `l-hdg-main-lev` (Main leverage), `l-hdg-main-col` (Main collateral)
    - Read-only actual size for main: `l-hdg-main-actual`, updated via `oninput` on the three fields above
    - Hedge position row (`field-grid--3`): `l-hdg-hedge-entry` (Hedge entry price), `l-hdg-hedge-lev` (Hedge leverage), `l-hdg-hedge-col` (Hedge collateral)
    - Read-only actual size for hedge: `l-hdg-hedge-actual`, updated via `oninput` on the three hedge fields
    - Slider range input row (`field-grid--halves`): `l-hdg-range` (Range %, pre-populated `value="20"`)
    - Slider section: axis labels `l-hdg-low` / `l-hdg-high`, track with `l-hdg-fill-loss`, `l-hdg-fill-profit`, `l-hdg-entry-tick`, `l-hdg-liq-main` (main liq tick), `l-hdg-liq-hedge` (hedge liq tick with `slider-liq-tick--hedge`), range input `l-hdg-slider`
    - Readout: simulated price `l-hdg-price-out`, main PnL card (`l-hdg-main-pnl`, `l-hdg-main-pct`), hedge PnL card (`l-hdg-hedge-pnl`, `l-hdg-hedge-pct`), net PnL card (`l-hdg-net-pnl`, `l-hdg-net-pct`)
    - All `oninput` on entry/leverage/collateral/range fields call `onHdgInput('long')`; slider `oninput` calls `onHdgSlider('long')`
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 2.1–2.10, 3.1, 5.1, 5.3, 6.3, 6.4, 7.3, 7.5, 8.3, 8.4, 8.6_

  - [x] 3.2 Add the Short panel card inside `#panel-short`
    - Identical structure to the Long card with `s-hdg-*` IDs, `card-badge--short` badge, `openModal('hdg-short')`, and `onHdgInput('short')` / `onHdgSlider('short')` handlers
    - _Requirements: 1.1, 1.4, 3.2_

- [x] 4. Implement `onHdgInput(type)` and `onHdgSlider(type)` in `calc.js`
  - [x] 4.1 Implement `onHdgInput(type)`
    - Derive `p = type[0]`
    - Read `entry`, `mainLev`, `mainCol`, `hedgeEntry`, `hedgeLev`, `hedgeCol`, `rangePct` from DOM
    - Update `{p}-hdg-main-actual` = `fmt(mainCol × mainLev)` and `{p}-hdg-hedge-actual` = `fmt(hedgeCol × hedgeLev)` (show `—` when inputs are invalid)
    - When `entry > 0`: set slider `min = entry × (1 − rangePct/100)`, `max = entry × (1 + rangePct/100)`, `value = entry`; update axis labels; call `onHdgSlider(type)`
    - When `entry ≤ 0` or missing: reset all output fields to `—`
    - _Requirements: 2.8, 2.9, 2.10, 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 4.2 Implement `onHdgSlider(type)`
    - Derive `p`, read `simPrice` from slider, read all six position inputs and `entry`
    - Compute `mainPnl = hdgLegPnl(mainDir, simPrice, entry, mainCol, mainLev)` where `mainDir` is `type`
    - Compute `hedgePnl = hdgLegPnl(hedgeDir, simPrice, hedgeEntry, hedgeCol, hedgeLev)` where `hedgeDir` is the opposite of `type`
    - Compute `netPnl = hdgNetPnl(mainPnl, hedgePnl)` and `netPct = hdgNetPnlPct(netPnl, mainCol, hedgeCol)`
    - Write formatted USD + percentage to main, hedge, and net readout elements; apply `metric--profit` / `metric--loss` classes
    - Display simulated price as formatted USD in `{p}-hdg-price-out`
    - Compute and position both liq ticks (`hdgLiqPrice`) — show when in range, hide when out of range
    - Update fill bars (`{p}-hdg-fill-loss`, `{p}-hdg-fill-profit`) based on thumb position relative to midpoint
    - _Requirements: 5.2, 5.3, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6_

- [x] 5. Register help modal entries in `HELP_CONTENT`
  - Add `'hdg-long'` and `'hdg-short'` keys to the `HELP_CONTENT` object in `calc.js` with appropriate title and body text explaining the hedging tool
  - _Requirements: 10.1, 10.2_

- [x] 6. Checkpoint — verify everything wires together
  - Ensure all tests pass, ask the user if questions arise.
