# Test Data Analysis: A High School Guide
## Part 5: Specifications & Capability - Do You Pass?

---

## The Big Question: Is My Product Good Enough?

Every product has requirements. Requirements are called **specifications** or **specs**.

**Examples:**

```
Light bulb: Must last 1000+ hours
Phone battery: Must last 8-10 hours per charge
Bridge: Must support 50,000+ pounds
Spring: Must be 10.0 ± 0.2 cm long
Water quality: pH must be 6.5-8.5
```

**Your job:** Test your product and compare against the specs.

---

## Specification Limits Explained

### Lower Spec Limit (LSL)

The **minimum acceptable value**.

**Examples:**
```
Light bulb: LSL = 1000 hours (must last at least this long)
Bridge: LSL = 50,000 pounds (must support at least this)
Water pH: LSL = 6.5 (can't go below this)
```

**What happens if you go below LSL?** FAIL. The product doesn't meet requirements.

### Upper Spec Limit (USL)

The **maximum acceptable value**.

**Examples:**
```
Temperature sensor error: USL = 2°C (error can't exceed 2°C)
Product weight: USL = 101g (can't be heavier than this)
Water pH: USL = 8.5 (can't go above this)
```

**What happens if you go above USL?** FAIL. The product doesn't meet requirements.

### Target (Nominal)

The **ideal value**. Right in the middle of the range.

**Example:**
```
Spec: 10.0 ± 0.5 mm
  LSL: 9.5 mm
  Target: 10.0 mm (ideal)
  USL: 10.5 mm
```

**In reality:** Any value between LSL and USL passes. But you should aim for the target.

---

## One-Sided vs Two-Sided Specs

### Two-Sided Spec (Most Common)

Has both a lower and upper limit.

**Example:**
```
Spring length spec: 10.0 ± 0.2 cm
  LSL: 9.8 cm
  Target: 10.0 cm
  USL: 10.2 cm

Pass if: 9.8 ≤ measurement ≤ 10.2
```

### One-Sided Spec (Lower Limit Only)

Only a minimum is specified.

**Example:**
```
Light bulb lifespan spec: ≥ 1000 hours
  LSL: 1000 hours
  No upper limit

Pass if: measurement ≥ 1000
(1500 hours is great, 10,000 is fine too)
```

### One-Sided Spec (Upper Limit Only)

Only a maximum is specified.

**Example:**
```
Water contamination: ≤ 10 ppm (parts per million)
  USL: 10 ppm
  No lower limit

Pass if: measurement ≤ 10
(0 ppm is great, 0.5 ppm is fine too)
```

---

## Yield: The Bottom Line

**Yield** = Percentage of products that pass spec.

**Formula:**
```
Yield (%) = (Number of items that pass) / (Total number of items) × 100
```

**Example:**
```
You test 100 springs
95 springs: Between 9.8 and 10.2 cm (PASS)
5 springs: Outside this range (FAIL)

Yield = 95/100 × 100 = 95%
```

**What's good yield?**
```
90% or higher: Acceptable
95% or higher: Good
99% or higher: Excellent
99.9% or higher: World-class
```

---

## Real Example: Testing Semiconductors

**Spec:** Leakage current must be 0.1 to 5.0 microamps

**Test results (10 chips):**
```
Chip 1: 0.8 µA  ✓ PASS (within spec)
Chip 2: 1.1 µA  ✓ PASS
Chip 3: 1.3 µA  ✓ PASS
Chip 4: 1.5 µA  ✓ PASS
Chip 5: 1.7 µA  ✓ PASS
Chip 6: 2.0 µA  ✓ PASS
Chip 7: 2.2 µA  ✓ PASS
Chip 8: 2.5 µA  ✓ PASS
Chip 9: 3.0 µA  ✓ PASS
Chip 10: 4.2 µA ✓ PASS

Yield: 10/10 = 100%
```

**All passed because all are between 0.1 and 5.0 µA.**

---

## But Yield Doesn't Tell the Whole Story

**Two processes, both 95% yield:**

```
Process A:
  95% of parts: 4.9-5.1 cm (very consistent, centered)
  5% of parts: Outside spec
  Yield: 95%
  
Process B:
  95% of parts: 4.5-5.5 cm (spread out, near edges)
  5% of parts: Outside spec
  Yield: 95%
```

**Same yield, but very different!**

- Process A has room for adjustment (safe)
- Process B is on the edge (risky)

**What if spec limit changes by 0.1 mm?**
- Process A: Still 95% (safe)
- Process B: Drops to 80% (disaster)

This is why we need **Capability Index (Cpk)**.

---

## Capability Index: Cpk

**What it measures:** Is your process consistently making good products? Do you have room for error?

**Simple formula:**
```
Cpk = (USL - Mean) / (3 × Std Dev)
```

Wait, that's not quite right. Let me give you the real formula:

```
Cpk = minimum of:
  [ (USL - Mean) / (3 × Std Dev) ]
  [ (Mean - LSL) / (3 × Std Dev) ]

In other words: How far is the mean from the nearest spec limit,
divided by how spread out the data is?
```

**Simpler thinking:**
- If your process mean is far from both limits and spread is tight = high Cpk
- If your process mean is close to a limit or spread is wide = low Cpk

### Cpk Interpretation

```
Cpk > 1.67  : EXCELLENT
             "We're nowhere near the limits"
             Very safe, lots of room for variation

Cpk = 1.33  : GOOD
             "We're doing well"
             Acceptable margin for error
             This is the minimum for many industries

Cpk = 1.0   : BORDERLINE
             "We're okay, but risky"
             About 0.3% defects expected
             Not comfortable

Cpk = 0.67  : MARGINAL
             "We're in trouble"
             About 5% defects
             Need immediate improvement

Cpk < 0.67  : POOR
             "Process is inadequate"
             Many defects
             Can't produce good products
```

---

## Real Example: Spring Manufacturing

**Specification:** Spring length 10.0 ± 0.2 cm
- LSL = 9.8 cm
- Target = 10.0 cm
- USL = 10.2 cm

### Scenario A: Good Process

```
Measurements: 9.95, 9.98, 10.00, 10.02, 10.05, 10.00, 9.99, 10.01

Mean: 10.00 cm
Std Dev: 0.03 cm

Distance to nearest limit:
  From mean to LSL: 10.00 - 9.8 = 0.2 cm
  From mean to USL: 10.2 - 10.00 = 0.2 cm
  Nearest distance: 0.2 cm

Cpk = 0.2 / (3 × 0.03) = 0.2 / 0.09 = 2.2

Interpretation: EXCELLENT
- Mean is right on target
- Spread is very tight
- Lots of room before hitting limits
- Almost no defects
```

### Scenario B: Off-Target Process

```
Measurements: 9.92, 9.95, 9.98, 10.00, 10.02, 10.05, 10.08, 10.10

Mean: 10.01 cm
Std Dev: 0.06 cm

Distance to nearest limit:
  From mean to LSL: 10.01 - 9.8 = 0.21 cm
  From mean to USL: 10.2 - 10.01 = 0.19 cm
  Nearest distance: 0.19 cm (closer to USL)

Cpk = 0.19 / (3 × 0.06) = 0.19 / 0.18 = 1.06

Interpretation: BORDERLINE
- Slightly off target (toward high)
- Higher variation than Scenario A
- Getting close to USL
- Some defects expected
- Need to adjust or tighten process
```

### Scenario C: Wide Spread Process

```
Measurements: 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4

Mean: 10.0 cm
Std Dev: 0.24 cm

Distance to nearest limit:
  From mean to LSL: 10.0 - 9.8 = 0.2 cm
  From mean to USL: 10.2 - 10.0 = 0.2 cm
  Nearest distance: 0.2 cm

Cpk = 0.2 / (3 × 0.24) = 0.2 / 0.72 = 0.28

Interpretation: POOR
- Mean is on target
- But variation is huge!
- Already hitting both limits
- Many defects
- Process is broken, needs major overhaul
```

---

## How to Improve Cpk

### Problem: Cpk Too Low

There are basically two things wrong:

**1. Mean is off-target** (process is running too high or too low)

```
Current: Mean = 10.05, Target = 10.00

Solution: Adjust the process
  - Reduce temperature/pressure/speed
  - Retune the machine
  - Change material batch
  - Usually a small tweak
```

**2. Variation is too high** (process is inconsistent)

```
Current: Std Dev = 0.15, Desired = 0.06

Solution: Reduce variation
  - Standardize procedures (everyone does it the same way)
  - Better quality material
  - Reduce environmental variation (temperature control)
  - Better trained workers
  - Better equipment
  - Usually requires more effort
```

### Most Common Issues

**Cpk > 1.33 but trending down:**
```
Your process is good now, but variation is increasing.
Action: Maintain equipment, standardize procedure
```

**Cpk near 1.33, customer changing spec:**
```
They want tighter tolerance (smaller spec window).
Action: Improve process or negotiate with customer
```

**High yield but low Cpk:**
```
You're passing now but only by luck.
One small change and you'll start failing.
Action: Don't wait—improve the process now
```

---

## Cpk in Manufacturing

**Semiconductor wafer testing:**
```
Spec: Leakage 0.1-5.0 µA
Measured: Mean=2.1, Std Dev=0.8
Cpk = (5.0-2.1) / (3×0.8) = 2.9/2.4 = 1.21

Acceptable but could be better
Action: Investigate why variation is high
```

**Phone battery life:**
```
Spec: 8.0-10.0 hours
Measured: Mean=9.0, Std Dev=0.3
Cpk = (10.0-9.0) / (3×0.3) = 1.0/0.9 = 1.11

Getting close to limit
Action: Keep monitoring, reduce variation if possible
```

**Water quality pH:**
```
Spec: 6.5-8.5 (range of 2.0)
Measured: Mean=7.5, Std Dev=0.15
Cpk = (8.5-7.5) / (3×0.15) = 1.0/0.45 = 2.22

Very good—wide safety margin
```

---

## Pass/Fail Rate Based on Cpk

If your process is normally distributed:

```
Cpk    | Defect Rate | Yield
-------|-------------|--------
1.67   | 0.006%      | 99.994%
1.33   | 0.063%      | 99.937%
1.00   | 0.270%      | 99.730%
0.67   | 4.27%       | 95.73%
0.50   | 13.36%      | 86.64%
```

---

## Practice: Calculate Cpk

**Resistor spec:** 1000Ω ± 50Ω
- LSL = 950Ω
- Target = 1000Ω
- USL = 1050Ω

**Measured values:**
```
987, 991, 995, 999, 1003, 1007, 1011, 1015
```

**Calculate:**
1. Mean
2. Std Dev
3. Cpk

**Solution:**

```
1. Mean = (987+991+995+999+1003+1007+1011+1015) / 8
       = 8008 / 8 = 1001Ω

2. Std Dev ≈ 9.9Ω (Use spreadsheet for this)

3. Distance to limits:
   From mean to LSL: 1001 - 950 = 51Ω
   From mean to USL: 1050 - 1001 = 49Ω
   Nearest: 49Ω

   Cpk = 49 / (3 × 9.9) = 49 / 29.7 = 1.65

Interpretation: GOOD (barely)
- Process is centered near target
- But close to USL
- Acceptable but not excellent
```

---

## Quick Reference Table

| Situation | Cpk | Action |
|-----------|-----|--------|
| Process is unstable | Any | Fix stability first |
| Cpk > 1.5 | High | Monitor only |
| 1.33 < Cpk < 1.5 | Good | Regular monitoring |
| 1.0 < Cpk < 1.33 | Borderline | Work on improvement |
| 0.67 < Cpk < 1.0 | Poor | Urgent improvement |
| Cpk < 0.67 | Fail | Process inadequate |
| Mean is drifting | Any | Investigate immediately |

---

## Summary: Specifications & Capability

**Specifications tell you:** What's acceptable

**Yield tells you:** What percentage passes right now

**Cpk tells you:** Are you safe long-term? Do you have room for error?

**All three together tell the real story:**
```
High yield + Low Cpk = Dangerous (will fail soon)
High yield + High Cpk = Great (stable, long-term safe)
Low yield + High Cpk = Setup problem (fix mean)
Low yield + Low Cpk = Broken process (major overhaul)
```

---

## Next Steps

Move to **Part 6: Visual Methods** to learn how to make charts that show all this information clearly.

---

**Last updated:** May 2026
**Difficulty level:** High School (Algebra II)
**Time to read:** 20-25 minutes
**Prerequisite:** Part 3 (Basic Statistics)
