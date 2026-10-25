---
type: regex
pattern: '^# Handoff: budget\n+Status: waiting'
target: { source: file, path: "handoffs/Handoff - budget.md" }
---
