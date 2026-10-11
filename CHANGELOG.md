# Changelog

## 0.2.0 (in testing)

- Installs as a Claude Code plugin; the repo is its own plugin marketplace.
- Deep review is now a second, harder pass by the master chat itself: figures worked out again from the sources, the strongest case against, what breaks if it's wrong. No separate agent.
- The master marks each decided item in the side chat's file with its verdict and date, so a later fold-in never reviews or applies it twice.
- Item letters are fixed for the life of a line; reworked items keep theirs, new ones continue after the highest used.
- A new handoff carries tossed items into "Don't redo", so they can't come back after a receipt is overwritten.
- Without a Project or folder, every change is a new post and the newest counts, so statuses, returns and receipts work there too.
- Chat titles show each chat's state first (`Handed off - market size 3`, `Returned - …`, `Folded - …`, `Continued - …`, `Master - …`, and `Released - …` when the last chat in a chain is finished and its work goes out). Claude can't see or rename chats, so it tells the user the new title at each change.
- Rules file: "Fold-ins" replaces "Master chat" and says which lines fold into which, so chains work (research into report, report into review).
- New worked example: a market expansion report for a grid-security firm, with handoff files at each stage. Replaces the product launch example.
- Cold-read check before saving a handoff.
- Commands trigger only as the whole message (or nearly), in any case, not inside ordinary sentences. Plain requests ("let's hand this off") count too.
- `fold <name>` folds a chat in; `pickup <name>` now always continues. Neither guesses: each asks in one line when it looks out of place. `fold` as the first message of a new chat goes ahead when the rules file says where that line folds (a fresh review chat).
- Dot-style commands, for those who think in git: `.push`, `.push?`, `.pull`, `.merge`, `.status`.
- The first `handoff` in a chat suggests a short line name and asks once; `handoff <name>` sets it, or renames the line (new file saved first, old one deleted after).
- The skill description no longer contains angle brackets, which claude.ai rejects on upload.

## 0.1.0 (October 9, 2026)

First version, in testing.

- Commands: `handoff`, `handoff?`, `pickup <name>`, `pickup`, `handoffs`.
- Pickup continues a chat when typed as the first message of a new chat, and folds it in when typed in a chat already underway.
- Fold-in review: one verdict per item (keep, change, toss or return), nothing applied until the user decides, independent review for high-stakes items.
- Returns written back to the side chat's file; folded files cut down to a receipt.
- Optional per-project rules file, with defaults when it is missing.
- Works in claude.ai Projects, in folders (Claude Code), and in plain chats through past-chat search.
