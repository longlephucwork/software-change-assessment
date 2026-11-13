# Desirability Board

A team tool for assessing proposed software changes (features, bug fixes, refactors, dependencies) and ranking them by desirability, based on the Equation of Software Design from *Code Simplicity: The Fundamentals of Software* by Max Kanat-Alexander.

```
D = (V_now + V_future) / (E_implement + E_maintain)
```

## Running it

Open `index.html` in a browser. There is no build step and no dependencies beyond Google Fonts.

The page has two storage modes:

- **On claude.ai** (published as an Artifact), assessments are saved in a shared database and sync live for everyone the board is shared with.
- **Anywhere else** (opened from disk or a static host), it runs in local mode. Assessments are kept only until the tab closes, and a banner says so. Shared storage outside claude.ai would need a small backend.

## How the score works

Each change is scored on these inputs:

| Input | Scale |
|---|---|
| Reach (share of users) | Under 5% … Nearly all |
| Frequency (how often it helps) | Rarely … Every session |
| Impact (how much it helps when it does) | Cosmetic … Critical |
| Harm | None … Severe |
| Value over time | Fades / Steady / Grows |
| Time to release | Days … Longer |
| Implementation effort | Hours … Months |
| Maintenance load | Near zero … Constant |
| Maintenance over time | Shrinks / Steady / Grows |

The calculation:

- `V = reach × frequency × impact ÷ 12.5`, multiplied down by harm. This gives a 0–10 scale of value per quarter.
- Value now is V, discounted when the release is slow.
- Future value is V per quarter across the software's expected lifetime, adjusted by the value trend.
- Implementation effort is 1, 2, 4, 8 or 16 (hours to months).
- Maintenance is 0.25 to 4 per quarter across the lifetime, adjusted by its trend.

Verdicts: **Strong** at 2 or above, **Worth doing** from 1 to 2, **Marginal** from 0.5 to 1, and **Avoid** below 0.5.

The longer the expected lifetime, the more the score depends on future value against maintenance. That is the book's main point: reducing maintenance effort matters more than reducing implementation effort.

The weights are a starting point, not taken from the book. Use the scores to rank changes against each other and tune the weights to match your team's judgment.

## Design checks and red flags

The sheet also checks for the book's warning signs:

- building for a predicted future need
- being more generic than today's needs require
- expanding the software's purpose
- lock-in to a technology
- reinventing the wheel
- changes that can't be split into small steps

Some flags are raised automatically:

- no stated benefit to users
- no evidence the need is real
- maintenance growing faster than value

## Further reading

`docs/code-simplicity-notes.md` summarizes the book's laws and rules.
