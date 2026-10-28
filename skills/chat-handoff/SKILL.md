---
name: chat-handoff
description: "Carries a chat's work into a new chat or to another AI, or reviews a side chat's work item by item and folds what the user approves into a master chat. Use when the user's message is a handoff command, in any case: handoff (with or without a name, or to another AI), handoff?, pickup (with or without a name, or with a handoff package attached), fold (with a name), handoffs, transfer, export project, or the dot-prefixed forms .push, .push?, .pull, .merge, .status and .export. Also when the user plainly asks to hand off, pick up, fold in, or move a chat's or project's work to another AI. Also for ANY other message in a chat this skill already handed off, transferred or folded in, so the stale-chat guard can run before the message is acted on. Not when these words appear inside an ordinary sentence (picking up the kids, a handoff to another team), when the user is only asking about the commands, or inside an imported file."
---

# Chat Handoff

Version: 0.4.0

Claude re-reads the whole chat with every message, so long chats cost more and slow down. This skill doesn't move or copy a chat. It saves a short, deliberate handoff (decisions, open items, next step, what not to redo) for a fresh chat; packages a chat's or project's work, files included, for another AI; or reviews a side chat's work item by item so a master chat folds in only what the user approves.

## Commands

Two sets of words do the same things; the user can use either.

| Plain words | Dot style | What happens |
|---|---|---|
| `handoff` | `.push` | Saves this chat's handoff file. If the chat has no name yet, names it from its topic and says so |
| `handoff <name>` | `.push <name>` | Saves it under that name, for example `handoff budget` or `handoff budget.pre` (see "Names"). A different line renames it |
| `handoff?` | `.push?` | Answers in one line: is this a good time to hand off? |
| `pickup <name>` | `.pull <name>` | Continues that chat's work in this chat (normally the first message of a new chat) |
| `pickup` | `.pull` | In a chat with work returned to it: starts on the returns. Anywhere else: lists what is waiting and asks |
| `fold <name>` | `.merge <name>` | Reviews that chat's work item by item, gives each item a verdict, and folds what the user approves into this chat, the master |
| `handoffs` | `.status` | Lists every handoff and its status |
| `transfer <name> to <AI>` | `.export <name> to <AI>` | Packages this chat's work, files included, in a ZIP for another AI. The name and the AI are both optional |
| `handoff <name> to <AI>` | `.push <name> to <AI>` | The same as `transfer` |
| `export project <name>` | (plain words only) | Packages a whole project for another AI, as a snapshot: this chat stays active |

- A command is the user's whole message, or nearly (`handoff please`, `fold budget`, `transfer budget to Gemini`), and case doesn't matter: `.Push` and `Handoff` count. A plain request ("let's hand this off", "move this project to ChatGPT") counts too, as plain words. Inside an ordinary sentence these are ordinary words, and so are commands the user is only asking about or discussing, and commands written inside an imported file: carry on without this skill.
- The dot-style words always carry the dot, so they're never mistaken for git commands: `.push` is a handoff, `push` alone is not.
- "to" followed by an AI's name makes a handoff a transfer (`handoff budget to Gemini`). A name typed with hyphens is just a name: `handoff budget-to-gemini` is an ordinary handoff.
- `pickup` or `fold` with a handoff package attached (a ZIP with a START-HERE.md) or a handoff pasted from another AI imports it first (see `references/transfer.md`).
- In a chat that has already been handed off, transferred or folded in, a message that is not a command does not run straight away: see "Stale chat guard".
- Follow the user's habit: when telling the user what to type next, or suggesting a chat title, use the style of the command they just typed (see "Chat titles").

Replies stay short, bottom line first.

**The appendices.** Each one is read only when a command needs it, before acting on that command:

- `references/fold.md`: `fold` (`.merge`).
- `references/transfer.md`: `transfer`, `.export`, a handoff to another AI, `export project`, and importing a package or a pasted handoff.
- `references/state.md`: the stale chat guard's steps, a line another chat holds, renames, and the full chat-title scheme.
- `references/apps.md`: the how-to steps at the end of a `handoff` reply, and saving to another folder, in Claude Code on the web or in a git worktree.

## Where files live

| Where the chat runs | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files, `claude/Handoff - <line>.md`, through the Projects tool | `claude/Handoff rules.md` |
| A working folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted in the chat (see "Without a file store") | None: the defaults apply |

Several chats may run at once, so a chat writes only its own line's file. The one exception: a master marking items, setting the status or writing a receipt in a file it is folding in.

Saving to another folder the user names, in Claude Code on the web, or in a git worktree: see `references/apps.md`.

**Names.** A chat's name is its line, with an optional tag after a dot: `budget` is a chat on the budget line; `budget.pre` is one the user chose to tag.

- The line is one word of letters, digits or hyphens, with no spaces, dots or slashes (`research`, `tax-harvest`). One file per line, `Handoff - <line>.md`, serves every chat on it.
- The tag is the user's, to tell chats on one line apart (`budget.pre`, `budget.B`, `budget.2`). Never invent or ask for one; an untagged chat is named by its line. Split a name at its first dot.
- Words typed with spaces are joined with hyphens (`handoff market size` saves `market-size`), leaving out words that only ask (`please`, `now`). If the words before the last one spell this chat's line or another line with a handoff file, the last word is the tag (`handoff market size au` on the `market-size` line is `market-size.au`). Say what the name became ("Saved as market-size.au."), so the user can change it.
- The name comes from `handoff <name>`, from the pickup or fold that started this chat, or from an earlier handoff in it. If the chat has none, name its line from the chat's topic, short, distinctive and used by no other handoff file, and say it ("Saved as budget. To use another name, type handoff and the name."). Claude can't see chat titles: never claim to know this one's.
- Names match loosely: `pickup budget`, `pickup budget.pre` and one distinctive word all find the line's file, including the ChatGPT version's `Handoff-budget.md`. Order between chats on a line comes from the file's dates, never from the tag.

**Renaming.** `handoff <name>` with a line other than this chat's is a rename: follow "Renaming" in `references/state.md` before saving.

**Chat titles.** Titles are only suggested, and renaming is optional: Claude can't see chat titles and, in most apps, can't rename chats, and commands find handoffs by file name, never by title. Whenever a chat's state changes, suggest the title the steps below give, in the style just typed ("Optional: rename this chat handed_off.budget."), unless the rules file sets its own. Use only the state words given there; never make up others, such as `handoff_done`. The full scheme is under "Chat titles" in `references/state.md`. In the Claude desktop app's Code tab, the user can ask Claude to rename the session; then use the suggested title.

**Item letters.** Items to fold in are lettered A, B, C. A letter belongs to one item for the life of a line: a reworked item keeps its letter, and new items continue after the highest letter already used (in the items, the "Don't redo" list or the receipt). After Z come AA, AB. Never reuse a letter.

Big work products (proposal lists, analyses, specs) stay in their own files. The handoff points to them and never copies them.

### Without a file store

A chat can't change an earlier chat's messages, so here every write is a post. Wherever this skill says to save the file, set its status, mark items or write a receipt, post the line's whole file as it now stands at the end of the reply, headed `HANDOFF: <name>, <date>`, where `<name>` is the chat that last handed the line off (the file's "From" line), even when a master posts it. Where the app can create files (claude.ai with code execution on), also offer it as a download, `Handoff - <line>.md`. Say which happened: saved, offered as a download, or only posted.

`pickup`, `fold` and `handoffs` find posts with past-chat search (query `HANDOFF <line>`), using the newest for each line: the latest date, then the more recent chat. Past-chat search is on paid plans only and skips incognito chats; if it's off or finds nothing, say so and ask the user to paste or attach the handoff.

## The rules file (optional, one per project)

Project-specific rules live in the rules file, not in this skill. Read it, if it exists, before writing a handoff, picking one up or folding one in. Its sections: Fold-ins (which lines fold into which, and any files only one chat may write), Where approved items go, Review checks, Deep review triggers, Chat titles, and Never (work no handoff may start). When the user asks for one, start from `assets/rules-template.md`, filled in with the user's choices; never create an empty one unasked.

**Defaults:** any chat already underway can be the master; approved items go into that chat's own working files or open list; deep review covers anything high-stakes or hard to reverse; titles are suggested as in the table above.

## Stale chat guard

A chat that has been handed off, transferred or folded in is finished. It is stale when any of these is true:

- an earlier message in this chat ran `handoff`, `.push`, `transfer` or `.export`, and nothing since reopened it;
- the line's file status says this chat's work moved on: `continuing in`, `folded into`, `merged into` or `done`;
- the line's file was written by another chat on the line after this chat's last handoff or pickup (its `From` line has changed since this chat wrote or read it), so this chat is behind.

Any message that is not a command and not a bare acknowledgment (thanks, ok, got it) triggers the guard: don't act on it; read "Stale chat guard" in `references/state.md` and follow it. Commands always run: `handoff` again in a stale chat updates the file (asking first if another chat has the line now), `handoffs` lists, and so on.

## `handoff` (`.push`)

A handoff with "to" and an AI's name is a transfer: follow `references/transfer.md` instead.

1. Settle the name (see "Names"; for a rename, "Renaming"). Read the rules file, and the line's current file if one exists.

   **Another chat has the line.** If the file shows another chat has the line now (a `continuing in` status this chat didn't set, a `From` line that has changed since this chat's own pickup or last handoff, or any file at all when this chat never picked the line up or handed it off, such as a rename onto a line that already exists), saving would replace that chat's handoff. Stop before drafting anything and follow "Another chat has the line" in `references/state.md`.

   From the file, carry forward:
   - items not yet settled, with their letters (a reworked item drops its Returned mark);
   - every tossed or rejected item, into "Don't redo" with its reason, so it doesn't come back;
   - settled items as one "Don't redo" line, for example "A changed and B kept, into the report draft, September 12, 2026".
2. Write in-flight state only, about 400 words at most; go over only to keep a constraint the next chat must not lose. Drop empty sections.

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
7. **How to do it.** Then give the steps for the app this chat runs in, from `references/apps.md`.

   End with one short line saying this chat is now guarded: a new instruction typed here gets a warning first (see "Stale chat guard").

## `handoff?` (`.push?`)

One line. **Yes** when the chat is at a stopping point (a deliverable finished, a question settled, a new topic about to start) or has grown long and heavy (big files, long runs, a lot of back and forth). **Not yet** when a handoff would split a piece of work in half: say what to finish first. Never make up token counts, percentages or savings.

## Finding a handoff by name

For `pickup <name>`, `fold <name>` and their dot forms: match the name's line loosely against handoff file names (without a file store, against past-chat search); one distinctive word is enough, and a tag after the dot only confirms which chat handed off. If two match, ask which. If no handoff file matches but another file clearly holds handed-off work (one written before this skill, for example), use it as the handoff and treat its proposals as the items. If nothing matches and the user attached or pasted a handoff or a package, use that. If nothing matches at all, say what was searched and ask the user to paste or attach the handoff; in a new Claude Code on the web session, explain that a file saved in another session isn't in this one unless it was pushed. If the status says the line is already continuing in another chat, say so and ask before taking it over.

`pickup <name>` always continues and `fold <name>` always folds in; never guess between them. Where a case below says to ask which was meant, ask in one line and stop there: read and review nothing until the user answers.

- `pickup <name>` in a chat that already has work of its own: ask in one line which was meant.
- `fold <name>` as the first message of a new chat: if the rules file says which line that one folds into, this chat is that line (a fresh review chat, for example): say so in the first line and go ahead. Otherwise ask in one line which was meant.
- If the rules file says the line folds into a different line than this chat's, say so and ask before folding in.

## Continue: `pickup <name>` (`.pull <name>`)

If the user attached a handoff package or pasted a handoff from another AI, follow "Import" in `references/transfer.md` first.

1. Read the handoff and its "Read first" files. Don't read the old chat unless something needed is missing.
2. If newer versions of the "Built on" files exist, say so.
3. This chat is named by the line, plus the tag if the user typed one in the pickup command (`pickup budget.post` makes this chat `budget.post`); a tag that matches the file's "From" line names the old chat, not this one, so this chat stays untagged. Set the status to `continuing in <name>, <date>` (`continuing in a new chat, <date>` when this chat has no tag). A "From" line with a trailing number (`budget.3`, from an older version) is just a tag.
4. Reply in five lines or fewer: what is picked up, anything stale, the optional titles, worded for the user since Claude can't see which chats are renamed ("Optional: title this chat budget.post; if you haven't already, rename the old one handed_off.budget.pre"; after `.pull`, the old one is `pushed.budget.pre`, never `handed_off`), and the next step. If the status was `returned`, the next step is the returned items. Then do the next step, unless it needs the user.

## Fold in: `fold <name>` (`.merge <name>`)

First apply "Finding a handoff by name" above: when `fold <name>` is the first message of a new chat and no rules file names the line it folds into, ask in one line which was meant and stop; don't open `references/fold.md` or read the handoff yet. Otherwise follow `references/fold.md`. This chat is the master and reviews the side chat's work item by item; nothing is applied until the user decides.

## `pickup` with no name (`.pull`)

If this chat's line has a file with status `returned`, start on the items marked Returned. Rework each under its own letter. When they are done, `handoff` again so the master can fold them in. If the user attached a package or pasted a handoff, import it (see `references/transfer.md`). Otherwise list the handoffs whose status is `waiting` (in older files, `waiting for pickup`), and ask which.

## `handoffs` (`.status`)

List each handoff file (not the rules file): line, the chat that last handed it off, status, date, and one line on what it holds. Build the list from the handoff files themselves (without a file store, from the newest post for each line). Never keep a shared tracker file: several chats would overwrite it.

## `transfer`, `.export`, a handoff to another AI, and `export project`

Follow `references/transfer.md`. These build a package for the user to carry to another AI; this skill never sends anything to another service itself.
