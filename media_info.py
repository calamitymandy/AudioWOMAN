import os
import tkinter as tk
from pymediainfo import MediaInfo
from tkinter import messagebox, filedialog

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

