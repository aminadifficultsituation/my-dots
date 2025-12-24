import customtkinter as ctk
from tkinter import messagebox
import subprocess
import os

# Set the visual style
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WinDotSync OS Manager")
        self.geometry("600x450")

        # Title
        self.label = ctk.CTkLabel(self, text="Dotfile Backup & Sync", font=("Roboto", 24))
        self.label.pack(pady=20)

        # Action Button
        self.btn = ctk.CTkButton(self, text="⚡ Start Daily Backup", command=self.run_backup, 
                                 corner_radius=10, hover_color="#2ecc71", fg_color="#27ae60")
        self.btn.pack(pady=10)

        # Progress Bar (Decorative)
        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.pack(pady=10)
        self.progress.set(0)

        # Log Display
        self.log_display = ctk.CTkTextbox(self, width=500, height=200, corner_radius=10)
        self.log_display.pack(pady=20)
        
        # Load initial logs
        self.update_logs()

    def run_backup(self):
        try:
            self.progress.set(0.5)
            # Running your Bash script
            subprocess.run(["/home/lilo/dotfiles/backup_dots.sh"], check=True)
            self.progress.set(1.0)
            
            self.update_logs()
            messagebox.showinfo("OS Task Complete", "Local backup and metadata logging successful!")
        except Exception as e:
            messagebox.showerror("OS Error", f"System failed to execute script: {e}")

    def update_logs(self):
        log_path = "/home/lilo/dotfile_backup.log"
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                content = f.read()
                self.log_display.delete("0.0", "end")
                self.log_display.insert("0.0", content)

if __name__ == "__main__":
    app = App()
    app.mainloop()
