# Test Data Analysis: A High School Guide
## Part 2: Understanding Your Data

---

## What is Test Data?

**Test data** = Any measurement or count you collect while testing something.

### Real Examples

**Chemistry Lab:**
- pH of a solution: 7.2, 7.1, 7.3, 7.2
- Reaction time in seconds: 42, 45, 43, 41
- Concentration in mg/L: 0.55, 0.58, 0.54, 0.57

**Physics Experiment:**
- Distance a ball rolls: 3.2 m, 3.1 m, 3.3 m
- Temperature change: +5.5°C, +5.8°C, +5.2°C
- Speed of a car: 25 mph, 26 mph, 24 mph

**Manufacturing:**
- Light bulb lifespan: 1000 hrs, 1050 hrs, 980 hrs
- Bolt diameter: 10.0 mm, 9.98 mm, 10.02 mm
- Pass or fail: PASS, PASS, FAIL, PASS

**Quality Control:**
- Number of defects per batch: 2, 3, 1, 4
- Customer satisfaction score: 4, 5, 3, 4, 5
- Weight of product: 499 g, 501 g, 500 g, 502 g

---

## Two Types of Data

### Type 1: Numerical Data (Quantitative)

**What it is:** Actual numbers with meaning.

**Examples:**
- Temperature: 25.3°C, 24.8°C, 25.1°C
- Time: 3.2 seconds, 3.5 seconds, 3.1 seconds
- Voltage: 5.0 V, 4.9 V, 5.1 V
- Count: 5 defects, 3 defects, 7 defects

**Two subtypes:**

**Discrete (Whole numbers):**
- Number of defects: 0, 1, 2, 3... (can't have 2.5 defects)
- Number of students: 15, 20, 18...
- Pass/fail count: 45 pass, 5 fail
- You count them, not measure them

**Continuous (Decimal numbers):**
- Temperature: 25.3°C, 24.8°C, 25.1°C (any value possible)
- Voltage: 5.04 V, 5.003 V (precise measurements)
- Weight: 100.2 g, 100.15 g, 100.33 g
- You measure them with instruments

**Why does this matter?** Different statistics work better for each type. Continuous data is usually easier to analyze.

---

### Type 2: Categorical Data (Qualitative)

**What it is:** Labels or categories, not numbers.

**Examples:**
- Test result: PASS, FAIL, FAIL, PASS
- Product type: Type A, Type B, Type A, Type C
- Color: Red, Blue, Red, Green
- Defect type: Crack, Burn, Short circuit, None
- Condition: Good, Fair, Poor, Good, Fair

**How you count them:**
```
Results: PASS, PASS, FAIL, PASS, FAIL, PASS, FAIL, PASS

Count:
  PASS: 5
  FAIL: 3
```

Or percentages:
```
PASS: 5/8 = 62.5%
FAIL: 3/8 = 37.5%
```

**When you use categorical data:**
- Quality control (Pass/Fail)
- Defect tracking (type of problem)
- Surveys (responses to questions)
- Categories (A, B, C grades)

---

## Real Example: Different Data Types

**Testing smartphone performance:**

```
Numerical (Continuous):
  Battery life: 8.2 hrs, 8.5 hrs, 7.9 hrs
  CPU speed: 2.8 GHz, 2.9 GHz, 2.8 GHz
  Weight: 185 g, 186 g, 184 g

Numerical (Discrete):
  Number of features that work: 23, 24, 22
  Number of defects found: 0, 1, 0

Categorical:
  Pass or fail: PASS, FAIL, PASS, PASS
  Color: Black, White, Gold, Silver
  Defect type: None, Battery issue, Screen defect, None
```

---

## Data Quality: The Foundation Everything Rests On

### Poor data = Useless conclusions

No matter how good your analysis is, garbage data = garbage results.

This is called **GIGO: Garbage In, Garbage Out**

### What Makes Data "Good"?

#### 1. Accurate

**Accurate** = The measurement is correct.

**How to ensure:**
- Use calibrated instruments
- Check that your measuring tool is working
- Repeat measurements to verify
- Follow proper procedures exactly

**Bad example:**
```
You test a thermometer. It reads 25°C.
Actually, the room is 20°C.
Your thermometer is wrong by 5°C.
Any data you collect will be off by 5°C.
```

**Good example:**
```
You calibrate a scale before use.
You weigh a known standard (100g weight).
Scale reads 100g. Good.
Now measurements will be accurate.
```

#### 2. Complete

**Complete** = You have all the measurements you're supposed to have.

**What's not complete:**
```
You're supposed to test 10 samples.
You only test 8 because you ran out of time.
You have incomplete data.
```

**What's complete:**
```
You test all 10 samples.
Even if some fail, you have all 10 measurements.
```

**Missing values problem:**
```
Measurements: 2.1, 2.3, ?, 2.2, 2.0, 2.4
(missing one value in the middle)

This causes problems because:
- Can't calculate accurate average
- Smaller sample size
- Might be biased (maybe the missing one was broken)
```

#### 3. Consistent

**Consistent** = Collected the same way every time.

**Inconsistent example (Bad):**
```
First 5 measurements: Using a ruler, measuring length
Next 5 measurements: Using a tape measure, measuring length
Different tools = Different precision = Inconsistent
```

**Consistent example (Good):**
```
All 10 measurements: Using same ruler, same method, same person
Or: Using same ruler, different people follow same procedure
Consistency means the measurement method doesn't change
```

**Why it matters:**
- If you switch methods, you can't compare results
- Variation might be from your method, not from what you're testing

#### 4. Representative

**Representative** = Your sample actually represents the whole thing.

**Not representative (Bad):**
```
Testing phone battery life.
You only test brand new phones.
You don't test phones that have been used for a year.
Your conclusion: "Phones last 8 hours"
But actually, used phones last only 5 hours.
```

**Representative (Good):**
```
Testing phone battery life.
You test: 3 brand new, 3 used for 6 months, 3 used for 1 year
You get the real picture across the phone's life
```

**Real example of sampling problems:**
```
You want to know: "What's the average height of teenagers?"

Bad sample: Test only basketball players
(Basketball players are taller than average)
Result: 6'2" average (too high)

Good sample: Random students from different schools
Result: 5'8" average (actually representative)
```

---

## How to Collect Good Data

### Checklist Before You Test

- [ ] Is my equipment calibrated? (Tested with known standard)
- [ ] Do I understand the procedure? (Read it carefully)
- [ ] Am I sampling fairly? (Not picking only good/bad items)
- [ ] Do I have a sample size? (How many measurements will you take?)
- [ ] Will I take all measurements? (Or are you stopping early?)
- [ ] Am I measuring the right thing? (Not a mistake)
- [ ] Will conditions be consistent? (Same temperature, pressure, etc.?)

### Recording Data Well

**Bad recording:**
```
2.1, 2.3, 2.2, ?, 2.0
(missing one, no date, no notes about what happened)
```

**Good recording:**
```
Date: May 27, 2026
Test: Battery life test
Equipment: Standard charger, Timer app
Procedure: Full charge then test until dead
Room temp: 22°C

Measurement #  Value (hours)  Notes
1              8.2            Normal
2              8.5            Normal
3              7.9            Normal
4              8.1            Normal (restart took time)
5              8.3            Normal
```

**Why this matters:**
- You remember why a measurement was odd
- Others can understand your data
- You can spot if something was different

---

## Red Flags: When Your Data is Suspect

### Red Flag 1: Outliers (Weird Values)

**Outlier** = A measurement that's way different from the others.

**Example:**
```
Measurements: 2.0, 2.1, 2.0, 2.1, 9.5, 2.0, 2.1
                                 ^^^
                    This one is VERY different
```

**Possible causes:**
- Measurement error (you read it wrong)
- Equipment error (scale malfunctioned)
- Real problem (the sample was bad)
- User error (someone used it wrong)

**What to do:**
1. Note it but don't delete it automatically
2. Investigate: "Why is it different?"
3. If you find it's a mistake, you can exclude it
4. If you don't know, include it anyway
5. Never just delete data because it looks weird

**Bad approach:**
```
"I got these numbers: 2, 2, 2, 9, 2, 2
The 9 looks wrong, so I'll delete it.
Final data: 2, 2, 2, 2, 2"
```
(This is dishonest if you're just removing what you don't like)

**Good approach:**
```
"I got these numbers: 2, 2, 2, 9, 2, 2
The 9 is very different. I checked:
- My measurement procedure: Correct
- The equipment: Works fine
- The sample: Sample #4 was from a different batch
Conclusion: The 9 is real, not a measurement error.
Final analysis: Include it, but note it as different
```

### Red Flag 2: Too Much Variation

**Example:**
```
You're testing light bulb lifespan.
Results: 100 hours, 1000 hours, 50 hours, 10000 hours
(These vary WILDLY)
```

**Possible causes:**
- Different testing conditions (room temperature varies)
- Poor quality control (some bulbs are bad)
- Testing method isn't standardized
- Different types of bulbs

### Red Flag 3: Same Value Repeated Too Much

**Example:**
```
You measure weight: 100, 100, 100, 100, 100
(Exactly the same every time - suspicious!)
```

**Possible causes:**
- Rounding (you rounded everything to nearest unit)
- Scale doesn't measure precisely (it rounds)
- You're not actually measuring, just recording a standard

**Why it's a problem:**
- Real measurements have variation
- This much consistency is unlikely
- Hard to analyze (no variation = no statistics to calculate)

### Red Flag 4: Suspicious Patterns

**Example:**
```
Measurements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8
(Goes up evenly - very suspicious!)
```

**Possible causes:**
- You're not actually measuring
- Data is made up
- There's a real trend (something changing)

**What to do:**
- Investigate if there's a real reason for the pattern
- Don't assume the worst
- But pay attention to this

---

## Data Organization: Setting Up for Success

### Spreadsheet Format (Best)

```
Date       | Sample# | Measurement | Temperature | Notes
-----------|---------|-------------|------------|-------
2026-05-27 | 1       | 2.1         | 22.0       | Normal
2026-05-27 | 2       | 2.3         | 22.1       | Normal
2026-05-27 | 3       | 2.0         | 21.9       | Normal
2026-05-27 | 4       | 2.2         | 22.0       | Normal
```

**Why this works:**
- Easy to see patterns
- Can sort/filter
- Can calculate statistics
- Can be imported to analysis tools
- Professional presentation

### Lab Notebook Format (Also Good)

```
Date: May 27, 2026
Experiment: Battery lifespan test
Technician: Sarah
Conditions: Room temp 22°C, Standard charger, Indoor location

Sample | Time (hours) | Observations
-------|--------------|------------------
1      | 8.2          | Normal shutdown
2      | 8.5          | Normal shutdown
3      | 7.9          | Fading before shutdown
4      | 8.1          | Normal shutdown
```

**Why this works:**
- Official record (hard to fake)
- Space for notes
- Professional
- Good for compliance/legal issues

---

## Summary Checklist: Before You Analyze

- [ ] Data is accurate (measurements are correct)
- [ ] Data is complete (no missing values without reason)
- [ ] Data is consistent (collected same way throughout)
- [ ] Data is representative (actual sample, not cherry-picked)
- [ ] Data is recorded with dates and context
- [ ] Outliers are investigated, not just deleted
- [ ] I have at least 5-10 measurements (minimum)
- [ ] I know where each measurement came from

If you can check all these, you have quality data.

**If you can't**, you have a problem that no amount of statistics can fix.

---

## Real Example: Poor Data Collection

**A student tests how long a phone battery lasts:**

```
Measurement 1: 8 hours (new phone, freshly charged)
Measurement 2: 7 hours (6-month-old phone, normal use)
Measurement 3: 12 hours (used phone in airplane mode)
Measurement 4: 2 hours (phone overheating from heavy gaming)
```

**Problems:**
- Different phones (ages vary)
- Different conditions (some airplane mode, some not)
- Different use cases (gaming vs normal)
- Not representative (mixes everything together)

**Better approach:**
```
Test only: Brand new phones, same model, same age
All tests: Same charger, same location, normal usage only
All conditions: Room temp 22°C, same time of day

Results are now comparable and meaningful.
```

---

## Next Steps

You now understand what good data looks like.

Move to **Part 3: Basic Statistics** to learn what to do with your data once you have it.

---

**Last updated:** May 2026
**Difficulty level:** High School
**Time to read:** 15-20 minutes
**Prerequisite:** Part 1 (Introduction)
