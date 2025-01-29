import tkinter as tk
from tkinter import messagebox

###################### EXPAND COLUMNS ######################
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

###################### ADD COLUMN ######################
def add_column(column_textboxes, content_frame, column_labels, id_column_selector, update_generate_button_position):
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

###################### REMOVE COLUMN ######################

def remove_column(column_textboxes, column_labels, id_column_selector, update_generate_button_position):
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


###################### GENERATE PATH ######################
def generate_paths(column_textboxes, extension_entry, id_column_selector, result_textbox):
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

