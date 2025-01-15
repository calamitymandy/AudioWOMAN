import tkinter as tk
from tkinter import ttk

def add_column():
    """Add a new column dynamically with scrollable text areas."""
    column_number = len(column_textboxes) + 1

    # Limit to a maximum of 12 columns
    if column_number > 12:
        return

    # Determine the row and column for the new column
    grid_row = 2 if column_number <= 6 else 3
    grid_col = (column_number - 1) % 6

    # Add a frame to hold the Text widget and scrollbar
    frame = tk.Frame(content_frame, bg="#e7d3b0")
    frame.grid(row=grid_row * 2, column=grid_col, padx=5, pady=5, sticky="n")

    # Add a Text widget
    textbox = tk.Text(frame, height=10, width=30, bg="#e7d3b0", wrap="word")
    textbox.pack(side="left", fill="both", expand=True)

    # Add a vertical scrollbar
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=textbox.yview)
    scrollbar.pack(side="right", fill="y")

    # Link the scrollbar to the Text widget
    textbox.config(yscrollcommand=scrollbar.set)

    column_textboxes.append(textbox)

# Main window
root = tk.Tk()
root.title("Test Scrollbars")
root.geometry("800x400")

# Content frame
content_frame = tk.Frame(root, padx=20, pady=20, bg="#ebb970")
content_frame.grid(row=0, column=0, sticky="nsew")

# Configure content frame for 6 columns
for col in range(6):
    content_frame.grid_columnconfigure(col, weight=1, uniform="fixed_columns")

# Button to add columns
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, pady=10)

add_button = tk.Button(button_frame, text="Add Column", command=add_column)
add_button.pack()

# Initialize storage for textboxes
column_textboxes = []

root.mainloop()
