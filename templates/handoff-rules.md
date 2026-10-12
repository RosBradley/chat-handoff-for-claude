# Handoff rules

Rules for chat handoffs in this project, read by the chat-handoff skill.

Save this file as `claude/Handoff rules.md` in a claude.ai Project, or as `handoffs/Handoff rules.md` in a folder. Replace each example with your own, and delete any section you don't need: the skill's defaults fill the gap.

The examples come from a market expansion report for Sablewire Grid Solutions, a made-up firm that does IT/OT engineering, NERC CIP compliance and OT cybersecurity for electric utilities. Four research chats fold into a report chat, and the report folds into a fresh review chat. The full walkthrough is in [examples/README.md](../examples/README.md).

## Fold-ins
*Which lines fold into which, and any files only one chat may write.*

- market-size, regulations, competitors, interviews → report
- report → review

Only report writes `claude/Expansion report draft.md`. Only review writes `claude/Expansion report final.md`.

## Where approved items go
*For each receiving line: the file approved items go into, and the format they take there.*

- report: `claude/Expansion report draft.md`, in the section the item belongs to, with its source and the date it was folded in.
- review: `claude/Expansion report final.md`, section by section as approved, with any change noted at the end of the section.

Re-read the file right before saving.

## Review checks
*What the receiving chat checks on every incoming item.*

- Every market figure has a source, a year and a currency (US dollars, at the exchange rates in the report's notes).
- Market sizes for IT/OT engineering, compliance and cybersecurity are not added together where they overlap.
- Every regulatory claim names the regulation and the country or province.
- Every finding from interviews says how many interviews back it.

## Deep review triggers
*What counts as high-stakes, so the receiving chat gives it a second, harder pass before you discuss it.*

- Any headline market number: a country's total, or the total across countries.
- A recommendation to enter, or stay out of, a country.
- Anything that commits money: an office, hires, a partner.

## Chat titles
*The title for each state. These are the skill's defaults: change the words, or delete this section to keep them. Renaming a chat is always optional.*

- Working, a master included: "todo.<line>.N"
- Handed off (continuing in a new chat, or waiting for the master): "handedoff.<line>.N", or "pushed.<line>.N" after dot-style commands (`.push`, `.pull`)
- Work sent back: "returned.<line>.N"
- Folded into the master: "folded.<line>.N", or "merged.<line>.N" after `.merge`
- Work went out: "done.<line>.N"

## Never
*Work no handoff may start without being asked.*

- Contact prospects, partners or regulators.
- Copy interview notes outside the project: they name people at customer utilities.
