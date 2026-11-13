#!/usr/bin/env python3
"""Score a proposed change with the Desirability Board's model.

Mirrors the scoring in index.html exactly, so the skill and the board agree.

Usage:
    python3 score.py assessment.json
    echo '{...}' | python3 score.py -

Input JSON: each scale field is a 0-based index into the options below
(the option label is also accepted).

    {
      "benefit": "Lets programmers save without leaving the keyboard",
      "evidence": 0, "reach": 3, "freq": 4, "impact": 2, "harm": 0,
      "valueTrend": 1, "release": 1, "impl": 1, "maint": 1, "maintTrend": 1,
      "checks": ["tested"],
      "horizon": 8
    }

horizon is the software's expected lifetime in quarters: 1, 2, 4, 8, 20 or 40.
"""
import json
import sys

OPTS = {
    "evidence": ["Users reported it", "Reproduced it", "Measured it", "Assumed"],
    "reach": ["Under 5%", "About 10%", "About 25%", "About half", "Nearly all"],
    "freq": ["Rarely", "Occasionally", "Regularly", "Often", "Every session"],
    "impact": ["Cosmetic", "Convenience", "Saves real time", "Unblocks a task", "Critical"],
    "harm": ["None", "Slight", "Noticeable", "Significant", "Severe"],
    "valueTrend": ["Fades", "Steady", "Grows"],
    "release": ["Days", "Weeks", "A quarter", "Longer"],
    "impl": ["Hours", "Days", "A week", "Weeks", "Months"],
    "maint": ["Near zero", "Light", "Moderate", "Heavy", "Constant"],
    "maintTrend": ["Shrinks", "Steady", "Grows"],
}
DEFAULTS = {"evidence": 0, "reach": 2, "freq": 2, "impact": 2, "harm": 0, "valueTrend": 1,
            "release": 1, "impl": 2, "maint": 1, "maintTrend": 1}
CHECKS = {
    "predicts": ("bad", "Designs for a future nobody can predict"),
    "generic": ("bad", "Overengineered: be only as generic as you need now"),
    "purpose": ("bad", "Strays from the software's purpose"),
    "lockin": ("bad", "Risk of lock-in to a technology"),
    "reinvent": ("bad", "Reinvents the wheel"),
    "bigbang": ("bad", "Large change: defect risk grows with change size"),
    "simplifies": ("good", "Simplifies existing code"),
    "removes": ("good", "Removes unused code"),
    "tested": ("good", "Covered by automated tests"),
}
HORIZONS = {1: "3 months", 2: "6 months", 4: "1 year", 8: "2 years", 20: "5 years", 40: "10 years"}


def index_of(field, value):
    opts = OPTS[field]
    if isinstance(value, str):
        for i, label in enumerate(opts):
            if label.lower() == value.strip().lower():
                return i
        raise ValueError(f"{field}: unknown option {value!r}; choose from {opts}")
    if isinstance(value, int) and 0 <= value < len(opts):
        return value
    raise ValueError(f"{field}: {value!r} is out of range 0-{len(opts) - 1}")


def assess(raw):
    c = {k: index_of(k, raw.get(k, DEFAULTS[k])) for k in OPTS}
    benefit = str(raw.get("benefit", "")).strip()
    checks = [x for x in raw.get("checks", []) if x in CHECKS]
    unknown = [x for x in raw.get("checks", []) if x not in CHECKS]
    if unknown:
        raise ValueError(f"checks: unknown ids {unknown}; choose from {list(CHECKS)}")
    T = int(raw.get("horizon", 8))
    if T not in HORIZONS:
        raise ValueError(f"horizon must be one of {list(HORIZONS)} (quarters)")

    V = (c["reach"] + 1) * (c["freq"] + 1) * (c["impact"] + 1) / 12.5 * [1, 0.85, 0.65, 0.4, 0.15][c["harm"]]
    Vn = V * [1, 0.9, 0.75, 0.5][c["release"]]
    tv = [0.25, 1, 2][c["valueTrend"]]
    Vf = V * T * (1 + tv) / 2
    Ei = [1, 2, 4, 8, 16][c["impl"]]
    m = [0.25, 0.5, 1, 2, 4][c["maint"]]
    te = [0.25, 1, 3][c["maintTrend"]]
    Em = m * T * (1 + te) / 2
    D = (Vn + Vf) / (Ei + Em)

    flags = []
    if not benefit:
        flags.append(("bad", "No stated benefit to users"))
    if c["evidence"] == 3:
        flags.append(("bad", "No evidence the need is real; don't fix what isn't shown to be broken"))
    if te > tv:
        flags.append(("bad", "Maintenance grows faster than value"))
    if c["harm"] >= 3:
        flags.append(("warn", "Harm may cancel out much of the help"))
    if c["release"] == 3:
        flags.append(("warn", "Slow to ship: unreleased work helps nobody"))
    flags += [CHECKS[k] for k in checks]
    if c["maintTrend"] == 0:
        flags.append(("good", "Maintenance shrinks over time"))
    order = ["bad", "warn", "good"]
    flags.sort(key=lambda f: order.index(f[0]))

    verdict = "Strong" if D >= 2 else "Worth doing" if D >= 1 else "Marginal" if D >= 0.5 else "Avoid"
    return {
        "desirability": round(D, 2), "verdict": verdict, "horizon": HORIZONS[T],
        "value_now": round(Vn, 2), "future_value": round(Vf, 2),
        "implementation_effort": round(Ei, 2), "maintenance_effort": round(Em, 2),
        "inputs": {k: OPTS[k][v] for k, v in c.items()},
        "flags": [{"tone": t, "message": msg} for t, msg in flags],
    }


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = sys.stdin if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8")
    try:
        print(json.dumps(assess(json.load(src)), indent=2))
    except ValueError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
