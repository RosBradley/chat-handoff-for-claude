# Changelog

## 0.3.0 (in testing)

- Stale chat guard: an ordinary instruction typed into a chat that was already handed off or folded in gets a warning first, with Stop (recommended), Continue here once, and Reopen this chat as the choices, shown as buttons where the app can. Handoff commands still run in such a chat, and every `handoff` reply says the guard is on.
- New opening in the README: why long chats cost more (Claude re-reads the whole chat with every message, so usage limits, API cost and speed all suffer, and near the length limit the app summarizes older messages or stops the chat), what the skill does (it doesn't move or copy a chat), and how it saves, with sources. The skill opens with a two-sentence summary instead, since Claude reads the skill with every command.
- Named Chat Handoff; the skill's ID stays `chat-handoff`. The docs say "the skill" wherever the skill does the work, and "Claude" only for what Claude itself does or can't do.
- Chats are named by line, with an optional tag of the user's own: `budget` or `budget.pre`. A line is one word (letters, digits or hyphens). The tag is anything the user likes (a word, a letter, a number) and is never invented or asked for by the skill; order between chats on a line comes from the dates in the file. Earlier 0.3.0 builds numbered chats (`budget.3`) and asked for the number when unsure; that is gone, and an old `From: budget.3` line is read as a tag.
- Names typed with spaces are joined with hyphens (`handoff market size` saves `market-size`), and the reply says what the name became. On an existing line, the last word is read as the tag (`market size au` on the `market-size` line is `market-size.au`). The README now says names have no spaces.
- Titles start with a state word and follow the commands you use: `todo`, `handedoff` (`pushed` after dot-style commands), `returned`, `folded` (`merged` after `.merge`) and `done`. Every title is offered as optional. `Continued -` and `Handed off -` both become `handedoff`; `Returned -`, `Folded -` and `Released -` become `returned`, `folded` and `done`; `Master -` is dropped, since a master is simply `todo` while it works.
- A new handoff's status is `waiting` (older files saying `waiting for pickup` still work). Receipts say `folded into` or `merged into`, matching the fold command, and the end of a chain is `done` (was `released`).
- The "From" line carries the chat's name (`From: budget.pre`). Without a Project or folder, posts are headed `HANDOFF: budget.pre, <date>`, naming the chat that last handed the line off, even when a master posts the file. The newest is the one with the latest date, then the more recent chat.
- Only a different line renames: `handoff budget.post` in `budget.pre` just changes the tag. A rename keeps the chat's tag (`handoff budget` in `research.pre` makes it `budget.pre`).
- `handoffs` shows each line's latest chat.
- The skill and plugin descriptions say the skill reviews a side chat's work item by item and folds in what the user approves.
- The rules template and the worked example use the new names and titles (`market-size.au`, `folded.market-size.au`).
- claude.ai users download `chat-handoff.zip` from the latest GitHub release instead of zipping the folder themselves. A new version in `plugin.json` publishes its release automatically.
- Upgrading from 0.2.0: older handoff files still work. A line named with two words (`Handoff - market size.md`) can move to one word with `handoff market-size` in its chat, which saves the new file and deletes the old one.

## 0.2.0 (October 10, 2026)

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
