# Test Data Analysis: A High School Guide
## Part 3: Basic Statistics - The Essential Numbers

---

## Why Statistics?

You have 100 measurements. What do you say in one sentence?

**Without statistics:**
"The measurements are 2.1, 2.3, 2.0, 2.4, 2.2, 2.1, 1.9, 2.3..." (goes on forever, meaningless)

**With statistics:**
"The average is 2.15, most are between 1.9 and 2.4, and they're pretty consistent." (one sentence, meaningful)

Statistics = Summarizing lots of numbers into a few key numbers.

---

## The Five Statistics You Must Know

### Statistic 1: Mean (Average)

**What it is:** The sum of all values divided by how many values you have.

**Formula:**
```
Mean = (Sum of all values) / (Number of values)
```

**Example:**
```
Measurements: 2, 4, 6, 8, 10

Sum: 2 + 4 + 6 + 8 + 10 = 30
Count: 5 measurements
Mean: 30 / 5 = 6
```

**In a spreadsheet:**
```
Excel: =AVERAGE(A1:A100)
Google Sheets: =AVERAGE(A1:A100)
```

**Real example: Battery lifespan**
```
Phone 1: 8.2 hours
Phone 2: 8.5 hours
Phone 3: 7.9 hours
Phone 4: 8.1 hours
Phone 5: 8.3 hours

Sum: 8.2 + 8.5 + 7.9 + 8.1 + 8.3 = 41.0
Count: 5
Mean: 41.0 / 5 = 8.2 hours
```

**What it tells you:** The "typical" value. What you'd expect on average.

**When to use it:** Most of the time. It's the most common summary statistic.

**Limitation:** One extreme outlier can pull it off.

**Example of outlier problem:**
```
Salaries: $30,000, $35,000, $32,000, $1,000,000

Mean: ($30k + $35k + $32k + $1M) / 4 = $274,250

Wait, that's not typical! The outlier ($1M) pulled the average way up.
Three people make ~$32k but the mean is $274k.
That's misleading.
```

---

### Statistic 2: Median (Middle Value)

**What it is:** Line up all values from smallest to largest. Pick the middle one.

**Example:**
```
Values (unsorted): 5, 2, 8, 1, 9
Values (sorted): 1, 2, 5, 8, 9
                        ↑
                     Middle one = 5
Median = 5
```

**If you have even number of values:**
```
Values: 1, 2, 5, 8, 9, 10
              ↑ ↑
           These two are in the middle
           Take the average: (5+8)/2 = 6.5
Median = 6.5
```

**In a spreadsheet:**
```
Excel: =MEDIAN(A1:A100)
Google Sheets: =MEDIAN(A1:A100)
```

**Real example:**
```
Test scores: 45, 67, 72, 78, 95

Sorted: 45, 67, 72, 78, 95
Median (middle): 72

Mean: (45+67+72+78+95)/5 = 71.4

In this case they're similar. Good.
```

**Real example with outlier:**
```
Salaries: $30,000, $35,000, $32,000, $1,000,000

Sorted: $30,000, $32,000, $35,000, $1,000,000
Median (middle): ($32,000 + $35,000)/2 = $33,500

Mean was $274,250 (misleading)
Median is $33,500 (more accurate to typical salary)
```

**What it tells you:** The middle value. Not affected by outliers.

**When to use it:** When you have outliers or very skewed data.

**Tip:** If mean and median are very different, you probably have an outlier problem.

---

### Statistic 3: Standard Deviation (Spread)

**What it is:** How spread out the measurements are around the average.

**Simple explanation:**
- Small standard deviation = values are close together
- Large standard deviation = values are spread out

**Visual example:**

```
Data Set A: [4.9, 5.0, 5.1, 5.0, 4.9]
(all very close to 5)
Standard Deviation ≈ 0.08 (very small - tightly clustered)

Data Set B: [1, 5, 9, 2, 8]
(spread all over the place)
Standard Deviation ≈ 3.5 (large - very spread out)
```

**Formula (don't worry about this):**
```
Std Dev = square root of [average of (each value - mean)²]
(It's complex to calculate by hand, that's why we use computers)
```

**In a spreadsheet:**
```
Excel: =STDEV(A1:A100)   or   =STDEV.S(A1:A100)
Google Sheets: =STDEV(A1:A100)
```

**Real example:**

```
Two phone models tested for battery life:

Model A: 8.1, 8.2, 8.0, 8.1, 8.0 (very consistent)
  Mean: 8.08
  Std Dev: 0.08
  
Model B: 6.5, 8.2, 7.1, 8.8, 9.4 (all over the place)
  Mean: 8.0
  Std Dev: 1.2

Same average! But Model A is consistent, Model B varies wildly.
A standard consumer would prefer Model A (reliability).
```

**What it tells you:** How reliable/consistent your process is.

**When to use it:** Comparing variability, checking if process is stable.

**In context of 68-95-99.7 rule:**
```
If data is normally distributed (bell curve):
- 68% of values fall within Mean ± 1 std dev
- 95% of values fall within Mean ± 2 std devs
- 99.7% of values fall within Mean ± 3 std devs

Example: Mean = 100, Std Dev = 10
- 68% of values: 90-110
- 95% of values: 80-120
- 99.7% of values: 70-130
```

---

### Statistic 4: Minimum & Maximum (Range)

**What it is:** The smallest and largest values.

**Example:**
```
Values: 2.1, 3.5, 1.9, 4.2, 2.0, 3.8
Minimum: 1.9
Maximum: 4.2
Range: 4.2 - 1.9 = 2.3
```

**In a spreadsheet:**
```
Excel minimum: =MIN(A1:A100)
Excel maximum: =MAX(A1:A100)
Google Sheets: =MIN(A1:A100) and =MAX(A1:A100)
```

**Real example:**
```
Temperature readings over a week:
22.1, 23.4, 21.8, 22.9, 23.2, 22.0, 21.5

Min: 21.5°C
Max: 23.4°C
Range: 23.4 - 21.5 = 1.9°C
```

**What it tells you:** The extremes. How extreme can things get?

**When to use it:** Catching problems, understanding limits.

**Real use case:**
```
You're testing a component that must work between 0°C and 40°C.

You test and get:
Min: 2°C
Max: 38°C

Interpretation: Good! Both within limits.
You're safe for that temperature range.
```

---

### Statistic 5: Percentiles

**What it is:** A value where P percent of your data is below it.

**Percentiles:**
- P10 = 10% of data is below this value
- P25 = 25% of data is below this value
- P50 = 50% of data is below this value (that's the median!)
- P75 = 75% of data is below this value
- P90 = 90% of data is below this value
- P99 = 99% of data is below this value

**Example:**
```
10 students took a test. Scores (sorted):
45, 50, 55, 60, 65, 70, 75, 80, 85, 95

P25 (first quartile): 55 (25% of students scored below 55)
P50 (median): Between 65 and 70 = 67.5 (50% below)
P75 (third quartile): 80 (75% of students scored below 80)

Interpretation:
- Lowest 25% scored 55 or below
- Middle 50% scored between 55 and 80
- Top 25% scored above 80
```

**In a spreadsheet:**
```
Excel: =PERCENTILE(A1:A100, 0.95)   for 95th percentile
Google Sheets: =PERCENTILE(A1:A100, 0.95)
```

**Real example: Risk management**
```
You're testing product reliability.
You test 100 units and measure failure time (hours):

P99 = 500 hours (99% of units last at least 500 hours)

Warranty decision:
If you offer 1-year warranty = 8760 hours
You're safe (only 1 unit out of 100 would fail)

If you offer 2-year warranty = 17520 hours
Risk! Many units would fail.
```

**What it tells you:** Worst-case scenarios, risk assessment.

**When to use it:** Understanding extremes without being fooled by outliers.

---

## Putting It All Together: A Real Analysis

**Experiment:** Test leakage current of 10 semiconductor chips.

**Raw measurements (microamps):**
```
0.8, 1.1, 1.3, 1.5, 1.7, 2.0, 2.2, 2.5, 3.0, 4.2
```

**Calculate all five statistics:**

```
Mean: (0.8 + 1.1 + 1.3 + 1.5 + 1.7 + 2.0 + 2.2 + 2.5 + 3.0 + 4.2) / 10
    = 21.3 / 10 = 2.13 µA

Median: Values are already sorted.
        Middle values are #5 (1.7) and #6 (2.0)
        Median = (1.7 + 2.0) / 2 = 1.85 µA

Min: 0.8 µA
Max: 4.2 µA
Range: 4.2 - 0.8 = 3.4 µA

Standard Deviation: (Calculated with formula or spreadsheet)
                    ≈ 1.1 µA

P90: 90th percentile
     About 90% of values should be below this
     Looking at our 10 values, the 9th and 10th are 3.0 and 4.2
     P90 ≈ 4.0 µA
```

**Interpretation:**

```
- Typical leakage: 2.13 µA (mean)
- Median: 1.85 µA (typical is actually a bit lower, pulled up by outlier)
- Spread: 1.1 µA std dev (moderate variation)
- Extremes: 0.8 to 4.2 µA
- 90th percentile: 4.0 µA (10% of chips leak more than this)

Summary: Most chips are in the 0.8-2.2 range, but one chip (4.2)
is notably higher than others. Investigate chip #10?
```

---

## Comparing Two Groups

**Often you want to compare:** Is Group A different from Group B?

**Example:**
```
Group A (New process): 2.0, 2.1, 2.0, 2.1, 2.0
Group B (Old process): 1.8, 2.5, 1.5, 2.8, 2.1

Group A mean: 2.04
Group B mean: 2.14

Is Group B worse?

Group A std dev: 0.04 (very consistent)
Group B std dev: 0.53 (all over the place)

Conclusion: Group B isn't just slightly worse—it's much more variable.
The new process (A) is better AND more consistent.
```

---

## When Statistics Lie (Common Mistakes)

### Mistake 1: Using Mean With Outliers

```
House prices in neighborhood: $300k, $320k, $350k, $10,000,000

Mean: $2,642,500

That's not representative! 3 houses are ~$320k but one billionaire
pulled the average way up.

Use median instead: ~$335,000 (much better)
```

### Mistake 2: Ignoring Standard Deviation

```
Two suppliers tested:
Supplier A: Average weight = 100g, Std Dev = 0.1g (very consistent)
Supplier B: Average weight = 100g, Std Dev = 5g (all over the place)

They have the same average!
But A is much better (consistent).
B might have some product at 95g and some at 105g (bad).
```

### Mistake 3: Small Sample Size

```
You survey 5 people about ice cream preference.
4 like vanilla, 1 likes chocolate.
Conclusion: "80% of people like vanilla"

But 5 people isn't representative of everyone!
With 1000 people, it might be 50% vanilla, 50% chocolate.
```

---

## Quick Reference Table

| Statistic | What It Answers | Best For | Limitation |
|-----------|-----------------|----------|-----------|
| **Mean** | What's typical? | General use | Fooled by outliers |
| **Median** | What's the middle? | Data with outliers | Doesn't use all info |
| **Std Dev** | How spread out? | Comparing consistency | Hard to interpret alone |
| **Min/Max** | What are extremes? | Limits, ranges | Doesn't show overall pattern |
| **Percentile** | What's worst case? | Risk, warranty | Depends on sample size |

---

## Calculating by Hand vs Calculator vs Spreadsheet

### By Hand (Mean only, for small sets)

```
Data: 2, 4, 6, 8, 10
Sum: 2 + 4 + 6 + 8 + 10 = 30
Count: 5
Mean: 30 ÷ 5 = 6
```

**Good for:** Understanding what mean means, small datasets

**Bad for:** Large datasets, standard deviation

### With Scientific Calculator

Most calculators have:
- [+] sum button
- [÷] divide
- [σ] standard deviation button

**Procedure:**
1. Enter numbers one by one
2. Hit sum button to get total
3. Hit σ button to get standard deviation
4. Read the results

**Good for:** Quick calculations without a computer

**Bad for:** Very tedious for 100+ data points

### With Spreadsheet (Best)

```
Put data in column A (A1 to A100)

Then type formulas:
=AVERAGE(A1:A100)          Mean
=MEDIAN(A1:A100)           Median
=STDEV(A1:A100)            Standard deviation
=MIN(A1:A100)              Minimum
=MAX(A1:A100)              Maximum
=PERCENTILE(A1:A100, 0.90) 90th percentile
```

**Good for:** Everything, fast, easy to change data

**Bad for:** None really, this is the best way

---

## Real Example: Student Test Scores

**Class of 25 students. Test scores:**

```
65, 72, 78, 81, 85, 88, 90, 92, 75, 88,
95, 82, 76, 89, 91, 87, 79, 84, 93, 80,
77, 86, 94, 81, 83
```

**Calculations:**

```
Mean: (65+72+78+...+83) / 25 = 84.4

Median: Sort them, find middle (13th out of 25)
        = 85

Std Dev: ≈ 6.8

Min: 65
Max: 95
Range: 30

P90: 92

Percentiles:
P25: 78 (bottom quarter scored below 78)
P50: 85 (bottom half scored below 85)
P75: 90 (bottom 75% scored below 90)
```

**Interpretation:**

```
- Most students: 84-85 range (mean and median close)
- Spread: About 7 points std dev (pretty tight distribution)
- Extremes: 65 to 95 (30 point spread)
- Good students: 25% scored 90 or above (P90)

Conclusion: Class performed well overall. Most clustered around 85.
One low performer at 65. No major outliers otherwise.
```

---

## Summary

These five statistics tell you almost everything:

1. **Mean** = typical value
2. **Median** = middle value (use if outliers exist)
3. **Std Dev** = consistency
4. **Min/Max** = extremes
5. **Percentile** = where specific points fall

Master these five, and you can analyze most data.

---

## Practice Problem

**You test a water sample 8 times. pH readings:**
```
7.1, 7.0, 6.9, 7.2, 7.0, 6.8, 7.1, 7.0
```

**Calculate:**
1. Mean
2. Median
3. Min and Max
4. Range

**Answers:**
```
1. Mean = (7.1+7.0+6.9+7.2+7.0+6.8+7.1+7.0)/8 = 56.1/8 = 7.01
2. Median = Sort: 6.8, 6.9, 7.0, 7.0, 7.0, 7.1, 7.1, 7.2
            Middle two: 7.0 and 7.0
            Median = 7.0
3. Min = 6.8, Max = 7.2
4. Range = 7.2 - 6.8 = 0.4
```

---

## Next Steps

Move to **Part 4: Control Charts** to learn how to track these statistics over time and spot problems early.

---

**Last updated:** May 2026
**Difficulty level:** High School (Algebra I)
**Time to read:** 25-30 minutes
**Prerequisite:** Part 2 (Understanding Your Data)
