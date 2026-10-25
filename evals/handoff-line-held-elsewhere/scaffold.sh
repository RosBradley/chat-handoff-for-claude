#!/bin/bash
set -euo pipefail
mkdir -p handoffs
cat > "handoffs/Handoff - budget.md" <<'EOF'
# Handoff: budget
Status: continuing in budget.post, October 12, 2026
From: budget.pre, October 12, 2026
Built on: Budget plan v2.md (October 10, 2026)

## Where it stands
- Rent, food and transport are set for 2027; travel is still open.

## Ready to fold in
A. Cut the gym line from $90 to $40 a month (Budget plan v2.md, section 3).

## Open
- Waiting on the user: include a trip to Spain in 2027 or not?

## Next step
Ask the user whether the Spain trip stays in the plan.

## Read first
- Budget plan v2.md

## Don't redo
- Car lease checked October 11: keep it.
EOF
cat > "Budget plan v2.md" <<'EOF'
# Budget plan v2
## 3. Health
Gym: $90 a month now; a $40 plan covers what is used.
EOF
