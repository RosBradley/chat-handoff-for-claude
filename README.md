# Chat Handoff for Claude

A skill for Claude that carries work from one chat to the next. The skill itself is named `chat-handoff`.

Long chats get slow and use up your limits faster, because every message re-sends the whole conversation. Starting a fresh chat fixes that, but you lose the thread. This skill keeps the thread: one word saves where things stand, and one word picks it up in a new chat.

It also handles a second pattern: several side chats feeding one master chat. The master doesn't just accept what comes in. It reviews every item as a second set of eyes, gives a verdict, and waits for you to decide.

**Status:** v0.1.0, in testing.

## Commands

| Type | What happens |
|---|---|
| `handoff` | Saves this chat's handoff file |
| `handoff?` | One line: is this a good time to hand off? |
| `pickup <name>` | As the first message of a new chat: continues that chat. In a chat already underway: folds that chat's work in, after review |
| `pickup` | In a chat with work pushed back to it: starts on the returns. Anywhere else: lists what is waiting and asks |
| `handoffs` | Lists every handoff and its status |

Names match loosely: `pickup budget` finds "Handoff - budget review.md". If two match, Claude asks which. A command works only as the whole message (or nearly), so "I'll pick up the kids" won't set it off.

## How it works

### Continue in a fresh chat

1. In the long chat, type `handoff`. Claude saves a short file (about 400 words at most) with only the work in progress: where it stands, decisions not yet recorded elsewhere, what's open, the next step, which files to read, and what not to redo.
2. Start a new chat and type `pickup <name>`. Claude reads the file, flags anything that has changed since, and starts on the next step.

### Fold a side chat into a master chat

1. In the side chat, type `handoff`.
2. In the master chat, type `pickup <name>`. The master reviews every incoming item: it checks the numbers, looks for conflicts with decisions already made, and flags anything missing or out of date. High-stakes items get a second, harder pass: the master works the figures out again from the sources and makes the strongest case against them.
3. You get one verdict per item:
   ```
   A. Launch budget: Keep
   B. Ad spend $12,000: Change, use the Q3 rate ($13,500)
   C. Second landing page: Toss, duplicates the pricing page
   D. Competitor pricing: Return, needs fresh research
   ```
4. You decide, usually in one line: "keep A, change B, toss C, return D."
5. Only then does the master apply anything. It marks each item in the side chat's file with its verdict, so nothing gets reviewed twice. Returned items go back to the side chat: type `pickup` there, or `pickup <name>` as the first message of a new chat. Once everything is settled, the side chat's file shrinks to a short receipt, and tossed items stay in it with their reason so they don't come back.

## Where the files live

| Where you work | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files: `claude/Handoff - <name>.md` | `claude/Handoff rules.md` |
| A folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <name>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted at the end of the chat's reply. Each later change is a new post, and the newest one counts; found again with past-chat search | None |

Each chat writes only its own file, so chats running at the same time can't overwrite each other.

## Project rules (optional)

Each project can have a rules file that says which chat is the master, where approved items go, what the master checks, what counts as high-stakes, how chats are titled, and what a handoff must never start. Without one, sensible defaults apply.

- Template, with a worked example in every section: [templates/handoff-rules.md](templates/handoff-rules.md)
- Example handoff file from the same project: [examples/handoff.md](examples/handoff.md)

## Install

### claude.ai (web, desktop and mobile)

1. Zip the skill folder itself, so the archive's top level is `chat-handoff/`:
   ```bash
   cd skills
   zip -r chat-handoff.zip chat-handoff/
   ```
2. Upload `chat-handoff.zip` and turn it on under **Customize > Skills**.

### Claude Code

Copy the skill folder to `~/.claude/skills/chat-handoff/` (all your projects) or `.claude/skills/chat-handoff/` (one repository). Then type `handoff`, or run it directly with `/chat-handoff`.

## Optional: a nudge

Claude can suggest a handoff on its own at natural stopping points. Add this to **Settings > Instructions for Claude** (or to `CLAUDE.md` in Claude Code):

> In long chats, at natural stopping points (a deliverable finished, a question settled, a long stretch of file work), suggest typing "handoff" in one short line at the end of the reply. Don't repeat it if I ignore it.

## Limits

- Claude can't see, close or rename chats. It tells you what to name each one (`budget 2` while open, `Done - budget 2` when finished, unless your rules file says otherwise).
- Claude can't see how full a chat is or how much usage you have left, so `handoff?` is a judgment call, not a meter.
- Chats in different claude.ai Projects can't see each other's files. Hand off within a project.
- Without a Project or folder, `pickup` depends on past-chat search (it must be on in your claude.ai settings) finding the handoff. If it doesn't, Claude asks you to paste it.

## License

MIT. See [LICENSE](LICENSE).
