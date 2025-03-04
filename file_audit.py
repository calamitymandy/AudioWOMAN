import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def get_filenames_from_textbox(textbox):
    """Extract filenames from the result_textbox."""
    filenames = textbox.get("1.0", tk.END).strip().split("\n")
    return set(f.strip() for f in filenames if f.strip())

def get_filenames_from_folder(folder_path):
    """Retrieve all filenames from the selected folder and subdirectories."""
    found_files = set()
    for root, _, files in os.walk(folder_path):
        for file in files:
            found_files.add(file)
    return found_files

def perform_file_audit(result_textbox, folder_path, missing_textbox, extra_textbox):
    """Compare filenames from result_textbox with the actual folder contents."""
    expected_files = get_filenames_from_textbox(result_textbox)
    found_files = get_filenames_from_folder(folder_path)
    
    missing_files = expected_files - found_files
    extra_files = found_files - expected_files
    
    missing_textbox.delete("1.0", tk.END)
    extra_textbox.delete("1.0", tk.END)
    
    if missing_files:
        missing_textbox.insert(tk.END, "\n".join(missing_files))
    else:
        missing_textbox.insert(tk.END, "No missing files")
    
    if extra_files:
        extra_textbox.insert(tk.END, "\n".join(extra_files))
    else:
        extra_textbox.insert(tk.END, "No extra files")

def export_audit_results(textbox, missing):
    """Open the audit results in Notepad with a unique name."""
    
    # Create a unique temporary file name using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if missing:
        temp_file_path = os.path.join(os.getenv("TEMP"), f"missing_files.txt")
    else:
        temp_file_path = os.path.join(os.getenv("TEMP"), f"extra_files.txt")
    
    # Write the contents of the textboxes into the temp file
    with open(temp_file_path, "w") as file:
        file.write(textbox.get("1.0", "end-1c").strip() + "\n")
    
    # Open the temporary file in Notepad (new instance)
    subprocess.Popen(["notepad.exe", temp_file_path])