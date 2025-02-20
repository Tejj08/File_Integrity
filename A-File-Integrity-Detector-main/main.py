import glob
import hashlib
import os
import tkinter as tk
from tkinter.filedialog import askdirectory
import customtkinter as ctk

# Calculate hash from data in a file
def calculate_sha512_hash(file_name: str) -> str:
    """Calculates the SHA-512 hash of a file."""
    buf_size = 65536  # 64kb chunks
    sha = hashlib.sha512()

    with open(file_name, 'rb') as file:
        while True:
            data = file.read(buf_size)
            if not data:
                break
            sha.update(data)
    return sha.hexdigest()


# Calculate hash from name of a file
def calculate_name_hash(filename: str) -> str:
    """Calculates the MD5 hash of a filename."""
    md5 = hashlib.md5()
    md5.update(filename.encode())
    return md5.hexdigest()


class FileIntegrityDetector:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.baselines = r"C:\Users\hp\OneDrive\Desktop\3rd Year\CS_CP"
        self.secure_path = ""
        self.name_hash = ""
        self.baseline_path = ""
        self.files_changed = []
        self.files_added = []
        self.files_removed = []
        self.files_all = []
        self.spaces = "                                                                        \n"
        self.folder = ""

        self.font_data = ("Helvetica", 14)
        self.label_text_clr = "#98F5FF"
        self.btn_fg_clr = "#FF4040"
        self.btn_text_clr = "#000000"
        self.btn_hover_clr = "#148f3f"
        self.error_label_clr = "#E94F37"

        self.create_widgets()

    def create_widgets(self):
        # Label1 : Monitor folder
        self.label1 = ctk.CTkLabel(master=self.root,
                                   text="Select a Folder",
                                   font=self.font_data,
                                   text_color=self.label_text_clr)
        self.label1.place(relx=0.35, y=40, anchor=tk.CENTER)

        # Browse button
        self.browse_btn = ctk.CTkButton(master=self.root,
                                        text="SEARCH",
                                        image=tk.PhotoImage(file=r"images icon\window_icon.png").subsample(10, 10),
                                        compound=ctk.RIGHT,
                                        command=self.open_file,
                                        fg_color=self.btn_fg_clr,
                                        text_color=self.btn_text_clr,
                                        font=self.font_data,
                                        hover_color=self.btn_hover_clr,
                                        height=40,
                                        width=125)
        self.browse_btn.place(relx=0.7, y=40, anchor=tk.CENTER)

        # Label2 : Selected Folder Path
        self.label2 = ctk.CTkLabel(master=self.root,
                                   text="(Selected Folder path will appear here)",
                                   wraplength=500,
                                   font=self.font_data,
                                   text_color=self.label_text_clr)
        self.label2.place(relx=0.5, y=110, anchor=tk.CENTER)

        # Button : Update Baseline
        self.update_baseline_btn = ctk.CTkButton(master=self.root,
                                                 text="Update Baseline",
                                                 image=tk.PhotoImage(file=r"images icon\updatebaseline.png").subsample(18, 18),
                                                 compound=ctk.RIGHT,
                                                 command=self.update_baseline,
                                                 fg_color=self.btn_fg_clr,
                                                 text_color=self.btn_text_clr,
                                                 font=self.font_data,
                                                 hover_color=self.btn_hover_clr,
                                                 height=40,
                                                 width=150)