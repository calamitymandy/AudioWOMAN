import tkinter as tk
from tkinter import ttk

from utils import set_placeholder, update_id_column_label, update_textbox_label
from modify_and_clear import clear_all, apply_truncation, apply_replace
from create_and_generate import generate_paths, add_column, remove_column, copy_paths
from rename_files import browse_files, apply_rename

def update_generate_button_position():
    """Update the position of the Generate Paths button."""
    # Find the correct row for the button: right below the last row of columns
    total_columns = len(column_textboxes)
    button_row = 4 if total_columns <= 6 else 5  # Depending on row count

    # Update the buttons positions (between columns and result area)
    generate_new_button.grid(row=button_row, column=0, columnspan=2, padx=5, pady=10, sticky="ew")
    generate_add_button.grid(row=button_row, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

###################### MAIN WINDOW CONFIGURATION ######################
root = tk.Tk()
root.title("AudioMAN")
root.geometry("1200x950")

###################### NAVIGATION BAR ######################
nav_bar = tk.Frame(root, height=40, bg="#2197a3", padx=10, pady=5)
nav_bar.grid(row=0, column=0, sticky="ew")

nav_bar.grid_columnconfigure(0, weight=1)
nav_bar.grid_columnconfigure(1, weight=1)
nav_bar.grid_columnconfigure(2, weight=1)
nav_bar.grid_columnconfigure(3, weight=1)
nav_bar.grid_columnconfigure(4, weight=1)
nav_bar.grid_columnconfigure(5, weight=1)

# Add Column button
add_column_button = tk.Button(
    nav_bar, 
    text="Add Column", 
    command=lambda: add_column(column_textboxes, content_frame, column_labels, id_column_selector, update_generate_button_position, update_textbox_label), 
    bg="#f07868", 
    fg="black"
    )
add_column_button.grid(row=0, column=0, padx=5, pady=5)

# Remove Column button
remove_column_button = tk.Button(
    nav_bar, 
    text="Remove Column", 
    command=lambda: remove_column(column_textboxes, column_labels, id_column_selector, update_generate_button_position), 
    bg="#f07868", 
    fg="black"
    )
remove_column_button.grid(row=0, column=1, padx=5, pady=5)

# ID column selector
id_column_selector = ttk.Combobox(nav_bar, state="readonly")
id_column_selector.grid(row=0, column=2, padx=5, pady=5)

# placeholder ID column selector
id_column_selector.set("Select ID Column")
id_column_selector['values'] = []  # Initialize empty
id_column_selector.bind(
    "<<ComboboxSelected>>",
    lambda event: update_id_column_label(column_labels, column_textboxes, id_column_selector, update_textbox_label),
)

# Extension entry #
extension_entry = tk.Entry(nav_bar)
extension_entry.grid(row=0, column=3, padx=5, pady=5)

# placeholder for the extension_entry
set_placeholder(extension_entry, "Extension (ex: .wav)")

# Copy paths from directory #
browse_button = tk.Button(
    nav_bar, 
    text="Copy all paths from directory", 
    bg="#f07868", 
    command=lambda: copy_paths(column_textboxes, column_labels, update_textbox_label)
    )
browse_button.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

## CLEAR DATA BUTTON ##
clear_button = tk.Button(
    nav_bar, 
    text="Clear", 
    command=lambda: clear_all(column_textboxes, extension_entry, result_textbox, result_label, id_column_selector, column_labels, set_placeholder, char_truncate_entry, char_specify_entry, truncate_dir_selector, ori_text_entry, dest_text_entry, path_files_entry),
    bg="#f71e6c", 
    fg="black"
)
clear_button.grid(row=0, column=5, padx=5, pady=5, rowspan=2)


###################### CONTENT FRAME WITH SCROLLBARS ######################
# Create a container frame for the canvas and scrollbars
content_container = tk.Frame(root, bg="#ebb970")
content_container.grid(row=1, column=0, sticky="nsew")  # Same position as the content frame

# Add a canvas to the container
canvas = tk.Canvas(content_container, bg="#ebb970")
canvas.grid(row=0, column=0, sticky="nsew")

# Add vertical and horizontal scrollbars
v_scrollbar = tk.Scrollbar(content_container, orient="vertical", command=canvas.yview)
v_scrollbar.grid(row=0, column=1, sticky="ns")

h_scrollbar = tk.Scrollbar(content_container, orient="horizontal", command=canvas.xview)
h_scrollbar.grid(row=1, column=0, sticky="ew")

# Configure the canvas to use the scrollbars
canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Create the actual content frame inside the canvas
content_frame = tk.Frame(canvas, padx=20, pady=20, bg="#ebb970")
content_frame_id = canvas.create_window((0, 0), window=content_frame, anchor="nw")

# Configure resizing behavior for the content_container
content_container.grid_rowconfigure(0, weight=1)
content_container.grid_columnconfigure(0, weight=1)

# Bind the canvas and content frame for scrolling
def on_canvas_configure(event):
    """Update the scroll region of the canvas when the content frame changes size."""
    canvas.configure(scrollregion=canvas.bbox("all"))

content_frame.bind("<Configure>", on_canvas_configure)

# Optional: Handle resizing of the canvas
def on_content_resize(event):
    """Resize the canvas to fill the container."""
    canvas_width = event.width
    canvas.itemconfig(content_frame_id, width=canvas_width)

canvas.bind("<Configure>", on_content_resize)

# Enable mouse wheel scrolling for the canvas
def on_mouse_wheel(event):
    """Scroll vertically with the mouse wheel."""
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows and MacOS
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # For Linux
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # For Linux

# Configure the content frame for a maximum of 6 columns
for col in range(6):
    content_frame.grid_columnconfigure(col, weight=1, uniform="fixed_columns")

## Configure dynamic row storage ##
column_textboxes = []
column_labels = []

## Button to generate new paths (& delete what was in result textbox) ##
generate_new_button = tk.Button(
    content_frame, 
    text="Generate New Paths", 
    command=lambda: generate_paths(
        column_textboxes, 
        extension_entry, 
        id_column_selector, 
        result_textbox, 
        result_label, 
        update_textbox_label, 
        append=False
        ), 
    bg="#f07868"
    )
generate_new_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

## Button to add paths to the one already existing ##
generate_add_button = tk.Button(
    content_frame, 
    text="Add more Paths", 
    command=lambda: generate_paths(
        column_textboxes, 
        extension_entry, 
        id_column_selector, 
        result_textbox,
        result_label, 
        update_textbox_label, 
        append=True
        ), 
    bg="#f07868"
    )
generate_add_button.grid(row=4, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

## Add the first two columns ##
add_column(column_textboxes, content_frame, column_labels, id_column_selector, update_generate_button_position, update_textbox_label)

###################### RESULT AREA WITH SCROLLBAR ######################
result_label = tk.Label(content_frame, text="Result:        0 lines", bg="#e7d3b0")
result_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

# Create a frame for the result area and scrollbar
result_frame = tk.Frame(content_frame, bg="#e7d3b0")
result_frame.grid(row=6, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add the Text widget inside the frame
result_textbox = tk.Text(result_frame, height=10, width=100, bg="#e7d3b0", wrap="word")
result_textbox.grid(row=0, column=0, sticky="nsew")

# Update the label dynamically
update_textbox_label(result_textbox, result_label, prefix="Result")

# Add a vertical scrollbar to the frame
result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=result_textbox.yview)
result_scrollbar.grid(row=0, column=1, sticky="ns")

# Link the scrollbar to the Text widget
result_textbox.config(yscrollcommand=result_scrollbar.set)

# Configure the row and column weights for the frame
result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

###################### TRUNCATION AREA ######################
# Frame for truncation inputs
truncate_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=10)
truncate_frame.grid(row=7, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add truncation controls inside the frame
truncate_label = tk.Label(truncate_frame, bg="#e7d3b0", text="TRUNCATE SETTINGS")
truncate_label.grid(row=0, column=0, padx=50, pady=5, sticky="nsew")

# Input for number of characters to truncate
char_truncate_label = tk.Label(truncate_frame, text="Truncate # Chars:", bg="#e7d3b0")
char_truncate_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
char_truncate_entry = tk.Entry(truncate_frame, width=10)
char_truncate_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Input for specific character to truncate up to
char_specify_label = tk.Label(truncate_frame, text="Truncate Up To Char:", bg="#e7d3b0")
char_specify_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
char_specify_entry = tk.Entry(truncate_frame, width=10)
char_specify_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

# Options for truncation direction
truncate_dir_label = tk.Label(truncate_frame, text="Direction:", bg="#e7d3b0")
truncate_dir_label.grid(row=0, column=5, padx=5, pady=5, sticky="e")

truncate_dir_selector = ttk.Combobox(
    truncate_frame, state="readonly", values=["Left", "Right"]
)
truncate_dir_selector.grid(row=0, column=5, padx=5, pady=5, sticky="w")
truncate_dir_selector.set("Left")  # Default to "Left"

# Button to apply truncation
truncate_button = tk.Button(
    truncate_frame,
    text="Apply Truncation",
    bg="#f07868",
    command=lambda: apply_truncation(
        result_textbox, char_truncate_entry, char_specify_entry, truncate_dir_selector
    ),
)
truncate_button.grid(row=0, column=6, padx=5, pady=5, sticky="w")

###################### REPLACE AREA ######################
# Frame for replace inputs
replace_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=10)
replace_frame.grid(row=8, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add replace controls inside the frame
replace_label = tk.Label(replace_frame, bg="#e7d3b0", text="REPLACE SETTINGS")
replace_label.grid(row=0, column=0, padx=50, pady=5, sticky="nsew")

# Input for the characters to replace
ori_text_label = tk.Label(replace_frame, text="Replace this:", bg="#e7d3b0")
ori_text_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
ori_text_entry = tk.Entry(replace_frame, width=10)
ori_text_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Input for the characters we want
dest_text_label = tk.Label(replace_frame, text="By that:", bg="#e7d3b0")
dest_text_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
dest_text_entry = tk.Entry(replace_frame, width=10)
dest_text_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

# Button to apply truncation
replace_button = tk.Button(
    replace_frame,
    text="Replace",
    bg="#f07868",
    command=lambda: apply_replace(
        result_textbox, ori_text_entry, dest_text_entry
    ),
)
replace_button.grid(row=0, column=6, padx=5, pady=5, sticky="w")



###################### RENAME AREA ######################
# Frame for rename inputs
rename_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=15)
rename_frame.grid(row=9, column=2, columnspan=2, padx=5, pady=5, sticky="new")

# Configure columns to expand evenly
rename_frame.grid_columnconfigure(0, weight=1)
rename_frame.grid_columnconfigure(1, weight=1)

# Add rename controls inside the frame
rename_label = tk.Label(rename_frame, bg="#e7d3b0", text="RENAMING")
rename_label.grid(row=0, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")

# Input for the files to rename
path_files_label = tk.Label(rename_frame, text="Replace from path:", bg="#e7d3b0")
path_files_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
path_files_entry = tk.Entry(rename_frame, width=30)  # Increased width
path_files_entry.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Browse button
browse_button = tk.Button(
    rename_frame, 
    text="Browse", 
    bg="#f07868", 
    command=lambda: browse_files(path_files_entry)
    )
browse_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Button to apply rename
rename_button = tk.Button(
    rename_frame,
    text="Rename",
    bg="#f07868",
    command=lambda: apply_rename(
        result_textbox, path_files_entry
    ),
)
rename_button.grid(row=3, column=0, columnspan=2, padx=5, pady=20, sticky="sew")

###################### MAIN WINDOW RESIZING ######################
root.grid_rowconfigure(1, weight=1)  # Content frame resizable
root.grid_columnconfigure(0, weight=1)

root.mainloop()