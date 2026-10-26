# Apps: special places to save, and the how-to steps

Read at step 7 of every `handoff`, and before saving when the user names another folder or the chat runs in Claude Code on the web or a git worktree.

## Special places to save

**Another folder.** The user can name another folder in plain words ("handoff, and save it in ~/Projects/other", "pickup budget from ~/Projects/first"): for that command, use that folder's `handoffs/`. claude.ai Projects can't see each other's files, so between Projects, post the handoff (see "Without a file store" in SKILL.md).

**Claude Code on the web.** Every session starts from a fresh copy of the branch, so a file saved here doesn't reach the next session on its own. If `handoffs/` is gitignored, the project keeps handoffs out of git: post the handoff, and commit it (`git add -f`) only if the user asks. Otherwise offer to commit and push it, or post it.

**A git worktree.** The file is saved in that worktree only: say so in the reply.

## How-to steps at the end of a `handoff` reply

People forget how their app starts, renames and finds chats, so after the reply's first lines give the steps for the app this chat runs in, with the real names and titles filled in, in the style just used (after `.push`: `/rename pushed.budget`, `.pull budget`). Give the steps for what comes next: continuing in a new chat, or folding into the master.

- **Claude Code:** a code block to type line by line, then one line on getting back to old sessions: "`/clear` keeps this session; `/resume` lists old ones, or run `claude --resume budget` in Terminal." To continue:
  ```
  /rename handed_off.budget
  /clear
  pickup budget
  /rename budget
  ```
  To fold in, the last three lines become two: `/resume` (pick the master), then `fold budget`. These commands work in the terminal and JetBrains. When the session clearly runs elsewhere, give that app's way instead: in the desktop app's Code tab, + New in the sidebar or Cmd+N (Ctrl+N on Windows), click the title to rename it (or ask Claude to), and find old sessions in the sidebar; in VS Code and its forks, the Command Palette's "Open in New Tab", then "Rename Session Tab", and the Session history button for old sessions. In Claude Code on the web, `/clear` and `/resume` don't work: start a new session from the sidebar.
- **claude.ai:** "Start a new chat in this Project and type pickup budget" (without a Project, any new chat), or, to fold in, open the master chat in the sidebar. To rename a chat: hover over it in the sidebar, click ⋮, then Rename; on iPhone, touch and hold it in the chat list; on Android, open it and tap ⋮ at the top right.
