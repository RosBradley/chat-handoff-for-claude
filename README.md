# Chat Handoff for Claude

Chat Handoff is a skill for Claude that lets a new chat pick up where a long one left off. Its ID is `chat-handoff`.

## Why

Claude re-reads the entire chat every time you send a message. So the longer a chat runs, the more each new message costs, even a one-line "thanks":

- **Usage and dollars.** On a Claude plan, usage limits are based on the length of the whole chat, not just the number of messages, so a long chat uses up your limit faster. On the API, the full history is sent, and billed, with every request.
- **Speed.** Claude answers shorter chats faster.
- **Detail.** Near a chat's length limit, the app either summarizes older messages on its own, choosing what to keep, or stops the chat.

Starting a fresh chat avoids all three, but normally means explaining the work all over again. This skill removes that step.

## What it does

This skill doesn't move or copy a chat. It lets you pick up the conversation in a new chat, or fold a side chat's work into a main one, with short commands:

- **`handoff`**: the skill writes a short handoff file, about 400 words: where the work stands, what was decided, what is still open, the next step, and what not to redo.
- **`pickup <name>`**, as the first message of a new chat: the skill reads that file, and only the files it points to, and the new chat carries on from there.
- **`fold <name>`**, in a main (master) chat that side chats feed into: the skill reviews the side chat's work as an independent second reviewer. It rechecks the figures against the current sources, looks for gaps and for conflicts with what is already settled, and gives each item a verdict (keep, change, toss, or return to the side chat for more work). Nothing is folded in until you approve.

Chains work too: research chats feed a report chat, and the report feeds a fresh review chat that reads it the way your audience will.

**How it saves.** A chat picked up from a handoff carries the handoff and the files it opens, not the old chat's back-and-forth, so each message costs far less. For example, once a chat has grown to 150,000 tokens, every message makes Claude re-read all 150,000; the new chat starts from a 400-word handoff instead. Side chats do the same for a main chat: the heavy work happens elsewhere, and only the reviewed results come back. And what carries forward is a deliberate handoff (decisions, open items, next step, what not to redo), not an automatic summary.

Sources: Anthropic's help center, [How can I maximize my Claude Pro usage?](https://support.anthropic.com/en/articles/8325614-how-can-i-maximize-my-claude-pro-usage) ("Claude needs to re-read the entire conversation every time you send a message"), [Understanding usage and length limits](https://support.claude.com/en/articles/11647753-understanding-usage-and-length-limits) and [How large is the context window on paid Claude plans?](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans) ("Claude summarizes earlier messages to make room for new content"); the Claude API docs, [Working with messages](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) ("The Messages API is stateless").

**Status:** v0.3.0, in testing.

## Commands

Use plain words or the dot style, whichever you like:

| Plain words | Dot style | What happens |
|---|---|---|
| `handoff` | `.push` | Saves this chat's handoff file. If the chat has no name yet, the skill suggests one, like `budget.1` (see Chat names) |
| `handoff <name>` | `.push <name>` | Saves it under that name (`handoff budget.3`); a different line renames it |
| `handoff?` | `.push?` | One line: is this a good time to hand off? |
| `pickup <name>` | `.pull <name>` | Continues that chat's work here, usually as the first message of a new chat |
| `fold <name>` | `.merge <name>` | Reviews that chat's work item by item and folds in what you approve |
| `pickup` | `.pull` | In a chat with work sent back to it: starts on the returns. Anywhere else: lists what is waiting and asks |
| `handoffs` | `.status` | Lists every handoff and its status |

- Names match loosely: `pickup budget` and `pickup budget.3` both find "Handoff - budget.md". If two match, the skill asks which.
- A command works as the whole message (or nearly), in any case, so `.Push` from a phone counts and "I'll pick up the kids" doesn't.
- The dot keeps the git-style words from being mistaken for real git commands: `.push` is a handoff, `push` is not.
- A different line renames, and the chat keeps its number: `handoff <new line>` saves the new file first, then deletes the old one, so nothing is left under the old name. A different number on the same line (`handoff budget.4` in `budget.3`) only corrects the number.

## Chat names

Each chat's name is its line and its number, joined by a dot: `budget.3` is the third chat on the budget line.

- The line is one word: letters, digits or hyphens, like `research` or `market-size`. One handoff file per line serves every chat on it.
- A chat started by `pickup` takes the next number after the chat it continues.
- Claude can't see chat titles, so the number comes from your command or the handoff file, never a guess. If neither settles it, the skill asks once.

## How it works

### Continue in a fresh chat

1. In the long chat, type `handoff`. The skill saves a short file (about 400 words at most) with only the work in progress: where it stands, decisions not yet recorded elsewhere, what's open, the next step, which files to read, and what not to redo.
2. Start a new chat and type `pickup <name>`. The skill reads the file, flags anything that has changed since, and starts on the next step.

### Fold a side chat into a master chat

1. In the side chat, type `handoff`.
2. In the master chat, type `fold <name>`. The skill reviews every incoming item: it checks the numbers, looks for conflicts with decisions already made, and flags anything missing or out of date. High-stakes items get a second, harder pass: the figures are worked out again from the sources, and the strongest case against each one is made.
3. You get one verdict per item:
   ```
   A. Canada, $310M a year: Change to $250M; compliance and OT security overlap, counted twice
   B. UK, $180M a year: Keep
   C. Australia, $140M a year: Return, rests on one 2021 survey; find a current source
   D. EU, $600M a year: Toss, the newer board brief drops the EU
   ```
4. You decide, usually in one line: "change A, keep B, return C, toss D."
5. Only then is anything applied. The skill marks each item in the side chat's file with its verdict, so nothing gets reviewed twice. Returned items go back to the side chat: type `pickup` there, or `pickup <name>` as the first message of a new chat. Once everything is settled, the side chat's file shrinks to a short receipt, and tossed items stay in it with their reason so they don't come back.

## Chat titles

Claude can't see or rename chats, so whenever a chat's state changes, the skill suggests a new title for it. Renaming is optional: commands find handoff files by name, never by chat title.

A title is a state word, a dot and the chat's name. The state comes first, so you can read it in the sidebar even when a long title is cut off. The words follow the commands you use:

| The chat is | After plain words | After dot style |
|---|---|---|
| Working, a master included | `todo.market-size.2` | `todo.market-size.2` |
| Handed off: continuing in a new chat, or waiting for the master | `handedoff.market-size.2` | `pushed.market-size.2` |
| Has work sent back to it | `returned.market-size.2` | `returned.market-size.2` |
| Finished, folded into the master | `folded.market-size.2` | `merged.market-size.2` |
| Finished: its work went out (sent, published, shipped) | `done.review.1` | `done.review.1` |

If you stick to one command style, one search (`folded.`, say) finds every chat in that state. A rules file can set different titles.

## Where the files live

| Where you work | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files: `claude/Handoff - <line>.md` | `claude/Handoff rules.md` |
| A folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted at the end of the chat's reply. Each later change is a new post, and the newest one counts; found again with past-chat search | None |

Each chat writes only its own line's file (the one exception: a master marking items in a file it folds in), so chats running at the same time can't overwrite each other.

## Project rules (optional)

Each project can have a rules file that says which chats fold into which, where approved items go, what the master checks, what counts as high-stakes, how chats are titled, and what a handoff must never start. Without one, sensible defaults apply.

- Template, with a worked example in every section: [templates/handoff-rules.md](templates/handoff-rules.md)

## Worked example

[examples/README.md](examples/README.md) follows one project from start to finish: a firm that does NERC CIP compliance and OT cybersecurity for utilities, deciding which countries to expand into. Four research lines feed a report chat, and the report goes to a fresh reviewer. It shows a long chat continuing in a new one, a double count caught at fold-in, work sent back, a receipt, and the handoff files at each stage.

## Install

### claude.ai (web, desktop and mobile)

1. Download [chat-handoff.zip](https://github.com/RosBradley/chat-handoff-for-claude/releases/latest/download/chat-handoff.zip) from the [latest release](https://github.com/RosBradley/chat-handoff-for-claude/releases/latest).
2. Upload it and turn it on under **Customize > Skills**.

To build the zip yourself instead (for a version not yet released), zip the skill folder itself, so the archive's top level is `chat-handoff/`:

```bash
cd skills
zip -r chat-handoff.zip chat-handoff/
```

### Claude Code

Install it as a plugin, in one step:

```
/plugin install chat-handoff --marketplace RosBradley/chat-handoff-for-claude
```

On Claude Code older than 2.1.275, use two steps instead:

```
/plugin marketplace add RosBradley/chat-handoff-for-claude
/plugin install chat-handoff@chat-handoff-for-claude
```

Then type `handoff` (or `.push`), or run it directly with `/chat-handoff:chat-handoff`.

To install without the plugin system, copy `skills/chat-handoff/` to `~/.claude/skills/chat-handoff/` (all your projects) or `.claude/skills/chat-handoff/` (one repository).

If the skill is also turned on in your claude.ai account, Claude Code loads that copy too (as `anthropic-skills:chat-handoff`). Keep one of them on, so you know which version answers.

## Optional: a nudge

Claude can suggest a handoff on its own at natural stopping points. Add this to **Settings > Instructions for Claude** (or to `CLAUDE.md` in Claude Code):

> In long chats, at natural stopping points (a deliverable finished, a question settled, a long stretch of file work), suggest typing "handoff" in one short line at the end of the reply. Don't repeat it if I ignore it.

## Limits

- Claude can't see, close or rename chats. The skill suggests a title for each one, and renaming is optional (see Chat titles).
- Claude can't see how full a chat is or how much usage you have left, so `handoff?` is a judgment call, not a meter.
- Chats in different claude.ai Projects can't see each other's files. Hand off within a project.
- Without a Project or folder, `pickup` depends on past-chat search (it must be on in your claude.ai settings) finding the handoff. If it doesn't, the skill asks you to paste it.

## License

MIT. See [LICENSE](LICENSE).
