import tkinter as tk
from tkinter import ttk
import sys
import os
import shutil


from utils import set_placeholder, update_id_column_label, update_textbox_label
from modify_and_clear import clear_all, apply_truncation, apply_replace
from create_and_generate import generate_paths, add_column, remove_column, copy_paths
from rename_files import browse_files, apply_rename
from file_audit_n_media_info import perform_file_audit, export_audit_results, browse_files_Audit, apply_mediainfo, check_lufs

def get_ffmpeg_path():
    """Detect platform and return the correct ffmpeg binary path."""
    if getattr(sys, 'frozen', False):  # Si estamos ejecutando el archivo empaquetado
        # Usamos _MEIPASS para obtener la ruta donde PyInstaller extrae los archivos
        temp_dir = sys._MEIPASS
        ffmpeg_path = os.path.join(temp_dir, 'ffmpeg.exe')
    else:
        # Si estamos en desarrollo, buscamos el binario en el directorio local
        ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg_bin', 'ffmpeg.exe')
    
    return ffmpeg_path


# Llamamos a la función para obtener la ruta de ffmpeg.exe
ffmpeg_path = get_ffmpeg_path()

if os.path.exists(ffmpeg_path):
    print(f"FFmpeg encontrado en: {ffmpeg_path}")
else:
    print("No se encontró ffmpeg.exe.")

def check_ffmpeg():
    ffmpeg_path = get_ffmpeg_path()
    print(f"Buscando ffmpeg.exe en: {ffmpeg_path}")
    if os.path.exists(ffmpeg_path):
        print(f"FFmpeg encontrado en: {ffmpeg_path}")
    else:
        print(f"No se encontró ffmpeg.exe en: {ffmpeg_path}")


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
root.title("AudioWOMAN")
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
    fg="black",
    highlightbackground="#2197a3"
    )
add_column_button.grid(row=0, column=0, padx=5, pady=5)

# Remove Column button
remove_column_button = tk.Button(
    nav_bar, 
    text="Remove Column", 
    command=lambda: remove_column(column_textboxes, column_labels, id_column_selector, update_generate_button_position), 
    bg="#f07868", 
    fg="black",
    highlightbackground="#2197a3"
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
    lambda event: update_id_column_label(column_labels, column_textboxes, id_column_selector, update_textbox_label)
)

# Extension entry #
extension_entry = tk.Entry(nav_bar, highlightbackground="#2197a3")
extension_entry.grid(row=0, column=3, padx=5, pady=5)

# placeholder for the extension_entry
set_placeholder(extension_entry, "Extension (ex: .wav)")

# Copy paths from directory #
copy_path_button = tk.Button(
    nav_bar, 
    text="Copy all paths from directory", 
    bg="#f07868",
    highlightbackground="#2197a3",
    command=lambda: copy_paths(column_textboxes, column_labels, update_textbox_label)
    )
copy_path_button.grid(row=0, column=4, padx=5, pady=5, sticky="nsew")

## CLEAR DATA BUTTON ##
clear_button = tk.Button(
    nav_bar, 
    text="Clear", 
    command=lambda: clear_all(
        column_textboxes, 
        extension_entry, 
        result_textbox, 
        result_label, 
        id_column_selector, 
        column_labels, 
        set_placeholder, 
        char_truncate_entry, 
        char_specify_entry, 
        truncate_dir_selector, 
        ori_text_entry, 
        dest_text_entry, 
        path_files_entry,
        analyze_files_entry,
        count_label_rename,
        count_label_audit,
        missing_files_textbox,
        extra_files_textbox
        ),
    bg="#f71e6c", 
    fg="black",
    highlightbackground="#2197a3"
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

def on_mouse_wheel(event):
    """Enable smooth scrolling for macOS trackpad and mouse wheel."""
    if event.num == 5 or event.delta < 0:  # Scroll down
        canvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta > 0:  # Scroll up
        canvas.yview_scroll(-1, "units")

# Detect macOS gestures properly
canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows/macOS scrolling
canvas.bind_all("<Shift-MouseWheel>", on_mouse_wheel)  # Enable horizontal scrolling
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux Scroll Up
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))  # Linux Scroll Down

# NEW: Detect trackpad two-finger gestures explicitly
def on_trackpad_scroll(event):
    """Mac trackpad gesture support using delta movement."""
    canvas.yview_scroll(-int(event.delta / 60), "units")

canvas.bind_all("<Motion>", on_trackpad_scroll)  # Trackpad two-finger gesture

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
    bg="#f07868",
    highlightbackground="#ebb970"
    )
generate_new_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="ew")

## Button to add paths to the one already existing ##
generate_add_button = tk.Button(
    content_frame, 
    text="Add More Paths", 
    command=lambda: generate_paths(
        column_textboxes, 
        extension_entry, 
        id_column_selector, 
        result_textbox,
        result_label, 
        update_textbox_label, 
        append=True
        ), 
    bg="#f07868",
    highlightbackground="#ebb970"
    )
generate_add_button.grid(row=4, column=2, columnspan=2, padx=5, pady=10, sticky="ew")

## Add the first column ##
add_column(column_textboxes, content_frame, column_labels, id_column_selector, update_generate_button_position, update_textbox_label)

###################### RESULT AREA WITH SCROLLBAR ######################
result_label = tk.Label(content_frame, text="Result:        0 lines", bg="#e7d3b0")
result_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")

# Create a frame for the result area and scrollbar
result_frame = tk.Frame(content_frame, bg="#e7d3b0")
result_frame.grid(row=7, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add the Text widget inside the frame
result_textbox = tk.Text(result_frame, height=10, width=100, bg="#e7d3b0", highlightbackground="#e7d3b0", wrap="word")
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
truncate_frame.grid(row=8, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add truncation controls inside the frame
truncate_label = tk.Label(truncate_frame, bg="#e7d3b0", text="TRUNCATE ->")
truncate_label.grid(row=0, column=0, padx=50, pady=5, sticky="nsew")

# Input for number of characters to truncate
char_truncate_label = tk.Label(truncate_frame, text="Truncate # Chars:", bg="#e7d3b0")
char_truncate_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
char_truncate_entry = tk.Entry(truncate_frame, width=10, highlightbackground="#e7d3b0")
char_truncate_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Input for specific character to truncate up to
char_specify_label = tk.Label(truncate_frame, text="Truncate Up To Char:", bg="#e7d3b0")
char_specify_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
char_specify_entry = tk.Entry(truncate_frame, width=10, highlightbackground="#e7d3b0")
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
    highlightbackground="#e7d3b0",
    command=lambda: apply_truncation(
        result_textbox, char_truncate_entry, char_specify_entry, truncate_dir_selector
    ),
)
truncate_button.grid(row=0, column=6, padx=5, pady=5, sticky="w")

###################### REPLACE ALL AREA ######################
# Frame for replace inputs
replace_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=10)
replace_frame.grid(row=9, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add replace controls inside the frame
replace_label = tk.Label(replace_frame, bg="#e7d3b0", text="REPLACE ALL ->")
replace_label.grid(row=0, column=0, padx=50, pady=5, sticky="nsew")

# Input for the characters to replace
ori_text_label = tk.Label(replace_frame, text="Replace this:", bg="#e7d3b0")
ori_text_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
ori_text_entry = tk.Entry(replace_frame, width=10, highlightbackground="#e7d3b0")
ori_text_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Input for the characters we want
dest_text_label = tk.Label(replace_frame, text="By that:", bg="#e7d3b0")
dest_text_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
dest_text_entry = tk.Entry(replace_frame, width=10, highlightbackground="#e7d3b0")
dest_text_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

# Button to apply replacing
replace_button = tk.Button(
    replace_frame,
    text="Replace",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: apply_replace(
        result_textbox, ori_text_entry, dest_text_entry, strict_mode=True
    ),
)
replace_button.grid(row=0, column=6, padx=5, pady=5, sticky="w")

###################### PARTIAL REPLACE AREA ######################
# Frame for partial replace inputs
partial_replace_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=10)
partial_replace_frame.grid(row=10, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Add replace controls inside the frame
partial_replace_label = tk.Label(partial_replace_frame, bg="#e7d3b0", text="PARTIAL REPLACE ->")
partial_replace_label.grid(row=0, column=0, padx=50, pady=5, sticky="nsew")

# Input for the characters to replace
partial_ori_text_label = tk.Label(partial_replace_frame, text="Find this:", bg="#e7d3b0")
partial_ori_text_label.grid(row=0, column=1, padx=5, pady=5, sticky="e")
partial_ori_text_entry = tk.Entry(partial_replace_frame, width=10, highlightbackground="#e7d3b0")
partial_ori_text_entry.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Input for the characters we want
partial_dest_text_label = tk.Label(partial_replace_frame, text="Replace it by that:", bg="#e7d3b0")
partial_dest_text_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")
partial_dest_text_entry = tk.Entry(partial_replace_frame, width=10, highlightbackground="#e7d3b0")
partial_dest_text_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

# Button to apply partial replacing
partial_replace_button = tk.Button(
    partial_replace_frame,
    text="Partial Replace",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: apply_replace(
        result_textbox, partial_ori_text_entry, partial_dest_text_entry, strict_mode=False
    ),
)
partial_replace_button.grid(row=0, column=6, padx=5, pady=5, sticky="w")


###################### RENAME AREA ######################
# Frame for rename inputs
rename_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=15)
rename_frame.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="new")

# Configure columns to expand evenly
rename_frame.grid_columnconfigure(0, weight=1)
rename_frame.grid_columnconfigure(1, weight=1)

# Add rename controls inside the frame
rename_label = tk.Label(rename_frame, bg="#e7d3b0", text="RENAMING")
rename_label.grid(row=0, column=0, columnspan=2, padx=5, pady=20, sticky="nsew")

# Input for the files to rename
path_files_label = tk.Label(rename_frame, text="Replace from path:", bg="#e7d3b0")
path_files_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
path_files_entry = tk.Entry(rename_frame, width=40, highlightbackground="#e7d3b0")  # Increased width
path_files_entry.grid(row=2, column=0, padx=5, pady=5, sticky="e")

# Browse button
browse_button = tk.Button(
    rename_frame, 
    text="Browse", 
    bg="#f07868",
    highlightbackground="#e7d3b0",
    width=10,
    command=lambda: browse_files(path_files_entry, count_label_rename)
    )
browse_button.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Add rename controls inside the frame
count_label_rename = tk.Label(rename_frame, bg="#e7d3b0", text="number of files: 0")
count_label_rename.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Button to apply rename
rename_button = tk.Button(
    rename_frame,
    text="Rename",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: apply_rename(
        result_textbox, path_files_entry
    ),
)
rename_button.grid(row=4, column=0, columnspan=2, padx=5, pady=20, sticky="sew")

###################### FILEAUDIT & MEDIAINFO AREA ######################
# Frame for inputs
analyze_frame = tk.Frame(content_frame, bg="#e7d3b0", highlightbackground="#2197a3", highlightthickness=1, bd=15)
analyze_frame.grid(row=11, column=2, columnspan=4, padx=5, pady=5, sticky="new")

# Configure columns to expand evenly
analyze_frame.grid_columnconfigure(0, weight=1)
analyze_frame.grid_columnconfigure(1, weight=1)
analyze_frame.grid_columnconfigure(2, weight=1)
analyze_frame.grid_columnconfigure(3, weight=1)

# Add title
analyze_label = tk.Label(analyze_frame, bg="#e7d3b0", text="FILE AUDIT & MEDIA INFO")
analyze_label.grid(row=0, column=0, columnspan=4, padx=5, pady=20, sticky="nsew")

# Folder selection
analyze_files_label = tk.Label(analyze_frame, text="Folder to Audit:", bg="#e7d3b0")
analyze_files_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
analyze_files_entry = tk.Entry(analyze_frame, highlightbackground="#e7d3b0")
analyze_files_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

# Browse button
browse_button = tk.Button(
    analyze_frame,
    text="Browse",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: browse_files_Audit(analyze_files_entry, count_label_audit, missing_files_textbox, extra_files_textbox),
)
browse_button.grid(row=1, column=2, padx=5, pady=5, sticky="w")

# Count number of files
count_label_audit = tk.Label(analyze_frame, bg="#e7d3b0", text="number of files: 0")
count_label_audit.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

# Button LUFS
lufs_button = tk.Button(
    analyze_frame,
    text="LUFS",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: check_lufs(analyze_files_entry.get(), lufs_button),
)
lufs_button.grid(row=1, column=3, padx=5, pady=5, sticky="sew")

# Button Media info
mediainfo_button = tk.Button(
    analyze_frame,
    text="Media info",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: apply_mediainfo(analyze_files_entry.get(), mediainfo_button),
)
mediainfo_button.grid(row=2, column=3, padx=5, pady=5, sticky="sew")

# Button File Audit
fileaudit_button = tk.Button(
    analyze_frame,
    text="File Audit",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: perform_file_audit(result_textbox, analyze_files_entry.get(), missing_files_textbox, extra_files_textbox),
)
fileaudit_button.grid(row=3, column=3, padx=5, pady=5, sticky="sew")

# Frames for Textboxes
missing_files_frame = tk.Frame(analyze_frame, bg="#e7d3b0")
missing_files_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=(30, 5), sticky="nsew")

extra_files_frame = tk.Frame(analyze_frame, bg="#e7d3b0")
extra_files_frame.grid(row=4, column=2, columnspan=2, padx=5, pady=(30, 5), sticky="nsew")

# Labels for Missing and Extra Files
missing_files_label = tk.Label(missing_files_frame, text="Missing files", bg="#e7d3b0")
missing_files_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

extra_files_label = tk.Label(extra_files_frame, text="Extra files", bg="#e7d3b0")
extra_files_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Missing Files Textbox + Scrollbar
missing_files_textbox = tk.Text(missing_files_frame, height=8, width=30, bg="white", highlightbackground="white", wrap="word")
missing_files_textbox.grid(row=1, column=0, pady=5, sticky="nsew")

missing_files_scrollbar = tk.Scrollbar(missing_files_frame, orient="vertical", command=missing_files_textbox.yview)
missing_files_scrollbar.grid(row=1, column=1, pady=5, sticky="ns")

missing_files_textbox.config(yscrollcommand=missing_files_scrollbar.set)

# Extra Files Textbox + Scrollbar
extra_files_textbox = tk.Text(extra_files_frame, height=8, width=30, bg="white", highlightbackground="white", wrap="word")
extra_files_textbox.grid(row=1, column=0, pady=5, sticky="nsew")

extra_files_scrollbar = tk.Scrollbar(extra_files_frame, orient="vertical", command=extra_files_textbox.yview)
extra_files_scrollbar.grid(row=1, column=1, pady=5, sticky="ns")

extra_files_textbox.config(yscrollcommand=extra_files_scrollbar.set)

# Open Missing files button
missing_button = tk.Button(
    missing_files_frame,
    text="See Missing Files",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: export_audit_results(missing_files_textbox, missing=True),
)
missing_button.grid(row=2, column=0, columnspan=2, padx=100, pady=5, sticky="nsew")

# Open extra files button
extra_button = tk.Button(
    extra_files_frame,
    text="See extra files",
    bg="#f07868",
    highlightbackground="#e7d3b0",
    command=lambda: export_audit_results(extra_files_textbox, missing=False),
)
extra_button.grid(row=2, column=0, columnspan=2, padx=100, pady=5, sticky="nsew")

# Make frames expandable
missing_files_frame.grid_rowconfigure(0, weight=1)
missing_files_frame.grid_columnconfigure(0, weight=1)

extra_files_frame.grid_rowconfigure(0, weight=1)
extra_files_frame.grid_columnconfigure(0, weight=1)

###################### MAIN WINDOW RESIZING ######################
root.grid_rowconfigure(1, weight=1)  # Content frame resizable
root.grid_columnconfigure(0, weight=1)

root.mainloop()