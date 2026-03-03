# These environment vairiables 
# need to be set before the workflow run:

# Get the SDK-AUTH by running the below command:

az ad sp create-for-rbac --name "github-deployer" \
  --role contributor \
  --scopes /subscriptions/ff6d5e12-4104-4634-b282-e83e0f074d88/resourceGroups/rg-dev \
  --sdk-auth

# the update the .env file.

AZURE_CREDENTIALS
FUNCTIONAPP_NAME

# Commands:
ls /mnt/c/MyWork/gitlocal/bootup/

cd /mnt/c/MyWork/gitlocal/bootup/

chmod +x /mnt/c/MyWork/gitlocal/bootup/set-secrets.sh

bash /mnt/c/MyWork/gitlocal/bootup/set-secrets.sh




