import tkinter as tk

# Extension box placeholder function
def set_placeholder(entry, placeholder, color="gray"):
    """Set placeholder text in an entry widget."""
    entry.insert(0, placeholder)
    entry.config(fg=color)

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=color)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def update_id_column_label(column_labels, column_textboxes, id_column_selector, update_textbox_label):
    """Update only the selected column label to 'ID' without modifying others."""
    selected_index = id_column_selector.current()

    if selected_index != -1:
        # Extract current line count from the label
        current_label_text = column_labels[selected_index].cget("text")
        parts = current_label_text.split(":")  # Example: ["Col 1", " 10 lines"]
        
        if len(parts) > 1:
            line_count_text = parts[1]  # Keep the existing "X lines" part
        else:
            line_count_text = "0 lines"  # Default if something is missing
        
        # Update the selected column label
        column_labels[selected_index].config(text=f"ID:{line_count_text}")

        # Ensure the label updates dynamically when the textbox changes
        update_textbox_label(column_textboxes[selected_index], column_labels[selected_index], "ID")

def update_textbox_label(textbox, label, prefix):
    """Update the label with the number of lines in the given textbox."""
    def update_label(event=None):  # Accept event parameter for bindings
        line_count = len(textbox.get("1.0", tk.END).strip().splitlines())
        label.config(text=f"{prefix}: {line_count} lines")

    # Bind the update function to key and mouse events
    textbox.bind("<KeyRelease>", update_label)
    textbox.bind("<ButtonRelease>", update_label)

    # Call the function once to set initial label
    update_label()