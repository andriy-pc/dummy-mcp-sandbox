# Design Document — Hedging Tool

## Overview

The Hedging Tool adds a new calculator card to both the Long and Short panels. A trader configures a main position and an opposing hedge position, then drags a single shared price slider to see per-leg PnL, liquidation markers, and combined net PnL in real time.

The card reuses every existing CSS primitive. The only new CSS is a second liquidation-tick colour modifier. All new logic lives in `calc.js`; all new markup in `app.html`; `tests.js` gains mirrored helpers and four new suites.

---

## Architecture

### Files changed

| File | Change |
|---|---|
| `app.html` | One hedging card inside `#panel-long`, one inside `#panel-short` |
| `calc.js` | Four pure helpers, `onHdgInput`, `onHdgSlider`, two `HELP_CONTENT` entries, `bindEvents` wiring |
| `style.css` | `.slider-liq-tick--hedge` colour modifier |
| `tests.js` | Mirror four pure helpers; four new suites |

No new files. No build step. No dependencies.

### Dependency flow

```
app.html  ──(DOM)──►  calc.js
                        ├── hdgLiqPrice()      (pure)
                        ├── hdgLegPnl()        (pure)
                        ├── hdgNetPnl()        (pure)
                        ├── hdgNetPnlPct()     (pure)
                        ├── onHdgInput(type)   (DOM handler)
                        └── onHdgSlider(type)  (DOM handler)
```

---

## Components and Interfaces

### HTML card structure

`{p}` = `l` or `s`. Long card uses `card-badge--long`; short card uses `card-badge--short`.
The help button `data-modal` value is `hdg-long` / `hdg-short`.

Note: per the `structure.md` convention, event handlers are **inline** `oninput` / `onclick` attributes in the HTML — not wired via `addEventListener`. The constraint in the original prompt to use `bindEvents` is superseded by the workspace steering rule.
