import os
import subprocess
import platform
import tkinter as tk
import tkinter.filedialog as fd
from datetime import datetime
from pymediainfo import MediaInfo
from tkinter import messagebox, filedialog


###################### BROWSE FILES ######################
def browse_files_Audit(analyze_files_entry, count_label_audit, missing_files_textbox, extra_files_textbox):
    """Open folder dialog, insert selected folder path, and count files (including subdirectories)."""
    # Clear the file audit & media info columns
    missing_files_textbox.delete("1.0", tk.END)
    extra_files_textbox.delete("1.0", tk.END)
    
    files_in_folder = fd.askdirectory()  # Open folder dialog
    if files_in_folder:
        analyze_files_entry.delete(0, tk.END)  # Clear existing text
        analyze_files_entry.insert(0, files_in_folder)  # Insert selected folder path

        # Count all files (including in subdirectories)
        file_count = sum(len(files) for _, _, files in os.walk(files_in_folder))

        # Update label with the file count
        count_label_audit.config(text=f"number of files: {file_count}")

###################### FILE AUDIT ######################
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
    """Open the audit results in Notepad (Windows) or TextEdit (macOS) with a unique name."""
    
    # Create a unique temporary file name using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    if missing:
        temp_file_path = os.path.join("/tmp", f"missing_files_{timestamp}.txt")  # macOS/Linux temp folder
    else:
        temp_file_path = os.path.join("/tmp", f"extra_files_{timestamp}.txt")
    
    # Write the contents of the textboxes into the temp file
    with open(temp_file_path, "w") as file:
        file.write(textbox.get("1.0", "end-1c").strip() + "\n")
    
    # Detect OS and open file in appropriate editor
    if platform.system() == "Windows":
        subprocess.Popen(["notepad.exe", temp_file_path])  # Open in Notepad (Windows)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", "-a", "TextEdit", temp_file_path])  # Open in TextEdit
    else:
        subprocess.Popen(["xdg-open", temp_file_path])  # Linux (for compatibility)


###################### MEDIA INFO ######################
def apply_mediainfo(folder_path, button):
    """Analyze the Sampling Rate, Bit Depth, and Number of Channels of all audio files in a folder."""
    
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Invalid folder path.")
        return
    
    # Disable button and show "Processing..."
    original_text = button["text"]
    button.config(text="Processing...", state=tk.DISABLED)
    button.update_idletasks()  # Update UI immediately

    audio_extensions = {".wav", ".flac", ".mp3", ".aac", ".m4a", ".ogg", ".wma"}
    reference_values = None
    mismatched_files = []

    # Iterate through all audio files
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext not in audio_extensions:
                continue

            file_path = os.path.join(root, file)
            media_info = MediaInfo.parse(file_path)
            
            for track in media_info.tracks:
                if track.track_type == "Audio":
                    sample_rate = float(track.sampling_rate) if track.sampling_rate else None
                    bit_depth = int(track.bit_depth) if track.bit_depth else None
                    channels = int(track.channel_s) if track.channel_s else None

                    if reference_values is None:
                        reference_values = (sample_rate, bit_depth, channels)
                    
                    if (sample_rate, bit_depth, channels) != reference_values:
                        mismatched_files.append((file_path, sample_rate, bit_depth, channels))
                    
                    break  # Only process the first audio track per file

    # Restore button text and enable it
    button.config(text=original_text, state=tk.NORMAL)

    if not reference_values:
        messagebox.showerror("Error", "No valid audio files found.")
        return

    if mismatched_files:
        message = "Mismatched Files:\n\n"
        message += "\n".join(
            [f"{file} -> {sr} KHz, {bd} bits, {ch} channels"
             for file, sr, bd, ch in mismatched_files]
        )

        # ✅ Copy to clipboard
        root = button.winfo_toplevel()
        root.clipboard_clear()
        root.clipboard_append(message)
        root.update()

        # ✅ Ask if user wants to save the results
        save_choice = messagebox.askyesno("Media Info - Mismatches", 
                                          message + "\n\nCopy to clipboard ✅\nWould you like to save the report?")
        if save_choice:
            save_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                                                     title="Save Mismatched Files Report")
            if save_path:
                with open(save_path, "w", encoding="utf-8") as file:
                    file.write(message)

    else:
        sr, bd, ch = reference_values
        messagebox.showinfo("Media Info", f"All files are {sr} KHz, {bd} bits, and {ch} channels.")

