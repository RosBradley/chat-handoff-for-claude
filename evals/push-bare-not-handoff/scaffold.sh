#!/bin/bash
set -euo pipefail
git init -q
echo "# Demo" > README.md
git add README.md
git -c user.name=eval -c user.email=eval@example.com commit -qm init
