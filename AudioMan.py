import tkinter as tk
from tkinter import ttk, messagebox


def expand_columns(columns, id_column_index, id_column):
    """Expands single constant values and ensures all columns match the ID column length."""
    expanded = []
    max_rows = len(id_column)  # Use ID column length for validation
    for i, col in enumerate(columns):
        if i != id_column_index:
            if len(col) == 1:  # Single constant value
                expanded.append(col * max_rows)  # Repeat the single value
            elif len(col) != max_rows:
                raise ValueError(f"Column {i + 1} must have the same number of rows as the ID column.")
            else:
                expanded.append(col)
        else:
            expanded.append(col)  # ID column remains unchanged
    return expanded


def generate_paths():
    """Generates concatenated paths with handling for constant columns."""
    try:
        # Extract data from textboxes
        columns = [
            column.get("1.0", tk.END).strip().splitlines()
            for column in column_textboxes
        ]
        extension = extension_entry.get().strip()

        # Check if the extension field still has the placeholder
        if extension == "Extension (ex: .wav)":
            extension = ""  # Treat it as empty

        # Get the selected ID column
        id_column_index = id_column_selector.current()
        if id_column_index == -1:
            messagebox.showerror("Error", "Please select an ID column.")
            return

        id_column = columns[id_column_index]

        # Expand columns to match the ID column length
        columns = expand_columns(columns, id_column_index, id_column)

        # Generate concatenated paths
        concatenated_paths = ["".join(row) + extension for row in zip(*columns)]

        # Display the result
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, "\n".join(concatenated_paths))
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate paths: {e}")

def update_generate_button_position():
    """Update the position of the Generate Paths button."""
    # Find the correct row for the button: right below the last row of columns
    total_columns = len(column_textboxes)
    button_row = 4 if total_columns <= 6 else 5  # Depending on row count

    # Update the button position (between columns and result area)
    generate_button.grid(row=button_row, column=2, columnspan=2, padx=5, pady=10, sticky="ew")


def add_column():
    """Add a new column dynamically."""
    column_number = len(column_textboxes) + 1

    if column_number > 12:
        messagebox.showerror("Error", "Cannot create more than 12 columns.")
        return

    # Determine the row and column position for the new column
    grid_row = 1 if column_number <= 6 else 2
    grid_col = (column_number - 1) % 6

    # Add a label for the column
    new_label = tk.Label(content_frame, text=f"Col {column_number}", bg="#e7d3b0")
    new_label.grid(row=grid_row * 2 - 1, column=grid_col, pady=5, sticky="s")
    column_labels.append(new_label)

    # Create a frame to hold the Text widget and its scrollbar
    frame = tk.Frame(content_frame, bg="#e7d3b0")
    frame.grid(row=grid_row * 2, column=grid_col, padx=5, pady=5, sticky="nsew")

    # Add a Text widget
    new_textbox = tk.Text(frame, height=10, width=30, bg="#e7d3b0", wrap="word")
    new_textbox.grid(row=0, column=0, sticky="nsew")

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=new_textbox.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Link the scrollbar to the Text widget
    new_textbox.config(yscrollcommand=scrollbar.set)

    # Configure row and column weights for the frame to make it resize correctly
    frame.grid_rowconfigure(0, weight=1)  # Let the row with Text widget expand
    frame.grid_columnconfigure(0, weight=1)  # Let the column with Text widget expand

    column_textboxes.append(new_textbox)

    # Update the ID column selector options
    id_column_selector['values'] = [f"Col {i + 1}" for i in range(len(column_textboxes))]

    # Update the position of the Generate button based on the number of columns
    update_generate_button_position()

def remove_column():
    """Remove the last column dynamically."""
    if len(column_textboxes) <= 1:
        messagebox.showerror("Error", "At least one column must remain.")
        return

    # Remove the last column's label, textbox, and frame
    last_label = column_labels.pop()
    last_label.destroy()

    last_textbox = column_textboxes.pop()
    last_textbox.destroy()

    last_frame = last_textbox.master  # The parent frame of the textbox
    last_frame.destroy()

    # Update the ID column selector options
    id_column_selector['values'] = [f"Col {i + 1}" for i in range(len(column_textboxes))]

    # Reset the ID column selection if the selected column was removed
    if id_column_selector.current() >= len(column_textboxes):
        id_column_selector.set("Select ID Column")

    # Update the position of the Generate button after removing a column
    update_generate_button_position()

    # Reconfigure the grid layout for the remaining columns
    for i, label in enumerate(column_labels):
        row = (i // 6) + 1  # Row 1 for columns 1-6, Row 2 for columns 7-12
        column = i % 6
        label.grid(row=row * 2 - 1, column=column, pady=5, sticky="s")  # Update positions for labels

    for i, textbox in enumerate(column_textboxes):
        row = (i // 6) + 1  # Row 1 for columns 1-6, Row 2 for columns 7-12
        column = i % 6
        textbox.master.grid(row=row * 2, column=column, padx=5, pady=5, sticky="nsew")  # Update positions for textboxes


def update_id_column_label(event):
    """Update the label of the selected ID column to 'ID'."""
    # Reset all labels to their original names
    for i, label in enumerate(column_labels):
        label.config(text=f"Col {i + 1}")

    # Set the selected column's label to 'ID'
    selected_index = id_column_selector.current()
    if selected_index != -1:
        column_labels[selected_index].config(text="ID")

def clear_all():
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

# Main window configuration
root = tk.Tk()
root.title("Fixed 6-Column Layout")
root.geometry("1200x700")

# Navigation bar (First Row)
nav_bar = tk.Frame(root, height=40, bg="#2197a3", padx=10, pady=5)
nav_bar.grid(row=0, column=0, sticky="ew")

nav_bar.grid_columnconfigure(0, weight=1)
nav_bar.grid_columnconfigure(1, weight=1)
nav_bar.grid_columnconfigure(2, weight=1)
nav_bar.grid_columnconfigure(3, weight=1)
nav_bar.grid_columnconfigure(4, weight=1)
nav_bar.grid_columnconfigure(5, weight=1)

# Add Column button
add_column_button = tk.Button(nav_bar, text="Add Column", command=add_column, bg="#f07868", fg="black")
add_column_button.grid(row=0, column=0, padx=5, pady=5)

# Remove Column button
remove_column_button = tk.Button(nav_bar, text="Remove Column", command=remove_column, bg="#f07868", fg="black")
remove_column_button.grid(row=0, column=1, padx=5, pady=5)

# ID column selector
id_column_selector = ttk.Combobox(nav_bar, state="readonly")
id_column_selector.grid(row=0, column=2, padx=5, pady=5)

# placeholder ID column selector
id_column_selector.set("Select ID Column")
id_column_selector['values'] = []  # Initialize empty
id_column_selector.bind("<<ComboboxSelected>>", update_id_column_label)

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

# Extension box
extension_entry = tk.Entry(nav_bar)
extension_entry.grid(row=0, column=3, padx=5, pady=5)

# Set placeholder for the extension_entry
set_placeholder(extension_entry, "Extension (ex: .wav)")

# Clear data button
clear_button = tk.Button(nav_bar, text="Clear", command=clear_all, bg="#f71e6c", fg="black")
clear_button.grid(row=0, column=5, padx=5, pady=5, rowspan=2)

# Content frame (Below Navigation Bar)
content_frame = tk.Frame(root, padx=20, pady=20, bg="#ebb970")
content_frame.grid(row=1, column=0, sticky="nsew")

# Configure content frame for a maximum of 6 columns
for col in range(6):
    content_frame.grid_columnconfigure(col, weight=1, uniform="fixed_columns")

# Configure dynamic row storage
column_textboxes = []
column_labels = []

# Button to generate paths
generate_button = tk.Button(content_frame, text="Generate Paths", command=generate_paths, bg="#f07868")
generate_button.grid(row=4, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

# Add the first two columns
for _ in range(2):
    add_column()

# Result area
result_label = tk.Label(content_frame, text="Result:", bg="#e7d3b0")
result_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

result_textbox = tk.Text(content_frame, height=10, width=100, bg="#e7d3b0")
result_textbox.grid(row=6, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Configure the main window resizing
root.grid_rowconfigure(1, weight=1)  # Content frame resizable
root.grid_columnconfigure(0, weight=1)

root.mainloop()