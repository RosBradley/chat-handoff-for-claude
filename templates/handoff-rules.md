# Handoff rules

Rules for chat handoffs in this project, read by the chat-handoff skill.

Save this file as `claude/Handoff rules.md` in a claude.ai Project, or as `handoffs/Handoff rules.md` in a folder. Replace each example with your own, and delete any section you don't need: the skill's defaults fill the gap.

The examples are for a product launch planned across several chats (pricing, ads, website), with one master chat, "plan", that keeps the launch plan.

## Master chat
*The chat that receives fold-ins, and any files only it may write.*

plan: the chat that keeps the launch plan. It is the only chat that writes `claude/Launch plan.md`.

## Where approved items go
*The file approved items are added to, and the format they take there.*

`claude/Launch plan.md`, under "Pending changes", one line per item with its date and source chat. Re-read the file right before saving.

## Review checks
*What the master checks on every incoming item.*

- Every cost against the approved budget in the launch plan.
- Every date against the launch calendar.
- Every task has a named owner.
- Every figure from outside research has a source link.

## Deep review triggers
*What counts as high-stakes, so the master gives it a second, harder pass before you discuss it.*

- The total budget moves by more than 10%.
- The launch date moves.
- Anything public-facing or legal: pricing, claims in ads, terms of service.

## Chat titles
*The naming convention for open and finished chats.*

"Open - <name> N" while open; "Done - <name> N" when finished.

## Never
*Work no handoff may start without being asked.*

- Send emails or post anything publicly.
