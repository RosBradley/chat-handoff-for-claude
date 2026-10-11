# Worked example: taking a grid-security firm international

Sablewire Grid Solutions does IT/OT engineering, NERC CIP compliance and OT cybersecurity for electric utilities in the US. Its board wants a report on which new markets to enter, in the rest of North America and abroad. (The company is made up, and so is every figure below.)

The work runs across seven chats in one claude.ai Project:

```
market size  ─┐
regulations  ─┤
competitors  ─┼─►  report  ─►  review
interviews   ─┘
```

- Four research chats work in parallel, one question each.
- **report** receives their work. It checks every finding before it goes into the draft.
- **review** is a fresh chat that has never seen the drafting. It reads the finished draft the way the board will.

The project's rules file is [templates/handoff-rules.md](../templates/handoff-rules.md). The handoff files are in [claude/](claude/), where they'd sit in the Project.

## 1. A long chat continues in a fresh one

`market size 1` has worked through a stack of industry reports and is getting slow. Canada and the UK are sized; Australia is half done.

```
You:     handoff?
Claude:  Yes. The chat is long, and Australian generation is a clean place to start fresh.

You:     handoff
Claude:  Saved claude/Handoff - market size.md.
         To continue: type "pickup market size" as the first message of a new chat.
         Name it "market size 2", and rename this one "Continued - market size 1".
         To fold it into the report instead: type "fold market size" in the report chat, and
         rename this one "Handed off - market size 1".
```

The file it saved: [Handoff - market size.md](claude/Handoff%20-%20market%20size.md). About 200 words: where things stand, two items ready, two decisions, one open question, the next step, and what not to redo. In a new chat:

```
You:     pickup market size
Claude:  Picked up market size: Canada and the UK sized, Australia half done. Nothing stale.
         Titles: this chat "market size 2"; the old one "Continued - market size 1".
         Next: sizing Australian generation.
```

It gets straight to work without rereading the old chat. Two days later Australia is done, the EU is sized as you asked, and `market size 2` hands off for fold-in with four items, A to D. The letters carry on from the first chat: Canada is still A.

## 2. The report chat catches a double count

In `report 1`, which already holds the draft outline:

```
You:     fold market size
Claude:  Market size: four items. One is counted twice, one needs a current source, one is out of scope.

         A. Canada, $310M a year: Change to $250M (deep review). The NERC CIP compliance
            figure already includes $60M of OT monitoring that is also in the OT
            cybersecurity figure. It was counted twice.
         B. UK, $180M a year: Keep (deep review). Re-added from the sources; it matches.
         C. Australia, $140M a year: Return. It rests on one 2021 survey; find a current source.
         D. EU, $600M a year: Toss. Board brief v2 (September 10) drops the EU from this
            round; this work was built on v1.

You:     agreed
Claude:  Done. A and B are in the draft, section 2. D stays tossed, with its reason.
         C is back with market size: rename that chat "Returned - market size 2" and type "pickup" there.
         Rename this chat "Master - report 1".
```

Nothing went into the draft until you agreed. The headline numbers got a second, harder pass because the rules file lists them as deep review triggers. The market size file now carries a verdict on each item, so none of them can be folded in twice.

When C comes back with current sources and is kept, the file shrinks to a receipt, and that chat becomes `Folded - market size 2`:

```
# Handoff: market size
Status: folded into Master - report 1, September 14, 2026
Kept: B, C (to the draft, section 2). Changed: A (Canada to $250M, overlap removed). Tossed: D (Board brief v2 drops the EU).
```

`regulations` and `competitors` fold in the same way.

## 3. A finding goes back for more work

[Handoff - interviews.md](claude/Handoff%20-%20interviews.md) shows the interviews file just after the report chat reviewed it. Two items are kept and one is tossed. One is returned because it rests on a single interview, from a US utility. In `interviews 1`:

```
You:     pickup
Claude:  One item returned from Master - report 1:
         B. Canadian utilities would pay more for NERC CIP experience. It rests on one interview,
            from a US utility. It needs at least three Canadian utilities.
         Starting on the interview list.
```

## 4. A fresh reviewer reads the report cold

With the draft done, `report 1` hands off: [Handoff - report.md](claude/Handoff%20-%20report.md). You open a new chat:

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

The week of September 28, the Canadian interviews are in. Finding B, now backed by three Canadian utilities, folds into the report, and `interviews 1` becomes `Folded - interviews 1`. The report chat reworks the recommendation and hands it back. In the review chat:

```
You:     fold report
Claude:  Report: one item, reworked.

         F. Recommendation: Keep (deep review). The Canada case now rests on three Canadian
            utilities, and the figures still match section 2.

You:     keep
Claude:  Done. The final report is complete in claude/Expansion report final.md.
         Nothing is waiting, returned or open; report is folded in.
         When it goes to the board, rename this chat "Released - review 1".
```

## The sidebar at the end

```
Released - review 1
Folded - report 1
Folded - interviews 1
Folded - competitors 1
Folded - regulations 1
Folded - market size 2
Continued - market size 1
```

Every chat says where it stands. One chat is released, the rest are folded or continued, and nothing is left waiting.

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
| Released: the end of the chain | Step 5 |
| Titles that show each chat's state | Every step |
