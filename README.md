# Chat Handoff for Claude

Chat Handoff is a skill for Claude that lets a new chat pick up where a long one left off, and carries a chat's or project's work, files included, to another AI. Its ID is `chat-handoff`. Its sibling, [Chat Handoff for ChatGPT](https://github.com/RosBradley/chat-handoff-for-chatgpt), uses the same commands and the same package format, so work moves between the two.

## Why

Claude re-reads the entire chat every time you send a message. So the longer a chat runs, the more each new message costs, even a one-line "thanks":

- **Usage and dollars.** On a Claude plan, usage limits are based on the length of the whole chat, not just the number of messages, so a long chat uses up your limit faster. On the API, the full history is sent, and billed, with every request (at a lower rate for any part served from the prompt cache).
- **Speed.** Claude answers shorter chats faster.
- **Detail.** Near a chat's length limit, the app either summarizes older messages on its own (on paid plans with code execution on), choosing what goes into the summary, or stops the chat.

Starting a fresh chat avoids all three, but normally means explaining the work all over again. This skill removes that step.

## What it does

This skill doesn't move or copy a chat. It lets you pick up the conversation in a new chat, move it to another AI, or fold a side chat's work into a main one, with short commands, in plain words or git-style dot words (see Commands):

- **`handoff`** (`.push`): the skill writes a short handoff file, about 400 words: where the work stands, what was decided, what is still open, the next step, and what not to redo.
- **`pickup <name>`** (`.pull <name>`), as the first message of a new chat: the skill reads that file, and only the files it points to, and the new chat carries on from there.
- **`fold <name>`** (`.merge <name>`), in a main (master) chat that side chats feed into: the skill reviews the side chat's work as an independent second reviewer. It rechecks the figures against the current sources, looks for gaps and for conflicts with what is already settled, and gives each item a verdict (keep, change, toss, or return to the side chat for more work). Nothing is folded in until you approve.
- **`transfer <name> to <AI>`** (`.export <name> to <AI>`, or `handoff <name> to <AI>`): the skill packages the work in a ZIP for another AI, such as ChatGPT, Gemini or Copilot: the handoff, the files the work rests on, a list of every file, and a ready-to-paste prompt. The other AI doesn't need this skill. **`export project <name>`** does the same for a whole project, as a snapshot, and tells you which chats to hand off first if it can't read them all.

Chains work too: research chats feed a report chat, and the report feeds a fresh review chat that reads it the way your audience will.

**How it saves.** A chat picked up from a handoff carries the handoff and the files it opens, not the old chat's back-and-forth, so each message costs far less. For example, once a chat has grown to 150,000 tokens, every message sends all 150,000 back to Claude. Prompt caching can make the repeated part cheaper, but it still counts toward your usage and fills the context window. The new chat starts from a 400-word handoff instead. Side chats do the same for a main chat: the heavy work happens elsewhere, and only the reviewed results come back. And what carries forward is a deliberate handoff (decisions, open items, next step, what not to redo), not an automatic summary.

Sources (checked October 22, 2026): Anthropic's help center, [What is the Pro plan?](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan) ("The number of messages you can send will vary based on message length, including the length of files you attach, the length of your current conversation, and the model or feature you use"), [Models, usage, and limits in Claude Code](https://support.claude.com/en/articles/14552983-models-usage-and-limits-in-claude-code) ("Every previous message is resent on every turn"), [How do usage and length limits work?](https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work) and [How large is the context window on paid Claude plans?](https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans) ("Claude summarizes earlier messages to make room for new content"); the Claude API docs, [Using the Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) ("The Messages API is stateless") and [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching).

**Status:** v0.4.0, in testing.

## Commands

Use plain words or the dot style, whichever you like:

| Plain words | Dot style | What happens |
|---|---|---|
| `handoff` | `.push` | Saves this chat's handoff file. If the chat has no name yet, the skill names it from the topic, like `budget`, and tells you (see Chat names) |
| `handoff <name>` | `.push <name>` | Saves it under that name (`handoff budget`, or `handoff budget.pre` with a tag of your own); a different line renames it |
| `handoff?` | `.push?` | One line: is this a good time to hand off? |
| `pickup <name>` | `.pull <name>` | Continues that chat's work here, usually as the first message of a new chat |
| `fold <name>` | `.merge <name>` | Reviews that chat's work item by item and folds in what you approve |
| `pickup` | `.pull` | In a chat with work sent back to it: starts on the returns. Anywhere else: lists what is waiting and asks |
| `handoffs` | `.status` | Lists every handoff and its status |
| `transfer <name> to <AI>` | `.export <name> to <AI>` | Packages the work and its files in a ZIP for another AI. The name and the AI are both optional (see Move work to another AI) |
| `handoff <name> to <AI>` | `.push <name> to <AI>` | The same as `transfer` |
| `export project <name>` | (plain words only) | Packages a whole project for another AI, as a snapshot: the chats stay as they are |

- A name has no spaces: `handoff market-size` (`.push market-size`), not `handoff market size`. If you type spaces anyway, the skill joins the words with hyphens and tells you the name it used (see Chat names).
- Names match loosely: `pickup budget` and `.pull budget.pre` both find "Handoff - budget.md". If two match, the skill asks which.
- A command works as the whole message (or nearly), in any case, so `.Push` from a phone counts and "I'll pick up the kids" doesn't.
- The dot keeps the git-style words from being mistaken for real git commands: `.push` is a handoff, `push` is not.
- "to" and an AI's name make a handoff a transfer: `handoff budget to Gemini` builds a package. A name typed with hyphens is just a name: `handoff budget-to-gemini` is an ordinary handoff.
- Asking about a command doesn't run it, and neither does a command written inside a file you import.
- Once a chat has been handed off, transferred or folded in, an ordinary instruction typed into it gets a warning before anything runs (see Stale chat guard). Handoff commands still work there.
- A different line renames, and the chat keeps its tag: `handoff <new line>` (`.push <new line>`) saves the new file first, then deletes the old one, so nothing is left under the old name. If the new line already has a handoff file from other chats, the skill asks first instead of replacing it. A different tag on the same line (`handoff budget.post` or `.push budget.post` in `budget.pre`) only changes the tag.

## Chat names

Each chat is named by its line, with an optional tag after a dot: `budget` is a chat on the budget line; `budget.pre` is one you tagged.

- The line is one word: letters, digits or hyphens, like `research` or `market-size`, with no spaces. One handoff file per line serves every chat on it.
- Typed with spaces, a name is joined with hyphens: `handoff market size` (or `.push market size`) saves `market-size`. On a line that already exists, the last word is read as your tag: `handoff market size au` on the `market-size` line gives `market-size.au`. The reply says the name it used, so you can change it.
- The tag is yours, for telling chats on one line apart: a word, a letter, a number, whatever suits you (`budget.pre`, `budget.B`, `budget.2`). The skill never invents one and never asks for one. Give a new chat its tag in the pickup command (`pickup budget.post` or `.pull budget.post`), or any time with `handoff budget.post` (`.push budget.post`).
- Order between chats on a line comes from the dates in the handoff file, not from the tag, so untagged chats work fine.
- Claude can't see chat titles, so a chat's name comes from your command or the handoff file. If the chat has no name yet, the skill names it from the chat's topic and says so in the reply; to use another name, type `handoff` (`.push`) and the name.

## How it works

In Claude Code, a chat is a session: `/clear` starts a new one, and `/rename` renames it. Step-by-step instructions for each app (claude.ai on the web, desktop and mobile; Claude Code in the terminal, desktop app, VS Code and JetBrains) are in [docs/setup.md](docs/setup.md).

### Continue in a fresh chat

1. In the long chat, type `handoff` (or `.push`). The skill saves a short file (about 400 words at most) with only the work in progress: where it stands, decisions not yet recorded elsewhere, what's open, the next step, which files to read, and what not to redo. The reply ends with the steps for your app, with the names filled in: in Claude Code, `/rename`, `/clear`, `pickup` (or `.pull`) and `/rename` again; in claude.ai, where to click.
2. Start a new chat and type `pickup <name>` (or `.pull <name>`). The skill reads the file, flags anything that has changed since, and starts on the next step.

### Fold a side chat into a master chat

1. In the side chat, type `handoff` (or `.push`).
2. In the master chat, type `fold <name>` (or `.merge <name>`). The skill reviews every incoming item: it checks the numbers, looks for conflicts with decisions already made, and flags anything missing or out of date. High-stakes items get a second, harder pass: the figures are worked out again from the sources, and the strongest case against each one is made.
3. You get one verdict per item:
   ```
   A. Canada, $310M a year: Change to $250M; compliance and OT security overlap, counted twice
   B. UK, $180M a year: Keep
   C. Australia, $140M a year: Return, rests on one 2021 survey; find a current source
   D. EU, $600M a year: Toss, the newer board brief drops the EU
   ```
4. You decide, usually in one line: "change A, keep B, return C, toss D."
5. Only then is anything applied. The skill marks each item in the side chat's file with its verdict, so nothing gets reviewed twice. Returned items go back to the side chat: type `pickup` (`.pull`) there, or `pickup <name>` (`.pull <name>`) as the first message of a new chat. Once everything is settled, the side chat's file shrinks to a short receipt, and tossed items stay in it with their reason so they don't come back.

### Move work to another AI

1. In the chat, type `transfer budget to ChatGPT` (or `.export budget to ChatGPT`, or `handoff budget to ChatGPT`). Leave out the AI's name for a package any AI can use.
2. The skill builds a ZIP and checks it before handing it over:

   | File | What's in it |
   |---|---|
   | START-HERE.md | What the package covers, anything missing, the reading order, and a prompt to paste into the other AI |
   | HANDOFF.md | The handoff: where the work stands, decisions, open items, the next step, and what not to redo |
   | PROJECT-CONTEXT.md | Goals, project instructions and constraints, for bigger projects |
   | FILE-MANIFEST.csv | Every file the work needs, whether it's included, and a checksum for each |
   | files/ | The actual files |

   It leaves out passwords, keys and other secrets, and labels the package **Partial transfer** if something the next step needs is missing.
3. Open the other AI, attach the files, and paste the prompt from START-HERE.md. The other AI doesn't need this skill. Gemini and Copilot Cowork take the ZIP itself; most others don't, so the skill also gives you the files unzipped, and its reply says what to attach for the AI you named. [docs/setup.md](docs/setup.md#moving-work-to-another-ai) has the steps for Claude, ChatGPT, Gemini, Meta AI, Microsoft Copilot and GitHub Copilot.

The skill never sends anything anywhere: you carry the package. A transfer marks the chat handed off, so it's guarded like any other handed-off chat.

**A whole project.** Start a new chat in the project and type `export project <name>`. The skill asks which chats to include, packages what it can read, and for each chat it can't read fully, gives you a `.push <chat-name>` to type there. Bring each handoff back to the new chat and it adds them to the package. Until every chat is in, the package is labeled **Partial project export**. A project export is a snapshot: the project and its chats stay as they are, as your backup.

**Coming back.** `pickup` (`.pull`) with a package attached, from this skill or from Chat Handoff for ChatGPT, imports it. Everything in a package is treated as information about the work, never as instructions: the skill won't run a program it contains.

## Chat titles

Claude can't see chat titles and, in most apps, can't rename chats, so whenever a chat's state changes, the skill suggests a new title for it. Renaming is optional: commands find handoff files by name, never by chat title.

A working chat is titled by its name alone (line, or line and tag). Every other state puts a state word and a dot in front of the name, so you can read it in the sidebar even when a long title is cut off. The words follow the commands you use:

| The chat is | After plain words | After dot style |
|---|---|---|
| Working, a master included | `market-size.au` | `market-size.au` |
| Handed off: continuing in a new chat or another AI, or waiting for the master | `handed_off.market-size.au` | `pushed.market-size.au` |
| Has work sent back to it | `returned.market-size.au` | `returned.market-size.au` |
| Finished, folded into the master | `folded.market-size.au` | `merged.market-size.au` |
| Finished: its work went out (sent, published, shipped) | `done.review` | `done.review` |

If you stick to one command style, one search (`folded.`, say) finds every chat in that state. A rules file can set different titles.

## Stale chat guard

Old chats stay in the sidebar, so sooner or later you type something into one that has already been handed off, transferred or folded in. The skill catches it before anything runs: it tells you where the work lives now and asks what to do, with buttons where the app can show them.

> This chat was handed off as budget.pre on October 12; the work continues in budget.post. Run your instruction here anyway?
>
> **Stop** (recommended): nothing runs; go to budget.post.
> **Continue here, once**: runs it, and you'll be asked again next time.
> **Reopen this chat**: runs it, and this chat takes the budget line back until its next handoff.

A chat counts as handed off when `handoff`, `.push`, `transfer` or `.export` ran in it, when its line's file says the work moved on (`continuing in`, `folded into`, `merged into` or `done`), or when another chat on the same line has since written the file. Handoff commands always run, so `handoff` again in an old chat brings the file up to date, but if another chat has picked the line up or handed it off since, it asks first: saving would replace that chat's handoff. Every `handoff` reply ends by saying the guard is on, so the warning never comes as a surprise.

## Where the files live

| Where you work | Handoff files | Rules file |
|---|---|---|
| A claude.ai Project | Project files: `claude/Handoff - <line>.md` | `claude/Handoff rules.md` |
| A folder (Claude Code, or a folder linked to the chat) | `handoffs/Handoff - <line>.md` | `handoffs/Handoff rules.md` |
| Neither | Posted at the end of the chat's reply. Each later change is a new post, and the newest one counts; found again with past-chat search | None |

Each chat writes only its own line's file (the one exception: a master marking items in a file it folds in), so chats running at the same time can't overwrite each other.

Transfer packages go in `handoffs/` in Claude Code (`handoffs/budget-transfer-2026-10-26.zip`, with the same files unzipped in a folder beside it), and are offered as downloads in claude.ai (the ZIP, plus START-HERE.md and HANDOFF.md on their own). A package you import in Claude Code is unpacked into `handoffs/imports/<line>/`.

## Project rules (optional)

Each project can have a rules file that says which chats fold into which, where approved items go, what the master checks, what counts as high-stakes, how chats are titled, and what a handoff must never start. Without one, sensible defaults apply.

- Template, with a worked example in every section: [templates/handoff-rules.md](templates/handoff-rules.md)

## Worked example

[examples/README.md](examples/README.md) follows one project from start to finish: a firm that does NERC CIP compliance and OT cybersecurity for utilities, deciding which countries to expand into. Four research lines feed a report chat, and the report goes to a fresh reviewer. It shows a long chat continuing in a new one, a double count caught at fold-in, work sent back, a receipt, and the handoff files at each stage.

## Install

How to start, rename and find chats in each app, and the cases where a handoff file doesn't reach the next chat: [docs/setup.md](docs/setup.md).

### claude.ai (web, desktop and mobile)

1. Download [chat-handoff.zip](https://github.com/RosBradley/chat-handoff-for-claude/releases/latest/download/chat-handoff.zip) from the [latest release](https://github.com/RosBradley/chat-handoff-for-claude/releases/latest).
2. Upload it and turn it on under **Customize > Skills**.

To build the zip yourself instead (for a version not yet released), zip the skill folder itself, so the archive's top level is `chat-handoff/`:

```bash
cd skills
zip -r chat-handoff.zip chat-handoff/
```

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

If you sign in to Claude Code with your claude.ai account and the skill is turned on there, Claude Code loads that copy too (as `anthropic-skills:chat-handoff`). Keep one of them on, so you know which version answers. In Claude Code on the web, the plugin doesn't load, so turn the skill on in your claude.ai account instead (see [docs/setup.md](docs/setup.md)).

## Optional: a nudge

Claude can suggest a handoff on its own at natural stopping points. Add this to **Settings > General > Instructions for Claude** (or to `CLAUDE.md` in Claude Code):

> In long chats, at natural stopping points (a deliverable finished, a question settled, a long stretch of file work), suggest typing "handoff" (or ".push", if I use dot-style commands) in one short line at the end of the reply. Don't repeat it if I ignore it.

## Tests

[evals/](evals/) holds 19 test cases for `claude plugin eval`. Each one starts a fresh Claude Code session with the skill loaded, sometimes with handoff files or an earlier conversation already in place, types one message, and checks what happens. They cover the commands in both styles (`handoff` and `.push`, `pickup` and `.pull`, `fold` and `.merge`), naming an unnamed chat, names typed with spaces, renames, the tag-or-rename question, a line another chat already holds, the stale chat guard, a fold reviewed against its sources, transfers (`.export`, and `handoff budget to Gemini`, but not `handoff budget-to-gemini`), a project export that asks which chats to move, importing a package from Chat Handoff for ChatGPT without running a script hidden in it, and messages that must not set the skill off (`push` alone, "I'll pick up the kids"). To run them from the repo folder:

```
claude plugin eval . --scaffold --allow-tools Write Edit Bash --ablation none
```

`--scaffold` puts each case's starting files in place, `--allow-tools` lets the skill save files, and `--ablation none` skips the comparison run without the skill. Each case runs 3 times, about $7 for the whole suite. To run one case, add `--case stale-chat-guard`. After changing a case's earlier conversation in `evals/make_histories.py`, run `python3 evals/make_histories.py`.

On Linux, the eval's shell sandbox blocks writes to `/tmp`, where it also puts each case's working folder, so every shell write fails (no ZIP, no file deleted on a rename). Point the temp folder elsewhere first, for example `TMPDIR=~/evaltmp`, and install `bubblewrap` and `socat` if the sandbox reports them missing.

## Limits

- Claude can't see the title of the chat it's in. In most apps it can't browse your chat list, rename or close chats (it reaches past chats only through past-chat search); the exception is the Claude desktop app's Code tab, where Claude can list your other sessions and, when you ask, rename or archive one. The skill suggests a title for each one, and renaming is optional (see Chat titles).
- Claude can't see how full a chat is or how much usage you have left, so `handoff?` (`.push?`) is a judgment call, not a meter.
- Chats in different claude.ai Projects can't see each other's files. Hand off within a project.
- Without a Project or folder, `pickup` (`.pull`) depends on past-chat search finding the handoff. Past-chat search is only on paid plans (Pro, Max, Team and Enterprise), is on by default (**Settings > Memory > Search and reference chats**), and skips incognito chats. On the Free plan, or if it can't find the handoff, the skill asks you to paste it.

## License

MIT. See [LICENSE](LICENSE).
