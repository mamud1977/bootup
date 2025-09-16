#!/bin/bash
# Commands:
#       chmod +x /mnt/c/MyWork/gitlocal/bootup/set-secrets.sh
#       /mnt/c/MyWork/gitlocal/bootup/set-secrets.sh
# The secrets to come from .env file
REPO="mamud1977/bootup"

# Loop through each line in .env and set as GitHub secret
while IFS='=' read -r key value; do
  if [[ -n "$key" && -n "$value" ]]; then
    echo "Setting secret: $key"
    gh secret set "$key" --repo "$REPO" --body "$value"
  fi
done < .env
