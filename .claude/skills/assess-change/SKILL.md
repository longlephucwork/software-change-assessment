---
name: assess-change
description: Assess whether a proposed software change is worth doing, and score it, using the Equation of Software Design from "Code Simplicity" (desirability = value ÷ effort, where future value and maintenance cost dominate). Use this skill whenever someone asks if a feature, bug fix, refactor, new dependency or optimization is worth building. Also use it to prioritize or rank a backlog, compare options, judge a ticket, PR, diff or design doc for overengineering, YAGNI, complexity or long-term maintenance cost, or to fill in a Desirability Board assessment. It applies even when the user doesn't mention the book, e.g. "should we build X?", "which of these should we do first?" or "is this PR over-engineered?". Do not use it for plain bug hunting or style-only code review.
---

# Assess a change

This skill judges a change the way *Code Simplicity* does. A change's desirability is its value divided by its effort. Software usually lives for years, so the score comes down to **future value against maintenance effort**: a change that is cheap to build but expensive to maintain is a bad deal. The scales and formula match the Desirability Board (`index.html` in the project this skill came from), so a team can compare Claude's assessments with their own.

If you need the book's reasoning for a judgment call, read `references/code-simplicity.md`. It summarizes the laws and rules quoted below.

## 1. Gather the facts

- **The change itself.** Read what you were given. For a PR or branch, read the actual diff (`git diff`, `gh pr diff <n>`), because descriptions often understate what changed. Maintenance cost lives in the code.
- **The software's purpose.** Check the README or docs. Every change is judged by "How does this help people do what this software is for?" If you can't find the purpose, state the one you assumed, so the reader can correct it.
- **Evidence that the need is real.** Look for user reports, a reproduction or measurements. The book's rule is to never fix anything without evidence that the problem exists. "Someone might want it" is a prediction, not evidence.
- **Expected lifetime.** If no one says, use 2 years. Software almost always lives longer than people plan for, and the lifetime decides how much maintenance counts.

Some facts may be missing, such as the number of users or how often a bug happens. Estimate them and label them as estimates. A confident score built on invented numbers misleads the team more than an honest range does.

## 2. Score it

Choose one option for each scale. Indexes start at 0, and the option label also works.

| Field | Options |
|---|---|
| `evidence` | Users reported it · Reproduced it · Measured it · Assumed |
| `reach` (share of users helped) | Under 5% · About 10% · About 25% · About half · Nearly all |
| `freq` (how often it helps them) | Rarely · Occasionally · Regularly · Often · Every session |
| `impact` (how much it helps when it does) | Cosmetic · Convenience · Saves real time · Unblocks a task · Critical |
| `harm` (ads, slower flows, broken habits) | None · Slight · Noticeable · Significant · Severe |
| `valueTrend` | Fades · Steady · Grows |
| `release` (time to ship) | Days · Weeks · A quarter · Longer |
| `impl` (research, discussion, code, review, testing) | Hours · Days · A week · Weeks · Months |
| `maint` (ongoing load) | Near zero · Light · Moderate · Heavy · Constant |
| `maintTrend` | Shrinks · Steady · Grows |

Things to get right:
- **Reach and impact are separate.** The book's example is accessibility support for blind users. It reaches few people, but without it they can't use the software at all, so its impact is Critical. Data-loss and security fixes are similar.
- **Maintenance is more than upkeep.** It includes:
  - bugs the change will bring in, which grow with the size of the change (the Law of Defect Probability)
  - tests to keep passing
  - docs
  - configuration options
  - every future feature that has to work with this one
- **The trend is the most important input.** Maintenance grows when a change adds special cases, duplicated logic, new dependencies or new options. It shrinks when the change simplifies code, removes code, or puts repeated logic in one place. The book's goal is maintenance that falls toward zero.

## 3. Run the design checks

Tick each check the change actually triggers, and note the evidence you'll cite for it:

| id | Trigger | The book's reason |
|---|---|---|
| `predicts` | Built for a predicted future need | You can't predict the future. Code written early gets redesigned when the real need arrives. |
| `generic` | More generic than today's needs require | Be only as generic as you know you need to be right now. |
| `purpose` | Expands or strays from the software's purpose | Purpose creep is a major source of complexity. |
| `lockin` | Adds a dependency that's hard to switch away from | Bad technologies lock you in. Judge by survival potential, interoperability and attention to quality. |
| `reinvent` | Reinvents something that already exists | Your time goes into the wheel instead of the product. |
| `bigbang` | Can't be split into small steps | Defect risk is proportional to the size of the change. |
| `simplifies` | Simplifies existing code | Maintenance effort is proportional to complexity. |
| `removes` | Removes unused code | Unused code rots and confuses people. |
| `tested` | Comes with automated tests | Unless you've tried it, you don't know that it works. |

When the input is code, also note:
- duplicated information or copy-pasted logic
- inconsistent naming or patterns
- comments that explain *what* instead of *why*
- dead code
- optimization without evidence of a real speed problem

These belong in the report, not the score.

## 4. Compute the score

Write the inputs as JSON and run `scripts/score.py` from this skill's directory. It uses the board's exact formula, so scores stay comparable across people and runs. Hand-calculated scores drift.

```bash
python3 <this-skill-dir>/scripts/score.py - <<'EOF'
{"benefit": "<one sentence>", "evidence": 0, "reach": 3, "freq": 4, "impact": 2, "harm": 0,
 "valueTrend": 1, "release": 1, "impl": 1, "maint": 1, "maintTrend": 1,
 "checks": ["tested"], "horizon": 8}
EOF
```

`horizon` is the lifetime in quarters: 1, 2, 4, 8, 20 or 40. The output gives:
- **D**, the desirability score
- **the verdict:** Strong at 2 or above, Worth doing from 1, Marginal from 0.5, Avoid below that
- **the four parts of the equation**
- **flags**, including automatic ones such as "Maintenance grows faster than value"

## 5. Report

```
## <Change title>: <Verdict> (D = <score>)

**Helps users by:** <one sentence tied to the software's purpose>

| Value now | Future value | Implementation | Maintenance |
|---|---|---|---|
| … | … | … | … |

**Scores:** reach <…>, frequency <…>, impact <…>, harm <…>, value <trend>; implementation <…>, maintenance <…> and <trend>. Mark estimates with "(est.)".

**Red flags:** <each with its evidence: file:line, or a quote from the ticket>
**In its favour:** <the positive checks that apply>

**Recommendation:** <do it / do it smaller / defer / drop>, plus the single change that would most raise the score.
```

The recommendation is the part people act on, so make it specific. Most of the score comes from future value and maintenance, so the strongest suggestions usually fit one of these patterns:
- Split the change into small steps.
- Cut it back to what's needed today.
- Simplify the surrounding code first, so this change becomes small.
- Collect evidence before building.

When comparing several changes, give one table ranked by D, with one line of reasoning per change.

**Saving to a Desirability Board.** The board keeps one document per change in its `changes` collection. Use the scale fields above, plus `title`, `kind` (Feature, Bug fix, Refactor / simplify, Dependency / tech, or Performance), `benefit`, `checks`, `notes` and `status` (Proposed, Accepted, Deferred, Rejected or Shipped).
