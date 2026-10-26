#!/bin/bash
set -euo pipefail
mkdir -p handoffs
cat > "handoffs/Handoff - budget.md" <<'MD'
# Handoff: budget
Status: waiting
From: budget, October 24, 2026

## Where it stands
- Rent, food, transport and savings are set; travel is open.

## Next step
Add utilities and insurance.
MD
cat > "handoffs/Handoff - travel.md" <<'MD'
# Handoff: travel
Status: waiting
From: travel, October 23, 2026

## Where it stands
- Two trips are planned for 2027; flights aren't priced yet.

## Next step
Price the flights.
MD
