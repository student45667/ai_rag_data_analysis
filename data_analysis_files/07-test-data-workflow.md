# Test Data Analysis: A High School Guide
## Part 7: Practical Workflow - Putting It All Together

---

## Real Testing Situation: You're in the Lab

You're testing water quality. Spec: pH must be 6.5-8.5. You've collected 20 samples.

**What do you do?**

This part walks you through the complete workflow.

---

## Step-by-Step Workflow

### Step 1: Organize Your Data

**Get it into a spreadsheet:**

```
Sample# | Date      | Time   | pH    | Temperature | Notes
--------|-----------|--------|-------|-------------|--------
1       | 2026-05-27| 08:00  | 7.2   | 22.0       | Clear
2       | 2026-05-27| 08:15  | 7.1   | 21.9       | Clear
3       | 2026-05-27| 08:30  | 7.3   | 22.1       | Clear
4       | 2026-05-27| 08:45  | 7.0   | 21.8       | Slight cloudiness
5       | 2026-05-27| 09:00  | 7.4   | 22.2       | Clear
...
20      | 2026-05-27| 11:45  | 7.2   | 22.0       | Clear
```

**Why this matters:**
- Digital record (can't lose it)
- Easy to calculate statistics
- Can spot patterns in notes
- Professional documentation

### Step 2: Check Data Quality

Before analyzing, ask yourself:

```
□ Are all 20 measurements present?
  (Or did I get only 19?)

□ Do the measurements make sense?
  (pH of 15 would be impossible)

□ Are there obvious mistakes?
  (A measurement of 71 instead of 7.1?)

□ Did conditions vary?
  (Temperature, time of day, equipment)

□ Are there suspicious patterns?
  (All exactly 7.0? Too perfect?)

□ Any outliers?
  (One measurement way different?)
```

**In our example:**
```
All 20 samples ✓
pH values 7.0-7.4 ✓ (all reasonable)
No obvious typos ✓
Temperature 21.8-22.2 ✓ (consistent)
Patterns look normal ✓
One is 6.8, most are 7.0-7.4 (check if real)
```

**If something looks wrong:** Investigate before proceeding.

### Step 3: Calculate Summary Statistics

Use your spreadsheet:

```
=AVERAGE(pH values)        → Mean = 7.15
=MEDIAN(pH values)         → Median = 7.2
=STDEV(pH values)          → Std Dev = 0.14
=MIN(pH values)            → Min = 6.8
=MAX(pH values)            → Max = 7.4
=PERCENTILE(pH values, 0.99) → P99 = 7.35
```

**Record these:**

```
Summary Statistics - Water pH Test
Date: May 27, 2026
Sample size: 20

Mean: 7.15
Median: 7.2
Std Dev: 0.14
Min: 6.8
Max: 7.4
Range: 0.6
P99: 7.35
```

### Step 4: Check Against Specification

**Specification:** LSL = 6.5, USL = 8.5

```
All measurements are between 6.5 and 8.5 ✓

Count of failures: 0
Yield: 20/20 = 100%

Cpk calculation:
  Distance to LSL: 7.15 - 6.5 = 0.65
  Distance to USL: 8.5 - 7.15 = 1.35
  Nearest distance: 0.65
  
  Cpk = 0.65 / (3 × 0.14) = 0.65 / 0.42 = 1.55

Interpretation: GOOD (>1.33)
Process is capable and centered well
```

**Record:**
```
Pass/Fail: 100% PASS
Cpk: 1.55 (GOOD)
Risk: Low (wide safety margin from both limits)
```

### Step 5: Create Visualizations

**Histogram:**
```
Create histogram to see distribution

[Should be roughly bell-shaped, centered at 7.15]
```

**Box Plot:**
```
Q1 (25th percentile): 7.05
Median (50th): 7.20
Q3 (75th): 7.30
```

**Trend Plot (if measured over time):**
```
Plot pH over time (morning to late morning)
Should be fairly flat (no drift)
```

### Step 6: Analyze & Interpret

**Key questions:**

1. **Is the process centered on target?**
   - Yes (Mean 7.15 is near middle of 6.5-8.5 range)

2. **How much variation?**
   - Low (Std Dev 0.14 is small)

3. **Any outliers?**
   - One at 6.8 (low end, but still in spec)

4. **Over time, is it drifting?**
   - No (trend plot shows flat line)

5. **Can I predict future results?**
   - Yes, with high confidence 95% will be 6.85-7.45

### Step 7: Make Conclusions

```
CONCLUSIONS:

1. Water quality is GOOD
   - All samples pass specification
   - 100% yield
   - Cpk of 1.55 is acceptable

2. Process is STABLE
   - No trends over time
   - Consistent measurements
   - Variation is normal and low

3. Process is SAFE
   - Good margin to both limits
   - One outlier at 6.8 is still safe
   - No risk of exceeding spec

4. Current status: CONTINUE MONITORING
   - No action needed
   - Maintain current procedure
   - Collect weekly samples
   - Alert if trend develops or outliers appear
```

### Step 8: Document & Communicate

**Create a report:**

```
═══════════════════════════════════════════════════════
WATER QUALITY TEST REPORT
Date: May 27, 2026
Technician: Sarah Chen
Location: Building 3, Lab A
═══════════════════════════════════════════════════════

SPECIFICATION:
  pH must be between 6.5 and 8.5

SAMPLE COLLECTION:
  Sample size: 20
  Time period: 08:00 - 11:45
  Sampling interval: ~15 minutes
  Equipment: pH meter #5 (calibrated 2026-05-26)
  Conditions: Room temperature 21.8-22.2°C

RESULTS:
  Mean:        7.15
  Median:      7.20
  Std Dev:     0.14
  Range:       6.8 - 7.4
  Min/Max:     6.8 / 7.4
  
  PASS/FAIL:   20/20 PASS (100%)
  Cpk:         1.55 (GOOD)

INTERPRETATION:
  Water quality is good. All samples meet specification.
  Process is stable with low variation and good margin
  to both limits.

HISTOGRAM:
  [Include chart showing distribution]

RECOMMENDATION:
  Continue current process. Maintain weekly sampling.
  
NEXT REVIEW:
  June 3, 2026

Signature: _______________
```

---

## Real Example: Semiconductor Testing

**Scenario:** Testing leakage current of 100 chips from wafer lot W001

### The Workflow Applied

**Step 1: Organize Data**
```
Column A: Chip number (1-100)
Column B: Leakage current (µA)
Column C: Pass/Fail
```

**Step 2: Check Quality**
```
✓ All 100 measurements present
✓ Range 0.5-4.2 µA (reasonable for leakage)
✓ No obvious typos
✓ One outlier at 5.2 µA (investigate?)
```

**Step 3: Calculate Statistics**
```
Mean: 2.15 µA
Std Dev: 0.85 µA
Min: 0.5 µA
Max: 5.2 µA (outlier!)
```

**Step 4: Check Specification**
```
Spec: 0.1-5.0 µA
- Chip #47 has 5.2 µA → FAIL
- All others PASS
Yield: 99/100 = 99%
Cpk: 1.12 (borderline)
```

**Step 5: Visualize**
```
Histogram: Shows roughly normal, maybe slight high tail
Box plot: Shows median ~2.0, upper whisker touching ~4.2
```

**Step 6: Analyze**
```
1. Process is acceptable (99% yield)
2. One failure (chip #47) - investigate if it's bad or measurement error
3. Cpk of 1.12 is okay but tight - upper limit is at risk
4. Consider tightening process or investigating high leakage trend
```

**Step 7: Conclusions**
```
✓ Wafer lot W001 is acceptable (99% yield, >Cpk 1.0)
! Watch the upper tail (some chips approaching 5.0 µA)
? Investigate the one failure at 5.2 µA (equipment error?)
→ Recommend: Accept lot, but monitor for upper-end drift
```

**Step 8: Document**
```
Wafer Sort Report - Lot W001
Date: May 27, 2026
Tester: John Smith

LEAKAGE TEST (Spec: 0.1-5.0 µA):
  Total dice: 100
  Pass: 99
  Fail: 1
  Yield: 99%
  Cpk: 1.12

NOTE: Chip #47 measured 5.2 µA (above spec).
      Recommend retest to verify.
      
RECOMMENDATION: ACCEPT LOT
  (99% yield is acceptable)
  Caution: Monitor trend toward upper limit
```

---

## Daily Testing Checklist

When you test something, use this checklist:

```
BEFORE TESTING:
□ Equipment calibrated?
□ Procedure reviewed?
□ Supplies ready?
□ Note conditions (temperature, humidity, time)

DURING TESTING:
□ Follow procedure exactly
□ Record all measurements (don't skip any)
□ Note anything unusual
□ Check for obvious problems

AFTER TESTING:
□ Organize data in spreadsheet
□ Check for data quality issues
□ Calculate mean, std dev, min, max
□ Check against spec limits
□ Calculate pass/fail rate and Cpk
□ Make a chart
□ Write a summary
□ Document conclusions
□ Plan next steps
```

---

## When Something Goes Wrong

**Red flag detected?** Follow this process:

```
RED FLAG DETECTED
        ↓
   STOP TESTING
        ↓
  INVESTIGATE
  - Check equipment calibration
  - Review procedure
  - Check sample/material
  - Check conditions
  - Look at your notes
        ↓
  FIND ROOT CAUSE
  - Was it a measurement error?
  - Was it a real process problem?
  - Something environmental?
        ↓
  FIX IT
  - Recalibrate equipment
  - Adjust process
  - Change conditions
  - Retrain if procedure was wrong
        ↓
  VERIFY FIX WORKED
  - Test again
  - Confirm measurements return to normal
        ↓
  DOCUMENT
  - What went wrong
  - What you did to fix it
  - What the root cause was
  - Prevention for future
        ↓
  RESUME NORMAL TESTING
```

---

## Quick Reference: Interpretation Summary

| Observation | Means | Action |
|-------------|-------|--------|
| All PASS, Cpk > 1.5 | Great! | Continue as is |
| All PASS, Cpk 1.0-1.5 | Good | Monitor closely |
| Some FAIL, Cpk < 1.0 | Problem | Investigate & improve |
| 100% PASS but Cpk low | Risky! | Will fail soon |
| Yield dropping trend | Drifting | Find & fix root cause |
| One large outlier | One-time issue? | Investigate that sample |
| Regular trend up/down | Equipment drift | Maintain/calibrate |
| Wild variation | Unstable process | Standardize procedure |

---

## Real Report Template

Use this for your actual testing:

```
═════════════════════════════════════════════
[PRODUCT] TEST REPORT
═════════════════════════════════════════════

Date: [Date]
Technician: [Name]
Equipment: [What you used]

SPECIFICATION:
[What must pass?]

PROCEDURE:
[How did you test?]

SAMPLE INFORMATION:
Size: [How many items tested?]
Time: [When collected?]
Conditions: [Temperature, pressure, etc.]

RESULTS - SUMMARY:
Total: [#]
Pass: [#] ([%])
Fail: [#] ([%])

STATISTICS:
Mean: [value]
Std Dev: [value]
Min/Max: [values]
Cpk: [value]

[INCLUDE CHART/HISTOGRAM]

INTERPRETATION:
[What does this mean?]

CONCLUSIONS:
[Are we good? Problem? Watch?]

ACTION ITEMS:
[What happens next?]

Signature: ___________
```

---

## Summary: The Complete Workflow

1. **Organize** your data properly
2. **Check** data quality before analyzing
3. **Calculate** summary statistics
4. **Compare** against specifications
5. **Visualize** with appropriate charts
6. **Analyze** what the data means
7. **Conclude** with clear interpretation
8. **Document** professionally
9. **Communicate** findings clearly
10. **Act** on recommendations

Follow this every time, and you'll be doing professional data analysis.

---

## Practice: Your Turn

**Scenario:** You test 10 light bulbs for lifespan.
Spec: 1000+ hours

**Data:**
```
Bulb 1: 1050 hours
Bulb 2: 980 hours
Bulb 3: 1100 hours
Bulb 4: 920 hours
Bulb 5: 1010 hours
Bulb 6: 1150 hours
Bulb 7: 990 hours
Bulb 8: 1020 hours
Bulb 9: 960 hours
Bulb 10: 1030 hours
```

**Do this:**
1. Calculate mean
2. Calculate std dev
3. Count pass/fail (>1000 is pass)
4. Calculate yield %
5. Write one sentence conclusion

**Answers:**
```
1. Mean = (1050+980+1100+920+1010+1150+990+1020+960+1030)/10
        = 10,210 / 10 = 1021 hours

2. Std Dev ≈ 68 hours (use spreadsheet)

3. Pass/Fail:
   1050 ✓, 980 ✗, 1100 ✓, 920 ✗, 1010 ✓,
   1150 ✓, 990 ✗, 1020 ✓, 960 ✗, 1030 ✓
   
   Pass: 6, Fail: 4

4. Yield = 6/10 = 60% (POOR!)

5. Conclusion: This batch of bulbs is NOT acceptable.
   60% failure rate is too high. Investigate manufacturing.
```

---

## Next Steps

Move to **Part 8: Common Mistakes** to learn what NOT to do.

Or, if you're ready, start applying this to your own experiments!

---

**Last updated:** May 2026
**Difficulty level:** High School
**Time to read:** 20-25 minutes
**Prerequisite:** Parts 1-6
**Real-world application:** Yes! Use this immediately in your testing
