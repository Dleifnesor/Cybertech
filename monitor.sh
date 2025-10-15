#!/bin/bash

# File where hashes are saved
BASELINE=~/important/baseline.txt

# After baseline file is created, check for changes to the baseline
if [ -f "$BASELINE" ]; then
  echo "Checking for changes..."
  sha256sum -c "$BASELINE"

# If no baseline file exists, create one
else
  echo "Creating baseline hashes..."
  find ~/important -type f ! -name baseline.txt -exec sha256sum {} \; > "$BASELINE"
  echo "Baseline created."
fi
