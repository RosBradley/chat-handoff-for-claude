#!/bin/bash
set -euo pipefail
mkdir -p handoffs
cat > "handoffs/Handoff - market-size.md" <<'EOF'
# Handoff: market-size
Status: waiting
From: market-size, September 12, 2026
Built on: Market sizing v3.md (September 11, 2026)

## Ready to fold in
A. Canada: $310M a year (Market sizing v3.md, section 2).
B. UK: $180M a year (Market sizing v3.md, section 3).
C. Australia: $140M a year (Market sizing v3.md, section 4).

## Next step
Fold A to C into the report draft.
EOF
cat > "Market sizing v3.md" <<'EOF'
# Market sizing v3
## 2. Canada
Compliance $160M plus OT security $150M, but $60M of OT security work is the same spend counted under compliance. Net: $250M a year.
## 3. UK
$180M a year, from the 2026 regulator survey.
## 4. Australia
$140M a year, from a single 2021 industry survey; no newer source found.
EOF
cat > "Report draft.md" <<'EOF'
# Expansion report draft
## Market sizes
(To be filled from the research lines.)
EOF
