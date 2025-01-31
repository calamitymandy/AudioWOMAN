# **AudioMAN Program - PROGRAMMER**

## **Actualize .exe:**
pyinstaller --onefile --noconsole .\AudioMan.py

## **Actualize .app & .dmg:**
pyinstaller --onefile --noconsole --windowed --name "AudioMan" AudioMan.py
dmgbuild -s settings.py "AudioMAN" dist/AudioMAN.dmg

------------------------------------------------------------------------

# **AudioMAN Program - USER GUIDE**

## **Overview**

This tool streamlines file organization and batch renaming, ensuring efficiency and accuracy. 🚀

AudioMAN is a user-friendly tool designed to generate file paths by combining multiple columns of text data. It ensures consistency while allowing flexibility in column inputs, making it ideal for batch processing and file organization. The program also allows users to modify paths through truncation or text replacement before applying the changes to actual files. Additionally, it provides an automated renaming feature that organizes files into structured directories based on the generated paths.

---

## **Features**

- **Dynamic Column Management**: Add or remove columns dynamically, with support for up to 12 columns across two rows.
- **ID Column Selection**: Choose one column as the reference for path generation.
- **Automatic Value Expansion**: Single-value columns are expanded to match the reference column length.
- **File Extension Support**: Append an optional file extension to each generated path.
- **Path Truncation**: Remove parts of a file path based on a specific character or a defined number of characters.
- **Text Replacement in Paths**: Quickly find and replace specific text within file paths.
- **Automated File Renaming**: Copy files into a structured `_renamed` folder and rename them based on generated paths, preserving subdirectories when necessary.
- **Error Handling**: Built-in warnings and error messages guide users through column mismatches or invalid inputs.

---

## **Getting Started**

### **Launching the Program**

Run the `.exe` (Windows) or `.dmg` (Mac) file to open the application.

---

## **How to Use**

### **Generate Paths**

🔹 **What it does:**
Creates file paths by concatenating the values entered in each column.

🔹 **How to use it:**

1.	Add up to 12 columns to put your text and remove them as needed
2.	Enter text into the textboxes for each column. Each line represents a separate entry.
3.	Ensure the ID column contains the reference row count. Other columns should either:
   - Match the ID column in the number of entries, or
   - Contain a single value (which will be automatically expanded).
4.	(Optional) Add a file extension (e.g., `.wav`, `.csv`) in the **Extension** input box.
5.	(Optional) Copy in the first column all file paths from a directory, including the ones in subdirectories. 
6. Use the **"ID Column"** dropdown to select the reference column.
7. Click **"Generate Paths"** to create concatenated paths. The results will appear in the **Result** area.

---

### **Truncate Paths**

🔹 **What it does:**
Removes part of a file path from the left or right.

🔹 **How to use it:**

1. Use your generated paths or enter text (copy/paste) into the **"Result"** textbox.
2. Enter the number of characters or a specific character to truncate at.
3. Select **"Left"** (keep the right part) or **"Right"** (keep the left part).
4. Click **"Apply Truncation"**.

⚠ **Important:** The program searches for the first occurrence of the specified character from the left or right. The character must be present in each path; otherwise, an error will be displayed.

---

### **Replace Text in Paths**

🔹 **What it does:**
Finds and replaces specific text in file paths.

🔹 **How to use it:**

1. Enter the text you want to replace.
2. Enter the new text (or nothing if you want to erase the text you entered).
3. Click **"Apply Replace"**.

💡 **Tip:** Use this to adjust filenames or modify folder names before renaming.

⚠ **Important:** The program searches for the first occurrence of the text you entered. If the text isn’t found in all paths, an error will be displayed.

---

### **Renaming Files**

🔹 **What it does:**
Copies all files from a selected folder to a new `_renamed` folder and renames them based on the paths listed in the **Result** textbox. It also creates subdirectories if needed.

🔹 **How to use it:**

1. Select the folder where your files are stored.
2. Click **"Rename"**.
3. The files will be copied into a `_renamed` folder, preserving subfolder structure.

⚠ **Important:** Ensure the number of copied files matches the number of paths to avoid errors.

---

### **Clear All: Reset Everything**

🔹 **What it does:**
Resets all text fields, selections, and settings, clearing any loaded paths.

💡 **Use this when:** You want to start over with a clean slate.

---

## **Results**

- Generated or modified paths (or manually entered paths) appear in the **Result** area.
- Example output for three columns (`Col 1`, `Col 2`, `Col 3`) with a `.txt` extension:
  ```
  value1_part1_value2.txt
  value1_part2_value2.txt
  value1_part3_value2.txt
  ```

---

Now do your magic!

