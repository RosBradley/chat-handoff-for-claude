# Fold in: `fold <name>` (`.merge <name>`)

Read for `fold` and `.merge`. A fold that brings in a handoff package from another AI starts with "Import" in `references/transfer.md`, then continues here with the package's HANDOFF.md as the side chat's file.

This chat is the master, and the skill is its reviewer: a second set of eyes on work this chat did not build. The side chat's conclusions are claims to test, not facts. Scrutinize; don't rubber-stamp. The user's part is the decision (step 4).

1. **Read** the handoff and the files it points to. Review only items without a verdict mark; marked items are already settled.
2. **Review every unmarked item:** check numbers against the current sources and rerun the math where figures matter; look for conflicts with settled decisions or other parts of the work; flag anything missing, or stale against "Built on"; apply the rules file's review checks.
3. **Deep review** for items that hit the rules file's triggers, or that are high-stakes or hard to reverse. Do a second, harder pass yourself: work the figures out again from the source files, not from the handoff; make the strongest case against the item; ask what breaks, and for whom, if it's wrong. Tag these verdicts "(deep review)".
4. **One verdict per item, one line each:** Keep; Change (to what); Toss (why); or Return (what the side chat must do, when it needs real work such as new research). Then stop and discuss. Nothing is applied until the user decides, usually in one line ("keep A to H, change C, toss I"). If the user already decided some items in this chat, apply those without asking again; never ask twice for the same decision.
5. **Apply what the user approved** where the rules file says approved items go (re-read that file right before saving, in case another chat changed it), and make the agreed changes. If the changes saved but marking the side chat's file (step 6) fails, say so, and on a retry check the receiving files first so nothing goes in twice.
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

   For a side chat whose package came from another AI, keep the receipt in this place's copy of its file; don't claim to update the chat in the other AI.

9. **Done:** if this chat folds into no other line (per the rules file, or because the user says it's the end) and nothing is waiting, returned or open, say the work is complete and where it is, and suggest the optional title `done.<name>` for this chat once the work goes out. If this line has a handoff file, set its status to `done, <date>`.
