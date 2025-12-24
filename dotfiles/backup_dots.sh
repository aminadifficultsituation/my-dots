#!/bin/bash

BACKUP_DIR="$HOME/dotfiles"
LOG_FILE="$HOME/dotfile_backup.log"
# Files to track
FILES=(".bashrc" ".bash_profile")

echo "--- Backup Started: $(date) ---" >> "$LOG_FILE"

for FILE in "${FILES[@]}"; do
    if [ -f "$HOME/$FILE" ]; then
        # Run your C program to log metadata
        $BACKUP_DIR/perm_check "$HOME/$FILE" >> "$LOG_FILE"
        # Sync the file
        cp -u "$HOME/$FILE" "$BACKUP_DIR/$FILE"
        echo "Successfully backed up $FILE" >> "$LOG_FILE"
    fi
done
