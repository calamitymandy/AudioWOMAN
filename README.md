# **AudioMAN Program - PROGRAMMER**

## **Actualize .exe:**
pyinstaller --onefile --noconsole .\AudioMan.py

## **Actualize .app & .dmg:**
pyinstaller --onefile --noconsole --windowed --name "AudioMan" AudioMan.py
dmgbuild -s settings.py "AudioMAN" dist/AudioMAN.dmg

# **AudioMAN Program - USER GUIDE**

## **Overview**
This program provides a graphical user interface (GUI) for generating file paths by concatenating multiple columns of text data. Each column represents a part of the path, and the program ensures data consistency while allowing flexibility in column inputs.

---

## **Features**
- **Dynamic Column Management**: Add or remove columns dynamically, up to a maximum of 12 columns across two rows.
- **ID Column Selection**: Choose one column as the ID column to define the reference row count for path generation.
- **Constant Value Handling**: Columns with a single value are automatically expanded to match the ID column length.
- **Extension Support**: Add an optional file extension to each generated path.
- **Error Handling**: Built-in error messages guide users through column mismatches or improper configurations.

---

## **Getting Started**
### **Launching the Program**
Run the .exe to open the program.

---

## **How to Use**
### **Step 1: Input Data**
1. Enter text into the textboxes for each column. Each line represents a separate entry.
2. Ensure the ID column contains the reference row count. Other columns should either:
   - Match the ID column in the number of entries, or
   - Contain a single value (this will be expanded automatically).

### **Step 2: Select ID Column**
- Use the dropdown labeled **"ID Column"** to select the reference column. The program requires this to validate and generate paths.

### **Step 3: Add an Extension (Optional)**
- Enter a file extension (e.g., `.wav`, `.csv`) in the **Extension** input box. This will be appended to each path.

### **Step 4: Generate Paths**
- Click the **"Generate Paths"** button to create concatenated paths from the column data. The results will appear in the **Result** area.

---

## **Results**
- Generated paths appear in the **Result** area. Copy and save them as needed.
- Example output for three columns (`Col 1`, `Col 2`, `Col 3`) with `.txt` extension:
  ```
  value1_part1_value2_part1.txt
  value1_part2_value2_part2.txt
  value1_part3_value2_part3.txt
  ```

---

Happy path generating!

