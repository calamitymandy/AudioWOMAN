import tkinter as tk
from tkinter import ttk, messagebox

###################### APPLY CLEAR DATA ######################
def clear_all(column_textboxes, extension_entry, result_textbox, result_label, id_column_selector, column_labels, set_placeholder, char_truncate_entry, char_specify_entry, truncate_dir_selector, ori_text_entry, dest_text_entry, path_files_entry, analyze_files_entry, count_label_rename, count_label_audit, missing_files_textbox, extra_files_textbox):
    """Clears all textboxes, extension field, and result area."""
    # Clear all column textboxes
    for textbox in column_textboxes:
        textbox.delete("1.0", tk.END)

    # Reset the extension entry field to its placeholder
    extension_entry.delete(0, tk.END)
    set_placeholder(extension_entry, "Extension (ex: .wav)")

    # Clear the result area
    result_textbox.delete("1.0", tk.END)
    result_label.config(text=f"Result:      0 lines")

    # Clear the truncate area
    char_truncate_entry.delete(0, tk.END)
    char_specify_entry.delete(0, tk.END)
    truncate_dir_selector.set("Left")
    
    # Clear the replace area
    ori_text_entry.delete(0, tk.END)
    dest_text_entry.delete(0, tk.END)

    # Clear the File audit & media info area
    path_files_entry.delete(0, tk.END)

    # Clear the rename area
    analyze_files_entry.delete(0, tk.END)

    # Reset the ID column selector
    id_column_selector.set("Select ID Column")

    # Reset column labels
    for i, label in enumerate(column_labels):
        label.config(text=f"Col {i + 1}:        0 lines")
    
    # Reset the copied file label for rename
    count_label_rename.config(text=f"number of files: 0")

    # Reset the copied file label for audit
    count_label_audit.config(text=f"number of files: 0")

    # Clear the file audit & media info columns
    missing_files_textbox.delete("1.0", tk.END)
    extra_files_textbox.delete("1.0", tk.END)

    
    
###################### APPLY TRUNCATION ######################
def apply_truncation(result_textbox, char_entry, char_specify, direction_selector):
    """Apply truncation to the generated paths and keep the remaining part."""
    try:
        # Get user inputs
        char_count_input = char_entry.get().strip()
        specific_char = char_specify.get().strip()
        direction = direction_selector.get()

        # Validate input for truncation
        if not char_count_input.isdigit() and not specific_char:
            messagebox.showerror("Error", "Please provide a valid number of characters or a specific character.")
            return

        char_count = int(char_count_input) if char_count_input.isdigit() else None

        # Read current paths from the result textbox
        paths = result_textbox.get("1.0", tk.END).strip().splitlines()
        if not paths:
            messagebox.showerror("Error", "No paths to truncate.")
            return

        # Perform truncation while keeping the remaining part
        truncated_paths = []
        for path in paths:
            if (path.find(specific_char) == -1):
                messagebox.showerror("Error", f"Char not found in path: {path}")
                return
            if specific_char:
                if direction == "Left":
                    truncated_paths.append(path[path.find(specific_char) + 1 :] if specific_char in path else path)
                else:
                    truncated_paths.append(path[: path.rfind(specific_char)] if specific_char in path else path)
            elif char_count is not None:
                if direction == "Left":
                    truncated_paths.append(path[char_count:])
                else:
                    truncated_paths.append(path[:-char_count])

        # Update the result textbox with truncated paths
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, "\n".join(truncated_paths))

    except Exception as e:
        messagebox.showerror("Error", f"Could not apply truncation: {e}")
    
    # reset settings
    char_entry.delete("0", tk.END)
    char_specify.delete("0", tk.END)
    direction_selector.set("Left")

###################### APPLY REPLACE ######################
import tkinter.messagebox as messagebox

def apply_replace(result_textbox, ori_text_entry, dest_text_entry, strict_mode=True):
    """Replace text in the generated paths.
    
    strict_mode=True: Requires all paths to contain `ori_input`, otherwise shows an error.  
    strict_mode=False: Replaces occurrences in paths that contain `ori_input`, skipping others.
    """
    try:
        ori_input = ori_text_entry.get().strip()
        dest_input = dest_text_entry.get().strip()

        if not ori_input:
            messagebox.showerror("Error", "Please provide text to replace.")
            return

        # Read current paths
        paths = result_textbox.get("1.0", tk.END).strip().splitlines()
        if not paths:
            messagebox.showerror("Error", "No paths were found.")
            return

        replaced_paths = []
        missing_replacement = False
        changed_count = 0  # Track how many paths were modified

        for path in paths:
            if ori_input in path:
                new_path = path.replace(ori_input, dest_input)
                replaced_paths.append(new_path)
                changed_count += 1
            else:
                replaced_paths.append(path)
                if strict_mode:
                    missing_replacement = True  # At least one path is missing the target

        if strict_mode and missing_replacement:
            messagebox.showerror("Error", f"'{ori_input}' not found in all paths. No changes applied.")
            return

        if changed_count == 0:
            messagebox.showinfo("Info", "No matching text found to replace.")
            return

        # Update the result textbox
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, "\n".join(replaced_paths))

    except Exception as e:
        messagebox.showerror("Error", f"Could not apply replacement: {e}")

    
    # reset settings
    ori_text_entry.delete("0", tk.END)
    dest_text_entry.delete("0", tk.END)