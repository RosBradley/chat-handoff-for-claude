---
type: llm
---

PASS if all of these hold:
- The reply says a ZIP package was made and where it is.
- It tells the user to attach the ZIP in ChatGPT and paste the prompt from START-HERE.md (or a fallback if ChatGPT won't take a ZIP).
- Any suggested title for this chat uses the dot-style word, pushed.budget, not handed_off.budget.
- It says this chat is now guarded.
FAIL if it claims to have sent anything to ChatGPT, or says no package was made.
