---
name: assess-change
description: Assess a proposed software change (a feature request, bug fix, refactor, dependency or performance change, given as a ticket, PR, diff, branch or design idea) using the Equation of Software Design and the rules from "Code Simplicity". Use when someone asks whether a change is worth doing, to prioritize or compare changes, to review a PR or design for complexity, overengineering or maintenance cost, or to fill in a Desirability Board assessment.
---

# Assess a change

Judge a change the way *Code Simplicity* does. Its desirability is its value divided by its effort. Over the software's lifetime this comes down to **future value against maintenance effort**. Score each change on the same scales as the Desirability Board (`index.html`) so the two agree. The book's laws and rules are summarized in `docs/code-simplicity-notes.md`; read it if you need more than this file.

## 1. Gather the facts

- **What is the change?** Read the ticket, PR description, diff or design you were given. For a PR or branch, read the actual diff (`git diff`, `gh pr diff`), not just the description.
- **What is the software's purpose?** Look in the README or the project's docs. If you can't tell, ask, or state the purpose you assumed. Each change is judged against the question "How does this help people do X?"
- **What evidence shows the need is real?** Look for user reports, a reproduction, or measurements. "Someone might want it" is not evidence.
- **How long will the software live?** If you aren't told, use 2 years. Most software lives longer than people expect.

Don't invent facts. If something you need is missing, such as the number of users or how often a bug happens, give your estimate and label it as an estimate.

## 2. Score it

Choose one option for each scale. Indexes start at 0.

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

Tips for scoring:
- **Reach and impact are separate.** A change that helps few users can still be critical, such as accessibility or preventing data loss. Score impact as high as it really is.
- **Maintenance includes** bugs the change will introduce, which grow with the size of the change. It also includes tests to keep green, docs, extra configuration, and every future feature that has to work with this one.
- **Maintenance grows** when the change adds special cases, duplicated logic, new dependencies or new options. **It shrinks** when the change simplifies code, removes code, or puts repeated logic in one place.

## 3. Run the design checks

Tick each check the change actually triggers, using its id:

- `predicts`: built for a predicted future need, not a known one (*don't write code until you need it*)
- `generic`: more generic than today's needs require (*be only as generic as you know you need to be right now*)
- `purpose`: expands or strays from the software's purpose
- `lockin`: adds a dependency that's hard to switch away from. Judge it by survival potential, interoperability and attention to quality.
- `reinvent`: reinvents something that already exists
- `bigbang`: can't be split into small steps (*defect risk is proportional to the size of the change*)
- `simplifies`: simplifies existing code
- `removes`: removes unused code
- `tested`: comes with automated tests (*unless you've tried it, you don't know that it works*)

When reviewing code, also look for:
- repeated information or copy-pasted logic (Don't Repeat Yourself)
- inconsistent naming or patterns
- comments that explain *what* instead of *why*
- unused code
- premature optimization without evidence of a real speed problem

## 4. Compute the score

Write the assessment as JSON and run the scorer. It uses the same formula as the board:

```bash
python3 .claude/skills/assess-change/scripts/score.py - <<'EOF'
{"benefit": "<one sentence>", "evidence": 0, "reach": 3, "freq": 4, "impact": 2, "harm": 0,
 "valueTrend": 1, "release": 1, "impl": 1, "maint": 1, "maintTrend": 1,
 "checks": ["tested"], "horizon": 8}
EOF
```

`horizon` is the expected lifetime in quarters: 1, 2, 4, 8, 20 or 40. The script prints the desirability score, the verdict (Strong ≥ 2, Worth doing ≥ 1, Marginal ≥ 0.5, Avoid below that), the four parts of the equation, and the flags. Don't calculate the score by hand.

## 5. Report

Use this shape:

```
## <Change title>: <Verdict> (D = <score>)

**Helps users by:** <one sentence tied to the software's purpose>

| Value now | Future value | Implementation | Maintenance |
|---|---|---|---|
| … | … | … | … |

**Scores:** reach <…>, frequency <…>, impact <…>, harm <…>, value <trend>; implementation <…>, maintenance <…> and <trend>. Mark any score that is an estimate.

**Red flags:** <each one, with the evidence: file and line, or a quote from the ticket>
**In its favour:** <the positive checks that apply>

**Recommendation:** <do it / do it smaller / defer / drop>, and the single change that would most improve the score.
```

Most of the score comes from future value and maintenance, so the most useful recommendation is usually one of these:
- Split the change into small steps.
- Cut it back to what is needed today.
- Simplify the surrounding code first, so this change becomes easy.
- Collect evidence before building.

When comparing several changes, give one table ranked by D, then one line per change.

To save the assessment to a shared Desirability Board, keep the same field names. The board stores them as one document per change in its `changes` collection.
