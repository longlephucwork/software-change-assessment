# Code Simplicity: Study Notes

Notes on *Code Simplicity: The Fundamentals of Software* by Max Kanat-Alexander (O'Reilly, 2012).

## Core thesis

Most software problems come from complexity: bugs, bloat, projects that never ship, and forced rewrites. A whole system is always complex, so the defense is to keep each individual piece simple. The book says the difference between a good and a bad programmer is understanding.

## The six laws

1. **The purpose of software is to help people.** Software never exists to help the computer.
2. **The Equation of Software Design:** `D = (Vn + Vf) / (Ei + Em)`. Over time it reduces to `D ≈ Vf / Em`, so reducing maintenance effort matters more than reducing implementation effort.
3. **Law of Change:** the longer a program exists, the more likely any piece of it will have to change.
4. **Law of Defect Probability:** the chance of introducing a defect is proportional to the size of the change. The best design allows the most change in the environment with the least change in the software.
5. **Law of Simplicity:** ease of maintenance is proportional to the simplicity of the individual pieces.
6. **Law of Testing:** you know how your software behaves only to the degree you have accurately tested it.

## Value

Value has three parts: how many users a change helps, how often it helps them, and how much it helps when it does. The book calls the first two "probability of value" and the third "potential value." Subtract any harm the change causes. A feature nobody uses, or work that never ships, has no value now.

## Key rules

- Don't predict the future. Design from what you know now, and leave room for change.
- **The three flaws:**
  1. Writing code that isn't needed.
  2. Not making code easy to change.
  3. Being too generic.
- Use incremental development and design: build a little, improve the design, then build the next piece.
- Don't fix anything without evidence that the problem exists. Avoid premature optimization.
- Don't Repeat Yourself.
- Simplicity is relative to the audience, and the target is "stupid, dumb simple."
- Be consistent.
- Name things clearly.
- Comments should explain *why*, not *what*.
- **Sources of complexity:**
  - expanding the software's purpose
  - adding programmers
  - changing things that don't need changing
  - lock-in to bad technologies
  - misunderstanding
  - poor design or no design
  - reinventing the wheel
- **Judge a technology** by its survival potential, interoperability and attention to quality.
- When complexity seems unsolvable, the real error usually sits a level below. Ask "What problem are you trying to solve?"
- **Handle complexity** by redesigning in small steps, each one tied to a feature or bug fix.
- Put a simple wrapper around complexity you can't remove.
- **Rewrite only if all of these are true:**
  - Experiments show a rewrite is cheaper than redesigning the existing system.
  - You have a lot of time.
  - You are a better designer than whoever built the original.
  - You will build it in small steps with feedback from users.
  - You can keep maintaining the old system at the same time.
