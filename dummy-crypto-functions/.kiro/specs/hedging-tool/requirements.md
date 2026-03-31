# Requirements Document

## Introduction

The Hedging Tool is a new calculator card added to both the Long and Short panels of the trading calculator. It lets a trader configure a main position and an opposing hedge position, then drag a shared price slider to see how each leg performs individually and combined. The card mirrors the visual and structural conventions of the existing "Live PnL Simulator" card.

## Glossary

- **Hedging_Tool**: The calculator card described in this document, rendered inside both `#panel-long` and `#panel-short`.
- **Main_Position**: The primary leveraged position whose direction matches the active panel (Long or Short).
- **Hedge_Position**: The opposing leveraged position; its direction is always the inverse of the Main_Position direction.
- **Entry_Price**: The price at which the Main_Position was opened. Used as the midpoint for the slider range.
- **Hedge_Entry_Price**: The price at which the Hedge_Position was opened. May differ from Entry_Price when the two legs were entered at different times or prices.
- **Main_Leverage**: The leverage multiplier applied to the Main_Position.
- **Hedge_Leverage**: The leverage multiplier applied to the Hedge_Position.
- **Main_Collateral**: The collateral in USD allocated to the Main_Position.
- **Hedge_Collateral**: The collateral in USD allocated to the Hedge_Position.
- **Slider**: The shared `<input type="range">` element whose value represents the simulated current price.
- **Slider_Range**: The configurable percentage band around Entry_Price (the Main_Position entry price) that defines the slider's minimum and maximum values; defaults to ±20%.
- **Liq_Marker**: A visual tick on the slider track indicating the liquidation price for a given leg.
- **Leg_PnL**: The profit or loss in USD for a single position leg at the current simulated price.
- **Leg_PnL_Pct**: Leg_PnL expressed as a percentage of that leg's collateral.
- **Net_PnL**: The sum of Main_Position Leg_PnL and Hedge_Position Leg_PnL.
- **Net_PnL_Pct**: Net_PnL expressed as a percentage of the sum of Main_Collateral and Hedge_Collateral.
- **Actual_Position_Size**: The notional position value equal to collateral × leverage for a given leg.

---

## Requirements

### Requirement 1: Card Structure and Placement

**User Story:** As a trader, I want the Hedging Tool to appear as a standard card in both the Long and Short panels, so that I can access it in the same way as other calculator tools.

#### Acceptance Criteria

1. THE Hedging_Tool SHALL render as a `<div class="card">` element inside `#panel-long` and as a separate `<div class="card">` element inside `#panel-short`.
2. THE Hedging_Tool SHALL include a `card-header` containing a title, a directional `card-badge`, and a help button that opens a help modal.
3. THE Hedging_Tool card in `#panel-long` SHALL display a `card-badge--long` badge.
4. THE Hedging_Tool card in `#panel-short` SHALL display a `card-badge--short` badge.
5. THE Hedging_Tool SHALL follow the element ID naming convention `{panel}-hdg-{field}` where `{panel}` is `l` for the long panel and `s` for the short panel.

---

### Requirement 2: Input Fields

**User Story:** As a trader, I want to enter all position parameters for both legs, so that the simulator can compute accurate PnL and liquidation prices.

#### Acceptance Criteria

1. THE Hedging_Tool SHALL provide a numeric input for Entry_Price (the Main_Position entry price).
2. THE Hedging_Tool SHALL provide a numeric input for Hedge_Entry_Price (the Hedge_Position entry price).
3. THE Hedging_Tool SHALL provide a numeric input for Main_Leverage.
4. THE Hedging_Tool SHALL provide a numeric input for Main_Collateral.
5. THE Hedging_Tool SHALL provide a numeric input for Hedge_Leverage.
6. THE Hedging_Tool SHALL provide a numeric input for Hedge_Collateral.
7. THE Hedging_Tool SHALL provide a numeric input for Slider_Range percentage, pre-populated with `20`.
8. THE Hedging_Tool SHALL display a read-only Actual_Position_Size field for the Main_Position, computed as Main_Collateral × Main_Leverage.
9. THE Hedging_Tool SHALL display a read-only Actual_Position_Size field for the Hedge_Position, computed as Hedge_Collateral × Hedge_Leverage.
10. WHEN any input field value changes, THE Hedging_Tool SHALL recompute and update both Actual_Position_Size read-only fields immediately without requiring a button press.

---

### Requirement 3: Direction Derivation

**User Story:** As a trader, I want the hedge direction to be automatically set to the opposite of my main position, so that I cannot accidentally configure two positions in the same direction.

#### Acceptance Criteria

1. WHEN the Hedging_Tool is rendered inside `#panel-long`, THE Hedging_Tool SHALL treat the Main_Position direction as Long and the Hedge_Position direction as Short.
2. WHEN the Hedging_Tool is rendered inside `#panel-short`, THE Hedging_Tool SHALL treat the Main_Position direction as Short and the Hedge_Position direction as Long.
3. THE Hedging_Tool SHALL NOT provide a user-selectable input for Hedge_Position direction.

---

### Requirement 4: Slider Initialisation

**User Story:** As a trader, I want the slider to be configured around my entry price as soon as I enter my inputs, so that I can immediately start simulating without extra steps.

#### Acceptance Criteria

1. WHEN Entry_Price is a positive number, THE Hedging_Tool SHALL set the slider minimum to `Entry_Price × (1 − Slider_Range / 100)` and the slider maximum to `Entry_Price × (1 + Slider_Range / 100)`.
2. WHEN Entry_Price is a positive number, THE Hedging_Tool SHALL set the slider initial value to Entry_Price so the thumb starts at the midpoint of the Main_Position entry price.
3. WHEN Entry_Price changes, THE Hedging_Tool SHALL reinitialise the slider range and reset the thumb to Entry_Price.
4. WHEN Slider_Range changes, THE Hedging_Tool SHALL reinitialise the slider range using the new percentage while keeping the thumb at Entry_Price.
5. IF Entry_Price is not a positive number, THEN THE Hedging_Tool SHALL display `—` in all output fields and leave the slider in its default state.

---

### Requirement 5: Linked Slider Behaviour

**User Story:** As a trader, I want a single slider that controls the simulated price for both legs simultaneously, so that I can see the combined effect of a price move without managing two separate controls.

#### Acceptance Criteria

1. THE Hedging_Tool SHALL render exactly one `<input type="range">` slider that represents the shared simulated price for both legs.
2. WHEN the slider value changes, THE Hedging_Tool SHALL update the PnL outputs for both the Main_Position and the Hedge_Position using the same simulated price.
3. THE Hedging_Tool SHALL display the current simulated price as a formatted USD value above or adjacent to the slider readout area.

---

### Requirement 6: Per-Leg PnL Calculation

**User Story:** As a trader, I want to see the individual PnL for each leg at the current simulated price, so that I can understand how each position contributes to my overall result.

#### Acceptance Criteria

1. WHEN the slider value changes, THE Hedging_Tool SHALL compute Main_Position Leg_PnL using the formula: `(simPrice − Entry_Price) / Entry_Price × Main_Leverage × Main_Collateral` for a Long main position, and the negation of that formula for a Short main position.
2. WHEN the slider value changes, THE Hedging_Tool SHALL compute Hedge_Position Leg_PnL using the formula: `(simPrice − Hedge_Entry_Price) / Hedge_Entry_Price × Hedge_Leverage × Hedge_Collateral` for a Long hedge position, and the negation of that formula for a Short hedge position.
3. THE Hedging_Tool SHALL display each Leg_PnL as a formatted USD value with a `+` prefix for positive values.
4. THE Hedging_Tool SHALL display each Leg_PnL_Pct as a percentage of the respective leg's collateral with a `+` prefix for positive values.
5. THE Hedging_Tool SHALL apply `metric--profit` styling to a Leg_PnL display when the value is positive and `metric--loss` styling when the value is negative.

---

### Requirement 7: Liquidation Price Markers

**User Story:** As a trader, I want to see where each leg would be liquidated on the slider track, so that I can visually assess how close the simulated price is to a liquidation event.

#### Acceptance Criteria

1. THE Hedging_Tool SHALL compute the Main_Position liquidation price as `Entry_Price × (1 − 1 / Main_Leverage)` for a Long main position and `Entry_Price × (1 + 1 / Main_Leverage)` for a Short main position.
2. THE Hedging_Tool SHALL compute the Hedge_Position liquidation price as `Hedge_Entry_Price × (1 − 1 / Hedge_Leverage)` for a Long hedge position and `Hedge_Entry_Price × (1 + 1 / Hedge_Leverage)` for a Short hedge position.
3. WHEN a liquidation price falls within the current slider range, THE Hedging_Tool SHALL display a Liq_Marker tick on the slider track at the proportional position corresponding to that liquidation price.
4. WHEN a liquidation price falls outside the current slider range, THE Hedging_Tool SHALL hide the corresponding Liq_Marker tick.
5. THE Hedging_Tool SHALL render the Main_Position Liq_Marker and the Hedge_Position Liq_Marker as visually distinct elements on the track.

---

### Requirement 8: Net PnL Display

**User Story:** As a trader, I want to see the combined net PnL of both legs at a glance, so that I can evaluate the overall effectiveness of my hedge at any simulated price.

#### Acceptance Criteria

1. WHEN the slider value changes, THE Hedging_Tool SHALL compute Net_PnL as the sum of Main_Position Leg_PnL and Hedge_Position Leg_PnL.
2. WHEN the slider value changes, THE Hedging_Tool SHALL compute Net_PnL_Pct as `Net_PnL / (Main_Collateral + Hedge_Collateral) × 100`.
3. THE Hedging_Tool SHALL display Net_PnL as a formatted USD value with a `+` prefix for positive values.
4. THE Hedging_Tool SHALL display Net_PnL_Pct as a percentage with a `+` prefix for positive values.
5. THE Hedging_Tool SHALL apply `metric--profit` styling to the Net_PnL display when Net_PnL is positive and `metric--loss` styling when Net_PnL is negative.
6. THE Hedging_Tool SHALL display the individual Main_Position and Hedge_Position Leg_PnL values alongside the Net_PnL so the breakdown remains visible at all times.

---

### Requirement 9: Pure Calculation Helpers

**User Story:** As a developer, I want the core financial formulas extracted as pure functions, so that they can be unit-tested independently of the DOM.

#### Acceptance Criteria

1. THE Hedging_Tool SHALL implement a pure function `hdgLiqPrice(type, entry, leverage)` that returns the liquidation price for a given direction, entry price, and leverage, using the same formula as the existing `liqPrice` helper.
2. THE Hedging_Tool SHALL implement a pure function `hdgLegPnl(type, simPrice, entryPrice, collateral, leverage)` that returns the Leg_PnL in USD for a given direction, simulated price, entry price, collateral, and leverage; callers pass Entry_Price for the main leg and Hedge_Entry_Price for the hedge leg.
3. THE Hedging_Tool SHALL implement a pure function `hdgNetPnl(mainPnl, hedgePnl)` that returns the sum of the two leg PnL values.
4. THE Hedging_Tool SHALL implement a pure function `hdgNetPnlPct(netPnl, mainCollateral, hedgeCollateral)` that returns Net_PnL_Pct, returning `0` when the sum of collaterals is zero.
5. FOR ALL valid inputs where `simPrice = entryPrice`, `hdgLegPnl` SHALL return `0` for both Long and Short directions (at-entry invariant).
6. FOR ALL valid inputs where both legs share the same entry price, collateral, and leverage, `hdgNetPnl(hdgLegPnl('long', p, e, c, l), hdgLegPnl('short', p, e, c, l))` SHALL equal `0` (symmetric hedge cancellation property); this property does NOT hold when Entry_Price differs from Hedge_Entry_Price.

---

### Requirement 10: Help Modal Content

**User Story:** As a trader, I want a help modal for the Hedging Tool that explains what the card does, so that I can understand how to use it without leaving the page.

#### Acceptance Criteria

1. THE Hedging_Tool SHALL register a help modal entry in `HELP_CONTENT` under the keys `'hdg-long'` and `'hdg-short'`.
2. WHEN the help button is clicked, THE Hedging_Tool SHALL open the shared modal displaying the title and body text registered for the active panel's key.
