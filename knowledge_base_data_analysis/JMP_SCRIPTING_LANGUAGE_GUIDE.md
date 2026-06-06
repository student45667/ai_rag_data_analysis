# JMP SCRIPTING LANGUAGE (JSL) BEGINNER'S GUIDE
## Learn to Automate JMP Tasks with Code
### Written in Simple, Easy-to-Understand Language

---

## TABLE OF CONTENTS

1. What is JSL and Why Should You Use It?
2. Getting Started with JSL
3. Basic JSL Syntax and Commands
4. Working with Data Tables
5. Real-World Examples
6. Common JSL Functions
7. Troubleshooting and Tips
8. Resources for Learning More

---

# SECTION 1: WHAT IS JSL AND WHY SHOULD YOU USE IT?

## What is JMP Scripting Language (JSL)?

JSL (JMP Scripting Language) is a programming language built into JMP that lets you **automate tasks** and **write code** instead of clicking buttons.

### Real-World Analogy

Imagine you have a kitchen recipe:
- **Without JSL (Manual way)**: Every day, you read the recipe, measure ingredients, mix, cook, and clean. Repetitive!
- **With JSL (Automated way)**: You write down the recipe as a program. You just run the program, and the computer does everything. Fast!

Same idea with JMP:
- **Without JSL**: Click menu → click option → click button → wait → look at results
- **With JSL**: Write code → run it → get results instantly

## Why Use JSL?

### Reason 1: **Automation** (Do Repetitive Tasks Faster)
```
You test 100 wafers every week.
Each one requires: Load data → Create chart → Calculate stats → Save report

Without JSL: 100 times of clicking (hours of work)
With JSL: Run one script (seconds of work)
```

### Reason 2: **Consistency** (Same Thing Every Time)
```
Without JSL: Manual clicking might miss steps or do things differently
With JSL: The code does exactly the same thing every time
```

### Reason 3: **Reproducibility** (You Can Show Others Your Work)
```
Without JSL: "I clicked... then I clicked... then I right-clicked..."
With JSL: Here's the code. Anyone can run it and get the same results.
```

### Reason 4: **Complex Tasks** (Do Things That Are Hard to Click)
```
Some analysis is too complicated to do by clicking.
JSL lets you program complex logic.
```

## When Should You Use JSL?

### Use JSL When:
✅ You do the same analysis repeatedly
✅ You have lots of data files to process
✅ You need to combine multiple analyses
✅ You need to create custom reports
✅ You need to automate a workflow

### Don't Need JSL When:
❌ You're doing one quick analysis
❌ You're exploring data for the first time
❌ You're learning to use JMP

---

# SECTION 2: GETTING STARTED WITH JSL

## Where to Write JSL Code

### Method 1: The Script Editor (Recommended)

In JMP:
1. Click **File** → **New** → **Script**
2. A script editor window opens
3. Type your code here
4. Click the **Run Script** button (play icon)

```
[Screenshot description:
The Script Editor window has:
- A big white area where you type code
- A "Run Script" button (green play icon) at the top
- A "Save" button
- Line numbers on the left
]
```

### Method 2: The Log Window

In JMP:
1. Click **View** → **Log**
2. The Log window appears at the bottom
3. You can type commands here too

(But Script Editor is better because you can save your code)

### Method 3: In a Data Table Window

1. Right-click in the data table
2. Select **New Script**
3. Type your code

## Your First JSL Program

Let's write the simplest possible JSL program:

```jsl
// This is a comment - it doesn't do anything
// Comments start with //

print("Hello, World!");
```

What to do:
1. Open the Script Editor
2. Copy and paste this code
3. Click "Run Script"

**Result:**
In the Log window, you'll see:
```
[1] "Hello, World!"
```

Congratulations! You wrote your first JSL program! 🎉

## Understanding the Code

```jsl
print("Hello, World!");
```

Breaking this down:
- `print` = A command that outputs text
- `("Hello, World!")` = What to print (in quotation marks)
- `;` = End of statement (like a period at the end of a sentence)

Think of it like English:
```
English:   "Output the text 'Hello, World!'"
JSL:       print("Hello, World!");
```

---

# SECTION 3: BASIC JSL SYNTAX AND COMMANDS

## Understanding JSL Syntax

JSL syntax is the "grammar" of the language. Just like English has rules (subject-verb-object), JSL has rules.

### Rule 1: Every Statement Ends with a Semicolon (;)

```jsl
// Correct
print("Hello");

// Wrong (no semicolon)
print("Hello")
```

### Rule 2: Comments Start with //

```jsl
// This is a comment - the computer ignores it
// Use comments to explain your code

print("This is code"); // This line prints text
```

### Rule 3: Text in Quotes is Called a String

```jsl
// These are strings (text)
"Hello"
"Leakage Current"
"2026-05-27"

// These are NOT strings (no quotes)
123
3.14
```

### Rule 4: Capitalization Matters

```jsl
// These are DIFFERENT
Print("Hello");  // Error - Print doesn't exist
print("Hello");  // Correct

// JSL is flexible with capitalization in some places, but:
Data Table("mydata");  // Correct
data table("mydata");  // Might not work
```

## Basic Data Types

### Type 1: Numbers

```jsl
// Integer (whole number)
x = 5;

// Decimal number
y = 3.14;

// Negative number
z = -10;
```

### Type 2: Text (Strings)

```jsl
// String in quotes
name = "John";
product = "Wafer W001";
```

### Type 3: TRUE/FALSE (Boolean)

```jsl
// Boolean (logical values)
is_good = true;      // This is true
is_bad = false;      // This is false

// Often used in comparisons
x = 5;
result = (x > 3);    // result = true
```

## Variables (Storing Values)

A variable is like a **labeled box** that holds a value.

```jsl
// Create a variable and store a value in it
name = "John";

// Use the variable
print(name);         // Prints: John

// Change the variable
name = "Sarah";
print(name);         // Prints: Sarah
```

Think of it like this:
```
Box labeled "name" contains: "John"
Box labeled "age" contains: 25
Box labeled "yield" contains: 95.5
```

## Basic Math Operations

```jsl
// Addition
x = 5 + 3;           // x = 8

// Subtraction
y = 10 - 4;          // y = 6

// Multiplication
z = 3 * 7;           // z = 21

// Division
w = 20 / 4;          // w = 5

// More complex
result = (5 + 3) * 2;  // result = 16
```

## Comparison Operations (TRUE or FALSE)

```jsl
// Equal to
5 == 5;              // true
5 == 3;              // false

// Not equal to
5 != 3;              // true

// Greater than
10 > 5;              // true

// Less than
3 < 8;               // true

// Greater than or equal to
5 >= 5;              // true

// Less than or equal to
4 <= 6;              // true
```

---

# SECTION 4: WORKING WITH DATA TABLES

## Opening a Data Table

### Method 1: Open an Existing File

```jsl
// Open a CSV or JMP file
dt = Open("C:\Users\John\wafer_data.csv");
```

(Note: On Mac, use forward slashes: `/Users/John/wafer_data.csv`)

### Method 2: Open a File with Dialog

```jsl
// User picks the file by clicking
dt = open();
```

### Method 3: Use Sample Data

```jsl
// Open a sample data file that comes with JMP
dt = Open("$SAMPLE_DATA\companies.jmp");
```

(The `$SAMPLE_DATA` is a special folder in JMP)

## Working with Columns (Variables)

### Get a Column

```jsl
// Reference a column
col = Column(dt, "LEAKAGE_UA");

// Or use the name directly
col = Column("LEAKAGE_UA");
```

### Create a New Column

```jsl
// Add a new column to the data table
dt << New Column("Yield_Percent", numeric);

// Or with a formula
dt << New Column("Pass_Fail", character);
```

### Access Column Data

```jsl
// Get the mean of a column
mean_value = Mean(Column(dt, "LEAKAGE_UA"));

// Get the standard deviation
std_value = Std Dev(Column(dt, "LEAKAGE_UA"));

// Get the minimum value
min_value = Min(Column(dt, "LEAKAGE_UA"));

// Get the maximum value
max_value = Max(Column(dt, "LEAKAGE_UA"));

// Print results
print(mean_value);
```

## Working with Rows (Data Points)

### Get Number of Rows

```jsl
// How many rows in the table?
n_rows = N Rows(dt);
print("Number of rows: " || n_rows);
```

### Filter Rows

```jsl
// Keep only rows where LEAKAGE_UA > 5
dt << Subset(Where(Column(dt, "LEAKAGE_UA") > 5));
```

### Sort Rows

```jsl
// Sort by LEAKAGE_UA in ascending order
dt << Sort(By(Column("LEAKAGE_UA")));
```

## Quick Statistical Analysis

```jsl
// Open data table
dt = Open("wafer_data.csv");

// Calculate statistics
mean_leakage = Mean(Column(dt, "LEAKAGE_UA"));
std_leakage = Std Dev(Column(dt, "LEAKAGE_UA"));
n = N Rows(dt);

// Print results
print("===== STATISTICS =====");
print("Mean: " || mean_leakage);
print("Std Dev: " || std_leakage);
print("Count: " || n);
```

**Output in Log:**
```
===== STATISTICS =====
Mean: 10.0234
Std Dev: 1.4823
Count: 125664
```

---

# SECTION 5: REAL-WORLD EXAMPLES

## Example 1: Analyze Wafer Test Data

```jsl
// ===== COMPLETE WAFER ANALYSIS SCRIPT =====

// Step 1: Open data
dt = Open("circular_grid_params.csv");

// Step 2: Get column references
leakage = Column(dt, "LEAKAGE_UA");
fmax = Column(dt, "FMAX_MHZ");
x_coord = Column(dt, "X_COORD");
y_coord = Column(dt, "Y_COORD");

// Step 3: Filter valid dies only
dt << Subset(Where(Column(dt, "BIN") == 1), Output Table("ValidDies"));
dt_valid = Data Table("ValidDies");

// Step 4: Calculate statistics
mean_leak = Mean(Column(dt_valid, "LEAKAGE_UA"));
std_leak = Std Dev(Column(dt_valid, "LEAKAGE_UA"));
min_leak = Min(Column(dt_valid, "LEAKAGE_UA"));
max_leak = Max(Column(dt_valid, "LEAKAGE_UA"));

// Step 5: Check against specification
spec_max = 15.0;
failures = N(Column(dt_valid, "LEAKAGE_UA") > spec_max);
pass_rate = (N Rows(dt_valid) - failures) / N Rows(dt_valid) * 100;

// Step 6: Print report
print("===== WAFER ANALYSIS REPORT =====");
print("Valid Dies: " || N Rows(dt_valid));
print("Mean Leakage: " || mean_leak);
print("Std Dev: " || std_leak);
print("Min: " || min_leak);
print("Max: " || max_leak);
print("Pass Rate: " || pass_rate || "%");
```

**What This Does:**
1. Opens wafer test data
2. Filters only valid dies
3. Calculates statistics
4. Checks against spec limits
5. Prints a report

## Example 2: Create a Control Chart

```jsl
// Open data
dt = Open("wafer_data.csv");

// Create a control chart for leakage
dt << Control Chart(
    Rational Subgroup(Column("WAFER_ID")),
    Y(Column("LEAKAGE_UA"))
);
```

**Result:** JMP creates a control chart automatically!

## Example 3: Loop Through Multiple Files

```jsl
// ===== PROCESS MULTIPLE FILES =====

// Folder with data files
folder = "C:\Users\John\wafer_data\";

// Get list of CSV files
files = Files in Directory(folder, "*.csv");

print("Processing " || N Items(files) || " files...");

// Loop through each file
For(i = 1, i <= N Items(files), i++,
    filename = files[i];
    file_path = folder || filename;
    
    print("Processing: " || filename);
    
    // Open the file
    dt = Open(file_path);
    
    // Do analysis
    mean_leak = Mean(Column(dt, "LEAKAGE_UA"));
    print("  Mean leakage: " || mean_leak);
    
    // Close the file
    dt << Close();
);

print("Done!");
```

**What This Does:**
1. Finds all CSV files in a folder
2. Opens each one
3. Calculates the mean
4. Closes the file
5. Moves to the next file

Imagine doing this manually - clicking 100 times! With JSL, it's automated.

---

# SECTION 6: COMMON JSL FUNCTIONS

## String Functions

```jsl
// Concatenate (combine) strings
text = "Leakage: " || "10.5 µA";
print(text);  // Output: Leakage: 10.5 µA

// Get substring
word = "LEAKAGE_UA";
part = Substr(word, 1, 7);  // "LEAKAGE"

// Convert to uppercase
lower = "hello";
upper = Upper(lower);  // "HELLO"

// Convert to lowercase
Upper_text = "HELLO";
lower = Lower(Upper_text);  // "hello"
```

## Math Functions

```jsl
// Absolute value
Abs(-5);           // 5

// Square root
Sqrt(16);          // 4

// Power
2 ^ 3;             // 8 (2 to the power of 3)

// Round
Round(3.7);        // 4
Round(3.14159, 2); // 3.14

// Minimum and maximum
Min(5, 3, 9);      // 3
Max(5, 3, 9);      // 9
```

## Statistical Functions

```jsl
// Mean (average)
Mean({1, 2, 3, 4, 5});           // 3

// Standard deviation
Std Dev({1, 2, 3, 4, 5});        // 1.58...

// Count
N Items({1, 2, 3, 4, 5});        // 5

// Minimum
Min({10, 5, 20});                // 5

// Maximum
Max({10, 5, 20});                // 20

// Percentile
Quantile({1, 2, 3, 4, 5}, 0.99); // 4.96 (99th percentile)
```

## Conditional Functions (IF)

```jsl
// Simple IF
If(x > 5,
    print("x is greater than 5"),
    print("x is 5 or less")
);

// Multiple conditions
If(x > 10,
    print("Very high"),
    If(x > 5,
        print("High"),
        print("Low")
    )
);
```

## Loop Functions (FOR)

```jsl
// Count from 1 to 5
For(i = 1, i <= 5, i++,
    print(i)
);
// Output: 1, 2, 3, 4, 5

// Loop through a list
items = {"apple", "banana", "cherry"};
For(i = 1, i <= N Items(items), i++,
    print(items[i])
);
// Output: apple, banana, cherry
```

---

# SECTION 7: TROUBLESHOOTING AND TIPS

## Common Errors and Fixes

### Error 1: Missing Semicolon

```jsl
// Wrong
print("Hello")
print("World");

// Error: Expecting ';' before 'print'

// Correct
print("Hello");
print("World");
```

### Error 2: Unknown Column Name

```jsl
// Wrong
Column("leakage_ua");  // Exact case must match!

// Error: Couldn't find column

// Correct
Column("LEAKAGE_UA");  // Match the exact name
```

### Error 3: String vs Number Confusion

```jsl
// Wrong - trying to add number and string
x = 5 + "3";  // Error!

// Correct - convert string to number first
x = 5 + Num("3");  // x = 8
```

### Error 4: Data Table Not Found

```jsl
// Wrong
dt = Data Table("non_existent_table");  // Error!

// Correct - check data table list first
Show(Data Tables());  // Shows all open tables
dt = Data Table("ValidDies");
```

## Debugging Tips

### Tip 1: Use Print to Check Values

```jsl
// Add print statements to see what's happening
x = 5;
print("x = " || x);  // Check the value

y = x + 10;
print("y = " || y);  // Check again
```

### Tip 2: Check Data Table Structure

```jsl
// See column names
Show(Column Names(dt));

// See number of rows
print("Rows: " || N Rows(dt));

// See first few rows
print(dt);
```

### Tip 3: Use the Log Window

```jsl
// The Log shows error messages
// If something goes wrong, check the Log window!
// View → Log (to show the Log)
```

## Best Practices

### 1. Comment Your Code

```jsl
// Good - comments explain what's happening
// Open the data file
dt = Open("wafer_data.csv");

// Filter to valid dies only
dt << Subset(Where(Column("BIN") == 1));

// Bad - no comments, hard to understand
dt = Open("wafer_data.csv");
dt << Subset(Where(Column("BIN") == 1));
```

### 2. Use Meaningful Variable Names

```jsl
// Good - name tells you what it is
mean_leakage = Mean(Column("LEAKAGE_UA"));

// Bad - name is unclear
x = Mean(Column("LEAKAGE_UA"));
```

### 3. Add Whitespace and Indentation

```jsl
// Good - organized and readable
For(i = 1, i <= 5, i++,
    If(i > 3,
        print("High: " || i),
        print("Low: " || i)
    )
);

// Bad - hard to read
For(i = 1, i <= 5, i++, If(i > 3, print("High: " || i), print("Low: " || i)));
```

### 4. Test with Small Data First

```jsl
// Test with 10 rows first
dt = Open("wafer_data.csv") << Subset(Rows(1::10), Output Table("test"));

// If it works, use all data
dt = Open("wafer_data.csv");
```

---

# SECTION 8: RESOURCES FOR LEARNING MORE

## Official JMP Resources

### 1. Scripting Index (Built into JMP)
- **Where**: Help → Scripting Index
- **What**: Shows all JSL functions and syntax
- **Best for**: Looking up how to do something

### 2. JMP Scripting Guide
- **Where**: Help → Books → Scripting Guide (PDF)
- **What**: Complete reference of all JSL commands
- **Best for**: Deep understanding of topics

### 3. JSL Syntax Reference
- **Where**: Help → Books → JSL Syntax Reference (PDF)
- **What**: Detailed syntax for every function
- **Best for**: Understanding exact parameters

## Books About JSL

### Book 1: "Jump into JMP Scripting" (2nd Edition)
- **Author**: Murphy & Lucas
- **Level**: Beginner
- **Best for**: Learning step-by-step with examples
- **Note**: Free code examples available on JMP website

### Book 2: "JSL Companion" (2nd Edition)
- **Author**: Utlaut, Morgan, Anderson
- **Level**: Intermediate/Advanced
- **Best for**: Real-world industrial problems
- **Note**: Contains real-world case studies

## Online Learning

### JMP User Community
- **Website**: community.jmp.com
- **What**: Forums where you can ask questions
- **Best for**: Getting help from experts

### JMP Training Videos
- **Website**: jmp.com/learning
- **What**: Video tutorials
- **Best for**: Visual learners

## Tips for Learning JSL

### 1. Start Simple
```jsl
// Start with simple print statements
print("Learning JSL");

// Then add variables
x = 5;
print(x);

// Then work with data
mean_value = Mean(Column("LEAKAGE_UA"));
```

### 2. Copy and Modify
- Find a script that does something similar
- Copy it
- Change it to do what you need
- Test it

### 3. Use Scripting Index
- Go to Help → Scripting Index
- Search for what you want to do
- Copy the example code
- Modify it

### 4. Practice
- Write a script every day
- Start with small problems
- Gradually do more complex tasks

### 5. Don't Memorize
- You don't need to memorize all commands
- Scripting Index and Google are your friends
- Just know how to find what you need

---

## QUICK REFERENCE CARD

### Opening and Closing Files
```jsl
dt = Open("filename.csv");
dt << Close();
```

### Working with Columns
```jsl
mean = Mean(Column(dt, "ColumnName"));
col_data = Column(dt, "ColumnName");
```

### Working with Rows
```jsl
n_rows = N Rows(dt);
dt << Subset(Where(Column("ColumnName") > value));
dt << Sort(By(Column("ColumnName")));
```

### Statistics
```jsl
Mean(Column("X"));
Std Dev(Column("X"));
Min(Column("X"));
Max(Column("X"));
```

### Printing and Output
```jsl
print("Text");
print("Value: " || variable);
```

### Loops and Conditions
```jsl
For(i = 1, i <= 10, i++, /*do something*/);
If(condition, /*true action*/, /*false action*/);
```

---

## SUMMARY

You've learned:
✅ What JSL is and why it's useful
✅ How to write basic JSL code
✅ How to open and work with data
✅ Real-world examples you can use
✅ Common functions
✅ How to debug problems
✅ Where to find help

**Next Steps:**
1. Open JMP
2. File → New → Script
3. Try one of the examples
4. Modify it to your data
5. Run it!

The more you practice, the more comfortable you'll become with JSL. Start simple, and build up gradually!

Good luck with your scripting! 🚀
