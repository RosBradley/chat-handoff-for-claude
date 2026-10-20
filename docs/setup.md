# Using Chat Handoff in each Claude app

The commands are the same everywhere, in plain words or dot style (`handoff` or `.push`, `pickup` or `.pull`, `fold` or `.merge`). What changes from app to app is where the handoff file is kept, and how you start, rename and find chats.

**A chat** here means any conversation with Claude. In Claude Code, it's a session.

| | Where the handoff is kept | A chat is |
|---|---|---|
| **claude.ai**: web, desktop app (Chat tab), iPhone and Android | The Project's files, or posted in the chat when there's no Project | A chat in the sidebar |
| **Claude Code**: terminal, desktop app (Code tab), VS Code and its forks (Cursor and others), JetBrains | `handoffs/` in your project folder | A session |

## The routine (any app)

1. In the chat you're leaving, type `handoff`. The first time, the skill suggests a name for the work, such as `forest-density`. If it doesn't fit, reply with your own, or name it yourself from the start: `handoff forest-density`.
2. Start a new chat in the same Project or folder.
3. Type `pickup forest-density`, or just `pickup` to see a list of what's waiting.

Along the way, the skill suggests a title for each chat: `handed_off.forest-density` for the old one, `forest-density` for the new one. Renaming is optional. Commands find handoffs by file name, never by chat title. You don't have to remember how: after a handoff, the reply lists the steps for your app, with the names filled in.

**One name per piece of work.** A name is one word: letters, digits or hyphens. If you type spaces, the skill joins the words with hyphens (`handoff forest density` saves `forest-density`) and tells you the name it used. Every chat on that work shares one file, and `pickup forest-density` always gets the latest. Don't fold a number into the name: `handoff forest-density2` would rename the work, so the skill asks first whether you meant the tag `forest-density.2`.

**Tags are yours, and optional.** To tell chats on the same work apart, add a tag after a dot: `pickup forest-density.v2`. The skill never invents a tag. On work that already has a file, a last word typed with a space is read as the tag: `handoff forest density v2` gives `forest-density.v2`.

**Several pieces of work at once:** each gets its own name and file. `handoffs` lists them all with their status.

**What Status means.** It changes only when you type `handoff`, `pickup` or `fold`. Renaming a chat doesn't change it.

| Status | Means |
|---|---|
| `waiting` | No chat has picked it up yet |
| `continuing in forest-density.v2` (or `in a new chat`) | A newer chat has it |
| `returned from <name>` | The master sent work back; type `pickup` in that chat |
| `folded into <name>` (or `merged into`) | Finished: the master took it in |
| `done` | Finished: the work went out |

**Hand off only from the newest chat.** Once the work has been picked up, the old chat is finished. An ordinary instruction typed there gets a warning first (see Stale chat guard in the [README](../README.md#stale-chat-guard)). A `handoff` typed there asks first, since saving would replace the newer chat's file.

## claude.ai (web, desktop app Chat tab, mobile)

- **Turn it on:** download `chat-handoff.zip` from the [latest release](https://github.com/RosBradley/chat-handoff-for-claude/releases/latest), then upload it and turn it on under **Customize > Skills** on the web. Code execution must be on. Skills work on the Free, Pro, Max, Team and Enterprise plans. The help center doesn't yet say whether a skill turned on on the web also runs in the mobile apps.
- **Where the handoff goes:** in a Project, the skill saves it to the Project's files. (This is still being tested: the help center doesn't describe Claude saving Project files. If the handoff is posted in the chat instead, copy it into the new chat.) Without a Project, the skill posts it at the end of its reply, and `pickup` finds it with past-chat search, which has to be on in your settings. If search can't find it, paste the handoff into the new chat.
- **New chat:** start it in the same Project, or it won't see the file.
- **Rename a chat** (optional): on the web and in the desktop app, hover over the chat in the sidebar, click ⋮, then Rename. On iPhone, touch and hold the chat in the chat list, then Rename. On Android, open the chat, tap ⋮ at the top right, then Rename.
- **Find an old chat:** in the sidebar on the web and desktop, or in the chat list on mobile.

## Claude Code

- **Turn it on:** install the plugin (see [Install](../README.md#claude-code)), or copy `skills/chat-handoff/` into `~/.claude/skills/`.
- **Where the handoff goes:** `handoffs/` in the project folder. To keep handoffs out of git, add `handoffs/` to `.gitignore`.

| App | Start a new session | Rename it (optional) | Find an old one |
|---|---|---|---|
| Terminal | `/clear` (the old session is kept), or quit and run `claude` | `/rename forest-density` | `/resume` for a list, `claude --resume forest-density` (`-r`), or `claude --continue` (`-c`) for the latest |
| Desktop app, Code tab | + New session, or Cmd+N | Click the title at the top of the session, or ask Claude to rename it | The sidebar, which has search |
| VS Code, Cursor and other forks | Command Palette: "Open in New Tab" or "Open in New Window" | "Rename Session Tab", or open Session history, hover over the session, then Rename | The Session history button at the top of the Claude panel |
| JetBrains | The plugin runs the terminal version in the IDE's terminal, so use the terminal commands | Same as the terminal | Same as the terminal |

In the terminal, the whole routine, with the optional renames, is five lines:

```
handoff forest-density
/rename handed_off.forest-density
/clear
pickup forest-density
/rename forest-density
```

**Two cases where the file doesn't reach the next session:**

- **Claude Code on the web** (claude.ai/code). Every session starts from a fresh copy of your GitHub branch, not your local folder, so uncommitted files and anything in `.gitignore` aren't there. Ask Claude to commit and push the handoff ("handoff, and commit and push it"; if `handoffs/` is in `.gitignore`, that takes `git add -f`), then start the new session on that branch. Or post the handoff and paste it. `/rename` works there, but `/clear` and `/resume` don't.
- **Worktrees**, such as the desktop app's worktree option. Each worktree is a separate copy of the project, so a handoff saved in one isn't in another. Start sessions that hand off to each other without a worktree, or add a `.worktreeinclude` file containing `handoffs/**` to the project. That copies handoffs into a new worktree when it's created, but not afterwards. Removing a worktree deletes its folder, along with any handoff saved only there.

## Handing off to another project folder

`handoff` saves into the folder you're working in, and `pickup` looks only there. To move work between folders, say so in plain words:

- In the old session: "handoff, and save it in ~/Projects/other/handoffs". Claude Code may ask your permission before writing outside the folder.
- Or in the new session: "pickup forest-density from ~/Projects/first/handoffs".
- Or move the file yourself.

In claude.ai, Projects can't see each other's files, so hand off within a Project, or paste the handoff.

## Other apps

- **The Excel, PowerPoint, Word and Outlook add-ins:** skills turned on in your Claude settings apply during cross-app tasks, and Claude works only with files open in the app. A handoff file may not carry over between sessions, so copy and paste it (see below).
- **Xcode** (Claude Agent, in Xcode 26.3) and **Microsoft 365 Copilot:** the official docs don't yet say whether skills run there. Copy and paste the handoff.

**Anywhere, as a last resort:** say "handoff, and post it here", copy what the skill posts, and paste it into the new chat after `pickup`.

## Sources (checked October 11, 2026)

- Claude Code sessions: https://code.claude.com/docs/en/sessions
- Claude Code skills: https://code.claude.com/docs/en/skills
- Desktop app: https://code.claude.com/docs/en/desktop
- VS Code: https://code.claude.com/docs/en/vs-code
- JetBrains: https://code.claude.com/docs/en/jetbrains
- Claude Code on the web: https://code.claude.com/docs/en/cloud-environments
- Skills in claude.ai: https://support.claude.com/en/articles/12512180-use-skills-in-claude
- Renaming chats: https://support.claude.com/en/articles/8230524-delete-or-rename-a-conversation
- Projects: https://support.claude.com/en/articles/9517075-what-are-projects
- Xcode: https://www.anthropic.com/news/apple-xcode-claude-agent-sdk
- Office add-ins: https://claude.com/docs/office-agents/overview.md and https://claude.com/docs/office-agents/connectors-and-skills.md
