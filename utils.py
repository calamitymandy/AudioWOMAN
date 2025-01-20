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

def update_id_column_label(column_labels, id_column_selector):
    """Update the label of the selected ID column to 'ID'."""
    # Reset all labels to their original names
    for i, label in enumerate(column_labels):
        label.config(text=f"Col {i + 1}")

    # Set the selected column's label to 'ID'
    selected_index = id_column_selector.current()
    if selected_index != -1:
        column_labels[selected_index].config(text="ID")