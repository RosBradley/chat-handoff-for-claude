---
type: llm
---

PASS if the reply says the handoff was saved, tells the user to type `pickup budget` in a new chat (or `fold budget` in a master), and suggests the optional title handed_off.budget for this chat.
FAIL if it asks for a name, or tells the user to type dot-style commands such as .pull.
