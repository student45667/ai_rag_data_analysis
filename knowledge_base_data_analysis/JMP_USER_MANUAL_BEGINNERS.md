# JMP USER MANUAL FOR BEGINNERS
## Basic Operations and Getting Started with JMP
### Written in Simple, Clear Language

---

## TABLE OF CONTENTS

1. What is JMP?
2. Getting Started
3. Opening and Creating Data Files
4. Entering and Editing Data
5. Creating Graphs
6. Basic Statistical Analysis
7. Creating Reports
8. Keyboard Shortcuts
9. Troubleshooting
10. Tips and Best Practices

---

# SECTION 1: WHAT IS JMP?

## Understanding JMP

JMP (pronounced "Jump") is a **data analysis software** that helps you:
- **Organize** data in tables
- **Visualize** data with graphs
- **Analyze** data with statistics
- **Report** findings professionally

### JMP vs Excel

**Excel:**
- Like a simple calculator
- Good for basic spreadsheets
- Limited analysis tools

**JMP:**
- Like a powerful analysis tool
- Great for complex statistics
- Professional graphs
- Advanced data analysis

Think of it this way:
- Excel = Adding up numbers
- JMP = Understanding what the numbers mean

## Why Use JMP?

✅ Beautiful graphs (for presentations)
✅ Professional reports
✅ Easy statistical analysis
✅ Good for scientific work
✅ Widely used in quality and manufacturing

---

# SECTION 2: GETTING STARTED

## Starting JMP

### Windows
1. Click the Windows **Start** button
2. Find **JMP** in your programs
3. Click to open
4. Wait for JMP to load (30 seconds)

### Mac
1. Open **Finder**
2. Go to **Applications**
3. Find **JMP**
4. Double-click to open

### What You See When JMP Opens

```
[JMP Welcome Screen]
├── Tip of the Day (can close this)
├── Quick Start Guide (optional)
├── File → Open (to open data)
├── File → New (to create new data)
└── Sample Data (practice data included)
```

**What to do:**
- Close the "Tip of the Day" if annoying
- Click "File → New → Data Table" to start fresh
- Or "File → Open" to open existing data

## The Main JMP Window

When JMP opens, you see:

```
┌─────────────────────────────────────────────┐
│ File  Edit  View  Analyze  Graph  Tools  Help│  ← Menu Bar
├─────────────────────────────────────────────┤
│                                             │
│   [My Data Table]                           │  ← Table Title
│                                             │
│   Column1  Column2  Column3                 │  ← Column Headers
│   ────────────────────────────────          │
│     5      10       apple                   │
│     6      12       banana                  │
│     7      14       cherry                  │
│                                             │
└─────────────────────────────────────────────┘
```

### The Four Parts of JMP:

**1. Menu Bar** (top)
- File: Open, Save, Close files
- Edit: Undo, Copy, Paste
- Analyze: Do statistics
- Graph: Make charts
- Help: Get help

**2. Data Table Window** (left/middle)
- Shows your spreadsheet
- Has columns and rows
- Where you enter data

**3. Results Window** (right/middle, when you analyze)
- Shows graphs and statistics
- Shows when you click "Analyze"

**4. Command Menu** (bottom)
- Shows other options

---

# SECTION 3: OPENING AND CREATING DATA FILES

## Creating a New Data Table

### Method 1: Using Menu

1. Click **File** → **New** → **Data Table**
2. A blank spreadsheet appears

### Method 2: Keyboard Shortcut

Press **Ctrl+N** (Windows) or **Cmd+N** (Mac)

## Opening an Existing File

### Method 1: Using File Menu

1. Click **File** → **Open**
2. A dialog box appears
3. Navigate to your file
4. Select it
5. Click **Open**

### Method 2: Drag and Drop

1. Find your file on your computer
2. Drag it onto the JMP icon
3. It opens automatically

### Supported File Types

✅ **.csv** (Comma-Separated Values)
✅ **.xlsx** (Excel)
✅ **.jmp** (JMP native format)
✅ **.txt** (Tab-delimited)
✅ **.sas7bdat** (SAS format)

### Example: Opening a CSV File

```
Steps:
1. File → Open
2. Find your file (wafer_data.csv)
3. Click on it
4. Click Open

Result:
JMP reads the CSV and creates a data table
All your data appears in the table
Column headers are the first row
```

## Saving Files

### Save in JMP Format

1. Click **File** → **Save**
2. File is saved as **.jmp** format
3. You can close and reopen it later

**Best for:** Keeping all your work together

### Save in CSV Format

1. Click **File** → **Save As**
2. Change **File Type** to "CSV"
3. Give it a name
4. Click **Save**

**Best for:** Sharing with other software

## Creating a New Column

### Method 1: Using Menu

1. Right-click on any column header
2. Select **New Column**
3. A dialog appears:
   - Name: (type the column name)
   - Data Type: Numeric or Character
   - Click OK

### Method 2: Click Column Label Row

1. Click on the empty column next to your data
2. Type the column name
3. Select data type

## Creating a New Row

Just click in an empty cell and start typing.
- Tab key moves to the next cell (right)
- Enter key moves to the next row (down)

---

# SECTION 4: ENTERING AND EDITING DATA

## Entering Data Manually

### Step-by-Step Example

Let's create a simple table:

```
1. Click File → New → Data Table
2. The first cell is highlighted
3. Type your first number or text
4. Press Tab to move right
5. Type the next value
6. Press Enter to move down
7. Continue until done
```

**Example data entry:**

```
You want to enter:
Name     Age    Score
John     25     85
Sarah    30     92
Mike     28     78

Steps:
1. Click first cell, type "Name", press Tab
2. Type "Age", press Tab
3. Type "Score", press Enter
4. Type "John", press Tab
5. Type "25", press Tab
6. Type "85", press Enter
7. Continue...

Result:
┌────────┬──────┬────────┐
│ Name   │ Age  │ Score  │
├────────┼──────┼────────┤
│ John   │  25  │   85   │
│ Sarah  │  30  │   92   │
│ Mike   │  28  │   78   │
└────────┴──────┴────────┘
```

## Editing Data

### Changing a Value

1. Click the cell you want to change
2. Type the new value
3. Press Enter

### Deleting Data

1. Click on the cell
2. Press Delete key
3. The cell becomes empty

### Deleting a Row

1. Click on the row number (left side)
2. Right-click
3. Select **Delete Rows**
4. The row is removed

### Deleting a Column

1. Right-click on the column header
2. Select **Delete Columns**
3. The column is removed

## Importing Data from Excel

### Step-by-Step

1. Open your Excel file (.xlsx)
2. In JMP: **File** → **Open**
3. Navigate to the Excel file
4. Click **Open**
5. A dialog appears asking about the data
6. Click **OK** to import
7. JMP creates a data table with your Excel data

---

# SECTION 5: CREATING GRAPHS

## Types of Graphs in JMP

### Graph 1: Histogram (Distribution of One Variable)

Shows how data is spread out.

**When to use:** See the shape of your data
**Example:** Distribution of test scores

**How to create:**
1. Click **Graph** → **Distribution**
2. Drag a column into **Y, Columns**
3. Click **OK**

### Graph 2: Box Plot (Comparing Distributions)

Shows median, quartiles, and outliers.

**When to use:** Compare groups or check for outliers
**Example:** Compare wafer quality across batches

**How to create:**
1. Click **Analyze** → **Distribution**
2. Drag column into **Y, Columns**
3. Click **OK**
4. In results, there's a box plot

### Graph 3: Scatter Plot (Two Variables)

Shows relationship between two things.

**When to use:** See if two variables are related
**Example:** Leakage vs Speed (are they correlated?)

**How to create:**
1. Click **Graph** → **Scatter Plot**
2. Drag one column to **X axis**
3. Drag another to **Y axis**
4. Click **OK**

### Graph 4: Line Plot (Trends Over Time)

Shows how something changes over time.

**When to use:** See trends or changes
**Example:** Temperature over the day

**How to create:**
1. Click **Graph** → **Line**
2. Drag column to **Y axis**
3. Click **OK**

## Quick Graph Example

**Problem:** You have wafer test data. You want to graph leakage current.

**Solution:**
```
1. Open your data file
2. Click Graph → Distribution
3. Drag "LEAKAGE_UA" to Y, Columns
4. Click OK

Result: A beautiful histogram appears!
Shows how leakage values are distributed.
```

## Saving Graphs

### Save as Image (PNG, JPG)

1. Right-click on the graph
2. Select **Save Image**
3. Choose format
4. Choose location
5. Click **Save**

### Save as PDF (for reports)

1. Right-click on the graph
2. Select **Save as PDF**
3. Choose location
4. Click **Save**

---

# SECTION 6: BASIC STATISTICAL ANALYSIS

## Analysis Menu Options

Click **Analyze** to see options:
- **Distribution** (histogram, summary stats)
- **Bivariate** (compare two variables)
- **Oneway ANOVA** (compare multiple groups)
- **Correlation** (find relationships)

## Example Analysis: Distribution

### What It Does
Calculates mean, standard deviation, min, max, quartiles.

### How to Do It

```
1. Open your data
2. Click Analyze → Distribution
3. Drag columns to Y, Columns
4. Click OK

Results show:
- Histogram (graph)
- Summary Statistics (table)
- Quartiles (Q1, median, Q3)
```

### Example Output

```
LEAKAGE_UA

N:                 125,664
Mean:              10.01
Std Dev:           1.48
Min:               5.23
Max:               14.87
Q1 (25%):          9.12
Median (50%):      10.05
Q3 (75%):          10.98
```

## Example Analysis: Compare Two Variables

### What It Does
Shows if two variables are related.

### How to Do It

```
1. Open your data
2. Click Analyze → Bivariate
3. Put one column in X
4. Put another in Y
5. Click OK

Results show:
- Scatter plot
- Correlation coefficient
- If relationship is significant
```

### Understanding Correlation

```
Correlation = -1.0 to +1.0

+1.0 = Perfect positive (both increase together)
+0.5 = Moderate positive (somewhat related)
 0.0 = No relationship
-0.5 = Moderate negative (opposite)
-1.0 = Perfect negative (perfect opposite)

Example:
Temperature vs Ice Cream Sales: +0.8 (positive)
Temperature vs Heating Bill: -0.9 (negative)
Temperature vs Random Numbers: 0.0 (no relationship)
```

---

# SECTION 7: CREATING REPORTS

## Saving Analysis Results

### Option 1: Print to PDF

1. Do your analysis (creates results window)
2. Click **File** → **Print to PDF**
3. Choose location
4. Click **Save**

**Result:** PDF file with all graphs and tables

### Option 2: Export Results

1. Select the results window (click on it)
2. Click **File** → **Save As**
3. Choose format (PDF, HTML, etc.)
4. Click **Save**

## Creating a Summary Table

### Problem
You want to summarize: Count, Mean, Std Dev by Group

### Solution: Tabulate Command

```
1. Click Analyze → Summary/Summary Statistics
2. Choose what to summarize (e.g., LEAKAGE_UA)
3. Choose grouping (e.g., by WAFER_ID)
4. Click OK

Results: Table showing stats by group
```

### Example Result

```
WAFER_ID  Count  Mean Leakage  Std Dev
────────────────────────────────────────
W001      100    9.95          1.42
W002      100    10.08         1.51
W003      100    10.23         1.45
W004      100    9.87          1.38
W005      100    10.12         1.49
```

## Copying Results to Word/PowerPoint

### Method 1: Copy Graph

1. Right-click on graph
2. Click **Copy**
3. Go to Word/PowerPoint
4. Press Ctrl+V (or Cmd+V)
5. Graph appears in document

### Method 2: Save as Image

1. Right-click on graph
2. Select **Save Image**
3. In Word: Insert → Picture
4. Select your saved image

---

# SECTION 8: KEYBOARD SHORTCUTS

## File Operations

| Action | Windows | Mac |
|--------|---------|-----|
| New File | Ctrl+N | Cmd+N |
| Open File | Ctrl+O | Cmd+O |
| Save File | Ctrl+S | Cmd+S |
| Print | Ctrl+P | Cmd+P |
| Close | Ctrl+W | Cmd+W |
| Quit JMP | Ctrl+Q | Cmd+Q |

## Editing

| Action | Windows | Mac |
|--------|---------|-----|
| Undo | Ctrl+Z | Cmd+Z |
| Redo | Ctrl+Y | Cmd+Y |
| Cut | Ctrl+X | Cmd+X |
| Copy | Ctrl+C | Cmd+C |
| Paste | Ctrl+V | Cmd+V |
| Select All | Ctrl+A | Cmd+A |

## Navigation

| Action | Windows | Mac |
|--------|---------|-----|
| Move to next cell | Tab | Tab |
| Move to next row | Enter | Enter |
| Move up | Up arrow | Up arrow |
| Move down | Down arrow | Down arrow |
| Go to beginning | Home | Home |
| Go to end | End | End |

---

# SECTION 9: TROUBLESHOOTING

## Problem 1: Can't Open a File

**Symptom:** "File not found" error

**Solutions:**
1. Check the file path is correct
2. Check the file hasn't been moved
3. Try dragging the file onto JMP instead

## Problem 2: Data Looks Weird in Table

**Symptom:** Columns are too narrow or too wide

**Solutions:**
1. Double-click the column border to auto-fit
2. Or drag the column border to resize manually

## Problem 3: Analysis Results Don't Appear

**Symptom:** Click Analyze but nothing happens

**Solutions:**
1. Make sure you selected at least one column
2. Make sure data type is correct (numeric for stats)
3. Check the Log window for error messages (View → Log)

## Problem 4: Graph Looks Wrong

**Symptom:** Graph is blank or incorrectly scaled

**Solutions:**
1. Check you have valid data
2. Check for missing values (blank cells)
3. Click on graph and try "Redo Graph"

## Problem 5: Data Won't Import from Excel

**Symptom:** Excel file won't open or data is jumbled

**Solutions:**
1. Save Excel file as CSV first, then open CSV
2. Check first row is headers, not data
3. Check data doesn't have special characters

---

# SECTION 10: TIPS AND BEST PRACTICES

## Tip 1: Always Start with Explore

```
Good workflow:
1. Open your data
2. Create Distribution analysis (see what you have)
3. Create Scatter plots (see relationships)
4. THEN do more complex analysis

This helps you understand your data first.
```

## Tip 2: Check Your Data First

```
Before analyzing, always check:
✓ No blank cells where there shouldn't be
✓ Data types are correct (numeric vs character)
✓ Column headers make sense
✓ Values look reasonable (not 99999 when should be 5)
```

## Tip 3: Use Meaningful Column Names

```
Good column names:
✓ LEAKAGE_UA (clear what it is, what units)
✓ FMAX_MHZ (frequency in megahertz)
✓ TEST_DATE (when the test happened)

Bad column names:
✗ X1, X2, X3 (no idea what they are)
✗ Data (too vague)
✗ leakage current microamps (too long)
```

## Tip 4: Label Your Analyses

```
When you do analysis, add labels:
1. Analyze → Distribution
2. Add a title like "Wafer W001 Leakage Analysis"
3. Add notes explaining what you're looking at
4. This helps when you review later
```

## Tip 5: Save Everything

```
Always keep:
- Original data (.csv or .jmp)
- Analysis results (.jmp)
- Exported graphs (.png or .pdf)

This way you can always go back to check things.
```

## Tip 6: Use Sample Data to Learn

```
JMP comes with free sample data:
1. Click File → Sample Data
2. Choose a dataset
3. Try different analyses on it
4. See what works and what doesn't

This is great for learning!
```

## Tip 7: Master the Scripting Index

```
When you need help:
1. Click Help → Scripting Index
2. Search for what you want to do
3. See example code

This is your best friend for learning.
```

---

# QUICK START GUIDE

## 5-Minute Tutorial

**Goal:** Analyze wafer test data and create a report

### Step 1: Open Data (1 minute)
```
1. File → Open
2. Select wafer_data.csv
3. Click Open
4. Wait for data to load
```

### Step 2: Explore Data (1 minute)
```
1. Analyze → Distribution
2. Drag LEAKAGE_UA to Y, Columns
3. Click OK
4. Look at the histogram
```

### Step 3: Create Graph (1 minute)
```
1. Graph → Scatter Plot
2. X: LEAKAGE_UA
3. Y: FMAX_MHZ
4. Click OK
5. See if they're related
```

### Step 4: Check Statistics (1 minute)
```
1. Look at the summary statistics from Distribution
2. Note Mean, Std Dev, Min, Max
3. Are values in spec range?
```

### Step 5: Save Everything (1 minute)
```
1. Right-click histogram → Save Image
2. File → Save As → Save as JMP
3. You've got: Graph + Data + Analysis
```

**Done!** You've completed a basic analysis! 🎉

---

# SUMMARY

You've learned:
✅ What JMP is
✅ How to open and create files
✅ How to enter and edit data
✅ How to create graphs
✅ How to do basic statistical analysis
✅ How to save and export results
✅ Keyboard shortcuts
✅ Troubleshooting tips
✅ Best practices

**Next Steps:**
1. Open JMP
2. Create a new data table
3. Enter some test data
4. Create a graph
5. Do an analysis

The more you practice, the better you'll get!

---

# APPENDIX: COMMON ANALYSIS WORKFLOWS

## Workflow 1: Basic Data Exploration

```
Goal: Understand your data

Steps:
1. Open data file
2. Analyze → Distribution (for each column)
3. Graph → Scatter Plot (for pairs of columns)
4. Review results
5. Save everything

Outcome: You understand what you have
```

## Workflow 2: Compare Two Groups

```
Goal: Are Group A and Group B different?

Steps:
1. Open data file
2. Analyze → Oneway ANOVA (if you have groups)
3. Or Analyze → Bivariate (if you have two variables)
4. Review p-value (if < 0.05, probably different)
5. Create graphs showing the difference
6. Save results

Outcome: Know if groups are significantly different
```

## Workflow 3: Quality Control Analysis

```
Goal: Check if process is in control

Steps:
1. Open data file (test measurements)
2. Analyze → Distribution (calculate mean, std dev)
3. Analyze → Control Charts (if available)
4. Check if anything is out of spec limits
5. Create report with findings
6. Save everything

Outcome: Know if process is good
```

---

**Good luck using JMP! It's a powerful tool, and practice makes perfect.** 🚀
