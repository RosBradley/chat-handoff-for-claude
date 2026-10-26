#!/bin/bash
set -euo pipefail
cat > "budget-2027.csv" <<'CSV'
line,monthly
rent,1800
food,600
transport,250
savings,900
CSV
