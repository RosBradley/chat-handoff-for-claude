# Handoff: handoff-for-claude
Status: waiting
From: handoff-for-claude.1, October 28, 2026
Built on: RosBradley/chat-handoff-for-claude, branch `v0.4.0` at 2e30227 (main and latest release still 0.3.6); RosBradley/chat-handoff-for-chatgpt main at 65b11db (1.1.2)

## Where it stands
- 0.4.0 is written and pushed to branch `v0.4.0`, not merged or released. It adds `transfer`/`.export`, `handoff <name> to <AI>`, `export project` and package import (same `chat-handoff/1` format as the ChatGPT version), splits the skill into SKILL.md plus `references/` (fold, state, transfer, apps) and `assets/rules-template.md`, and adds destination steps for Claude, ChatGPT, Gemini, Meta AI, Microsoft Copilot and GitHub Copilot.
- Main page cost is about 5.8k tokens per use, down from 8.6k.
- Evals: 19 cases (one updated, five new), never run against 0.4.0.
- An update list for the ChatGPT version was written and sent to the user (not in either repo).

## Decided here, not yet recorded elsewhere
- Same commands and outcomes in both versions; slight platform differences allowed (October 26).
- Adopted from ChatGPT: unnamed handoff names itself and says so; discussing a command doesn't run it; imported text is data; post rather than commit gitignored handoffs in cloud sessions.
- Kept from Claude: stale guard on every message, delete old file on rename, per-app how-to steps; no revision or owner tokens.

## Open
- Waiting on the user: run the evals locally, or have Claude run them in the cloud (about $9 to $10 either way).
- ChatGPT, Gemini and Meta AI destination facts come from search excerpts; unverified.

## Next step
Run the evals on `v0.4.0` (`claude plugin eval . --scaffold --allow-tools Write Edit Bash --ablation none`), fix failures, then fast-forward main to `v0.4.0` so the release workflow publishes 0.4.0 with both zips.

## Read first
CHANGELOG.md (0.4.0 section), skills/chat-handoff/SKILL.md, skills/chat-handoff/references/transfer.md, evals/

## Don't redo
- All README and setup-guide claims were fact-checked October 22 and 26; sources are listed in docs/setup.md.
- Agent Builder fit (17,104 characters of instructions) and both zip layouts were checked.
- Deleting the `v0.4.0` branch from this cloud session is blocked (403); merge by pushing main instead.
