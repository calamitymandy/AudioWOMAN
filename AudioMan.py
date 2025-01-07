import tkinter as tk
from tkinter import messagebox


def generate_paths():
    """Generate concatenated paths from the input columns and extension."""
    try:
        # Collect text from all column textboxes
        columns = [col.get("1.0", tk.END).strip().splitlines() for col in column_textboxes]
        extension = extension_entry.get().strip()

        # Check for empty columns or mismatched row counts
        if not all(columns):
            messagebox.showwarning("Warning", "All columns must have data.")
            return
        if len(set(len(col) for col in columns)) != 1:
            messagebox.showwarning("Warning", "All columns must have the same number of rows.")
            return
        if not extension:
            messagebox.showwarning("Warning", "Introduce an extension.")
            return

        # Generate the concatenated paths
        concatenated_paths = ["".join(row) + extension for row in zip(*columns)]

        # Display the result in the textbox
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, "\n".join(concatenated_paths))
    except Exception as e:
        messagebox.showerror("Error", f"Not possible to create paths: {e}")


def add_column():
    """Add a new column dynamically."""
    column_number = len(column_textboxes) + 1
    new_label = tk.Label(margin_frame, text=f"Col {column_number}:")
    new_label.grid(row=1, column=column_number - 1, sticky="w", padx=5)
    new_textbox = tk.Text(margin_frame, height=10, width=20)
    new_textbox.grid(row=2, column=column_number - 1, sticky="w", padx=5)
    column_textboxes.append(new_textbox)


# Main window configuration
root = tk.Tk()
root.title("Dynamic Columns Generator")
root.geometry("900x600")

# Create a frame to act as a margin
margin_frame = tk.Frame(root, padx=20, pady=20)
margin_frame.pack(fill="both", expand=True)

# Dynamic column storage
column_textboxes = []

# Add the first two columns
for i in range(2):
    add_column()

# Button to add more columns
add_column_button = tk.Button(margin_frame, text="Add Column", command=add_column)
add_column_button.grid(row=0, column=0, padx=5, pady=10, sticky="w")

# Extension input
extension_label = tk.Label(margin_frame, text="Extension (e.g., .wav):")
extension_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
extension_entry = tk.Entry(margin_frame)
extension_entry.grid(row=3, column=1, padx=5, pady=5)

# Button to generate paths
generate_button = tk.Button(margin_frame, text="Generate Paths", command=generate_paths)
generate_button.grid(row=4, column=1, padx=5, pady=10, sticky="w")

# Result area
result_label = tk.Label(margin_frame, text="Result:")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="w")
result_textbox = tk.Text(margin_frame, height=10, width=80)
result_textbox.grid(row=5, column=0, columnspan=10, padx=5, pady=5)

root.mainloop()
