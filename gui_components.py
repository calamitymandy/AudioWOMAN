import tkinter as tk
from tkinter import ttk, messagebox

# Clear data
def clear_all(column_textboxes, extension_entry, result_textbox, id_column_selector, column_labels, set_placeholder, char_truncate_entry, char_specify_entry):
    """Clears all textboxes, extension field, and result area."""
    # Clear all column textboxes
    for textbox in column_textboxes:
        textbox.delete("1.0", tk.END)

    # Reset the extension entry field to its placeholder
    extension_entry.delete(0, tk.END)
    set_placeholder(extension_entry, "Extension (ex: .wav)")

    # Clear the result area
    result_textbox.delete("1.0", tk.END)

    # Clear the truncate entry fields
    char_truncate_entry.delete(0, tk.END)
    char_specify_entry.delete(0, tk.END)

    # Reset the ID column selector
    id_column_selector.set("Select ID Column")

    # Reset column labels
    for i, label in enumerate(column_labels):
        label.config(text=f"Col {i + 1}")
    
    ## FUNCTION TO APPLY TRUNCATION ##
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
                messagebox.showerror("Error", "Char not found in path.")
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