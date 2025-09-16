#!/bin/bash
# Commands:
#       chmod +x /mnt/c/MyWork/gitlocal/bootup/set-secrets.sh
#       /mnt/c/MyWork/gitlocal/bootup/set-secrets.sh
# The secrets to come from .env file
REPO="mamud1977/bootup"
ENV_FILE=".env"

# Check if .env exists
if [[ ! -f "$ENV_FILE" ]]; then
  echo "❌ Error: $ENV_FILE not found."
  exit 1
fi

# Read and set each secret
while IFS='=' read -r key value; do
  # Trim whitespace and remove quotes
  key=$(echo "$key" | xargs)
  value=$(echo "$value" | sed 's/^"\(.*\)"$/\1/' | xargs)

  # Skip empty lines and comments
  if [[ -n "$key" && "$key" != \#* ]]; then
    echo "🔐 Setting secret: $key"
    gh secret set "$key" --repo "$REPO" --body "$value"
  fi
done < <(grep -v '^#' "$ENV_FILE" | grep -v '^\s*$')