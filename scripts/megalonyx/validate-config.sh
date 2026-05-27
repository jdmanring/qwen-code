#!/usr/bin/env bash
set -euo pipefail

echo " Validating Configuration Files..."

FILES=(
  "config/settings.json"
  "config/meta/layout.json"
)

FAILED=0

for FILE in "${FILES[@]}"; do
  if [ ! -f "$FILE" ]; then
    echo " ERROR: Missing critical config file: $FILE"
    FAILED=1
    continue
  fi

  if python3 -c "import json; json.load(open('$FILE'))" >/dev/null 2>&1; then
    echo " $FILE is valid JSON"
  else
    echo " ERROR: $FILE is NOT valid JSON"
    FAILED=1
  fi
done

if [ $FAILED -eq 1 ]; then
  echo -e "\n Configuration validation failed."
  exit 1
fi

echo -e "\n All configuration files are valid."
exit 0
