#!/bin/bash
set -euo pipefail
mkdir -p handoffs
cat > "handoffs/Handoff - test.md" <<'EOF'
# Handoff: test
Status: continuing in a new chat, October 24, 2026
From: test, October 23, 2026
Built on: Setup notes.md

## Where it stands
- The setup notes are drafted; the error-message section is next.

## Next step
Write the error-message section.
EOF
printf '# Setup notes\n\n## Error messages\nThree common errors, each with its fix.\n' > "Setup notes.md"
