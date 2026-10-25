#!/usr/bin/env python3
"""Write the earlier-conversation transcripts that some eval cases resume.

Each case that needs a chat history gets evals/<case>/history.jsonl, built from
the conversations below: text turns only, with no tool calls, paths or account
details, so the transcripts are safe to publish. Run from the repo root:

    python3 evals/make_histories.py
"""
import json
import pathlib
import uuid

BUDGET = [
    ("user", "Let's plan my 2027 household budget. Rent is $1,800 a month, food $600, transport $250."),
    ("assistant", "Got it: those three come to $2,650 a month, or $31,800 for the year. Next come utilities and insurance, then savings. Do you want to set a savings target first?"),
    ("user", "Savings is 15% of take-home, which is $6,000 a month. Leave travel open for now."),
    ("assistant", "Savings is $900 a month, so the fixed lines plus savings come to $3,550, leaving $2,450 a month for utilities, insurance, travel and the rest. Travel stays open."),
]

MARKET = [
    ("user", "Let's size the market for OT security services for electric utilities in Canada and the UK."),
    ("assistant", "Canada nets out to about $250M a year once compliance work counted twice is removed; the UK is about $180M a year, from the 2026 regulator survey. Australia is next if you want it."),
]

AFTER_HANDOFF = BUDGET + [
    ("user", "handoff budget"),
    ("assistant", "Saved handoffs/Handoff - budget.md.\n"
                  "To continue: type pickup budget as the first message of a new chat.\n"
                  "Optional: rename this chat handed_off.budget, and title the new one budget.\n"
                  "This chat is now guarded: a new instruction typed here gets a warning first."),
]

PICKED_UP_TEST = [
    ("user", "pickup test"),
    ("assistant", "Picked up test: the setup notes are drafted, and the error-message section is next. Status set to continuing in a new chat.\n"
                  "Optional: title this chat test; if you haven't already, rename the old one handed_off.test."),
    ("user", "Add a short section on error messages."),
    ("assistant", "Added the error-message section to Setup notes.md: three common errors, each with its fix."),
]

PICKED_UP_RESEARCH = [
    ("user", "pickup research"),
    ("assistant", "Picked up research: rent, food and transport are set for 2027, and travel is still open. Status set to continuing in a new chat.\n"
                  "Optional: title this chat research; if you haven't already, rename the old one handed_off.research."),
    ("user", "This line is really about the budget, not research. Travel stays open."),
    ("assistant", "Understood: travel stays open, and nothing else changes."),
]

CASES = {
    "push-dot-no-git": BUDGET,
    "handoff-unnamed-asks": BUDGET,
    "handoff-named-saves": BUDGET,
    "handoff-line-held-elsewhere": BUDGET,
    "handoff-spaced-name": MARKET,
    "stale-chat-guard": AFTER_HANDOFF,
    "rename-tag-or-line": PICKED_UP_TEST,
    "rename-to-new-line": PICKED_UP_RESEARCH,
}


def transcript(turns):
    session = str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(turns)))
    parent = None
    for i, (role, text) in enumerate(turns):
        entry_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{session}/{i}"))
        if role == "user":
            message = {"role": "user", "content": text}
        else:
            message = {"model": "claude-opus-5-5", "id": f"msg_eval{i:04d}", "type": "message",
                       "role": "assistant", "content": [{"type": "text", "text": text}],
                       "stop_reason": "end_turn", "stop_sequence": None,
                       "usage": {"input_tokens": 1, "output_tokens": 1}}
        yield {"parentUuid": parent, "isSidechain": False, "type": role, "message": message,
               "uuid": entry_id, "timestamp": f"2026-10-24T12:{i:02d}:00.000Z",
               "userType": "external", "entrypoint": "cli", "sessionId": session}
        parent = entry_id


root = pathlib.Path(__file__).parent
for case, turns in CASES.items():
    path = root / case / "history.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(entry) + "\n" for entry in transcript(turns)))
    print("wrote", path)
