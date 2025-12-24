#!/bin/bash

echo "===================================="
echo "    WinDotSync GitHub Wizard"
echo "===================================="

# 1. Ask for credentials
read -p "Paste your GitHub Repo URL: " REPO_URL
read -s -p "Paste your GitHub Token: " GIT_TOKEN
echo -e "\n"
read -p "Full path of file to upload: " FILE_PATH

# 2. Run the C Inspector
./inspector "$FILE_PATH"
if [ $? -ne 0 ]; then
    echo "Stopping: Inspector could not verify that file."
    exit 1
fi

# 3. Setup the sync folder
VAULT="$HOME/WinDotSync_Vault"
mkdir -p "$VAULT"
cp -a "$FILE_PATH" "$VAULT/"
cd "$VAULT"

# 4. Auth Logic (Injects token into the URL)
AUTH_URL=$(echo "$REPO_URL" | sed "s/https:\/\/ /https:\/\/$GIT_TOKEN@/")

# 5. Git Sync
echo "Uploading to GitHub..."
if [ ! -d ".git" ]; then
    git init
    git remote add origin "$AUTH_URL"
    git branch -M main
fi

git add .
git commit -m "Uploaded via Wizard on $(date)"
git push -u origin main --force

echo "===================================="
echo "Done! Check your GitHub repository."
