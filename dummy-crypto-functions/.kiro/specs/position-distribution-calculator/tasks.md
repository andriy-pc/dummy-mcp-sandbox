# Implementation Plan: Position Distribution Calculator

## Overview

Add a Position Distribution Calculator card to both the Long and Short panels of `app.html`, implement the `calcDist(type)` function and `HELP_CONTENT` entries in `calc.js`, and wire up all event handlers. No new files or CSS rules are needed.

## Tasks

- [x] 1. Add HTML card markup to both panels in `app.html`
  - Add a `<div class="card">` block inside `#panel-long` with card-header (title "Position distribution", badge, help button keyed `dist-long`), a `field-grid field-grid--halves` containing inputs `l-dist-balance` and `l-dist-reserve`, a `btn--long` button (`l-dist-btn`), and a results section (`l-dist-results`) with metric cards for `l-dist-spend-card`/`l-dist-spendable`/`l-dist-spend-pct` and `l-dist-reserve-out`/`l-dist-res-pct`
  - Duplicate the card inside `#panel-short` using `s-` prefixed IDs, `card-badge--short`, `btn--short`, and help key `dist-short`
  - Use inline `onclick` attributes on buttons and no `addEventListener` calls, consistent with the existing card pattern
  - _Requirements: 1.1, 1.2, 1.3, 4.1, 4.2, 4.3, 4.4_

- [x] 2. Implement `calcDist` and `HELP_CONTENT` entries in `calc.js`
  - [x] 2.1 Add `dist-long` and `dist-short` entries to the `HELP_CONTENT` constant
    - Title and body text describing the Position Distribution Calculator for each panel direction
    - _Requirements: 4.5_

  - [x] 2.2 Implement `calcDist(type)` function
    - Derive `p = type[0]`, read `{p}-dist-balance` and `{p}-dist-reserve` input values
    - Apply three ordered guard clauses with `alert()`: invalid balance, negative reserve, reserve ≥ balance
    - Compute `spendable = balance − reserve`, `spendablePct = (spendable / balance) × 100` rounded to 2 dp, `reservePct = (reserve / balance) × 100` rounded to 2 dp
    - Write `fmt(spendable)` to `{p}-dist-spendable`, `spendablePct + '%'` to `{p}-dist-spend-pct`, `fmt(reserve)` to `{p}-dist-reserve-out`, `reservePct + '%'` to `{p}-dist-res-pct`
    - Apply `metric--profit` to `{p}-dist-spend-card` and `metric--neutral` to the reserve card
    - Call `showResults('{p}-dist-results')`
    - _Requirements: 1.4, 1.5, 1.6, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.6_

  - [ ]* 2.3 Write property test for invalid balance rejection (Property 1)
    - **Property 1: Invalid balance is rejected**
    - **Validates: Requirements 1.4**
    - Load fast-check via CDN in `tests.js` (or a dedicated test HTML file); generate non-positive/non-finite balance values; stub `window.alert`; assert correct alert message and no DOM change

  - [ ]* 2.4 Write property test for negative reserve rejection (Property 2)
    - **Property 2: Negative reserve is rejected**
    - **Validates: Requirements 1.5**
    - Generate `fc.tuple(fc.float({ min: 0.01 }), fc.float({ max: -0.01 }))`; assert alert "Reserve amount cannot be negative."

  - [ ]* 2.5 Write property test for reserve ≥ balance rejection (Property 3)
    - **Property 3: Reserve ≥ balance is rejected**
    - **Validates: Requirements 1.6**
    - Generate positive balance and reserve ≥ balance; assert alert "Reserve amount must be less than the account balance."

  - [ ]* 2.6 Write property test for calculation correctness and percentage invariant (Property 4)
    - **Property 4: Calculation correctness and percentage invariant**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4**
    - Generate valid (balance, reserve) pairs; call `calcDist`; read DOM output; assert `spendable = balance − reserve`, correct percentages, and that `spendablePct + reservePct === 100.00`

  - [ ]* 2.7 Write property test for output display and CSS classes (Property 5)
    - **Property 5: Output display reflects computed values**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 4.6**
    - Same generator as Property 4; additionally assert `metric--profit` on spend card, `metric--neutral` on reserve card, and `visible` class on results container

- [x] 3. Checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Add unit tests for `calcDist` pure logic in `tests.js`
  - [x] 4.1 Add pure helper functions mirroring `calcDist` arithmetic to `tests.js`
    - `distSpendable(balance, reserve)` → `balance − reserve`
    - `distSpendablePct(spendable, balance)` → `(spendable / balance) × 100`
    - `distReservePct(reserve, balance)` → `(reserve / balance) × 100`
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ]* 4.2 Write unit tests for the pure helper functions
    - Test `distSpendable` with typical values and edge case where reserve is 0
    - Test `distSpendablePct` and `distReservePct` sum to 100 for representative inputs
    - Test that percentages are rounded to two decimal places
    - _Requirements: 2.1, 2.2, 2.3, 2.4_

- [x] 5. Final checkpoint — Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- The design specifies JavaScript (plain ES6+, no TypeScript, no build step)
- fast-check must be loaded via CDN `<script>` tag — not installed locally
- All CSS classes needed (`metric--profit`, `metric--neutral`, `results.visible`) already exist in `style.css`
- No new files are required beyond the existing `app.html`, `calc.js`, and `tests.js`
