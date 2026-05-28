# Test Data Analysis: A High School Guide
## Part 6: Visual Methods - Making Data Speak

---

## Why Visualization Matters

**Imagine presenting this to your boss:**

"Our measurements were 2.1, 2.3, 2.0, 2.4, 2.2, 2.1, 1.9, 2.3, 2.5, 2.2. The mean is 2.21, the standard deviation is 0.18, and the range is 0.6. Therefore..."

**Your boss's eyes glaze over.**

**Now show them a chart:**

[Visual representation]

**Your boss immediately understands.**

**Truth:** A good chart beats 1000 statistics. People think in pictures.

---

## Chart 1: Histogram (Distribution)

**What it shows:** How many times each value appears. The "shape" of your data.

### Simple Histogram

**Data:** Leakage current of 100 chips
```
0.5µA: 2 chips
1.0µA: 8 chips
1.5µA: 18 chips
2.0µA: 25 chips
2.5µA: 30 chips
3.0µA: 12 chips
3.5µA: 4 chips
4.0µA: 1 chip
```

**Histogram visualization:**

```
Frequency
   │
30 │       ▓
   │       ▓
25 │   ▓   ▓
   │   ▓   ▓
20 │   ▓   ▓
   │   ▓   ▓
15 │   ▓   ▓   ▓
   │   ▓   ▓   ▓
10 │   ▓   ▓   ▓
   │ ▓ ▓   ▓   ▓
 5 │ ▓ ▓   ▓   ▓   ▓
   │ ▓ ▓   ▓   ▓   ▓ ▓
───┼──────────────────────── Leakage Current (µA)
   0.5 1.0 1.5 2.0 2.5 3.0 3.5 4.0
```

### What to Look for in a Histogram

**Good histogram (Normal/Bell Curve):**
```
       ▓
     ▓ ▓ ▓
   ▓ ▓ ▓ ▓ ▓
 ▓ ▓ ▓ ▓ ▓ ▓ ▓
▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓

Meaning: Data is predictable, centered, well-behaved
Action: Use normal statistics, process is stable
```

**Histogram with multiple peaks:**
```
 ▓           ▓
 ▓           ▓
 ▓   ▓       ▓
 ▓   ▓   ▓   ▓
─────────────────

Meaning: Two different groups mixed together
Possible cause: Different batches, two different machines
Action: Investigate why data has two modes
```

**Histogram shifted to the side:**
```
           ▓
         ▓ ▓ ▓
       ▓ ▓ ▓ ▓
     ▓ ▓ ▓ ▓ ▓
───────────────────
         ↑
      Off-target

Meaning: Process is running high/low, not centered
Action: Adjust the process to center it
```

**Histogram very spread out:**
```
▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓ ▓
────────────────────

Meaning: High variation, unstable
Action: Find and reduce sources of variation
```

### How to Make a Histogram in Excel

```
1. Organize data in column A (values to analyze)
2. Select Data → Data Analysis → Histogram
3. Choose your bin size (group width, e.g., 0.5)
4. Click OK
5. Format as needed
```

---

## Chart 2: Box Plot (Quartile Summary)

**What it shows:** Distribution using quartiles. Good for comparing multiple groups.

### Box Plot Anatomy

```
     ●  Outlier (beyond 1.5×IQR)
     │
  ┌──┴──┐
  │     │  Upper whisker (95th percentile)
  │     │
  │┌────┤  Top of box (75th percentile / Q3)
  ││    │
  ││────┤  Line in middle (50th percentile / Median)
  ││    │
  │└────┤  Bottom of box (25th percentile / Q1)
  │     │
  │     │  Lower whisker (5th percentile)
  └─────┘
```

### Real Example: Comparing Suppliers

**Battery life test (hours)**

**Supplier A:**
```
─────────────────────────────────
     ┌─────────────┤  
     │   ┌──────┤
──────┴─────┴───┴──────────────── Hours
7    8     9    10   11    12
```

**Supplier B:**
```
─────────────────────────────────
      ┌──────────────────┤  
      │  ┌──────┤
────┬─┴──┴──────┴──────────────── Hours  
6   7  8    9    10   11   12
```

**What the comparison tells you:**
- Supplier A: Consistent, centered around 9 hours
- Supplier B: More variable, lower, maybe some defects

**Visual comparison beats listing numbers.**

### How to Make a Box Plot in Excel

```
1. Arrange data in columns (one per group to compare)
2. Select Data → Data Analysis → Descriptive Statistics
3. Or: Insert Chart → Box and Whisker
4. Choose your data range
5. Excel creates the box plot
```

---

## Chart 3: Trend Plot (Change Over Time)

**What it shows:** How measurements change over time. Detects drift, trends, problems.

### Simple Trend Plot

**Temperature readings over 24 hours:**

```
Temperature (°C)
30 │                          ▲
   │                    ▲   ▲
25 │              ▲   ▲   ▲
   │        ▲   ▲   ▲
20 │    ▲ ▲
   │  ▲
15 │
   └─────────────────────────────── Time
    0 4  8  12  16  20  24 hours
```

**Reading this chart:**
- Temperature slowly rises from 0-16 hours
- Peaks around 16 hours
- Slowly falls from 16-24 hours

This is a normal daily temperature cycle.

### Trend Plot Showing a Problem

**Machine speed over 10 days:**

```
Speed (RPM)
3050 │                    ▲
     │               ▲   ▲
3000 │          ▲   ▲   ▲      ← Machine slowing down
     │    ▲   ▲   ▲
2950 │──▲───▲─────────────────── Target = 2950
     │ ▲
2900 │
     └──────────────────────────
       0 2 4 6 8 10 Days
```

**What this shows:**
- Days 0-4: Machine is fine
- Days 4-10: Clear upward trend (machine is speeding up)
- By day 10: Above target
- WARNING: Keep trending and it will exceed spec limit!

**Action:** Investigate on day 8 or 9, not day 11.

### How to Make a Trend Plot in Excel

```
1. Column A: Time values (Day 1, Day 2, etc.)
2. Column B: Measurement values
3. Select both columns
4. Insert → Chart → Line Chart
5. Excel creates trend line
6. You can add a reference line for the target/spec
```

---

## Chart 4: Scatter Plot (Relationship Between Two Things)

**What it shows:** Is there a relationship between two measurements?

### Example: Speed vs Power Consumption

```
Power (Watts)
50 │           ●
   │         ● ●
40 │       ●   ●
   │     ●     ●
30 │   ●       ●
   │ ●         ●
20 │           ●
   │
10 │
   └─────────────────────── Speed (MHz)
    500  600  700  800  900  1000
```

**What this shows:**
- Higher speed = Higher power consumption
- Linear relationship (straight line)
- Predictable correlation

**Real use case:** If you want a chip that's fast AND power-efficient, you can see the tradeoff.

### Example: No Relationship

```
Height (inches)
72 │ ●           ●
   │   ●       ●
68 │     ●   ●
   │       ●
64 │   ●       ●
   │ ●           ●
60 │
   └─────────────────── Test Score
    0   20   40   60   80   100
```

**What this shows:**
- Random scatter, no pattern
- Height doesn't predict test score (as expected)
- No correlation

### How to Make a Scatter Plot in Excel

```
1. Column A: First measurement (e.g., Speed)
2. Column B: Second measurement (e.g., Power)
3. Select both columns
4. Insert → Chart → Scatter
5. Excel shows dots for each pair
6. Look for pattern/trend
```

---

## Combining Charts for Full Picture

**Good analysis presentation:**

```
1. Histogram: Shows distribution (normal? skewed? two modes?)
2. Box Plot: Shows quartiles and outliers
3. Control Chart: Shows if stable over time
4. Capability chart: Compares to spec limits
```

**Together they tell the whole story.**

---

## Real Example: Manufacturing Report

**Test: Spring length spec 10.0 ± 0.2 cm**

**Histogram:**
```
Shows: Most springs are 9.95-10.05, roughly bell-shaped
Conclusion: Process is normal, centered
```

**Box Plot:**
```
Shows: Q1=9.98, Median=10.00, Q3=10.02, no outliers
Conclusion: Very tight distribution, good consistency
```

**Trend Plot (over 20 days):**
```
Shows: Flat line at 10.00, no drift
Conclusion: Process is stable
```

**Summary:**
- Process is centered on target
- Low variation
- Stable over time
- Cpk would be high
- Yield would be near 100%

**Recommendation:** Keep doing what you're doing.

---

## Common Visualization Mistakes

### Mistake 1: Wrong Chart Type

```
Bad: Use a pie chart for "Measurements by day"
     (pie charts are for percentages of a whole, not trends)

Good: Use a line/trend chart to show measurements over time
```

### Mistake 2: Wrong Scale

```
Bad: Y-axis goes from 0 to 10,000 when data is only 2-4
     (tiny data, wasted space)

Good: Y-axis goes from 1 to 5 (zooms in, shows variation)
```

### Mistake 3: No Labels

```
Bad: Chart with no title, axes not labeled, legend missing
     (confusing)

Good: Clear title, axis labels with units, legend, 
      and maybe reference lines for spec limits
```

### Mistake 4: Too Much Information

```
Bad: 10 different lines on one chart, impossible to read

Good: Break into multiple charts or only show key lines
```

---

## Quick Reference: When to Use Each Chart

| Question | Chart | Why |
|----------|-------|-----|
| How is data distributed? | Histogram | Shows shape, center, spread |
| Compare multiple groups? | Box Plot | Easy visual comparison |
| Is process stable over time? | Trend Plot | Shows drift and variation |
| Two measurements related? | Scatter | Shows correlation/relationship |
| Are we in spec? | Add spec limits to any chart | Visual pass/fail |
| How many pass vs fail? | Pie or Bar Chart | Percentage comparison |

---

## Making Professional Charts

### Essential Elements

```
Title: What is this showing?
X-axis: Label with units (e.g., "Time (hours)")
Y-axis: Label with units (e.g., "Temperature (°C)")
Legend: If multiple lines/series
Grid: Optional but helps read values
Reference lines: Spec limits, target, average
Data labels: Optional, helps accuracy
```

### Excel Tips

```
1. Keep it simple (don't add 3D, fancy effects)
2. Use consistent colors
3. Make it large enough to read
4. Put spec limits on the chart (makes pass/fail obvious)
5. Use a title that answers a question
   Bad: "Data Chart"
   Good: "Spring Length Over Time vs Specification"
```

---

## Summary: Visual Methods

Charts make data understandable instantly.

- **Histogram**: See distribution
- **Box Plot**: Compare groups
- **Trend Plot**: Spot changes over time
- **Scatter Plot**: Find relationships

Use the right chart for the right question.

---

## Practice: Interpret Charts

**You see this histogram:**
```
Frequency
   │       ▓
   │       ▓
 5 │   ▓   ▓
   │   ▓   ▓   ▓
 3 │   ▓   ▓   ▓
   │   ▓   ▓   ▓
 1 │ ▓ ▓   ▓ ▓ ▓
   └─────────────────
    1  2  3  4  5  Value
```

**Questions:**
1. Is this normal/bell-shaped?
2. Where is the mode (most frequent)?
3. Is there high or low variation?

**Answers:**
```
1. No, it's relatively flat (uniform distribution)
2. Multiple modes around 2, 3, and 4 (somewhat bimodal)
3. High variation (spread across whole range 1-5)

Conclusion: Process is unstable or has mixed groups
```

---

## Next Steps

Move to **Part 7: Practical Workflow** to see how to put all this together in real testing situations.

---

**Last updated:** May 2026
**Difficulty level:** High School
**Time to read:** 20-25 minutes
**Prerequisite:** Parts 3 & 4 (Statistics and Control Charts)
