# Worked example: taking a grid-security firm international

Sablewire Grid Solutions does IT/OT engineering, NERC CIP compliance and OT cybersecurity for electric utilities in the US. Its board wants a report on which new markets to enter, in the rest of North America and abroad. (The company is made up, and so is every figure below.)

The work runs across seven chats in one claude.ai Project:

```
market-size  ─┐
regulations  ─┤
competitors  ─┼─►  report  ─►  review
interviews   ─┘
```

- Four research lines work in parallel, one question each. Market size takes two chats (the second one tagged `au`, since it starts on Australia), so there are seven chats in all.
- **report** receives their work. It checks every finding before it goes into the draft.
- **review** is a fresh chat that has never seen the drafting. It reads the finished draft the way the board will.

The project's rules file is [templates/handoff-rules.md](../templates/handoff-rules.md). The handoff files are in [claude/](claude/), where they'd sit in the Project.

The walkthrough uses plain words. Every command has a git-style twin (`.push?`, `.push`, `.pull`, `.merge`, `.status`), and the skill answers in whichever style you type; section 1 shows the same handoff both ways. After dot-style commands, the titles it suggests say `pushed` and `merged` where this walkthrough says `handed_off` and `folded`.

## 1. A long chat continues in a fresh one

`market-size` has worked through a stack of industry reports and is getting slow. Canada and the UK are sized; Australia is half done.

```
You:     handoff?
Claude:  Yes. The chat is long, and Australian generation is a clean place to start fresh.

You:     handoff
Claude:  Use market-size as this chat's handoff name? Reply yes or give another.

You:     yes
Claude:  Saved claude/Handoff - market-size.md.
         To continue: type "pickup market-size" as the first message of a new chat.
         To fold it into the report instead: type "fold market-size" in the report chat.
         Optional: rename this chat handed_off.market-size, and title the new one market-size.
         How: start a new chat in this Project and type "pickup market-size". To rename a
         chat, hover over it in the sidebar, click ⋮, then Rename.
```

In dot style, with the name typed in the command so the skill doesn't need to ask:

```
You:     .push?
Claude:  Yes. The chat is long, and Australian generation is a clean place to start fresh.

You:     .push market-size
Claude:  Saved claude/Handoff - market-size.md.
         To continue: type ".pull market-size" as the first message of a new chat.
         To fold it into the report instead: type ".merge market-size" in the report chat.
         Optional: rename this chat pushed.market-size, and title the new one market-size.
         How: start a new chat in this Project and type ".pull market-size". To rename a
         chat, hover over it in the sidebar, click ⋮, then Rename.
```

The skill asks for a chat's name only once, the first time it needs one; the rest of this walkthrough leaves that step out. The file it saved: [Handoff - market-size.md](claude/Handoff%20-%20market-size.md). About 200 words: where things stand, two items ready, two decisions, one open question, the next step, and what not to redo. In a new chat:

```
You:     pickup market-size.au
Claude:  Picked up market-size: Canada and the UK sized, Australia half done. Nothing stale.
         Optional: title this chat market-size.au; if you haven't already, rename the old one handed_off.market-size.
         Next: sizing Australian generation.
```

The `au` tag is your choice, so the two chats on the line are easy to tell apart; `pickup market-size` (or `.pull market-size`) alone would have worked too. It gets straight to work without rereading the old chat. Two days later Australia is done, the EU is sized as you asked, and `market-size.au` hands off for fold-in with four items, A to D. The letters carry on from the first chat: Canada is still A.

## 2. The report chat catches a double count

In `report`, which already holds the draft outline:

```
You:     fold market-size
Claude:  Market-size: four items. One is counted twice, one needs a current source, one is out of scope.

         A. Canada, $310M a year: Change to $250M (deep review). The NERC CIP compliance
            figure already includes $60M of OT monitoring that is also in the OT
            cybersecurity figure. It was counted twice.
         B. UK, $180M a year: Keep (deep review). Re-added from the sources; it matches.
         C. Australia, $140M a year: Return. It rests on one 2021 survey; find a current source.
         D. EU, $600M a year: Toss. Board brief v2 (September 10) drops the EU from this
            round; this work was built on v1.

You:     agreed
Claude:  Done. A and B are in the draft, section 2. D stays tossed, with its reason.
         C is back with market-size: type "pickup" in that chat.
         Optional: rename it returned.market-size.au.
```

Nothing went into the draft until you agreed. The headline numbers got a second, harder pass because the rules file lists them as deep review triggers. The market-size file now carries a verdict on each item, so none of them can be folded in twice.

When C comes back with current sources and is kept, the file shrinks to a receipt, and that chat can become `folded.market-size.au`:

```
# Handoff: market-size
Status: folded into report, September 14, 2026
Kept: B, C (to the draft, section 2). Changed: A (Canada to $250M, overlap removed). Tossed: D (Board brief v2 drops the EU).
```

`regulations` and `competitors` fold in the same way.

## 3. A finding goes back for more work

[Handoff - interviews.md](claude/Handoff%20-%20interviews.md) shows the interviews file just after the report chat reviewed it. Two items are kept and one is tossed. One is returned because it rests on a single interview, from a US utility. In `interviews`:

```
You:     pickup
Claude:  One item returned from report:
         B. Canadian utilities would pay more for NERC CIP experience. It rests on one interview,
            from a US utility. It needs at least three Canadian utilities.
         Starting on the interview list.
```

## 4. A fresh reviewer reads the report cold

With the draft done, `report` hands off: [Handoff - report.md](claude/Handoff%20-%20report.md). You open a new chat:

```
You:     fold report
Claude:  This is the review chat (report folds into review). Seven sections, read as the board
         will read them. Three changes, one goes back.

         A. Executive summary: Change. Lead with the recommendation, then the three country totals.
         B. Market size by country: Keep (deep review). Re-added each country from Market sizing v3; it matches.
         C. Regulatory fit: Change. Name the provinces where NERC CIP applies, instead of "most of Canada".
         D. Competitors: Keep.
         E. What customers say: Keep.
         F. Recommendation: Return (deep review). The Canada case leans on interviews finding B,
            which is still out. Rework it once the Canadian interviews are in, or say plainly
            that Canadian demand is unconfirmed.
         G. Risks: Change. Add currency risk: UK and Australian revenue arrives in pounds and
            Australian dollars.
```

The report chat knew finding B was still out; it says so in its own handoff. The reviewer had never seen that discussion, so it read the recommendation the way the board would and saw what it rests on.

## 5. The report goes out

The week of September 28, the Canadian interviews are in. Finding B, now backed by three Canadian utilities, folds into the report, and `interviews` becomes `folded.interviews`. The report chat reworks the recommendation and hands it back. In the review chat:

```
You:     fold report
Claude:  Report: one item, reworked.

         F. Recommendation: Keep (deep review). The Canada case now rests on three Canadian
            utilities, and the figures still match section 2.

You:     keep
Claude:  Done. The final report is complete in claude/Expansion report final.md.
         Nothing is waiting, returned or open; report is folded in.
         Optional: rename the report chat folded.report, and once the report goes to the
         board, this one done.review.
```

## The sidebar at the end

```
done.review
folded.report
folded.interviews
folded.competitors
folded.regulations
folded.market-size.au
handed_off.market-size
```

Every chat says where it stands, if you renamed them as suggested. One chat is done, the rest are folded or handed off, and nothing is left waiting.

## What this example shows

| Feature | Where |
|---|---|
| Continue a long chat in a fresh one | Step 1 |
| Every number checked, not rubber-stamped | Step 2, item A |
| Work flagged as built on an outdated file | Step 2, item D |
| Deep review of high-stakes items | Steps 2 and 4 |
| Verdicts marked in place, so nothing is folded in twice | Step 2, and the interviews file |
| Returned work, then a receipt | Steps 2 and 3 |
| Chains: research into report, report into review | Step 4 |
| Done: the end of the chain | Step 5 |
| Titles that show each chat's state | Every step |
