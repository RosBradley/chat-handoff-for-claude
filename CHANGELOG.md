# Changelog

## Unreleased

- Installs as a Claude Code plugin; the repo is its own plugin marketplace.
- Deep review is now a second, harder pass by the master chat itself: figures worked out again from the sources, the strongest case against, what breaks if it's wrong. No separate agent.
- The master marks each decided item in the side chat's file with its verdict and date, so a later fold-in never reviews or applies it twice.
- Item letters are fixed for the life of a line; reworked items keep theirs, new ones continue after the highest used.
- A new handoff carries tossed items into "Don't redo", so they can't come back after a receipt is overwritten.
- Without a Project or folder, every change is a new post and the newest counts, so statuses, returns and receipts work there too.
- Claude works out chat titles (line plus number) and tells the user what to name each chat, since it can't see them.
- Cold-read check before saving a handoff.
- Commands trigger only as the whole message, not inside ordinary sentences.

## 0.1.0 (October 9, 2026)

First version, in testing.

- Commands: `handoff`, `handoff?`, `pickup <name>`, `pickup`, `handoffs`.
- Pickup continues a chat when typed as the first message of a new chat, and folds it in when typed in a chat already underway.
- Fold-in review: one verdict per item (keep, change, toss or return), nothing applied until the user decides, independent review for high-stakes items.
- Returns written back to the side chat's file; folded files cut down to a receipt.
- Optional per-project rules file, with defaults when it is missing.
- Works in claude.ai Projects, in folders (Claude Code), and in plain chats through past-chat search.
