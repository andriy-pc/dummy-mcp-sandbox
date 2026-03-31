# Design Document: Position Distribution Calculator

## Overview

The Position Distribution Calculator is a new card added to both the Long and Short panels of the existing browser-based trading calculator. It accepts two inputs — total account balance and a reserve amount — and outputs how much the trader can safely deploy into positions versus how much must be kept as a liquidation buffer, expressed both in USD and as percentages.

The feature is purely client-side arithmetic with no state persistence. It follows the exact same card pattern, ID conventions, and JS function structure as every other tool in the app.

---

## Architecture

The app has no build step, no modules, and no framework. All logic lives in `calc.js`, all markup in `app.html`, and all styles in `style.css`. The new feature slots into this structure without introducing any new files or patterns.

```
app.html        ← two new <div class="card"> blocks (one per panel)
calc.js         ← one new calcDist(type) function + HELP_CONTENT entries
style.css       ← no new rules needed (all required classes already exist)
```

Data flow:

```
User input (balance, reserve)
        │
        ▼
  calcDist(type)          ← validates inputs, computes values
        │
        ├─ alert()        ← on invalid input
        │
        └─ DOM writes     ← on valid input: updates metric cards, calls showResults()
```

---

## Components and Interfaces

### calcDist(type)

Top-level function following the same signature as `calcStop`, `calcPnl`, etc.

```
calcDist(type: 'long' | 'short') → void
```

- Reads `{p}-dist-balance` and `{p}-dist-reserve` input values
- Validates inputs (three guard clauses with `alert()`)
- Computes spendable amount, spendable %, reserve %
- Writes results to DOM output elements
- Calls `showResults('{p}-dist-results')`

### HELP_CONTENT entries

Two new keys added to the existing `HELP_CONTENT` constant:

```js
'dist-long':  { title: '...', body: '...' }
'dist-short': { title: '...', body: '...' }
```

### HTML card structure (per panel)

Each panel gets one new card. IDs follow `{p}-dist-{field}`:

| Element              | Long ID              | Short ID             |
|----------------------|----------------------|----------------------|
| Balance input        | `l-dist-balance`     | `s-dist-balance`     |
| Reserve input        | `l-dist-reserve`     | `s-dist-reserve`     |
| Calculate button     | `l-dist-btn`         | `s-dist-btn`         |
| Results container    | `l-dist-results`     | `s-dist-results`     |
| Spendable value      | `l-dist-spendable`   | `s-dist-spendable`   |
| Spendable % sub-line | `l-dist-spend-pct`   | `s-dist-spend-pct`   |
| Reserve value        | `l-dist-reserve-out` | `s-dist-reserve-out` |
| Reserve % sub-line   | `l-dist-res-pct`     | `s-dist-res-pct`     |
| Spendable card       | `l-dist-spend-card`  | `s-dist-spend-card`  |

---

## Data Models

All values are plain JS numbers. No objects, no state, no persistence.

| Variable             | Formula                                          | Type   |
|----------------------|--------------------------------------------------|--------|
| `balance`            | user input                                       | number |
| `reserve`            | user input                                       | number |
| `spendable`          | `balance − reserve`                              | number |
| `spendablePct`       | `(spendable / balance) × 100`, 2 decimal places  | number |
| `reservePct`         | `(reserve / balance) × 100`, 2 decimal places    | number |

Validation rules (checked in order, short-circuit on first failure):

1. `balance` must be a positive finite number → alert "Please enter a valid account balance."
2. `reserve` must be ≥ 0 → alert "Reserve amount cannot be negative."
3. `reserve` must be strictly less than `balance` → alert "Reserve amount must be less than the account balance."

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Invalid balance is rejected

*For any* non-positive or non-finite value supplied as the account balance (zero, negative, NaN, Infinity), calling `calcDist` should trigger an alert with the message "Please enter a valid account balance." and leave the results section unchanged.

**Validates: Requirements 1.4**

### Property 2: Negative reserve is rejected

*For any* positive account balance and any negative reserve amount, calling `calcDist` should trigger an alert with the message "Reserve amount cannot be negative." and leave the results section unchanged.

**Validates: Requirements 1.5**

### Property 3: Reserve ≥ balance is rejected

*For any* positive account balance and any reserve amount that is greater than or equal to that balance, calling `calcDist` should trigger an alert with the message "Reserve amount must be less than the account balance." and leave the results section unchanged.

**Validates: Requirements 1.6**

### Property 4: Calculation correctness and percentage invariant

*For any* valid pair (balance, reserve) where `balance > 0` and `0 ≤ reserve < balance`, the computed spendable amount must equal `balance − reserve`, the spendable percentage must equal `(spendable / balance) × 100` rounded to two decimal places, the reserve percentage must equal `(reserve / balance) × 100` rounded to two decimal places, and the two percentages must sum to exactly `100.00`.

**Validates: Requirements 2.1, 2.2, 2.3, 2.4**

### Property 5: Output display reflects computed values

*For any* valid pair (balance, reserve), after `calcDist` runs, the spendable metric card must display the USD-formatted spendable amount with its percentage in the sub-line, the reserve metric card must display the USD-formatted reserve amount with its percentage in the sub-line, the spendable card must carry the `metric--profit` class, the reserve card must carry the `metric--neutral` class, and the results container must carry the `visible` class.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 4.6**

---

## Error Handling

All error handling is synchronous and inline, matching the existing pattern in `calcStop` and `calcPnl`:

```js
if (!balance || balance <= 0) {
  alert('Please enter a valid account balance.');
  return;
}
if (reserve < 0) {
  alert('Reserve amount cannot be negative.');
  return;
}
if (reserve >= balance) {
  alert('Reserve amount must be less than the account balance.');
  return;
}
```

No exceptions are thrown. No error state is stored. The results section is never shown on an error path — `showResults()` is only called after all guards pass.

---

## Testing Strategy

The tech stack has no test runner installed. Tests are loaded via CDN `<script>` tags in a standalone `tests.js` file (already present in the repo) and run in the browser.

**Property-based testing library**: [fast-check](https://fast-check.dev/) loaded via CDN:
```html
<script src="https://cdn.jsdelivr.net/npm/fast-check/lib/bundle/fast-check.min.js"></script>
```

### Dual approach

Unit tests (examples) cover:
- DOM structure: both panels contain the card with correct IDs, labels, badge, and help button
- HELP_CONTENT has entries for `dist-long` and `dist-short`
- Results section is hidden before any calculation

Property tests cover all five correctness properties above. Each runs a minimum of 100 iterations.

### Property test tags

Each property test must include a comment in the format:

```
// Feature: position-distribution-calculator, Property N: <property_text>
```

### Property test sketches

**Property 1** — generate arbitrary non-positive numbers as balance, stub `window.alert`, call `calcDist`, assert alert was called with the correct message.

**Property 2** — generate `fc.tuple(fc.float({ min: 0.01 }), fc.float({ max: -0.01 }))` for (balance, negative reserve), assert correct alert.

**Property 3** — generate `fc.float({ min: 0.01 })` for balance, then generate reserve as `balance + fc.float({ min: 0 })`, assert correct alert.

**Property 4** — generate `fc.float({ min: 0.01, max: 1e9 })` for balance and `fc.float({ min: 0, max: balance - 0.01 })` for reserve, call `calcDist`, read DOM output elements, assert arithmetic correctness and that percentages sum to 100.00.

**Property 5** — same generator as Property 4, additionally assert CSS classes and `visible` class on results container.

Unit tests for Properties 4 and 5 share the same setup; they can be combined into a single property test that checks both arithmetic and DOM state simultaneously, eliminating redundancy.
