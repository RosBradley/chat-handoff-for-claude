---
name: chat-handoff
description: "Carries a chat's work into a new chat, or reviews a side chat's work item by item and folds what the user approves into a master chat. Use when the user's message is a handoff command, in any case: handoff (with or without a name), handoff?, pickup (with or without a chat name), fold (with a chat name), handoffs, or the dot-prefixed forms .push, .push?, .pull, .merge and .status. Also when the user plainly asks to hand off, pick up or fold in a chat's work. Also for ANY other message in a chat that this skill already handed off or folded in (an earlier handoff or .push ran in this chat, or the chat was told it is folded, merged or done), so the stale-chat guard can run before the message is acted on. Not when these words appear inside an ordinary sentence, such as picking up the kids or a handoff to another team."
---

# Chat Handoff

Version: 0.3.3

Claude re-reads the whole chat with every message, so a long chat uses up the user's limits faster, costs more on the API, answers more slowly, and near the length limit gets summarized or stopped. This skill doesn't move or copy a chat. It saves a short, deliberate handoff (decisions, open items, next step, what not to redo) that a fresh chat picks up, or it reviews a side chat's work item by item so a master chat folds in only what the user approves.

## Commands

Two sets of words do the same things; the user can use either.

| Plain words | Dot style | What happens |
|---|---|---|
| `handoff` | `.push` | Saves this chat's handoff file. If the chat has no name yet, asks for one first, with a suggestion |
| `handoff <name>` | `.push <name>` | Saves it under that name, for example `handoff budget` or `handoff budget.pre` (see "Names"). A different line renames it (see "Renaming") |
| `handoff?` | `.push?` | Answers in one line: is this a good time to hand off? |
| `pickup <name>` | `.pull <name>` | Continues that chat's work in this chat (normally the first message of a new chat) |
| `fold <name>` | `.merge <name>` | Reviews that chat's work item by item, gives each item a verdict, and folds what the user approves into this chat, the master |
| `pickup` | `.pull` | In a chat with work returned to it: starts on the returns. Anywhere else: lists what is waiting and asks |
| `handoffs` | `.status` | Lists every handoff and its status |

- A command is the user's whole message, or nearly (`handoff please`, `fold budget`), and case doesn't matter: `.Push` and `Handoff` count. A plain request ("let's hand this off") counts too, as plain words. Inside an ordinary sentence these are ordinary words: carry on without this skill.
- The dot-style words always carry the dot, so they're never mistaken for git commands: `.push` is a handoff, `push` alone is not.
- In a chat that has already been handed off or folded in, a message that is not a command does not run straight away: see "Stale chat guard".
- Follow the user's habit: when telling the user what to type next, or suggesting a chat title, use the style of the command they just typed (see "Chat titles").

Replies stay short, bottom line first.

## Where files live

| Where the chat runs | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files, `claude/Handoff - <line>.md`, through the Projects tool | `claude/Handoff rules.md` |
| A working folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted in the chat (see "Without a file store") | None: the defaults apply |

Several chats may run at once, so a chat writes only its own line's file. The one exception: a master marking items, setting the status or writing a receipt in a file it is folding in.

**Another folder.** The user can name another folder in plain words ("handoff, and save it in ~/Projects/other", "pickup budget from ~/Projects/first"): for that command, use that folder's `handoffs/`. claude.ai Projects can't see each other's files, so between Projects, post the handoff (see "Without a file store").

**When the file won't reach the next session.** In Claude Code on the web, every session starts from a fresh copy of the branch: after saving, offer to commit and push the handoff (`git add -f` if `handoffs/` is gitignored), or post it. In a git worktree, the file is saved in that worktree only: say so in the reply.

**Names.** A chat's name is its line, with an optional tag after a dot: `budget` is a chat on the budget line; `budget.pre` is one the user chose to tag.

- The line is the working name: one word of letters, digits or hyphens, with no spaces or dots (for example `research`, `budget`, `tax-harvest`). One file per line, `Handoff - <line>.md`, serves every chat on that line.
- The tag is the user's, for telling chats on one line apart: a word, a letter, a number, whatever they like (`budget.pre`, `budget.B`, `budget.2`). This skill never invents a tag and never asks for one; a chat with no tag is simply named by its line. Read a name by splitting it at its first dot.
- A name typed with spaces is joined with hyphens: `handoff market size` saves `market-size`. Leave out words that only ask (`please`, `now`). If the words before the last one spell this chat's line or another line with a handoff file, the last word is the tag: `handoff market size au` on the `market-size` line is `market-size.au`. Say in the reply what the name became ("Saved as market-size.au."), so the user can change it.
- Take the name from `handoff <name>`, from the pickup or fold that started this chat, or from an earlier handoff in it. If the chat has no name at all, the first time a command needs one, ask once, in one line, with a short line drawn from the chat's topic ("Use budget as this chat's handoff name? Reply yes or give another."), and use the answer. Never pick a name silently: Claude can't see chat titles.
- Names match loosely: `pickup budget`, `pickup budget.pre` and one distinctive word all find the line's file. Order between chats on a line comes from the dates in the file, never from the tag.

**Renaming.** `handoff <name>` with a line other than this chat's is a rename, and no trace of the old name stays behind. A different tag on the same line is not a rename: it only sets or changes this chat's tag. A rename keeps this chat's tag unless the new name gives one (`handoff budget` in `research.pre` makes it `budget.pre`). When the new line is this chat's line with a number or letter run on (`handoff test2` on the `test` line), a tag was probably meant: ask in one line before renaming ("Rename the test line to test2, or tag this chat test.2?").

1. Save the file under the new line, with its `# Handoff:` line changed to match.
2. Only after that save succeeds, delete the old file (in a Project, `project_delete`; in a folder, remove it). Never delete first.
3. Say so in the reply: "Renamed from <old> to <new>", with the chat's new title, marked optional.

Rename only this chat's own line. If the old file's status shows another chat already has it (`continuing in`, `folded into` or `merged into`), ask first, since that chat knows it by the old name. Without a file store, an earlier post can't be removed, so the new post's heading adds "(renamed from <old>)".

**Chat titles.** Claude can't see chat titles and, in most apps, can't rename chats. Whenever a chat's state changes, suggest the title the user can rename it to, and say it's optional ("Optional: rename this chat handed_off.budget."). Commands find handoffs by file name, never by chat title, so everything works the same whether or not a chat is renamed. In the Claude desktop app's Code tab, the user can ask Claude to rename the session; when they do, use the suggested title.

A working chat, a master included, is titled by its name alone (line, or line and tag): `budget`, `budget.pre`. Every other state puts a state word and a dot in front of the name, so the state still shows when the sidebar cuts a long title off, and, as long as the user sticks to one command style, a search for it (`folded.`, say) finds every chat in that state. Where a state is named after a command, its word follows the style of the command just typed; the other states use the same word in both styles. Use the rules file's titles if it sets them; otherwise:

| The chat is | After plain words | After dot style | Suggested by |
|---|---|---|---|
| Working, a master included | `<name>` | `<name>` | `handoff` and `pickup`, for the next chat; the master, when a side chat's topic stays open |
| Handed off: its work continues in a new chat, or waits for the master | `handed_off.<name>` | `pushed.<name>` | `handoff`, for this chat; `pickup`, for the old chat |
| Has work sent back to it | `returned.<name>` | `returned.<name>` | The master's fold |
| Finished, folded into the master | `folded.<name>` | `merged.<name>` | The master's fold |
| Finished: its work went out, nothing handed on | `done.<name>` | `done.<name>` | The last chat in a chain, once everything is settled |

**Item letters.** Items to fold in are lettered A, B, C. A letter belongs to one item for the life of a line: a reworked item keeps its letter, and new items continue after the highest letter already used (in the items, the "Don't redo" list or the receipt). Never reuse a letter.

Big work products (proposal lists, analyses, specs) stay in their own files. The handoff points to them and never copies them.

### Without a file store

A chat can't change an earlier chat's messages, so here every write is a post. Wherever this skill says to save the file, set its status, mark items or write a receipt, post the line's whole file as it now stands at the end of the reply, under the heading `HANDOFF: <name>, <date>`. `<name>` is the chat that last handed the line off (the file's "From" line); a master posting a file it is folding in uses that name too, not its own.

`pickup`, `fold` and `handoffs` find these posts with past-chat search (query `HANDOFF <line>`) and use the newest one for each line: the latest date; on the same date, the one from the more recent chat. If past-chat search is off or finds nothing, say so and ask the user to paste the handoff.

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
The title for each state, if not the defaults (for example, one set of words for both command styles).
## Never
Work no handoff may start.
```

**Defaults:** any chat already underway can be the master; approved items go into that chat's own working files or open list; deep review covers anything high-stakes or hard to reverse; titles are suggested as in the table above.

## Stale chat guard

A chat that has been handed off or folded in is finished; its work lives in another chat now. Old chats stay in the sidebar, so sooner or later a message meant for the new chat lands in the old one. This guard catches that before anything runs.

**When this chat is stale.** Any of these:

- an earlier message in this chat ran `handoff` (`.push`), and nothing since reopened it (see choice 3 below);
- the line's file status says this chat's work moved on: `continuing in`, `folded into`, `merged into` or `done`;
- the line's file was written by another chat on the line after this chat's last handoff or pickup (its `From` line has changed since this chat wrote or read it), so this chat is behind.

**What triggers it.** Any message that is not a handoff command and not a bare acknowledgment (thanks, ok, got it). Commands always run: `handoff` again in a stale chat updates the file (asking first if another chat has the line now; see "`handoff`"), `handoffs` lists, and so on.

**What this skill does.** Don't act on the message. Read the line's file for the current status, then ask. Two lines, then the choices: the first line says this chat is handed off and where the work is now ("This chat was handed off as budget.pre on October 12; the work continues in budget.post."); the second asks whether to run the instruction here anyway. Offer the choices as buttons when the chat can show them (the AskUserQuestion tool); otherwise end with "Reply stop, continue or reopen."

1. **Stop** (recommended, first in the list). Don't run it here. Reply with the chat to use instead, by its name and suggested title ("Type it in budget.post"), and nothing else. No part of the instruction is carried out, not even a partial answer.
2. **Continue here, once.** Run the instruction in this chat, but the chat stays stale: the next instruction gets the warning again. If the result matters to the line, end the reply by suggesting `handoff` (`.push`) so the file catches up.
3. **Reopen this chat.** Run it, and this chat takes the line back; the guard stays off until the next `handoff`. Set the file status to `waiting` and suggest the optional title `<name>`, with no state word. If the status showed another chat already continuing the line, say that both chats now hold it, and that the user should `handoff` from whichever one wins so the file settles it.

Never run the instruction before the user answers, and never let the warning swallow the instruction: once the user answers continue or reopen, carry out the message exactly as typed. If the user types a new instruction instead of answering, treat that as choosing stop for the first one and warn once more, since the chat is still stale.

**Cost.** One file read per guarded message. After stop, nothing else. The `handoff` reply tells the user the guard is on, so the warning never comes as a surprise.

## `handoff` (`.push`)

1. Settle the name (see "Names" and "Renaming"). Read the rules file, and the line's current file if one exists.

   **Another chat has the line.** If the file shows another chat has the line now (a `continuing in` status this chat didn't set, or a `From` line that has changed since this chat's own pickup or last handoff), saving would replace that chat's handoff. Ask before drafting anything: one line says which chat has the line and since when ("budget.post picked this line up on October 12; saving here would replace its handoff."), then the choices, as buttons when the chat can show them (the AskUserQuestion tool):

   1. **Stop** (recommended, first in the list). Save nothing. Reply with the chat that has the line, by its name ("Hand off from budget.post instead").
   2. **Add to it.** Keep that chat's file as it is, status and `From` line included, and add only this chat's new work, as items under "Ready to fold in" with the next letters, each marked "(from <this chat's name>, <date>)". Step 1's carry-forward keeps them in that chat's next handoff. Say so, and that this chat stays stale.
   3. **Replace it.** Save as usual: this chat takes the line back, with status `waiting`. Say that the other chat is now behind (its guard will warn there), and that anything it hasn't handed off lives only in that chat.

   From the file, carry forward:
   - items not yet settled, with their letters (a reworked item drops its Returned mark);
   - every tossed or rejected item, into "Don't redo" with its reason, so it doesn't come back;
   - settled items as one "Don't redo" line, for example "A changed and B kept, into the report draft, September 12, 2026".
2. Write in-flight state only, about 400 words at most. Drop empty sections.

```
# Handoff: <line>
Status: waiting
From: <name>, <date>
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
6. Tell the user, in four lines or fewer, in the style they just used: saved (and renamed from what, if it was a rename); what to type next (`pickup <line>` or `.pull <line>` as the first message of a new chat to continue; `fold <line>` or `.merge <line>` in the master to fold it in); and the optional titles: this chat `handed_off.<name>` (`pushed.<name>` after `.push`), and, if continuing, the new chat `<line>` (the user can add a tag of their own when they pick it up). For example: "Optional: rename this chat handed_off.budget, and title the new one budget."
7. **How to do it.** People forget how their app starts, renames and finds chats, so after those lines give the steps for the app this chat runs in, with the real names and titles filled in, in the style just used (after `.push`: `/rename pushed.budget`, `.pull budget`). Give the steps for what comes next: continuing in a new chat, or folding into the master.
   - **Claude Code:** a code block to type line by line, then one line on getting back to old sessions: "`/clear` keeps this session; `/resume` lists old ones, or run `claude --resume budget` in Terminal." To continue:
     ```
     /rename handed_off.budget
     /clear
     pickup budget
     /rename budget
     ```
     To fold in, the last three lines become two: `/resume` (pick the master), then `fold budget`. These commands work in the terminal and JetBrains. When the session clearly runs elsewhere, give that app's way instead: in the desktop app's Code tab, + New session or Cmd+N, click the title to rename it (or ask Claude to), and find old sessions in the sidebar; in VS Code and its forks, the Command Palette's "Open in New Tab", then "Rename Session Tab", and the Session history button for old sessions.
   - **claude.ai:** "Start a new chat in this Project and type pickup budget" (without a Project, any new chat), or, to fold in, open the master chat in the sidebar. To rename a chat: hover over it in the sidebar, click ⋮, then Rename; on iPhone, touch and hold it in the chat list; on Android, open it and tap ⋮ at the top right.

   End with one short line saying this chat is now guarded: a new instruction typed here gets a warning first (see "Stale chat guard").

## `handoff?` (`.push?`)

One line. **Yes** when the chat is at a stopping point (a deliverable finished, a question settled, a new topic about to start) or has grown long and heavy (big files, long runs, a lot of back and forth). **Not yet** when a handoff would split a piece of work in half: say what to finish first.

## Finding a handoff by name

For `pickup <name>`, `fold <name>` and their dot forms: match the name's line loosely against handoff file names (without a file store, against past-chat search); one distinctive word is enough, and a tag after the dot only confirms which chat handed off. If two match, ask which. If no handoff file matches but another file clearly holds handed-off work (one written before this skill, for example), use it as the handoff and treat its proposals as the items. If the status says the line is already continuing in another chat, say so and ask before taking it over.

`pickup <name>` always continues and `fold <name>` always folds in; never guess between them.

- `pickup <name>` in a chat that already has work of its own: ask in one line which was meant.
- `fold <name>` as the first message of a new chat: if the rules file says which line that one folds into, this chat is that line (a fresh review chat, for example): say so in the first line and go ahead. Otherwise ask in one line which was meant.
- If the rules file says the line folds into a different line than this chat's, say so and ask before folding in.

## Continue: `pickup <name>` (`.pull <name>`)

1. Read the handoff and its "Read first" files. Don't read the old chat unless something needed is missing.
2. If newer versions of the "Built on" files exist, say so.
3. This chat is named by the line, plus the tag if the user typed one in the pickup command (`pickup budget.post` makes this chat `budget.post`); a tag that matches the file's "From" line names the old chat, not this one, so this chat stays untagged. Set the status to `continuing in <name>, <date>` (`continuing in a new chat, <date>` when this chat has no tag). A "From" line with a trailing number (`budget.3`, from an older version) is just a tag.
4. Reply in five lines or fewer: what is picked up, anything stale, the optional titles, worded for the user since Claude can't see which chats are renamed ("Optional: title this chat budget.post; if you haven't already, rename the old one handed_off.budget.pre", or `pushed` after `.pull`), and the next step. If the status was `returned`, the next step is the returned items. Then do the next step, unless it needs the user.

## Fold in: `fold <name>` (`.merge <name>`)

This chat is the master, and the skill is its reviewer: a second set of eyes on work this chat did not build. The side chat's conclusions are claims to test, not facts. Scrutinize; don't rubber-stamp. The user's part is the decision (step 4).

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
8. **Set the side chat's status, and suggest its optional title** in the style of the fold command just typed:
   - Any item returned: `Status: returned from <this chat's name>, <date>`. Suggest the title `returned.<name>`, and tell the user to type `pickup` (`.pull`) in that chat, or `pickup <line>` (`.pull <line>`) as the first message of a new chat.
   - Nothing returned, but a whole topic still open: `Status: continuing in <side chat's name>, <date>`. Suggest the side chat goes back to its plain name, `<name>`.
   - Everything settled: cut the file down to a receipt, with `Status: folded into` (`merged into` after `.merge`), and suggest the title `folded.<name>` (`merged.<name>` after `.merge`). Tossed items stay in the receipt with their reason, so they don't come back.

```
# Handoff: <line>
Status: folded into <this chat's name>, <date>
Kept: A, B, D (to <where>). Changed: C (<how>). Tossed: I (<why>).
```

9. **Done:** if this chat folds into no other line (per the rules file, or because the user says it's the end) and nothing is waiting, returned or open, say the work is complete and where it is, and suggest the optional title `done.<name>` for this chat once the work goes out. If this line has a handoff file, set its status to `done, <date>`.

## `pickup` with no name (`.pull`)

If this chat's line has a file with status `returned`, start on the items marked Returned. Rework each under its own letter. When they are done, `handoff` again so the master can fold them in. Otherwise list the handoffs whose status is `waiting` (in older files, `waiting for pickup`), and ask which.

## `handoffs` (`.status`)

List each handoff file (not the rules file): line, the chat that last handed it off, status, date, and one line on what it holds. Build the list from the handoff files themselves (without a file store, from the newest post for each line). Never keep a shared tracker file: several chats would overwrite it.
