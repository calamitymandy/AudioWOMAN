import tkinter as tk

# Clear data
def clear_all(column_textboxes, extension_entry, result_textbox, id_column_selector, column_labels, set_placeholder):
    """Clears all textboxes, extension field, and result area."""
    # Clear all column textboxes
    for textbox in column_textboxes:
        textbox.delete("1.0", tk.END)

    # Reset the extension entry field to its placeholder
    extension_entry.delete(0, tk.END)
    set_placeholder(extension_entry, "Extension (ex: .wav)")

    # Clear the result area
    result_textbox.delete("1.0", tk.END)

    # Reset the ID column selector
    id_column_selector.set("Select ID Column")

    # Reset column labels
    for i, label in enumerate(column_labels):
        label.config(text=f"Col {i + 1}")