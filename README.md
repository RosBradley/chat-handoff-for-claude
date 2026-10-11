# Chat Handoff for Claude

A skill for Claude that carries work from one chat to the next. The skill itself is named `chat-handoff`.

Long chats get slow and use up your limits faster, because every message re-sends the whole conversation. Starting a fresh chat fixes that, but you lose the thread. This skill keeps the thread: one word saves where things stand, and one word picks it up in a new chat.

It also handles a second pattern: several side chats feeding one master chat. The master doesn't just accept what comes in. It reviews every item as a second set of eyes, gives a verdict, and waits for you to decide. Chains work too: research chats feed a report chat, and the report feeds a fresh review chat that reads it the way your audience will.

**Status:** v0.2.0, in testing.

## Commands

Use plain words or the dot style, whichever you like:

| Plain words | Dot style | What happens |
|---|---|---|
| `handoff` | `.push` | Saves this chat's handoff file. The first time, Claude suggests a short name for it |
| `handoff <name>` | `.push <name>` | Saves it under that name, or renames it |
| `handoff?` | `.push?` | One line: is this a good time to hand off? |
| `pickup <name>` | `.pull <name>` | Continues that chat's work here, usually as the first message of a new chat |
| `fold <name>` | `.merge <name>` | Reviews that chat's work and folds it into this one, once you decide |
| `pickup` | `.pull` | In a chat with work sent back to it: starts on the returns. Anywhere else: lists what is waiting and asks |
| `handoffs` | `.status` | Lists every handoff and its status |

- Names match loosely: `pickup budget` finds "Handoff - budget review.md". If two match, Claude asks which.
- A command works as the whole message (or nearly), in any case, so `.Push` from a phone counts and "I'll pick up the kids" doesn't.
- The dot keeps the git-style words from being mistaken for real git commands: `.push` is a handoff, `push` is not.
- Renaming with `handoff <new name>` saves the new file first, then deletes the old one, so nothing is left under the old name.

## How it works

### Continue in a fresh chat

1. In the long chat, type `handoff`. Claude saves a short file (about 400 words at most) with only the work in progress: where it stands, decisions not yet recorded elsewhere, what's open, the next step, which files to read, and what not to redo.
2. Start a new chat and type `pickup <name>`. Claude reads the file, flags anything that has changed since, and starts on the next step.

### Fold a side chat into a master chat

1. In the side chat, type `handoff`.
2. In the master chat, type `fold <name>`. The master reviews every incoming item: it checks the numbers, looks for conflicts with decisions already made, and flags anything missing or out of date. High-stakes items get a second, harder pass: the master works the figures out again from the sources and makes the strongest case against them.
3. You get one verdict per item:
   ```
   A. Canada, $310M a year: Change to $250M; compliance and OT security overlap, counted twice
   B. UK, $180M a year: Keep
   C. Australia, $140M a year: Return, rests on one 2021 survey; find a current source
   D. EU, $600M a year: Toss, the newer board brief drops the EU
   ```
4. You decide, usually in one line: "change A, keep B, return C, toss D."
5. Only then does the master apply anything. It marks each item in the side chat's file with its verdict, so nothing gets reviewed twice. Returned items go back to the side chat: type `pickup` there, or `pickup <name>` as the first message of a new chat. Once everything is settled, the side chat's file shrinks to a short receipt, and tossed items stay in it with their reason so they don't come back.

## Chat titles

Claude can't see or rename chats, so whenever a chat's state changes it tells you what to rename it to. The status comes first, so you can read it in the sidebar even when a long title is cut off:

| Title | The chat is |
|---|---|
| `market size 3` | Working |
| `Master - report 2` | The master chat |
| `Handed off - market size 3` | Waiting for the master |
| `Continued - market size 2` | Moved on to `market size 3` |
| `Returned - market size 3` | Has work sent back to it |
| `Folded - market size 3` | Finished, folded into the master |
| `Released - review 1` | Finished: the work went out (sent, published, shipped) |

The number goes up by one each time a chat continues in a new one. A rules file can set different titles.

## Where the files live

| Where you work | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files: `claude/Handoff - <name>.md` | `claude/Handoff rules.md` |
| A folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <name>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted at the end of the chat's reply. Each later change is a new post, and the newest one counts; found again with past-chat search | None |

Each chat writes only its own file, so chats running at the same time can't overwrite each other.

## Project rules (optional)

Each project can have a rules file that says which chats fold into which, where approved items go, what the master checks, what counts as high-stakes, how chats are titled, and what a handoff must never start. Without one, sensible defaults apply.

- Template, with a worked example in every section: [templates/handoff-rules.md](templates/handoff-rules.md)

## Worked example

[examples/README.md](examples/README.md) follows one project from start to finish: a firm that does NERC CIP compliance and OT cybersecurity for utilities, deciding which countries to expand into. Four research chats feed a report chat, and the report goes to a fresh reviewer. It shows a long chat continuing in a new one, a double count caught at fold-in, work sent back, a receipt, and the handoff files at each stage.

## Install

### claude.ai (web, desktop and mobile)

1. Zip the skill folder itself, so the archive's top level is `chat-handoff/`:
   ```bash
   cd skills
   zip -r chat-handoff.zip chat-handoff/
   ```
2. Upload `chat-handoff.zip` and turn it on under **Customize > Skills**.

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

- Claude can't see, close or rename chats. It tells you what to rename each one (see Chat titles).
- Claude can't see how full a chat is or how much usage you have left, so `handoff?` is a judgment call, not a meter.
- Chats in different claude.ai Projects can't see each other's files. Hand off within a project.
- Without a Project or folder, `pickup` depends on past-chat search (it must be on in your claude.ai settings) finding the handoff. If it doesn't, Claude asks you to paste it.

## License

MIT. See [LICENSE](LICENSE).
