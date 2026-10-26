# Chat state: the stale chat guard, a line another chat holds, renames and titles

## Stale chat guard

A chat that has been handed off, transferred or folded in is finished; its work lives in another chat, or another AI, now. Old chats stay in the sidebar, so sooner or later a message meant for the new chat lands in the old one. This guard catches that before anything runs. When the guard applies is in SKILL.md ("Stale chat guard"); this is what to do.

**What this skill does.** Don't act on the message. Read the line's file for the current status, then ask. Two lines, then the choices: the first line says this chat is handed off and where the work is now ("This chat was handed off as budget.pre on October 12; the work continues in budget.post."); the second asks whether to run the instruction here anyway. Offer the choices as buttons when the chat can show them (the AskUserQuestion tool); otherwise end with "Reply stop, continue or reopen."

1. **Stop** (recommended, first in the list). Don't run it here. Reply with the chat to use instead, by its name and suggested title ("Type it in budget.post"), and nothing else. No part of the instruction is carried out, not even a partial answer.
2. **Continue here, once.** Run the instruction in this chat, but the chat stays stale: the next instruction gets the warning again. If the result matters to the line, end the reply by suggesting `handoff` (`.push`) so the file catches up.
3. **Reopen this chat.** Run it, and this chat takes the line back; the guard stays off until the next `handoff`. Set the file status to `waiting` and suggest the optional title `<name>`, with no state word. If the status showed another chat already continuing the line, say that both chats now hold it, and that the user should `handoff` from whichever one wins so the file settles it.

Never run the instruction before the user answers, and never let the warning swallow the instruction: once the user answers continue or reopen, carry out the message exactly as typed. If the user types a new instruction instead of answering, treat that as choosing stop for the first one and warn once more, since the chat is still stale. If the user's message already says to go ahead here ("do this here anyway", "reopen this chat"), that is the answer: don't ask again.

**Cost.** One file read per guarded message. After stop, nothing else. The `handoff` reply tells the user the guard is on, so the warning never comes as a surprise.

## Another chat has the line

Read when step 1 of `handoff` finds that another chat has the line now (a `continuing in` status this chat didn't set, a `From` line that has changed since this chat's own pickup or last handoff, or any file at all when this chat never picked the line up or handed it off, such as a rename onto a line that already exists). Saving would replace that chat's handoff. Ask before drafting anything: one line says which chat has the line and since when ("budget.post picked this line up on October 12; saving here would replace its handoff."), then the choices, as buttons when the chat can show them (the AskUserQuestion tool):

1. **Stop** (recommended, first in the list). Save nothing. Reply with the chat that has the line, by its name ("Hand off from budget.post instead"); if this chat never had the line, ask for another name instead.
2. **Add to it.** Keep that chat's file as it is, status and `From` line included, and add only this chat's new work, as items under "Ready to fold in" with the next letters, each marked "(from <this chat's name>, <date>)". Step 1's carry-forward keeps them in that chat's next handoff. Say so, and that this chat stays stale.
3. **Replace it.** Save as usual: this chat takes the line back, with status `waiting`. Say that the other chat is now behind (its guard will warn there), and that anything it hasn't handed off lives only in that chat.

## Renaming

`handoff <name>` with a line other than this chat's is a rename, and no trace of the old name stays behind. A different tag on the same line is not a rename: it only sets or changes this chat's tag. A rename keeps this chat's tag unless the new name gives one (`handoff budget` in `research.pre` makes it `budget.pre`). When the new line is this chat's line with a number or letter run on (`handoff test2` on the `test` line), a tag was probably meant: ask in one line before renaming ("Rename the test line to test2, or tag this chat test.2?").

1. Save the file under the new line, with its `# Handoff:` line changed to match.
2. Only after that save succeeds, delete the old file (in a Project, `project_delete`; in a folder, remove it). Never delete first. If the new line already had a file and the user chose Stop or Add to it (see "Another chat has the line"), keep the old file.
3. Say so in the reply: "Renamed from <old> to <new>", with the chat's new title, marked optional.

Rename only this chat's own line. If the old file's status shows another chat already has it (`continuing in`, `folded into` or `merged into`), ask first, since that chat knows it by the old name. Without a file store, an earlier post can't be removed, so the new post's heading adds "(renamed from <old>)".

## Chat titles

Titles are only suggested, and renaming is optional: Claude can't see chat titles and, in most apps, can't rename chats, and commands find handoffs by file name, never by title. Whenever a chat's state changes, suggest one ("Optional: rename this chat handed_off.budget."). In the Claude desktop app's Code tab, the user can ask Claude to rename the session; then use the suggested title. A working chat is titled by its name alone (`budget`, `budget.pre`); every other state puts a state word and a dot first, so the state shows even when the sidebar cuts the title off, and one search (`folded.`) finds every chat in that state while the user sticks to one command style. A state word named after a command follows the style just typed. The rules file's titles win; otherwise:

| The chat is | After plain words | After dot style | Suggested by |
|---|---|---|---|
| Working, a master included | `<name>` | `<name>` | `handoff` and `pickup`, for the next chat; the master, when a side chat's topic stays open |
| Handed off: its work continues in a new chat or another AI, or waits for the master | `handed_off.<name>` | `pushed.<name>` | `handoff` and `transfer` (`.push`, `.export`), for this chat; `pickup`, for the old chat |
| Has work sent back to it | `returned.<name>` | `returned.<name>` | The master's fold |
| Finished, folded into the master | `folded.<name>` | `merged.<name>` | The master's fold |
| Finished: its work went out, nothing handed on | `done.<name>` | `done.<name>` | The last chat in a chain, once everything is settled |
