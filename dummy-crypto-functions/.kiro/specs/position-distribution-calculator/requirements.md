# Requirements Document

## Introduction

The Position Distribution Calculator is a new tool card added to the existing browser-based trading calculator. It helps traders on a cross futures account decide how to split their available balance: how much they can safely deploy into new or existing positions, and how much they must keep as a buffer to delay liquidation. The tool accepts two inputs — total account balance and the amount to reserve — and outputs the spendable amount, the reserve amount, and both as percentages of the total balance.

The tool is account-agnostic (works for any cross futures account regardless of exchange) and follows the same card-based UI pattern as all existing tools. It appears in both the Long and Short panels.

## Glossary

- **Calculator**: The browser-based trading calculator application running in `app.html`.
- **Distribution_Calculator**: The new Position Distribution Calculator card component.
- **Account_Balance**: The total amount of funds currently held in the user's cross futures account, expressed in USD.
- **Reserve_Amount**: The portion of the Account_Balance the user wants to keep untouched to postpone liquidation.
- **Spendable_Amount**: The portion of the Account_Balance available to deploy into positions, computed as `Account_Balance − Reserve_Amount`.
- **Spendable_Percentage**: The ratio of Spendable_Amount to Account_Balance, expressed as a percentage.
- **Reserve_Percentage**: The ratio of Reserve_Amount to Account_Balance, expressed as a percentage.

---

## Requirements

### Requirement 1: Accept account balance and reserve inputs

**User Story:** As a trader, I want to enter my total cross futures account balance and the amount I want to keep in reserve, so that the calculator has the data it needs to compute the distribution.

#### Acceptance Criteria

1. THE Distribution_Calculator SHALL provide a numeric input field for Account_Balance, labelled "Account balance ($)".
2. THE Distribution_Calculator SHALL provide a numeric input field for Reserve_Amount, labelled "Amount to keep ($)".
3. THE Distribution_Calculator SHALL display both input fields in the same card, following the existing `field-grid` layout pattern.
4. WHEN the user submits the form with an Account_Balance that is not a positive number, THE Distribution_Calculator SHALL display an alert stating "Please enter a valid account balance."
5. WHEN the user submits the form with a Reserve_Amount that is negative, THE Distribution_Calculator SHALL display an alert stating "Reserve amount cannot be negative."
6. WHEN the user submits the form with a Reserve_Amount greater than or equal to Account_Balance, THE Distribution_Calculator SHALL display an alert stating "Reserve amount must be less than the account balance."

---

### Requirement 2: Calculate spendable and reserve distribution

**User Story:** As a trader, I want the calculator to tell me how much I can spend and how much I must keep, so that I can make informed position-sizing decisions without risking premature liquidation.

#### Acceptance Criteria

1. WHEN the user clicks the Calculate button with valid inputs, THE Distribution_Calculator SHALL compute Spendable_Amount as `Account_Balance − Reserve_Amount`.
2. WHEN the user clicks the Calculate button with valid inputs, THE Distribution_Calculator SHALL compute Spendable_Percentage as `(Spendable_Amount / Account_Balance) × 100`, rounded to two decimal places.
3. WHEN the user clicks the Calculate button with valid inputs, THE Distribution_Calculator SHALL compute Reserve_Percentage as `(Reserve_Amount / Account_Balance) × 100`, rounded to two decimal places.
4. THE Distribution_Calculator SHALL ensure that Spendable_Percentage and Reserve_Percentage sum to exactly 100.00%.

---

### Requirement 3: Display distribution results

**User Story:** As a trader, I want to see the spendable and reserve amounts alongside their percentages in a clear results section, so that I can read the split at a glance.

#### Acceptance Criteria

1. WHEN results are available, THE Distribution_Calculator SHALL display Spendable_Amount formatted as a USD value in a metric card labelled "Can spend".
2. WHEN results are available, THE Distribution_Calculator SHALL display Spendable_Percentage in the sub-line of the "Can spend" metric card.
3. WHEN results are available, THE Distribution_Calculator SHALL display Reserve_Amount formatted as a USD value in a metric card labelled "Must keep".
4. WHEN results are available, THE Distribution_Calculator SHALL display Reserve_Percentage in the sub-line of the "Must keep" metric card.
5. WHEN results are available, THE Distribution_Calculator SHALL apply the `metric--profit` CSS modifier to the "Can spend" metric card and the `metric--neutral` CSS modifier to the "Must keep" metric card, consistent with the existing colour conventions.
6. WHILE results have not yet been calculated, THE Distribution_Calculator SHALL keep the results section hidden, consistent with the existing `.results` / `.results.visible` pattern.

---

### Requirement 4: Fit the existing card-based UI pattern

**User Story:** As a developer, I want the new tool to follow the same structure and conventions as existing calculator cards, so that the codebase stays consistent and maintainable.

#### Acceptance Criteria

1. THE Distribution_Calculator SHALL be implemented as a `<div class="card">` inside both `#panel-long` and `#panel-short`.
2. THE Distribution_Calculator SHALL include a `card-header` with a `card-title`, a `card-badge`, and a help button (`?`) that opens a help modal keyed `dist-long` or `dist-short` respectively.
3. THE Distribution_Calculator SHALL use element IDs following the pattern `{panel}-dist-{field}` (e.g. `l-dist-balance`, `s-dist-reserve`, `l-dist-results`).
4. THE Distribution_Calculator SHALL use a `btn--long` styled Calculate button in the Long panel and a `btn--short` styled Calculate button in the Short panel.
5. THE Calculator SHALL register help modal content for keys `dist-long` and `dist-short` in the `HELP_CONTENT` constant in `calc.js`.
6. THE Distribution_Calculator SHALL call `showResults(id)` to reveal the results section after a successful calculation, consistent with all other `calc*` functions.
