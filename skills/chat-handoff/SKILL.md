---
name: chat-handoff
description: "Carries a chat's work into a new chat, or folds a side chat's work into a master chat after review. Use when the user's message is a handoff command, in any case: handoff (with or without a name), handoff?, pickup (with or without a chat name), fold (with a chat name), handoffs, or the dot-prefixed forms .push, .push?, .pull, .merge and .status. Also when the user plainly asks to hand off, pick up or fold in a chat's work. Not when these words appear inside an ordinary sentence, such as picking up the kids or a handoff to another team."
---

# Chat handoff

Long chats get slow and use up limits faster. This skill lets the user end a chat and carry its work into a fresh one, or fold a side chat's work into a master chat after a review.

## Commands

Two sets of words do the same things; the user can use either.

| Plain words | Dot style | What happens |
|---|---|---|
| `handoff` | `.push` | Save this chat's handoff file. If the chat has no line name yet, ask for one first, with a suggestion |
| `handoff <name>` | `.push <name>` | Save it under that name. A name different from this chat's line renames it (see "Renaming") |
| `handoff?` | `.push?` | One line: is this a good time to hand off? |
| `pickup <name>` | `.pull <name>` | Continue that chat's work in this chat (normally the first message of a new chat) |
| `fold <name>` | `.merge <name>` | Review that chat's work and fold it into this chat, the master, once the user decides |
| `pickup` | `.pull` | In a chat with work returned to it: start on the returns. Anywhere else: list what is waiting and ask |
| `handoffs` | `.status` | List every handoff and its status |

- A command is the user's whole message, or nearly (`handoff please`, `fold budget`), and case doesn't matter: `.Push` and `Handoff` count. A plain request ("let's hand this off") counts too. Inside an ordinary sentence these are ordinary words: carry on without this skill.
- The dot-style words always carry the dot, so they're never mistaken for git commands: `.push` is a handoff, `push` alone is not.
- When telling the user what to type next, use the style they just used.

Replies stay short, bottom line first.

## Where files live

| Where the chat runs | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files, `claude/Handoff - <line>.md`, through the Projects tool | `claude/Handoff rules.md` |
| A working folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted in the chat (see "Without a file store") | None: the defaults apply |

Several chats may run at once, so a chat writes only its own line's file. The one exception: a master marking items, setting the status or writing a receipt in a file it is folding in.

**The line** is the chat's working name: one or two words, without any status word or chat number (for example "research", "budget"). Take it from `handoff <name>`, from the pickup or fold that started this chat, or from an earlier handoff in it. Otherwise, the first time a command needs it, ask once, in one line, with a short name drawn from the chat's topic ("Name this line 'budget'? Reply yes or give another."), and use the answer. Never pick a name silently. Names match loosely, so one distinctive word finds the file later.

**Renaming.** `handoff <name>` with a name other than this chat's line is a rename, and no trace of the old name stays behind:

1. Save the file under the new name, with its `# Handoff:` line changed to match.
2. Only after that save succeeds, delete the old file (in a Project, `project_delete`; in a folder, remove it). Never delete first.
3. Say so in the reply: "Renamed from <old> to <new>", with the chat's new title.

Rename only this chat's own line. If the old file's status shows another chat already has it (`continuing in` or `folded into`), ask first, since that chat knows it by the old name. Without a file store, an earlier post can't be removed, so the new post's heading adds "(renamed from <old>)".

**Chat titles.** Claude can't see or rename chats, so work out each title and tell the user what to rename a chat to whenever its state changes. The status word comes first, so it still shows when the sidebar cuts a long title off. Use the rules file's titles if it sets them; otherwise:

| Title | The chat is | Given by |
|---|---|---|
| `<line> N` | Working | `pickup` when it continues; the master, when a side chat's topic stays open |
| `Master - <line> N` | The master | The master, the first time it folds something in |
| `Handed off - <line> N` | Waiting for the master | `handoff`, when folding in |
| `Continued - <line> N` | Moved on to `<line> N+1` | `handoff` when continuing, and `pickup` in the new chat |
| `Returned - <line> N` | Has work sent back to it | The master |
| `Folded - <line> N` | Finished, folded into the master | The master |
| `Released - <line> N` | Finished: its work went out | The last master in a chain, once everything is settled |

The first chat on a line is 1. A chat started by `pickup` takes the next number after the chat it continues, and a master's next chat keeps the `Master` prefix.

**Item letters.** Items to fold in are lettered A, B, C. A letter belongs to one item for the life of a line: a reworked item keeps its letter, and new items continue after the highest letter already used (in the items, the "Don't redo" list or the receipt). Never reuse a letter.

Big work products (proposal lists, analyses, specs) stay in their own files. The handoff points to them and never copies them.

### Without a file store

A chat can't change an earlier chat's messages, so here every write is a post. Wherever this skill says to save the file, set its status, mark items or write a receipt, post the line's whole file as it now stands at the end of the reply, under the heading `HANDOFF: <line>, <date>`.

`pickup`, `fold` and `handoffs` find these posts with past-chat search (query `HANDOFF <line>`) and use the newest one for each line: the latest date, or, on the same date, the one from the more recent chat. If past-chat search is off or finds nothing, say so and ask the user to paste the handoff.

## The rules file (optional, one per project)

Project-specific rules live in the rules file, not in this skill. Read it, if it exists, before writing a handoff, picking one up or folding one in. When it is missing, use the defaults below.

```
# Handoff rules
## Fold-ins
Which lines fold into which (chains are fine: research into report, report into review), and any files only one chat may write.
## Where approved items go
For each receiving line, the file and the format items take there.
## Review checks
What the master checks on every incoming item.
## Deep review triggers
What counts as high-stakes in this project.
## Chat titles
The title for each state, if not the defaults.
## Never
Work no handoff may start.
```

**Defaults:** any chat already underway can be the master; approved items go into that chat's own working files or open list; deep review covers anything high-stakes or hard to reverse; chats are titled as in the table above.

## `handoff` (`.push`)

1. Settle the line (see "The line" and "Renaming"). Read the rules file, and the line's current file if one exists. From it, carry forward:
   - items not yet settled, with their letters (a reworked item drops its Returned mark);
   - every tossed or rejected item, into "Don't redo" with its reason, so it doesn't come back;
   - settled items as one "Don't redo" line, for example "A changed and B kept, into the report draft, September 12, 2026".
2. Write in-flight state only, about 400 words at most. Drop empty sections.

```
# Handoff: <line>
Status: waiting for pickup
From: <this chat's title>, <date>
Built on: <the files this work rests on, with versions and dates>

## Where it stands
Two to four bullets.

## Ready to fold in
Lettered items, one line each, pointing to the file and section that hold the detail.

## Decided here, not yet recorded elsewhere
Each with its date and the user's own wording.

## Open
Waiting on the user; waiting on others.

## Next step
The first thing the next chat does.

## Read first
Exact file names.

## Don't redo
Anything checked, rejected, tossed or settled, one line each, with the reason.
```

3. Leave out background, history and reasoning already recorded in project files or memory.
4. **Cold read.** Before saving, read the draft as a fresh chat would, with only this file and its "Read first" files. Could it take the next step without asking anything? If not, add what's missing, within the length limit.
5. Save it. In a Project, `project_write` overwrites the line's file, with `present_to_user: true`. For a rename, delete the old file now (see "Renaming").
6. Tell the user, in four lines or fewer: saved (and renamed from what, if it was a rename); what to type next, in the style they used (`pickup <line>` or `.pull <line>` as the first message of a new chat to continue; `fold <line>` or `.merge <line>` in the master to fold it in); and the titles. If continuing, name the new chat `<line> N+1` and rename this one `Continued - <line> N`. If folding in, rename this one `Handed off - <line> N`.

## `handoff?` (`.push?`)

One line. **Yes** when the chat is at a stopping point (a deliverable finished, a question settled, a new topic about to start) or has grown long and heavy (big files, long runs, a lot of back and forth). **Not yet** when a handoff would split a piece of work in half: say what to finish first.

## Finding a handoff by name

For `pickup <name>`, `fold <name>` and their dot forms: match the name loosely against handoff file names (without a file store, against past-chat search); one distinctive word is enough. If two match, ask which. If no handoff file matches but another file clearly holds handed-off work (one written before this skill, for example), use it as the handoff and treat its proposals as the items. If the status says the line is already continuing in another chat, say so and ask before taking it over.

`pickup <name>` always continues and `fold <name>` always folds in; never guess between them.

- `pickup <name>` in a chat that already has work of its own: ask in one line which was meant.
- `fold <name>` as the first message of a new chat: if the rules file says which line that one folds into, this chat is that line (a fresh review chat, for example): say so in the first line and go ahead. Otherwise ask in one line which was meant.
- If the rules file says the line folds into a different line than this chat's, say so and ask before folding in.

## Continue: `pickup <name>` (`.pull <name>`)

1. Read the handoff and its "Read first" files. Don't read the old chat unless something needed is missing.
2. If newer versions of the "Built on" files exist, say so.
3. Set the status to `continuing in <this chat's title>, <date>`.
4. Reply in five lines or fewer: what is picked up, anything stale, the titles (this chat `<line> N+1`; the old one `Continued - <line> N`, if not renamed already), and the next step. If the status was `returned`, the next step is the returned items. Then do the next step, unless it needs the user.

## Fold in: `fold <name>` (`.merge <name>`)

This chat is the master: a second set of eyes on work it did not build. The side chat's conclusions are claims to test, not facts. Scrutinize; don't rubber-stamp.

1. **Read** the handoff and the files it points to. Review only items without a verdict mark; marked items are already settled.
2. **Review every unmarked item:** check numbers against the current sources and rerun the math where figures matter; look for conflicts with settled decisions or other parts of the work; flag anything missing, or stale against "Built on"; apply the rules file's review checks.
3. **Deep review** for items that hit the rules file's triggers, or that are high-stakes or hard to reverse. Do a second, harder pass yourself: work the figures out again from the source files, not from the handoff; make the strongest case against the item; ask what breaks, and for whom, if it's wrong. Tag these verdicts "(deep review)".
4. **One verdict per item, one line each:** Keep; Change (to what); Toss (why); or Return (what the side chat must do, when it needs real work such as new research). Then stop and discuss. Nothing is applied until the user decides, usually in one line ("keep A to H, change C, toss I").
5. **Apply what the user approved** where the rules file says approved items go (re-read that file right before saving, in case another chat changed it), and make the agreed changes.
6. **Mark each decided item** in the side chat's file, in place, with its verdict and date, so no later fold-in reviews it twice:

```
B. UK: $180M a year (Market sizing v3, section 3). Kept, September 12, 2026, into the draft, section 2.
C. Australia: $140M a year (Market sizing v3, section 4). Returned, September 12, 2026: rests on one 2021 survey; find a current source.
D. EU: $600M a year (Market sizing v3, section 5). Tossed, September 12, 2026: Board brief v2 drops the EU.
```

7. **Open items:** small ones join this chat's open list.
8. **Set the side chat's status:**
   - Any item returned: `Status: returned from <this chat's title>, <date>`. Tell the user to rename the side chat `Returned - <line> N` and type `pickup` in it, or `pickup <line>` as the first message of a new chat.
   - Nothing returned, but a whole topic still open: `Status: continuing in <side chat's title>, <date>`. The side chat goes back to `<line> N`.
   - Everything settled: cut the file down to a receipt, and tell the user to rename the side chat `Folded - <line> N`. Tossed items stay in the receipt with their reason, so they don't come back.

```
# Handoff: <line>
Status: folded into <master chat's title>, <date>
Kept: A, B, D (to <where>). Changed: C (<how>). Tossed: I (<why>).
```

   The first time this chat folds something in, also tell the user to rename it `Master - <line> N`.

9. **Released:** if this chat folds into no other line (per the rules file, or because the user says it's the end) and nothing is waiting, returned or open, say the work is complete and where it is. Tell the user to rename this chat `Released - <line> N` once it goes out. If this line has a handoff file, set its status to `released, <date>`.

## `pickup` with no name (`.pull`)

If this chat's line has a file with status `returned`, start on the items marked Returned. Rework each under its own letter. When they are done, `handoff` again so the master can fold them in. Otherwise list the handoffs waiting for pickup and ask which.

## `handoffs` (`.status`)

List each handoff file (not the rules file): line, status, date, and one line on what it holds. Build the list from the handoff files themselves (without a file store, from the newest post for each line). Never keep a shared tracker file: several chats would overwrite it.
