#!/bin/bash

# Capture GUI variables
TOKEN=${GIT_TOKEN}
REPO=${GIT_REPO}
USER=${GIT_USER}

# 1. Force the script into the correct directory
# Using absolute paths is safer for background processes
cd /home/lilo/dotfiles || exit

# 2. Metadata Check (C Program)
./perm_check /home/lilo/.bashrc >> /home/lilo/dotfile_backup.log

# 3. Setup Remote with Authentication
STRIPPED_URL=$(echo $REPO | sed 's/https:\/\///')
FULL_AUTH_URL="https://$USER:$TOKEN@$STRIPPED_URL"

# Re-link the remote origin every time to ensure the token is fresh
git remote remove origin 2>/dev/null
git remote add origin "$FULL_AUTH_URL"

# 4. Sync
git add .
git commit -m "GUI Sync: $(date)"
git push -u origin main
