import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

# Set UI Theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WinDotSync: OS Final Project")
        self.geometry("600x750")

        # 1. Title Label
        self.label = ctk.CTkLabel(self, text="GitHub Sync & Metadata Tracker", font=("Roboto", 22, "bold"))
        self.label.pack(pady=20)

        # 2. Create Input Fields
        self.repo_url = self.create_input("GitHub Repo URL", "https://github.com/user/repo.git")
        self.token = self.create_input("Personal Access Token", "ghp_xxxxxxxxxxxx", show="*")
        self.username = self.create_input("GitHub Username", "your-username")
        
        # 3. Backup Button
        self.btn = ctk.CTkButton(self, text="🚀 Run System Backup", command=self.run_backup, 
                                 height=45, corner_radius=10, fg_color="#27ae60", hover_color="#2ecc71")
        self.btn.pack(pady=20)

        # 4. Log Display (The Textbox)
        self.log_display = ctk.CTkTextbox(self, width=520, height=200, corner_radius=10)
        self.log_display.pack(pady=10)
        self.update_logs()

    def create_input(self, label_text, placeholder, show=None):
        label = ctk.CTkLabel(self, text=label_text)
        label.pack(pady=(10, 0))
        entry = ctk.CTkEntry(self, placeholder_text=placeholder, width=400, show=show)
        entry.pack(pady=(0, 10))

        # Fix for Right-Click Paste on Fedora
        def show_menu(event):
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Paste", command=lambda: entry.insert(tk.INSERT, self.clipboard_get()))
            menu.post(event.x_root, event.y_root)

        entry.bind("<Button-3>", show_menu) 
        return entry

    def run_backup(self):
        # Get data from the UI boxes
        url = self.repo_url.get()
        tok = self.token.get()
        user = self.username.get()

        if not url or not tok or not user:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        # Prepare Environment Variables to pass to the Shell
        my_env = os.environ.copy()
        my_env["GIT_TOKEN"] = tok
        my_env["GIT_REPO"] = url
        my_env["GIT_USER"] = user

        try:
            # Correct Path for Fedora
            script_path = os.path.expanduser("~/dotfiles/backup_dots.sh")
            
            # Explicitly call /bin/bash to avoid Exec Format errors
            result = subprocess.run(
                ["/bin/bash", script_path], 
                env=my_env, 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            # Refresh logs and show success
            self.update_logs()
            messagebox.showinfo("Success", "GitHub Sync Completed!")
            
        except subprocess.CalledProcessError as e:
            # Capture and show the specific Git error message
            error_msg = e.stderr if e.stderr else e.stdout
            messagebox.showerror("Sync Failed", f"Git says: {error_msg}")
        except Exception as e:
            messagebox.showerror("System Error", f"Could not start process: {e}")

    def update_logs(self):
        # Pulls the metadata text file into the GUI
        log_path = os.path.expanduser("~/dotfile_backup.log")
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                self.log_display.delete("0.0", "end")
                self.log_display.insert("0.0", f.read())
        else:
            self.log_display.insert("0.0", "No logs found. Run backup to generate.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
