# **AudioWOMAN Program - PROGRAMMER**

## **Actualize .exe:**
* pyinstaller --onefile --noconsole .\AudioWOMAN.py
* *OR* pyinstaller --onefile --windowed --hidden-import pymediainfo --name "AudioWOMAN" AudioWOMAN.py

## **Actualize .app & .dmg:**
* pyinstaller --onefile --noconsole --windowed --name "AudioWOMAN" AudioWOMAN.py
* *OR* pyinstaller --onefile --windowed --hidden-import=pymediainfo AudioWOMAN.py
* dmgbuild -s settings.py "AudioWOMAN" dist/AudioWOMAN.dmg

------------------------------------------------------------------------

# **AudioWOMAN Program - USER GUIDE**

## **Overview**

This tool streamlines file organization and batch renaming, ensuring efficiency and accuracy. 🚀

AudioWOMAN is a tool designed for efficient file path generation, modification, and renaming. By combining multiple columns of text data, it ensures consistency while allowing flexibility in column inputs—making it ideal for batch processing and file organization.

The program includes tools to modify paths through truncation or text replacement before applying changes to actual files. 

It also features an automated renaming system that organizes files into structured directories based on the generated paths, and 2 tools for analyzing data: file audit and media info.


---

## **Features**

- **Dynamic Column Management**: Add or remove columns dynamically, with support for up to 12 columns across two rows.
- **ID Column Selection**: Choose one column as the reference for path generation.
- **Automatic Value Expansion**: Single-value columns are expanded to match the reference column length.
- **File Extension Support**: Append an optional file extension to each generated path.
- **Path Truncation**: Remove parts of a file path based on a specific character or a defined number of characters.
- **Text Replacement in Paths**: Quickly find and replace specific text within file paths.
- **Automated File Renaming**: Copy files into a structured `_renamed` folder and rename them based on generated paths, preserving subdirectories when necessary.
- **File Audit**: Compare filenames from a list with files in a selected folder, identifying missing and extra files.
- **Media Info**: Checks all audio files in a selected directory for uniformity in sampling rate, bit depth, and number of channels.
- **Error Handling**: Built-in warnings and error messages guide users through column mismatches or invalid inputs.

---

## **Getting Started**

### **Launching the Program**

Run the `.exe` (Windows) or `.dmg` (Mac) file to open the application.

---

## **How to Use**

### **Generate New Paths / Add More Paths**

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

To generate your list of path you can choose one of thes two options:
  - Click **"Generate New Paths"** to create concatenated paths. The results will appear in the **Result** area and will overwrite whatever was already in the result area.
  - Click **"Add More Paths"** to add concatenated paths below the one that are already in the **Result** area.

## **Results**

- Generated or modified paths (or manually entered paths) appear in the **Result** area.
- Example output for three columns (`Col 1`, `Col 2`, `Col 3`) with a `.txt` extension:
  ```
  value1_part1_value2.txt
  value1_part2_value2.txt
  value1_part3_value2.txt
  ```

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

💡 **Tip:** Tip: Use this to cut parts of your path (e.g. replace “/001/” by nothing).

⚠ **Important:** 
- For the “Replace All” option, the program searches for the first occurrence of the text you entered.  If the text isn’t found in all paths, an error will be displayed.

- For the “Partial Replace” option, every occurrence of the text present in any path will be replaced.

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

### **File Audit**
🔹 **What it does:**
Compares filenames from the generated paths with actual files in a selected folder, identifying missing and extra files.

📌 Steps:
1.	Put the list of filenames in result textbox (copy/paste it or generate it)
⚠ **Important:** Ensure the list of filenames contains the exact name of the files with the extension (e.g. “name_of_the_audio_file.wav”)
2.	Select a folder to analyze.
3.	Click on button **"File Audit"**.
4.	The program will compare the generated paths with actual filenames and display missing and extra files.
You can export the results as a text files.

---

### **Media Info**

🔹 **What it does:**
Checks all audio files in a selected directory for uniformity in sampling rate, bit depth, and number of channels.

📌 Steps:
1.	Select a folder containing audio files.
2.	Click on button **"Media Info"**.
3.	The program will check if all files have the same parameters.
If discrepancies are found, a detailed report will be displayed and can be saved.


### **Clear All: Reset Everything**

🔹 **What it does:**
Resets all text fields, selections, and settings, clearing any loaded paths.

💡 **Use this when:** You want to start over with a clean slate.

---

Now do your magic!

