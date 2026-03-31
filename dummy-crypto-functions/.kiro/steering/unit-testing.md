# Unit Testing

## Running Tests

Tests run inside a Node.js Docker container — no local Node install required.

**PowerShell:**
```powershell
docker run -it --rm -v "${PWD}:/app" -w /app node:24-alpine node tests.js
```

**Git Bash:**
```bash
docker run -it --rm -v "$(pwd):/app" -w /app node:24-alpine node tests.js
```

A non-zero exit code means at least one test failed. The final line always prints a summary:
```
42 tests: 42 passed, 0 failed
```

## File Layout

All tests live in a single file: `tests.js` at the project root.

- No test framework installed — uses Node's built-in `assert/strict` module loaded via `require`
- No ES modules — `'use strict';` at the top, CommonJS only
- Pure functions are re-implemented at the top of `tests.js` (mirroring the formulas in `calc.js` / `auth.js`) so the file is self-contained and needs no imports from the app source

## Test File Structure

```
'use strict';
const assert = require('assert/strict');

/* ─── Pure calculation helpers (mirroring calc.js formulas) ─────────────── */
// Re-implement every function under test here

/* ─── Test runner ────────────────────────────────────────────────────────── */
// suite(), test(), assertClose() helpers

/* ─── <Feature group> ───────────────────────────────────────────────────── */
suite('featureName');
test('description', () => { … });

/* ─── Summary ────────────────────────────────────────────────────────────── */
console.log(`\n${passed + failed} tests: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
```

## Test Runner Helpers

These three helpers are defined once in `tests.js` and must not be changed:

```js
let passed = 0;
let failed = 0;
let currentSuite = '';

function suite(name) {
  currentSuite = name;
  console.log(`\n${name}`);
}

function test(desc, fn) {
  try {
    fn();
    console.log(`  ✓ ${desc}`);
    passed++;
  } catch (e) {
    console.error(`  ✗ ${desc}\n    ${e.message}`);
    failed++;
  }
}

function assertClose(a, b, tol = 1e-9) {
  if (Math.abs(a - b) > tol) {
    throw new Error(`expected ${b}, got ${a} (tol ${tol})`);
  }
}
```

## Assertion Conventions

| Situation | Use |
|---|---|
| Exact string / boolean equality | `assert.equal(actual, expected)` |
| Floating-point numeric result | `assertClose(actual, expected)` — default tolerance `1e-9` |
| Looser numeric tolerance needed | `assertClose(actual, expected, 1e-6)` |
| Sign / ordering check | `assert.ok(value > 0)` |

Never use `assert.strictEqual` for floats — always use `assertClose`.

## Naming & Organisation

- Group related tests under a `suite('name')` call — one suite per logical function or feature
- Test descriptions are lowercase, plain English, and describe the specific behaviour: `'long stop is below entry'`, `'zero range → 50'`
- Align test descriptions with spaces so the arrow functions line up vertically within a suite (see existing tests for style)
- Section comment banners match the JS style used in `calc.js`:
  ```js
  /* ─── Section name ───────────────────────────────────────────────────────── */
  ```

## What to Test

For every new pure function added to `calc.js` or `auth.js`:

1. Mirror the function verbatim at the top of `tests.js` under the helpers block
2. Add a `suite` block with tests covering:
   - Typical / happy-path inputs
   - Boundary values (zero, equal inputs, min/max)
   - Sign / direction correctness (long vs short where applicable)
   - Linearity or scaling properties where the formula allows it
   - Edge cases that could produce `NaN`, `Infinity`, or division-by-zero

DOM-dependent functions (`calc*`, `on*`, event handlers) are **not** unit-tested here — only pure calculation helpers are tested.

## Adding Tests for a New Feature

1. Implement the pure helper(s) in `calc.js`
2. Copy the same function(s) verbatim into the helpers block at the top of `tests.js`
3. Add a new section banner and `suite` / `test` calls at the bottom of `tests.js`, before the Summary block
4. Run via Docker to confirm all tests pass before committing
