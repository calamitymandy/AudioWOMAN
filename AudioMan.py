import tkinter as tk
from tkinter import ttk, messagebox


def expand_columns(columns, id_column_index, id_column):
    """Expands constant values and ensures all columns match the ID column length."""
    expanded = []
    max_rows = len(id_column)  # Use ID column length for validation
    for i, col in enumerate(columns):
        if i != id_column_index and len(col) != max_rows:
            raise ValueError(f"Column {i + 1} must have the same number of rows as the ID column.")
        expanded.append(col)
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


def add_column():
    """Add a new column dynamically."""
    column_number = len(column_textboxes) + 1

    # Add a label for the column
    new_label = tk.Label(margin_frame, text=f"Col {column_number}:")
    new_label.grid(row=3, column=column_number - 1, sticky="w", padx=5)
    column_labels.append(new_label)

    # Add a textbox for the column
    new_textbox = tk.Text(margin_frame, height=10, width=20)
    new_textbox.grid(row=4, column=column_number -1, sticky="w", padx=5)
    column_textboxes.append(new_textbox)

    # Update the ID column selector options
    id_column_selector['values'] = [f"Col {i + 1}" for i in range(len(column_textboxes))]


def remove_column():
    """Remove the last column dynamically."""
    if len(column_textboxes) <= 1:
        messagebox.showerror("Error", "At least one column must remain.")
        return

    # Remove the last column's label and textbox
    last_label = column_labels.pop()
    last_label.destroy()
    last_textbox = column_textboxes.pop()
    last_textbox.destroy()

    # Update the ID column selector options
    id_column_selector['values'] = [f"Col {i + 1}" for i in range(len(column_textboxes))]

    # Reset the ID column selection if the selected column was removed
    if id_column_selector.current() >= len(column_textboxes):
        id_column_selector.set("Select ID Column")


def update_id_column_label(event):
    """Update the label of the selected ID column to 'ID'."""
    # Reset all labels to their original names
    for i, label in enumerate(column_labels):
        label.config(text=f"Col {i + 1}:")

    # Set the selected column's label to 'ID'
    selected_index = id_column_selector.current()
    if selected_index != -1:
        column_labels[selected_index].config(text="ID:")


# Main window configuration
root = tk.Tk()
root.title("Batman like")
root.geometry("900x900")

# Create a frame to act as a margin
margin_frame = tk.Frame(root, padx=20, pady=20)
margin_frame.pack(fill="both", expand=True)

# Dynamic column storage
column_textboxes = []
column_labels = []

# ID column selector
id_column_label = tk.Label(margin_frame, text="ID col:")
id_column_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")

id_column_selector = ttk.Combobox(margin_frame, state="readonly")
id_column_selector.grid(row=0, column=2, padx=5, pady=5, columnspan=1, sticky="w")

# Set placeholder text for the ID column selector
id_column_selector.set("Select ID Column")
id_column_selector['values'] = []  # Initialize empty
id_column_selector.bind("<<ComboboxSelected>>", update_id_column_label)

# Add the first two columns
for _ in range(2):
    add_column()

# Button to add more columns
add_column_button = tk.Button(margin_frame, text="Add Column", command=add_column)
add_column_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

# Button to remove the last column
remove_column_button = tk.Button(margin_frame, text="Remove Column", command=remove_column)
remove_column_button.grid(row=0, column=1, padx=0, pady=5, sticky="w")

# Extension input
extension_label = tk.Label(margin_frame, text="Extension (ex: .wav):")
extension_label.grid(row=0, column=4, padx=5, pady=5, sticky="e")
extension_entry = tk.Entry(margin_frame)
extension_entry.grid(row=0, column=5, padx=5, pady=5, sticky="w")

# Button to generate paths
generate_button = tk.Button(margin_frame, text="Generate Paths", command=generate_paths)
generate_button.grid(row=5, columnspan=5, padx=5, pady=10)

# Result area
result_label = tk.Label(margin_frame, text="Result:")
result_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
result_textbox = tk.Text(margin_frame, height=10, width=80)
result_textbox.grid(row=7, columnspan=6, padx=5, pady=5, sticky="w")

# Configure columns to expand only the textboxes
#for i in range(2, 10):  # Assuming up to 10 columns
#    margin_frame.grid_columnconfigure(i, weight=1, uniform="same_group")

root.mainloop()