---
name: chat-handoff
description: "Carries a chat's work into a new chat, or folds a side chat's work into a master chat after review. Use when the user's message is one of these commands, alone or with a word or two around it: handoff, handoff?, pickup, pickup <chat name>, or handoffs. Not when these words appear inside an ordinary sentence, such as picking up the kids or a handoff to another team."
---

# Chat handoff

Long chats get slow and use up limits faster. This skill lets the user end a chat and carry its work into a fresh one, or fold a side chat's work into a master chat after a review. These commands do all of it:

| The user types | What happens |
|---|---|
| `handoff` | Save this chat's handoff file |
| `handoff?` | One line: is this a good time to hand off? |
| `pickup <name>` | As the first message of a new chat: continue that chat. In a chat already underway: fold that chat's work in, after review |
| `pickup` | In a chat with work returned to it: start on the returns. Anywhere else: list what is waiting and ask |
| `handoffs` | List every handoff and its status |

A command counts only as the user's whole message, or nearly (`handoff please`, `pickup budget`). Inside an ordinary sentence these are ordinary words: carry on without this skill.

Replies stay short, bottom line first.

## Where files live

| Where the chat runs | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files, `claude/Handoff - <line>.md`, through the Projects tool | `claude/Handoff rules.md` |
| A working folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted in the chat (see "Without a file store") | None: the defaults apply |

Several chats may run at once, so a chat writes only its own line's file. The one exception: a master marking items, setting the status or writing a receipt in a file it is folding in.

**The line** is the chat's working name, without any status word or chat number (for example "planning", "research", "budget"). Take it from the pickup that started this chat or an earlier handoff in it. Otherwise ask the user once, in one line.

**Chat titles.** Claude can't see or change chat titles, so work them out and tell the user what to name each chat. A title is the line plus the chat's number, in the rules file's format, or by default `<line> N` while open and `Done - <line> N` when finished. The first chat on a line is 1. A chat started by `pickup` takes the next number after the chat it continues.

**Item letters.** Items to fold in are lettered A, B, C. A letter belongs to one item for the life of a line: a reworked item keeps its letter, and new items continue after the highest letter already used (in the items, the "Don't redo" list or the receipt). Never reuse a letter.

Big work products (proposal lists, analyses, specs) stay in their own files. The handoff points to them and never copies them.

### Without a file store

A chat can't change an earlier chat's messages, so here every write is a post. Wherever this skill says to save the file, set its status, mark items or write a receipt, post the line's whole file as it now stands at the end of the reply, under the heading `HANDOFF: <line>, <date>`.

`pickup` and `handoffs` find these posts with past-chat search (query `HANDOFF <line>`) and use the newest one for each line: the latest date, or, on the same date, the one from the more recent chat. If past-chat search is off or finds nothing, say so and ask the user to paste the handoff.

## The rules file (optional, one per project)

Project-specific rules live in the rules file, not in this skill. Read it, if it exists, before writing a handoff, picking one up or folding one in. When it is missing, use the defaults below.

```
# Handoff rules
## Master chat
The line that receives fold-ins, and any files only it may write.
## Where approved items go
The file, and the format items take there.
## Review checks
What the master checks on every incoming item.
## Deep review triggers
What counts as high-stakes in this project.
## Chat titles
The naming convention for open and finished chats.
## Never
Work no handoff may start.
```

**Defaults:** any chat already underway can be the master; approved items go into that chat's own working files or open list; deep review covers anything high-stakes or hard to reverse; chats are titled `<line> N` while open and `Done - <line> N` when finished.

## `handoff`

1. Read the rules file, and the line's current file if one exists. From it, carry forward:
   - items not yet settled, with their letters (a reworked item drops its Returned mark);
   - every tossed or rejected item, into "Don't redo" with its reason, so it doesn't come back;
   - settled items as one "Don't redo" line, for example "A, B kept and C changed, into the launch plan, October 10, 2026".
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
5. Save it. In a Project, `project_write` overwrites the line's file, with `present_to_user: true`.
6. Tell the user, in four lines or fewer: saved; what to type (`pickup <line>` as the first message of a new chat to continue, or in the master chat to fold it in); and the titles. If continuing, name the new chat `<line> N+1` and this one `Done - <line> N`. If folding in, the master gives this chat's finished title once everything is settled.

## `handoff?`

One line. **Yes** when the chat is at a stopping point (a deliverable finished, a question settled, a new topic about to start) or has grown long and heavy (big files, long runs, a lot of back and forth). **Not yet** when a handoff would split a piece of work in half: say what to finish first.

## `pickup <name>`: finding the handoff

Match the name loosely against handoff file names (without a file store, against past-chat search). If two match, ask which. If no handoff file matches but another file clearly holds handed-off work (one written before this skill, for example), use it as the handoff and treat its proposals as the items. If the status says the line is already continuing in another chat, say so and ask before taking it over.

As the first message of a new chat, `pickup <name>` continues. In a chat that already has work of its own, it folds in. If the rules file names a different chat as master, say so and ask before folding in. If it is unclear which, ask in one line.

## Continue (first message of a new chat)

1. Read the handoff and its "Read first" files. Don't read the old chat unless something needed is missing.
2. If newer versions of the "Built on" files exist, say so.
3. Set the status to `continuing in <this chat's title>, <date>`.
4. Reply in five lines or fewer: what is picked up, anything stale, the title for this chat, and the next step. If the status was `returned`, the next step is the returned items. Then do the next step, unless it needs the user.

## Fold in (a chat already underway)

This chat is the master: a second set of eyes on work it did not build. The side chat's conclusions are claims to test, not facts. Scrutinize; don't rubber-stamp.

1. **Read** the handoff and the files it points to. Review only items without a verdict mark; marked items are already settled.
2. **Review every unmarked item:** check numbers against the current sources and rerun the math where figures matter; look for conflicts with settled decisions or other parts of the work; flag anything missing, or stale against "Built on"; apply the rules file's review checks.
3. **Deep review** for items that hit the rules file's triggers, or that are high-stakes or hard to reverse. Do a second, harder pass yourself: work the figures out again from the source files, not from the handoff; make the strongest case against the item; ask what breaks, and for whom, if it's wrong. Tag these verdicts "(deep review)".
4. **One verdict per item, one line each:** Keep; Change (to what); Toss (why); or Return (what the side chat must do, when it needs real work such as new research). Then stop and discuss. Nothing is applied until the user decides, usually in one line ("keep A to H, change C, toss I").
5. **Apply what the user approved** where the rules file says approved items go (re-read that file right before saving, in case another chat changed it), and make the agreed changes.
6. **Mark each decided item** in the side chat's file, in place, with its verdict and date, so no later fold-in reviews it twice:

```
A. Tier prices (Pricing proposal v1, section 2). Kept, October 10, 2026, into the launch plan.
C. Second landing page. Tossed, October 10, 2026: duplicates the pricing page.
D. Competitor pricing. Returned, October 10, 2026: redo with current prices.
```

7. **Open items:** small ones join this chat's open list.
8. **Set the side chat's status:**
   - Any item returned: `Status: returned from <this chat's title>, <date>`. Tell the user to type `pickup` in the side chat, or `pickup <line>` as the first message of a new chat.
   - Nothing returned, but a whole topic still open: `Status: continuing in <side chat's title>, <date>`.
   - Everything settled: cut the file down to a receipt, and give the user the side chat's finished title. Tossed items stay in the receipt with their reason, so they don't come back.

```
# Handoff: <line>
Status: folded into <master chat's title>, <date>
Kept: A, B, D (to <where>). Changed: C (<how>). Tossed: I (<why>).
```

## `pickup` with no name

If this chat's line has a file with status `returned`, start on the items marked Returned. Rework each under its own letter. When they are done, `handoff` again so the master can pick them up. Otherwise list the handoffs waiting for pickup and ask which.

## `handoffs`

List each handoff file (not the rules file): line, status, date, and one line on what it holds. Build the list from the handoff files themselves (without a file store, from the newest post for each line). Never keep a shared tracker file: several chats would overwrite it.
