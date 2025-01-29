import tkinter as tk
import tkinter.filedialog as fd
import os
import shutil

from tkinter import messagebox

###################### BROWSE ORI FILES FOR RENAMING ######################
def browse_files(path_files_entry):
    """Open file dialog and insert selected file path into the entry."""
    file_path = fd.askdirectory()  # Open file dialog
    if file_path:
        path_files_entry.delete(0, tk.END)  # Clear existing text
        path_files_entry.insert(0, file_path)  # Insert selected file path

###################### DO RENAMING ######################

def apply_rename(result_textbox, path_files_entry):
    """Copies files from the selected folder to a new folder at the same level."""
    
    # Get the selected folder path
    source_folder = path_files_entry.get().strip()
    
    if not source_folder or not os.path.isdir(source_folder):
        messagebox.showerror("Error", "Invalid folder path.\n")
        return
    
    # Determine new folder name at the same level
    parent_dir, folder_name = os.path.split(source_folder)
    new_folder = os.path.join(parent_dir, folder_name + "_renamed")

    # If the _renamed folder exists, delete all its content
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    else:
        for root, dirs, files in os.walk(new_folder, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for directory in dirs:
                shutil.rmtree(os.path.join(root, directory))

    # Step 1: Copy all files to _renamed folder (ignoring subdirectories)
    copied_files = []
    for root, _, files in os.walk(source_folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            new_path = os.path.join(new_folder, file_name)  # Flat copy
            shutil.copy(file_path, new_path)
            copied_files.append(new_path)  # Keep track of copied files

    # Step 2: Rename files based on result_textbox
    lines = result_textbox.get("1.0", "end").strip().split("\n")  # Get file paths
    if len(lines) != len(copied_files):
        messagebox.showerror("Error", "Number of files and renaming paths do not match.")
        return

    for old_path, new_relative_path in zip(copied_files, lines):
        new_absolute_path = os.path.join(new_folder, new_relative_path)

        # Ensure subdirectories exist
        new_parent_folder = os.path.dirname(new_absolute_path)
        if not os.path.exists(new_parent_folder):
            os.makedirs(new_parent_folder)

        # Rename (move) file
        shutil.move(old_path, new_absolute_path)

    messagebox.showinfo("Success", f"Files successfully renamed and structured in:\n\n{new_folder}")