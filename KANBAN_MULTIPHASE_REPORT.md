# Kanban Multi-Phase Smoke Test — Final Report

## Phase 1: Length Converter

**Commit:** `cf4f097e506ca9a45a9afba4aa67e88c06977b4f`
**Branch:** `main` (pushed to origin)

Built a Python length converter supporting four units with meters-as-base architecture:

- **m** (meters)
- **km** (kilometers)
- **mi** (miles)
- **ft** (feet)

**API:** `convert_length(value, from_unit, to_unit) -> float`
**Error handling:** `ValueError("Unknown unit: ...")` for unsupported units
**Tests:** 19 tests covering identity, simple, cross-unit, edge cases (zero, negative, precision), and error handling

**Report:** `PHASE1_REPORT.md` (untracked in worktree)

---

## Phase 2: Weight Converter + Unified CLI

**Implementation commit:** `368fed15560b7fb61061c03096a94e52df8d5cbe`
**Merge commit (Phase 3 starting point):** `3486afddaa27f4a7dd62d07cab36553f1f0c3d50`

Added weight conversion alongside the existing length converter, plus a unified CLI.

### Weight converter

**API:** `convert_weight(value, from_unit, to_unit) -> float`
**Units:** kg, g, lb, oz (kilograms-as-base)
**Tests:** 17 tests

### Unified CLI

**Invocation:** `python3 -m converter.cli <category> <value> <from_unit> <to_unit>`
**Categories:** `length`, `weight`
**Success output:** bare float on stdout, exit 0
**Error output:** `Error: <message>` on stderr, exit 1

**Total tests after Phase 2:** 47 (19 length + 17 weight + 11 CLI)

---

## Phase 3: JSON Output Mode + Final Report

**Starting point:** main at `3486afddaa27f4a7dd62d07cab36553f1f0c3d50`
**Implementation branch:** `p3-json-output-mode`

Added `--json` flag to both CLI subcommands for machine-readable output.

### JSON success output (stdout, exit 0)

```json
{"success": true, "category": "length", "value": 1000.0, "from_unit": "m", "to_unit": "km", "result": 1.0}
```

Fields: `success`, `category`, `value`, `from_unit`, `to_unit`, `result`

### JSON error output (stderr, exit 1)

```json
{"success": false, "category": "length", "value": 5.0, "from_unit": "parsec", "to_unit": "m", "result": null, "error": "Unknown unit: 'parsec'"}
```

Fields: `success`, `category`, `value`, `from_unit`, `to_unit`, `result`, `error`

### Behavior preserved

- Default (non-JSON) output unchanged: bare float on stdout, `Error:` prefix on stderr
- Argparse usage errors remain deterministic (nonzero exit, typically 2)

### Tests added (12 new CLI tests)

- JSON length conversion (happy path, identity)
- JSON weight conversion (happy path: kg→g, lb→oz)
- JSON zero value
- JSON negative value
- Non-JSON regression (length and weight still produce bare floats)
- JSON invalid unit (stderr parseable JSON, `success: false`, `result: null`)
- JSON invalid category (argparse exit 2)
- JSON missing args (argparse exit 2)

**Total tests after Phase 3:** 59 (19 length + 17 weight + 23 CLI)

---

## Final Verification

```bash
$ python3 -m pytest -q
59 passed in 0.53s

$ python3 -m converter.cli length 1000 m km
1.0

$ python3 -m converter.cli length 1000 m km --json
{"success": true, "category": "length", "value": 1000.0, "from_unit": "m", "to_unit": "km", "result": 1.0}

$ python3 -m converter.cli weight 1 lb oz --json
{"success": true, "category": "weight", "value": 1.0, "from_unit": "lb", "to_unit": "oz", "result": 16.0}

$ python3 -m converter.cli length 5 parsec m --json
{"success": false, "category": "length", "value": 5.0, "from_unit": "parsec", "to_unit": "m", "result": null, "error": "Unknown unit: 'parsec'"}
# exit: 1
```
