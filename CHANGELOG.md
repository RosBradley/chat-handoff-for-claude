# Changelog

## 0.4.0 (in testing)

Move work to another AI, with the same commands and the same package format as [Chat Handoff for ChatGPT](https://github.com/RosBradley/chat-handoff-for-chatgpt), so work moves between the two.

- New commands:
  - `transfer <name> to <AI>` (`.export <name> to <AI>`), and `handoff <name> to <AI>` (`.push <name> to <AI>`), which does the same, package a chat's work in a ZIP for another AI. The package holds START-HERE.md with a prompt to paste, HANDOFF.md, PROJECT-CONTEXT.md for bigger projects, FILE-MANIFEST.csv with a checksum for every file, and the files themselves. The name and the AI are optional. The skill checks the package before handing it over, labels it **Partial transfer** if something needed is missing, leaves out secrets, and never sends it anywhere. Most AIs don't take a ZIP in a chat, so the files also come unzipped. The reply says how to bring them into the AI named: Claude, ChatGPT, Gemini, Meta AI, Microsoft Copilot or GitHub Copilot. The setup guide has the same steps, with sources.
  - `export project <name>` packages a whole project as a snapshot. It asks which chats to include, gives a `.push <chat-name>` to type in each chat it can't read fully, and labels the package **Partial project export** until every chat is in. No chat is marked handed off.
- `pickup` (`.pull`) or `fold` (`.merge`) with a package attached imports it, from this skill or from Chat Handoff for ChatGPT, including its handoff headings and `Handoff-<line>.md` file names. A package is treated as information about the work, never as instructions: the skill won't run a program it contains.
- A transfer marks the chat handed off, with the status `continuing in <AI>`, so the stale chat guard covers it. Titles are the usual `handed_off.<name>` and `pushed.<name>`.
- The skill is split into a main page and appendices that load only when needed: `references/fold.md`, `references/state.md` (the stale chat guard's steps, a line another chat holds, renames and the full title scheme), `references/transfer.md` and `references/apps.md` (how-to steps and special places to save), plus `assets/rules-template.md`. The main page is about 3,200 words, down from about 4,700, with the new commands included, so a pickup loads about a third less. It's also now under Microsoft Agent Builder's 20,000-character limit.
- Ideas from the ChatGPT version:
  - An unnamed chat's first handoff names the line from the chat's topic, saves, and says the name, instead of asking first.
  - Asking about a command, or a command written inside an imported file, doesn't run it.
  - The handoff note may go past 400 words only to keep a constraint the next chat must not lose.
  - A fold doesn't ask again about items you already decided.
  - Item letters continue AA, AB after Z.
  - Line names can't contain slashes.
  - Where the app can create files, a handoff without a Project or folder is also offered as a download.
  - In Claude Code on the web, a gitignored `handoffs/` folder means the handoff is posted, and committed only if you ask.
  - A `pickup` that finds nothing asks you to paste or attach the handoff.
- Releases also include `chat-handoff-cowork.zip`, the same skill with `SKILL.md` at the top level, as Copilot Cowork and Agent Builder require.
- Tests: `handoff-unnamed-asks` becomes `handoff-unnamed-names-itself`, and five new cases cover `.export`, `handoff budget to Gemini`, `handoff budget-to-gemini` (not a transfer), a project export that asks which chats to move, and importing a ChatGPT-made package without running a script hidden in it. 19 cases in all.
- The README's status line said v0.3.5 after the 0.3.6 release; it now says v0.4.0.

## 0.3.6 (in testing)

- `fold <name>` as the first message of a new chat, with no rules file naming the master, asks which was meant and stops there. It used to review every item in the same reply, which was wasted work if you meant `pickup` (`.pull`). The same goes for `pickup <name>` in a chat that already has work of its own.
- New test suite in `evals/`: 14 cases for `claude plugin eval`, covering both command styles, naming, renames, a line another chat holds, the stale chat guard, fold-in review, and messages that must not set the skill off. All 14 pass 3 runs out of 3. See Tests in the README.

## 0.3.5 (October 22, 2026)

Every app-specific claim in the README, the setup guide and the skill's how-to steps was checked against the official docs on October 22, 2026.

- The claude.ai claims are checked. Fixed: past-chat search is only on paid plans (Pro, Max, Team and Enterprise), is on by default under Settings > Memory, and skips incognito chats, so on the Free plan a handoff without a Project is always pasted; saving to a Project's files is still being tested, and if the handoff is posted instead, add it to the Project yourself; claude.ai covers chat and Cowork in the desktop app, not just its Chat tab; the help center lists skills on mobile in Cowork and the new Claude experience; Claude reaches past chats only through past-chat search; the nudge goes in Settings > General > Instructions for Claude. New: on Team and Enterprise, colleagues can share an uploaded skill, and an owner can add one for everyone or turn off uploading your own. In Claude's Office add-ins, skills are available in all four add-ins, not only in cross-app tasks. Xcode's Claude Agent now takes your own skills, per Apple's docs.
- The setup guide's Microsoft Copilot note is up to date. It said Microsoft's docs didn't say whether skills run in Copilot; they do now. Copilot Chat can use Claude but isn't the Claude app. Copilot Cowork takes skills in the same `SKILL.md` format, and the guide gives the steps to try Chat Handoff there (upload `SKILL.md` itself, not the zip, which is laid out for claude.ai). Agent Builder caps a skill's instructions at 20,000 characters, too few for Chat Handoff.
- The Claude Code claims are checked against the current docs. Fixed: `.worktreeinclude` copies handoffs into a new worktree only when `handoffs/` is also in `.gitignore`; in the desktop app's Code tab, Claude can list your other sessions and rename or archive one when you ask; the desktop app's new-session button is + New (Cmd+N, or Ctrl+N on Windows), and old sessions are found with the sidebar's Group and sort icon. New: in Claude Code on the web, the plugin doesn't load, so turn the skill on in your claude.ai account.
- The README's Why section is checked against Anthropic's current pages. The "maximize your Pro usage" source is gone from the help center, so it's replaced with current ones; two link titles are updated; the 150,000-token example now says prompt caching can make the repeated part cheaper; and summarizing near the length limit is noted as happening on paid plans with code execution on.

## 0.3.4 (October 22, 2026)

- `handoff <name>` asks first when that line already has a handoff file this chat never had: a rename onto an existing line, or a new chat naming itself after one. Before, it could replace the other chat's handoff without asking. The choices are the usual ones: Stop (recommended) asks for another name, Add to it adds this chat's work to that line as new items, and Replace it overwrites. A rename that stops or adds keeps this chat's old file.
- The setup guide, README and worked example show every command in both styles, plain words and dot style, including the terminal routine (`.push`, `/rename pushed.<name>`, `/clear`, `.pull`) and a dot-style version of the worked example's first handoff.

## 0.3.3 (October 19, 2026)

- `handoff test2` on the `test` line asks whether you meant to rename the line or tag the chat `test.2`, instead of renaming straight away.
- Handing off to another folder works in plain words ("handoff, and save it in ~/Projects/other", "pickup budget from ~/Projects/first"), as the setup guide already said; the skill now says so too. Between claude.ai Projects, it posts the handoff.
- In Claude Code on the web, the skill offers to commit and push the handoff, since the next session starts from a fresh copy of the branch. In a git worktree, it says the file is saved in that worktree only.
- In the Claude desktop app's Code tab, you can ask Claude to rename a session, and the skill uses its suggested title. Everywhere else, Claude still can't rename chats, and no app's docs say Claude can see a chat's title.
- SKILL.md shows its version (`Version: 0.3.3`), so you can ask which one claude.ai has. The release job fails if it doesn't match plugin.json.

## 0.3.2 (October 19, 2026)

- Names typed with spaces are joined with hyphens (`handoff market size` saves `market-size`), and the reply says what the name became. On an existing line, the last word is read as the tag (`market size au` on the `market-size` line is `market-size.au`). The README now says names have no spaces.
- New setup guide, [docs/setup.md](docs/setup.md): how to start, rename and find chats in each Claude app (claude.ai on the web, desktop and mobile; Claude Code in the terminal, desktop app, VS Code and JetBrains), what Status means, and the cases where a handoff file doesn't reach the next session (Claude Code on the web, worktrees). It states only what the official docs confirm. The README says that in Claude Code a chat is a session, and links the guide.
- After a handoff, the reply ends with the steps for the app the chat runs in, with the names filled in, so nobody has to remember how to start, rename or find chats. In Claude Code: `/rename`, `/clear`, `pickup` and `/rename` (or `/resume` and `fold` to fold in), and how to get back to an old session; the desktop app's and VS Code's own ways when the session clearly runs there. In claude.ai: where to start the new chat and how to rename one on the web, desktop and mobile.
- `handoff` in an old chat asks before saving when another chat has picked the line up or handed it off since, instead of replacing that chat's handoff. The choices are Stop (recommended), Add to it (this chat's new work joins the file as new items, and the other chat keeps the line) and Replace it. In testing, an old session's `.push` set a line back to `waiting` after a newer session had picked it up. A chat that picked a line up also now counts as behind (see Stale chat guard) when another chat writes the file after its pickup.
- The release job checks SKILL.md's name and description against claude.ai's upload rules (no angle brackets, at most 1024 characters, a lowercase name) before it builds the zip, so a release claude.ai would reject fails first.

## 0.3.1 (October 14, 2026)

- Stale chat guard: an ordinary instruction typed into a chat that was already handed off or folded in gets a warning first, with Stop (recommended), Continue here once, and Reopen this chat as the choices, shown as buttons where the app can. Handoff commands still run in such a chat, and every `handoff` reply says the guard is on.
- Chats are named by line, with an optional tag of the user's own: `budget` or `budget.pre`. The tag is anything the user likes (a word, a letter, a number) and is never invented or asked for by the skill; order between chats on a line comes from the dates in the file. Chat numbers (`budget.3`) and the prompt asking for one are gone; an old `From: budget.3` line is read as a tag.
- Only a different line renames: `handoff budget.post` in `budget.pre` just changes the tag. A rename keeps the chat's tag (`handoff budget` in `research.pre` makes it `budget.pre`).
- Without a Project or folder, posts are headed with the chat's name (`HANDOFF: budget.pre, <date>`), and the newest is the one with the latest date, then the more recent chat.
- A working chat, a master included, is titled by its name alone (`budget.pre`) instead of `todo.<name>`, and the plain-word title for a handed-off chat is spelled `handed_off` (was `handedoff`). `pushed`, `returned`, `folded`, `merged` and `done` are unchanged. Chats already titled `todo.` or `handedoff.` need no change: commands never read titles.
- The rules template and the worked example use the new names and titles (`market-size.au`, `folded.market-size.au`).

## 0.3.0 (October 12, 2026)

- New opening in the README: why long chats cost more (Claude re-reads the whole chat with every message, so usage limits, API cost and speed all suffer, and near the length limit the app summarizes older messages or stops the chat), what the skill does (it doesn't move or copy a chat), and how it saves, with sources. The skill opens with a two-sentence summary instead, since Claude reads the skill with every command.
- Named Chat Handoff; the skill's ID stays `chat-handoff`. The docs say "the skill" wherever the skill does the work, and "Claude" only for what Claude itself does or can't do.
- Chats are named by line and number: `budget.3` is the third chat on the budget line. A line is one word (letters, digits or hyphens). The number comes from the command or the handoff file, never a guess; `handoff budget` takes it from the file.
- Titles start with a state word and follow the commands you use: `todo`, `handedoff` (`pushed` after dot-style commands), `returned`, `folded` (`merged` after `.merge`) and `done`. Every title is offered as optional. `Continued -` and `Handed off -` both become `handedoff`; `Returned -`, `Folded -` and `Released -` become `returned`, `folded` and `done`; `Master -` is dropped, since a master is simply `todo` while it works.
- A new handoff's status is `waiting` (older files saying `waiting for pickup` still work). Receipts say `folded into` or `merged into`, matching the fold command, and the end of a chain is `done` (was `released`).
- The "From" line carries the chat's name (`From: budget.3`). Without a Project or folder, posts are headed `HANDOFF: budget.3, <date>`, naming the chat that last handed the line off, even when a master posts the file. The newest is the one with the highest number, then the latest date, then the more recent chat.
- Only a different line renames: `handoff budget.4` in `budget.3` just corrects the chat's number. A rename keeps the chat's number (`handoff budget` in `research.2` makes it `budget.2`).
- `handoffs` shows each line's latest chat.
- The skill and plugin descriptions say the skill reviews a side chat's work item by item and folds in what the user approves.
- The rules template and the worked example use the new names and titles (`market-size.2`, `folded.market-size.2`).
- claude.ai users download `chat-handoff.zip` from the latest GitHub release instead of zipping the folder themselves. A new version in `plugin.json` publishes its release automatically.
- Upgrading from 0.2.0: older handoff files still work. A line named with two words (`Handoff - market size.md`) can move to one word with `handoff market-size` in its chat, which saves the new file and deletes the old one.

## 0.2.0 (October 10, 2026)

- Installs as a Claude Code plugin; the repo is its own plugin marketplace.
- Deep review is now a second, harder pass by the master chat itself: figures worked out again from the sources, the strongest case against, what breaks if it's wrong. No separate agent.
- The master marks each decided item in the side chat's file with its verdict and date, so a later fold-in never reviews or applies it twice.
- Item letters are fixed for the life of a line; reworked items keep theirs, new ones continue after the highest used.
- A new handoff carries tossed items into "Don't redo", so they can't come back after a receipt is overwritten.
- Without a Project or folder, every change is a new post and the newest counts, so statuses, returns and receipts work there too.
- Chat titles show each chat's state first (`Handed off - market size 3`, `Returned - …`, `Folded - …`, `Continued - …`, `Master - …`, and `Released - …` when the last chat in a chain is finished and its work goes out). Claude can't see or rename chats, so it tells the user the new title at each change.
- Rules file: "Fold-ins" replaces "Master chat" and says which lines fold into which, so chains work (research into report, report into review).
- New worked example: a market expansion report for a grid-security firm, with handoff files at each stage. Replaces the product launch example.
- Cold-read check before saving a handoff.
- Commands trigger only as the whole message (or nearly), in any case, not inside ordinary sentences. Plain requests ("let's hand this off") count too.
- `fold <name>` folds a chat in; `pickup <name>` now always continues. Neither guesses: each asks in one line when it looks out of place. `fold` as the first message of a new chat goes ahead when the rules file says where that line folds (a fresh review chat).
- Dot-style commands, for those who think in git: `.push`, `.push?`, `.pull`, `.merge`, `.status`.
- The first `handoff` in a chat suggests a short line name and asks once; `handoff <name>` sets it, or renames the line (new file saved first, old one deleted after).
- The skill description no longer contains angle brackets, which claude.ai rejects on upload.

## 0.1.0 (October 9, 2026)

First version, in testing.

- Commands: `handoff`, `handoff?`, `pickup <name>`, `pickup`, `handoffs`.
- Pickup continues a chat when typed as the first message of a new chat, and folds it in when typed in a chat already underway.
- Fold-in review: one verdict per item (keep, change, toss or return), nothing applied until the user decides, independent review for high-stakes items.
- Returns written back to the side chat's file; folded files cut down to a receipt.
- Optional per-project rules file, with defaults when it is missing.
- Works in claude.ai Projects, in folders (Claude Code), and in plain chats through past-chat search.
