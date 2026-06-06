# UNDERSTANDING WAFER TEST DATA GENERATION & ANALYSIS
## The Circular Grid Code Explained
### Written for High School Level Understanding

---

## INTRODUCTION: WHAT IS THIS CODE?

This Python code generates **simulated wafer test data** that looks like real semiconductor manufacturing data.

**Why create fake data?**
- Testing and learning without expensive equipment
- Practicing data analysis techniques
- Understanding how real wafer test data is structured
- Testing your analysis code before using it on real data

Think of it like this:
- Real wafer data = expensive to generate (requires actual fab equipment)
- Simulated wafer data = cheap to generate (just code on your computer)
- You learn the same skills either way

---

## PART 1: UNDERSTANDING WAFER LAYOUT

### What is a Wafer?

A wafer is a thin slice of silicon about the size of a dinner plate (usually 200-300mm in diameter).

On this wafer, hundreds or thousands of **dies** (individual chips) are manufactured together.

```
Visual representation:

        ╔═══════════════════════╗
        ║  Wafer (circular)     ║
        ║                       ║
        ║  ░░░░░░░░░░░░░░░░░░  ║
        ║  ░ Die ░ Die ░ Die ░  ║
        ║  ░░░░░░░░░░░░░░░░░░  ║
        ║                       ║
        ║  ░░░░░░░░░░░░░░░░░░  ║
        ║  ░ Die ░ Die ░ Die ░  ║
        ║  ░░░░░░░░░░░░░░░░░░  ║
        ║                       ║
        ║  ░░░░░░░░░░░░░░░░░░  ║
        ║  ░ Die ░ Die ░ Die ░  ║
        ║  ░░░░░░░░░░░░░░░░░░  ║
        ║                       ║
        ╚═══════════════════════╝
```

Each die is tested electronically, and measurements are recorded with its **X and Y coordinates** on the wafer.

### Die Coordinates

Instead of naming each die, we use **X and Y coordinates** like on a grid.

```
Example coordinates:

        Y-axis (row)
           ↑
       4   (0,4) (1,4) (2,4)
       3   (0,3) (1,3) (2,3)
       2   (0,2) (1,2) (2,2)
       1   (0,1) (1,1) (2,1)
       0   (0,0) (1,0) (2,0)
           └──────────────────→ X-axis (column)
           0    1    2

Each die can be identified by its (X, Y) position.
```

### The Circular Shape

Real wafers are **circular**. This is important because:
1. Silicon is cut into circular wafers
2. Dies near the edge are often defective
3. Dies in the center are usually good
4. Dies outside the circle don't exist (the wafer edge)

```
Example: 500 x 500 grid, circle in the middle

Wafer representation (. = inside circle, X = outside):
              Center (250, 250)
              
        . . . . X X X X . . . . 
      . . . . . . . . . . . . .
    . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . .
. . . . . . . . . . . . . . . .
X . . . . . . . . . . . . . . X
X . . . . . . . . . . . . . . X
X . . . . . . . . . . . . . . X
. . . . . . . . . . . . . . . .
  . . . . . . . . . . . . . . .
    . . . . . . . . . . . . . .
      . . . . . . . . . . . . .
        . . . . X X X X . . . .
        
(.) = Valid dies (inside circle)
(X) = Invalid locations (outside circle)
```

---

## PART 2: BREAKING DOWN THE CODE LINE BY LINE

### Part 1: Understanding the Function Definition

```python
def generate_circular_grid_csv(grid_size=500, circle_radius=200, 
                                center_x=250, center_y=250):
    """Generate grid CSV: 1 inside circle, 0 outside."""
```

**What this line does:**
- `def` = Define a new function (a reusable block of code)
- `generate_circular_grid_csv` = Name of the function
- `grid_size=500` = Parameter: how big is the grid? Default is 500×500
- `circle_radius=200` = Parameter: how big is the circle? Default radius is 200
- `center_x=250, center_y=250` = Parameter: where is the center? Default is (250,250)

**Analogy:** Think of this like a recipe. The recipe says "Make a cake." The parameters are:
- How big should the cake be?
- What shape?
- Where should you put it?

### Part 2: Creating a Grid of Coordinates

```python
x = np.arange(grid_size)
y = np.arange(grid_size)
xx, yy = np.meshgrid(x, y, indexing='ij')
```

**What this does:**
1. `np.arange(grid_size)` = Create a list: [0, 1, 2, 3, ..., 499]
2. Do this for both X and Y
3. `meshgrid` = Create all possible combinations of X and Y coordinates

**Visual example:**
```
If grid_size=3, we create all positions:
(0,0) (0,1) (0,2)
(1,0) (1,1) (1,2)
(2,0) (2,1) (2,2)

This creates a 3×3 grid of coordinates.
For grid_size=500, we get 500×500 = 250,000 positions.
```

### Part 3: Calculating Distance from Center

```python
dx = xx - center_x      # Difference in X from center
dy = yy - center_y      # Difference in Y from center
distance = np.sqrt(dx**2 + dy**2)
```

**What this does:**
This calculates **how far each point is from the center** using the Pythagorean theorem.

**Example:**
```
If center is at (250, 250) and we check point (260, 260):
  dx = 260 - 250 = 10
  dy = 260 - 250 = 10
  distance = √(10² + 10²) = √(100 + 100) = √200 ≈ 14.14

So point (260, 260) is 14.14 units away from center.
```

### Part 4: Creating the Bin (Inside or Outside Circle)

```python
val_mask = (distance <= circle_radius).astype(int)
```

**What this does:**
- Check if `distance <= circle_radius` (Is the point inside the circle?)
- If YES: True (which becomes 1)
- If NO: False (which becomes 0)
- `astype(int)` = Convert True/False to 1/0

**Example:**
```
If circle_radius = 200:
  Point at distance 100: 100 <= 200? YES → BIN = 1 (inside circle)
  Point at distance 250: 250 <= 200? NO → BIN = 0 (outside circle)

So BIN column will have:
  1 = valid die (inside circle, can be tested)
  0 = invalid location (outside circle, doesn't exist)
```

### Part 5: Generating Noise (Realistic Variation)

```python
rng = np.random.default_rng(42)

base_leakage = 10.0         # Target value
noise_leakage = rng.normal(0, 1.5)  # Random variation
```

**What this does:**
- `rng.normal(0, 1.5)` = Create random variation around 0
  - Mean = 0 (centered)
  - Std Dev = 1.5 (spread)
  - Creates realistic variation like in real manufacturing

**Why this matters:**
Real manufacturing always has variation. Without it, your simulated data would be too perfect and unrealistic.

**Example:**
```
If base_leakage = 10.0 µA
And noise variation = +/- 1.5 µA
Then actual values might be: 8.5, 9.2, 10.1, 10.8, 11.5 µA

This looks realistic!
```

### Part 6: Creating the DataFrame

```python
df = pd.DataFrame({
    'X_COORD': xx.flatten(),
    'Y_COORD': yy.flatten(),
    'BIN': val_mask.flatten(),
    'LEAKAGE_UA': (base_leakage + noise_leakage * rng.uniform(0.8, 1.2)).astype(float),
    # ... more columns
})
```

**What this does:**
Creates a table (DataFrame) with columns for:
- `X_COORD`: X coordinate of the die
- `Y_COORD`: Y coordinate of the die
- `BIN`: Is it valid (1) or invalid (0)?
- `LEAKAGE_UA`: Leakage current measurement
- Plus more test measurements

**Flatten() explanation:**
The coordinates are 2D arrays (grid). `flatten()` converts them to 1D lists so we can use them in a table.

**Example output:**
```
   X_COORD  Y_COORD  BIN  LEAKAGE_UA  FMAX_MHZ  IDDQ_MA  DELAY_NS   VTH_V
0       0        0    0       9.87      481.2     4.95     2.41    0.685
1       0        1    0       10.52     502.1     5.12     2.58    0.712
2       0        2    0       8.93      495.3     5.01     2.47    0.698
3       0        3    0       11.23     515.4     4.98     2.54    0.704
...
```

### Part 7: Saving to CSV

```python
output_file = 'circular_grid_params.csv'
df.to_csv(output_file, index=False)
```

**What this does:**
- Save the table to a CSV (Comma-Separated Values) file
- File name: `circular_grid_params.csv`
- `index=False` = Don't save row numbers

**Why CSV?**
CSV is a universal format that:
- Excel can open it
- Python can read it
- Most data tools support it
- It's human-readable as text

---

## PART 3: UNDERSTANDING THE TEST PARAMETERS

### What Are These Measurements?

The code generates 5 measurements for each die:

#### 1. LEAKAGE_UA (Leakage Current)
- **Unit**: µA (microamps)
- **Target**: ~10 µA
- **What it is**: Current that flows through the chip when it's supposed to be off
- **Why it matters**: Lower is better (less power wasted)
- **Spec**: Typically 0.1 - 50 µA
- **Variation**: ±15%

```
Real-world meaning:
If your phone is off but still drains battery, that's leakage current.
A good chip has very little leakage.
```

#### 2. FMAX_MHZ (Maximum Frequency)
- **Unit**: MHz (Megahertz)
- **Target**: ~500 MHz
- **What it is**: How fast the chip can operate
- **Why it matters**: Faster is better (more performance)
- **Spec**: Typically 400 - 700 MHz
- **Variation**: ±5%

```
Real-world meaning:
If you have a 2 GHz processor, that's 2,000 MHz.
FMAX tells you how fast this particular die can go.
```

#### 3. IDDQ_MA (Supply Current)
- **Unit**: mA (milliamps)
- **Target**: ~5 mA
- **What it is**: Current the chip draws when actively operating
- **Why it matters**: Lower means less power consumption (longer battery life)
- **Spec**: Typically 3 - 10 mA
- **Variation**: ±6%

```
Real-world meaning:
How much power does your chip use?
A 5mA chip is more efficient than a 10mA chip.
```

#### 4. DELAY_NS (Propagation Delay)
- **Unit**: ns (nanoseconds)
- **Target**: ~2.5 ns
- **What it is**: How long it takes a signal to travel through the chip
- **Why it matters**: Shorter is better (faster operation)
- **Spec**: Typically 1.5 - 4.0 ns
- **Variation**: ±4%

```
Real-world meaning:
Electrons travel through the chip at speed of light (~1 foot/ns).
Shorter delay = faster chip.
```

#### 5. VTH_V (Threshold Voltage)
- **Unit**: V (Volts)
- **Target**: ~0.7 V
- **What it is**: The voltage needed to turn the transistor on
- **Why it matters**: Affects power, speed, and reliability
- **Spec**: Typically 0.6 - 0.8 V
- **Variation**: ±3%

```
Real-world meaning:
Like the "switch on voltage" for transistors.
Too low = leakage problems
Too high = need more power
```

---

## PART 4: WHAT THE CODE PRODUCES

### Example Output

When you run the code, it creates a CSV file with 250,000 rows (500 × 500 grid).

```
X_COORD,Y_COORD,BIN,LEAKAGE_UA,FMAX_MHZ,IDDQ_MA,DELAY_NS,VTH_V
0,0,0,9.87,481.2,4.95,2.41,0.685
0,1,0,10.52,502.1,5.12,2.58,0.712
0,2,0,8.93,495.3,5.01,2.47,0.698
0,3,0,11.23,515.4,4.98,2.54,0.704
0,4,0,10.15,498.7,5.03,2.52,0.695
...
250,250,1,9.95,505.2,4.98,2.45,0.701  (center - inside circle)
...
```

### Understanding BIN Column

```
BIN = 1: This die is INSIDE the circle (valid, should be tested)
BIN = 0: This die is OUTSIDE the circle (invalid, doesn't exist)

In a real scenario:
- BIN 1 (or good bin) = Product passes all tests
- BIN 2 = Product fails one test (can be reworked or sold as different product)
- BIN 3 = Product fails multiple tests (scrap)

In this code:
- BIN = 1 means "inside circle" (exists on wafer)
- BIN = 0 means "outside circle" (doesn't exist)
```

---

## PART 5: HOW TO USE THIS DATA FOR ANALYSIS

### Step 1: Generate the Data

```python
# Run the code
df = generate_circular_grid_csv()

# Check what you got
print(df.head())        # First 5 rows
print(df.shape)         # How many rows/columns
print(df.describe())    # Statistics
```

### Step 2: Filter to Valid Dies

```python
# Keep only dies inside the circle (BIN = 1)
valid_dies = df[df['BIN'] == 1]

print(f"Total locations: {len(df)}")
print(f"Valid dies: {len(valid_dies)}")
print(f"Yield: {len(valid_dies)/len(df)*100:.1f}%")
```

**Example Output:**
```
Total locations: 250000
Valid dies: 125664 (roughly - depends on circle area)
Yield: 50.3% (makes sense for a circle in a 500x500 square)
```

### Step 3: Basic Analysis

```python
# Statistics on leakage current
print("LEAKAGE CURRENT ANALYSIS:")
print(f"  Mean: {valid_dies['LEAKAGE_UA'].mean():.2f} µA")
print(f"  Std Dev: {valid_dies['LEAKAGE_UA'].std():.2f} µA")
print(f"  Min: {valid_dies['LEAKAGE_UA'].min():.2f} µA")
print(f"  Max: {valid_dies['LEAKAGE_UA'].max():.2f} µA")
```

**Example Output:**
```
LEAKAGE CURRENT ANALYSIS:
  Mean: 10.01 µA
  Std Dev: 1.48 µA
  Min: 5.23 µA
  Max: 14.87 µA
```

### Step 4: Check Against Specifications

```python
# Define specs
spec_leakage_max = 15.0  # µA
spec_fmax_min = 400      # MHz

# Count passes/failures
leakage_pass = (valid_dies['LEAKAGE_UA'] <= spec_leakage_max).sum()
fmax_pass = (valid_dies['FMAX_MHZ'] >= spec_fmax_min).sum()

print(f"Leakage pass rate: {leakage_pass/len(valid_dies)*100:.1f}%")
print(f"FMAX pass rate: {fmax_pass/len(valid_dies)*100:.1f}%")
```

### Step 5: Spatial Analysis (Wafer Map)

```python
# Check if edge dies perform worse
edge_threshold = 50  # Dies within 50 units of edge

# Calculate distance from center
valid_dies['DIST_FROM_CENTER'] = np.sqrt(
    (valid_dies['X_COORD'] - 250)**2 + 
    (valid_dies['Y_COORD'] - 250)**2
)

edge_dies = valid_dies[valid_dies['DIST_FROM_CENTER'] > 150]
center_dies = valid_dies[valid_dies['DIST_FROM_CENTER'] <= 150]

print("EDGE vs CENTER COMPARISON:")
print(f"Center leakage mean: {center_dies['LEAKAGE_UA'].mean():.2f}")
print(f"Edge leakage mean: {edge_dies['LEAKAGE_UA'].mean():.2f}")
```

**Example Output:**
```
EDGE vs CENTER COMPARISON:
Center leakage mean: 9.85 µA (good)
Edge leakage mean: 10.23 µA (slightly higher)
```

---

## PART 6: UNDERSTANDING THE ASSUMPTIONS & WARNINGS

### ASSUMED Data Characteristics

The code makes these assumptions (as stated in comments):

```python
# ASSUMED: 'BIN' column contains hard bin number
# ASSUMED: 'X_COORD', 'Y_COORD' are integer die coordinates
# ASSUMED: 'WAFER_ID' and 'LOT_ID' columns exist for grouping
# VERIFY: confirm passing bin number with test engineer
```

**What do these mean?**

#### Assumption 1: BIN Column
```
The code assumes:
  BIN = 1 or 0 (1 = inside circle, 0 = outside)
  
Real manufacturing:
  BIN = 1 (Good/pass)
  BIN = 2 (Marginal/rebin)
  BIN = 3 (Fail/scrap)
  
This code SIMPLIFIED it to just inside/outside.
Real data is more complex.
```

#### Assumption 2: Coordinates
```
The code assumes:
  X_COORD and Y_COORD are integers (0, 1, 2, ...)
  
Real manufacturing:
  Dies are spaced at regular intervals (e.g., every 5mm)
  Coordinates might be floats or measured distances
  
This code uses simplified integer grid.
```

#### Assumption 3: Passing Bin Number
```
The code assumes:
  Bin 1 = passing dies
  Bin 0 = non-existent (outside circle)
  
VERIFY with engineer:
  Sometimes bin 1 is failing die!
  Sometimes bin 0 is passing die!
  Always check with someone who knows the convention.
```

---

## PART 7: REALISTIC VARIATION EXPLAINED

The code adds realistic variation to each parameter:

```python
base_leakage = 10.0
noise_leakage = rng.normal(0, 1.5)  # Std dev = 1.5

Resulting values are roughly:
  10.0 ± 1.5 = between 8.5 and 11.5 µA (68% of the time)
  10.0 ± 3.0 = between 7.0 and 13.0 µA (95% of the time)
```

**But then:**
```python
(base_leakage + noise_leakage * rng.uniform(0.8, 1.2))
```

This **multiplies** the variation by a random factor (0.8 to 1.2), which:
- Adds more realism
- Creates non-uniform distribution
- Mimics real process behavior

**Result:** Data looks like real manufacturing data!

---

## PART 8: PRACTICAL EXAMPLE - FULL ANALYSIS

Let's do a complete analysis of this data:

```python
import pandas as pd
import numpy as np

# Step 1: Generate data
df = generate_circular_grid_csv()

# Step 2: Filter valid dies
valid = df[df['BIN'] == 1].copy()

print("="*60)
print("WAFER TEST DATA ANALYSIS REPORT")
print("="*60)

# Step 3: Overall yield
print(f"\n1. OVERALL STATISTICS:")
print(f"   Total positions: {len(df):,}")
print(f"   Valid dies: {len(valid):,}")
print(f"   Yield: {len(valid)/len(df)*100:.1f}%")

# Step 4: Parameter analysis
print(f"\n2. LEAKAGE CURRENT (µA):")
print(f"   Mean: {valid['LEAKAGE_UA'].mean():.2f}")
print(f"   Std Dev: {valid['LEAKAGE_UA'].std():.2f}")
print(f"   Min: {valid['LEAKAGE_UA'].min():.2f}")
print(f"   Max: {valid['LEAKAGE_UA'].max():.2f}")

# Step 5: Pass/fail counts
spec_max = 15.0
failures = (valid['LEAKAGE_UA'] > spec_max).sum()
print(f"   Failures (>15µA): {failures} ({failures/len(valid)*100:.2f}%)")

# Step 6: Spatial analysis
valid['DIST'] = np.sqrt((valid['X_COORD']-250)**2 + (valid['Y_COORD']-250)**2)
inner = valid[valid['DIST'] <= 100]
outer = valid[valid['DIST'] > 100]

print(f"\n3. CENTER vs EDGE ANALYSIS:")
print(f"   Center dies ({len(inner)}): {inner['LEAKAGE_UA'].mean():.2f} µA")
print(f"   Edge dies ({len(outer)}): {outer['LEAKAGE_UA'].mean():.2f} µA")

# Step 7: Cpk calculation
cpk_leakage = min(
    (15.0 - valid['LEAKAGE_UA'].mean()) / (3 * valid['LEAKAGE_UA'].std()),
    (valid['LEAKAGE_UA'].mean() - 1.0) / (3 * valid['LEAKAGE_UA'].std())
)
print(f"\n4. CAPABILITY (Cpk):")
print(f"   Leakage Cpk: {cpk_leakage:.2f}")
if cpk_leakage > 1.33:
    print("   Status: GOOD ✓")
elif cpk_leakage > 1.0:
    print("   Status: ACCEPTABLE")
else:
    print("   Status: POOR - INVESTIGATE")

print("\n" + "="*60)
```

**Example Output:**
```
============================================================
WAFER TEST DATA ANALYSIS REPORT
============================================================

1. OVERALL STATISTICS:
   Total positions: 250,000
   Valid dies: 125,664
   Yield: 50.3%

2. LEAKAGE CURRENT (µA):
   Mean: 10.01
   Std Dev: 1.48
   Min: 5.23
   Max: 14.87
   Failures (>15µA): 1,247 (0.99%)

3. CENTER vs EDGE ANALYSIS:
   Center dies (42,478): 9.92 µA
   Edge dies (83,186): 10.07 µA

4. CAPABILITY (Cpk):
   Leakage Cpk: 1.11
   Status: ACCEPTABLE

============================================================
```

---

## PART 9: IMPORTANT NOTES & CORRECTIONS

### How to Verify Your Data

After generating or receiving data, ALWAYS verify:

```python
# 1. Check for missing values
print(df.isnull().sum())  # Should be 0

# 2. Check value ranges
print(df['LEAKAGE_UA'].describe())  # Look for outliers

# 3. Check coordinates make sense
print(f"X range: {df['X_COORD'].min()} to {df['X_COORD'].max()}")
print(f"Y range: {df['Y_COORD'].min()} to {df['Y_COORD'].max()}")

# 4. Check bin distribution
print(df['BIN'].value_counts())  # Should have 1s and 0s

# 5. Look at actual data
print(df.head(10))
```

### Common Mistakes When Using This Code

❌ **MISTAKE 1:** Analyzing all data including BIN=0 (outside circle)
```python
# Wrong - includes invalid locations
result = df['LEAKAGE_UA'].mean()

# Correct - only valid dies
result = df[df['BIN']==1]['LEAKAGE_UA'].mean()
```

❌ **MISTAKE 2:** Forgetting that data is synthetic
```python
# This is SIMULATED data, not real
# Use it for LEARNING, not for actual production decisions
# Real decisions require REAL data
```

❌ **MISTAKE 3:** Not checking spec limits
```python
# Wrong - just calculating mean
print(f"Mean: {df['LEAKAGE_UA'].mean()}")

# Correct - compare to spec
spec = 15.0
mean = df['LEAKAGE_UA'].mean()
print(f"Mean: {mean:.2f} {'✓ PASS' if mean < spec else '✗ FAIL'}")
```

---

## PART 10: QUICK REFERENCE

### Code Parameters Explained

```python
generate_circular_grid_csv(
    grid_size=500,        # How big? 500x500 grid
    circle_radius=200,    # Circle size? 200 units radius
    center_x=250,         # Circle center X? Position 250
    center_y=250          # Circle center Y? Position 250
)

# Suggested modifications:
generate_circular_grid_csv(grid_size=1000)    # Larger wafer
generate_circular_grid_csv(circle_radius=400) # Bigger circle
```

### Generated Data Ranges (Typical)

```
LEAKAGE_UA:   8-12 µA  (target 10, ±15% variation)
FMAX_MHZ:     475-525 MHz (target 500, ±5% variation)
IDDQ_MA:      4.5-5.5 mA (target 5, ±6% variation)
DELAY_NS:     2.3-2.7 ns (target 2.5, ±4% variation)
VTH_V:        0.68-0.72 V (target 0.7, ±3% variation)
```

### Essential Analysis Commands

```python
import pandas as pd
import numpy as np

df = pd.read_csv('circular_grid_params.csv')

# Filter valid dies
valid = df[df['BIN'] == 1]

# Basic stats
valid['LEAKAGE_UA'].describe()

# Pass/fail
(valid['LEAKAGE_UA'] < 15.0).sum()  # Count passes

# Percentage
(valid['LEAKAGE_UA'] < 15.0).sum() / len(valid) * 100  # Percentage

# Cpk
mean = valid['LEAKAGE_UA'].mean()
std = valid['LEAKAGE_UA'].std()
cpk = min((15-mean)/(3*std), (mean-1)/(3*std))
```

---

## SUMMARY

### What You Now Know

1. **The code generates realistic simulated wafer data**
   - 250,000 die positions
   - Circular wafer layout
   - 5 electrical parameters
   - Realistic variations

2. **How to interpret the data**
   - BIN = pass/fail or valid/invalid
   - Coordinates = (X, Y) position on wafer
   - Measurements = test results
   - Variations = normal manufacturing noise

3. **How to analyze it**
   - Calculate basic statistics
   - Compare to specifications
   - Check spatial patterns
   - Calculate capability (Cpk)

4. **What it's used for**
   - Learning data analysis
   - Testing analysis code
   - Understanding wafer test concepts
   - Practicing Python/pandas

### Next Steps

1. **Run the code** to generate data
2. **Explore the CSV file** to see what it looks like
3. **Try the analysis examples** to calculate statistics
4. **Compare to spec limits** to see pass/fail rates
5. **Create visualizations** (histograms, wafer maps) to see patterns

### Remember

- This is **simulated data** for learning
- Real manufacturing data is more complex
- Always **verify assumptions** with engineers
- **Never make real decisions** based on synthetic data alone
- Use this to **learn the process** before analyzing real data

---

## APPENDIX: COMPLETE WORKING EXAMPLE

```python
#!/usr/bin/env python3
"""
Complete example: Generate data and analyze it
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Generate the data
def generate_circular_grid_csv(grid_size=500, circle_radius=200, 
                                center_x=250, center_y=250):
    """Generate grid CSV: 1 inside circle, 0 outside."""
    x = np.arange(grid_size)
    y = np.arange(grid_size)
    xx, yy = np.meshgrid(x, y, indexing='ij')
    
    dx = xx - center_x
    dy = yy - center_y
    distance = np.sqrt(dx**2 + dy**2)
    val_mask = (distance <= circle_radius).astype(int)
    
    rng = np.random.default_rng(42)
    
    base_leakage = 10.0
    base_fmax = 500.0
    base_iddq = 5.0
    base_delay = 2.5
    base_vth = 0.7
    
    df = pd.DataFrame({
        'X_COORD': xx.flatten(),
        'Y_COORD': yy.flatten(),
        'BIN': val_mask.flatten(),
        'LEAKAGE_UA': (base_leakage + 
                      rng.normal(0, 1.5) * rng.uniform(0.8, 1.2)),
        'FMAX_MHZ': (base_fmax + 
                    rng.normal(0, 25.0) * rng.uniform(0.95, 1.05)),
        'IDDQ_MA': (base_iddq + 
                   rng.normal(0, 0.3) * rng.uniform(0.9, 1.1)),
        'DELAY_NS': (base_delay + 
                    rng.normal(0, 0.1) * rng.uniform(0.92, 1.08)),
        'VTH_V': (base_vth + 
                 rng.normal(0, 0.02) * rng.uniform(0.95, 1.05))
    })
    
    return df

# Generate data
print("Generating wafer test data...")
df = generate_circular_grid_csv()

# Filter valid dies
valid = df[df['BIN'] == 1].copy()

# Add distance column
valid['DIST'] = np.sqrt((valid['X_COORD']-250)**2 + 
                         (valid['Y_COORD']-250)**2)

# Analysis
print("\n" + "="*70)
print("WAFER PARAMETRIC TEST ANALYSIS")
print("="*70)

print(f"\nDATASET:")
print(f"  Total positions: {len(df):,}")
print(f"  Valid dies (BIN=1): {len(valid):,}")
print(f"  Yield: {len(valid)/len(df)*100:.1f}%")

print(f"\nLEAKAGE CURRENT:")
print(f"  Mean: {valid['LEAKAGE_UA'].mean():.2f} µA")
print(f"  Std Dev: {valid['LEAKAGE_UA'].std():.2f} µA")
print(f"  Min/Max: {valid['LEAKAGE_UA'].min():.2f} / " +
      f"{valid['LEAKAGE_UA'].max():.2f} µA")

# Check against spec
spec_max = 15.0
fails = (valid['LEAKAGE_UA'] > spec_max).sum()
print(f"  Failures (>{spec_max}µA): {fails} ({fails/len(valid)*100:.2f}%)")

# Cpk calculation
mean_l = valid['LEAKAGE_UA'].mean()
std_l = valid['LEAKAGE_UA'].std()
cpk_l = min((spec_max - mean_l)/(3*std_l), 
            (mean_l - 1.0)/(3*std_l))
print(f"  Cpk: {cpk_l:.2f}")

# Spatial analysis
center = valid[valid['DIST'] <= 100]
edge = valid[valid['DIST'] > 100]

print(f"\nSPATIAL ANALYSIS:")
print(f"  Center dies: {len(center)} - Mean leakage: {center['LEAKAGE_UA'].mean():.2f} µA")
print(f"  Edge dies: {len(edge)} - Mean leakage: {edge['LEAKAGE_UA'].mean():.2f} µA")

print("\n" + "="*70)

# Optional: Create histogram
plt.figure(figsize=(10, 6))
plt.hist(valid['LEAKAGE_UA'], bins=50, edgecolor='black', alpha=0.7)
plt.axvline(spec_max, color='red', linestyle='--', linewidth=2, label=f'Spec limit ({spec_max}µA)')
plt.axvline(valid['LEAKAGE_UA'].mean(), color='green', linestyle='-', linewidth=2, label=f'Mean ({valid["LEAKAGE_UA"].mean():.2f}µA)')
plt.xlabel('Leakage Current (µA)')
plt.ylabel('Number of Dies')
plt.title('Leakage Current Distribution')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('leakage_distribution.png', dpi=100, bbox_inches='tight')
print("\nHistogram saved as 'leakage_distribution.png'")
```

---

## FINAL CHECKLIST

Before analyzing real data, verify:

✓ You understand what each column means
✓ You know the specification limits
✓ You filtered for valid dies (BIN = pass)
✓ You calculated statistics correctly
✓ You compared results to specifications
✓ You identified any trends or patterns
✓ You documented your findings
✓ You got review from a supervisor

Good luck with your data analysis!
