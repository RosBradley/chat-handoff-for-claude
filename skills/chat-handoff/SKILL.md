---
name: chat-handoff
description: Use when the user types handoff, handoff?, pickup (with or without a chat name), or handoffs, to carry a chat's work into a new chat or fold it into a master chat after review.
---

# Chat handoff

Long chats get slow and use up limits faster. This skill lets the user end a chat and carry its work into a fresh one, or fold a side chat's work into a master chat after a review. These commands do all of it:

| The user types | What happens |
|---|---|
| `handoff` | Save this chat's handoff file |
| `handoff?` | One line: is this a good time to hand off? |
| `pickup <name>` | As the first message of a new chat: continue that chat. In a chat already underway: fold that chat's work in, after review |
| `pickup` | In a chat with work pushed back to it: start on the returns. Anywhere else: list what is waiting and ask |
| `handoffs` | List every handoff and its status |

Replies stay short, bottom line first.

## Where files live

| Where the chat runs | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files, `claude/Handoff - <line>.md`, through the Projects tool | `claude/Handoff rules.md` |
| A working folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | The chat's final reply, under the heading `HANDOFF: <line>, <date>`. Pickup finds it with past-chat search (query `HANDOFF <line>`) | None: the defaults apply |

Several chats may run at once, so a chat writes only its own line's file. The one exception: a master writing a status, return or receipt into a file it is folding in. Without a shared file store, returns go to the user as text to paste into the side chat.

**The line** is the chat's working name, without any status word or chat number (for example "planning", "research", "budget"). Take it from the pickup that started this chat or an earlier handoff in it. Otherwise ask the user once, in one line.

Big work products (proposal lists, analyses, specs) stay in their own files. The handoff points to them and never copies them.

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

**Defaults:** any chat already underway can be the master; approved items go into that chat's own working files or open list; deep review covers anything high-stakes or hard to reverse; a finished chat gets "Done" added to the start of its title.

## `handoff`

1. Read the rules file, and the line's current file if one exists (to carry forward items still open and to get the chat number).
2. Write in-flight state only, about 400 words at most. Drop empty sections.

```
# Handoff: <line>
Status: waiting for pickup
From: <this chat's title>, <date>
Built on: <the files this work rests on, with versions and dates>

## Where it stands
Two to four bullets.

## Ready to fold in
Lettered items (A, B, C), one line each, pointing to the file and section that hold the detail.

## Decided here, not yet recorded elsewhere
Each with its date and the user's own wording.

## Open
Waiting on the user; waiting on others.

## Next step
The first thing the next chat does.

## Read first
Exact file names.

## Don't redo
Anything checked, rejected or settled, one line each.
```

3. Leave out background, history and reasoning already recorded in project files or memory.
4. Save it. In a Project, `project_write` overwrites the line's file, with `present_to_user: true`.
5. Tell the user in three lines: saved; the chat titles to use (from the rules file, or the default); and what to type: `pickup <line>`, as the first message of a new chat to continue, or in the master chat to fold it in.

## `handoff?`

One line. **Yes** when the chat is at a stopping point (a deliverable finished, a question settled, a new topic about to start) or has grown long and heavy (big files, long runs, a lot of back and forth). **Not yet** when a handoff would split a piece of work in half: say what to finish first.

## `pickup <name>`: finding the handoff

Match the name loosely against handoff file names (without a file store, against past-chat search). If two match, ask which. If no handoff file matches but another file clearly holds handed-off work (one written before this skill, for example), use it as the handoff and treat its proposals as the items.

As the first message of a new chat, `pickup <name>` continues. In a chat that already has work of its own, it folds in. If the rules file names a different chat as master, say so and ask before folding in. If it is unclear which, ask in one line.

## Continue (first message of a new chat)

1. Read the handoff and its "Read first" files. Don't read the old chat unless something needed is missing.
2. If newer versions of the "Built on" files exist, say so.
3. Set the file's status line to `Status: continuing in <this chat's title>, <date>`.
4. Reply in five lines or fewer: what is picked up, anything stale, the next step. Then do the next step, unless it needs the user.

## Fold in (a chat already underway)

This chat is the master: a second set of eyes on work it did not build. Scrutinize; don't rubber-stamp.

1. **Read** the handoff and the files it points to.
2. **Review every item:** check numbers against the current sources and rerun the math where figures matter; look for conflicts with settled decisions or other parts of the work; flag anything missing, or stale against "Built on"; apply the rules file's review checks.
3. **Deep review** for items that hit the rules file's triggers, or that are high-stakes or hard to reverse: have an independent agent that has not seen this discussion check them before presenting.
4. **One verdict per item, one line each:** Keep; Change (to what); Toss (why); or Return (what the side chat must do, when it needs real work such as new research). Then stop and discuss. Nothing is applied until the user decides, usually in one line ("keep A to H, change C, toss I").
5. **Apply what the user approved** where the rules file says approved items go (re-read that file right before saving, in case another chat changed it), and make the agreed changes.
6. **Open items:** small ones join this chat's open list. A whole topic still open keeps the side chat alive: set its status to `continuing in <side chat's title>`.
7. **Returns:** add this to the side chat's file, set `Status: returned`, and tell the user to open that chat and type `pickup`:

```
## Returned from <master chat's title>, <date>
- <item>: what to fix, and why
```

8. **Fully folded:** cut the side chat's file down to a receipt, and give the user the side chat's finished title. Tossed items stay in the receipt with their reason, so they don't come back.

```
# Handoff: <line>
Status: folded into <master chat's title>, <date>
Kept: A, B, D (to <where>). Changed: C (<how>). Tossed: I (<why>).
```

## `pickup` with no name

If this chat's line has a file with status `returned`, read the returned items and start on them. When they are done, `handoff` again so the master can pick them up. Otherwise list the handoffs waiting for pickup and ask which.

## `handoffs`

List each handoff file (not the rules file): line, status, date, and one line on what it holds. Build the list from the handoff files themselves (without a file store, from a past-chat search for `HANDOFF`). Never keep a shared tracker file: several chats would overwrite it.
