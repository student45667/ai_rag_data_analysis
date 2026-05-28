# Test Data Analysis: A High School Guide
## Part 4: Control Charts - Catching Problems Early

---

## What is a Control Chart?

A control chart tracks your measurements over time to spot when something goes wrong.

**Simple idea:**
- Plot your measurements on a graph
- Draw a line for the average (center line)
- Draw lines for upper and lower limits
- Watch for measurements that go outside the limits

**Real example: Manufacturing**
```
Day 1: 5.0, 5.1, 4.9 (all normal)
Day 2: 5.2, 5.1, 5.0 (still normal)
Day 3: 5.3, 5.4, 5.5 (starting to drift up)
Day 4: 5.6, 5.7, 5.8 (definitely trending up!)
ALERT: Something changed in the process!
```

The control chart catches this drift and you can fix it before products fail.

---

## The Simple Control Chart Setup

You need three lines:

### 1. Center Line (CL)

The average of your data.

**Formula:**
```
CL = Mean of your measurements
```

**Example:**
```
Measurements: 5.0, 5.1, 4.9, 5.0, 5.1, 5.2, 4.9, 5.0
Mean = (5.0+5.1+4.9+5.0+5.1+5.2+4.9+5.0) / 8 = 5.05
Center Line = 5.05
```

### 2. Upper Control Limit (UCL)

Usually calculated as:
```
UCL = Mean + (3 × Standard Deviation)
```

This means 99.7% of your normal data should fall below this line.

**Example:**
```
Mean = 5.05
Std Dev = 0.1
UCL = 5.05 + (3 × 0.1) = 5.05 + 0.3 = 5.35
```

### 3. Lower Control Limit (LCL)

Usually calculated as:
```
LCL = Mean - (3 × Standard Deviation)
```

**Example:**
```
Mean = 5.05
Std Dev = 0.1
LCL = 5.05 - (3 × 0.1) = 5.05 - 0.3 = 4.75
```

---

## Drawing the Control Chart

**Voltage measurements over 15 days:**

```
Day  Voltage (V)
1    5.0
2    5.1
3    4.9
4    5.0
5    5.2
6    5.1
7    4.9
8    5.0
9    5.1
10   5.2
11   5.3
12   5.4
13   5.5
14   5.6
15   5.7
```

**Calculate:**
```
Mean = 5.13 V
Std Dev = 0.22 V
UCL = 5.13 + (3 × 0.22) = 5.79 V
LCL = 5.13 - (3 × 0.22) = 4.47 V
```

**Chart visualization:**

```
Voltage
  ↑     ━━━━━━━━━━━━━━━━━━━━━━━━━━━ UCL = 5.79
  │
5.5├─ ─ ─ ─ ─ ─ ─ ●───────────────
  │          ●  ● ●
5.0├───●───●●    ─ ─ ─ CL = 5.13
  │  ● ● ●●    ●
4.5├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ LCL = 4.47
  │
  └─────────────────────────────→ Day
    1  3  5  7  9  11 13 15
```

**Interpretation:**

```
Days 1-10: All within limits, random variation
Days 11-15: Trending upward!
Day 15: Value of 5.7 is approaching the UCL

Conclusion: Something is changing. Investigate!
```

---

## How Control Charts Help

### Before Control Charts

```
You: "Our measurements are: 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6"
Boss: "Are they okay?"
You: "Uh... they're between 5.0 and 5.6? I guess so?"

Meanwhile the process is degrading and will fail tomorrow.
```

### With Control Charts

```
Day 1-3: All normal
Day 4-5: Slightly above center, but within limits
Day 6-7: Clearly trending upward!

You: "Boss, we have a trend. I recommend we investigate
      and probably maintain the equipment before it fails."
Boss: "Good catch! Let's fix it now before we waste material."
```

The chart makes the trend visible immediately.

---

## Red Flags: What to Watch For

### Red Flag 1: Point Beyond Limits

**This means:** Measurement is way off from normal. Something definitely wrong.

```
          UCL ━━━━━━━━━━━━━━━━━●← OUT OF BOUNDS!
             ───────────────────
       CL ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ●
          ───────────────────
          LCL ━━━━━━━━━━━━━━━━━

Action: STOP and investigate immediately.
```

**Common causes:**
- Equipment malfunction
- Wrong sample
- Measurement error
- Process upset

### Red Flag 2: Trend (6+ Points Going Up or Down)

**This means:** Process is drifting. Not suddenly bad, but getting worse.

```
          UCL ━━━━━━━━━━━━━━━━━━
             ───────────────────
       CL ─ ─ ─ ─ ─ ┌───●
          ───────────●────●
          LCL ━━━━●━━━━━━━━━━
                  ↑
              Starting here
```

**Common causes:**
- Equipment wearing out
- Temperature drift
- Calibration drifting
- Material batch change

**Why catch it early:**
```
If you catch the trend at point 3, you can maintain equipment.
If you wait until it breaks at point 10, you waste 7 days of bad material.
```

### Red Flag 3: Clustering (Most Points Above or Below Center)

**This means:** Process is off-target, but consistently.

```
          UCL ━━━━━━━━━━━━━━━━━━
             ───●───●───●──────
       CL ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
          ───────────────────
          LCL ━━━━━━━━━━━━━━━━━

(All points above the center line)
```

**Common causes:**
- Process is running hot/fast
- Equipment calibration is off
- New material batch

**Action:**
```
Check calibration. Something is systematically high.
```

### Red Flag 4: High Variation (Points Jumping Around)

**This means:** Process is unstable, random variation is high.

```
          UCL ━━━━━━━━━━━━━━━━━━
             ●───────────●─────
       CL ─ ─ ─●───●───●───────
          ───────────●─────●──
          LCL ━━●━━━━━━━━━━━━━

(Jumping all over the place)
```

**Common causes:**
- Unstable process
- Inconsistent procedure
- Environmental interference
- Multiple small problems

**Action:**
```
Standardize the process. Make sure everyone follows the same steps.
Reduce environmental variation (temperature, humidity, etc.).
```

---

## Real Example: Battery Testing

**Test: How long phone batteries last (hours)**

**Week 1 (New process):**
```
Day 1: 8.1, 8.2, 8.0
Day 2: 8.0, 8.1, 8.2
Day 3: 8.2, 8.1, 8.0
Daily averages: 8.10, 8.10, 8.10
```

**Week 2 (Something changed):**
```
Day 4: 8.1, 8.2, 8.1
Day 5: 8.2, 8.3, 8.2
Day 6: 8.3, 8.4, 8.3
Daily averages: 8.13, 8.23, 8.33 ← Trending up!
```

**Week 3 (Getting worse):**
```
Day 7: 8.5, 8.4, 8.4
Day 8: 8.6, 8.5, 8.6
Day 9: 8.7, 8.6, 8.7
Daily averages: 8.43, 8.57, 8.67 ← Much higher!
```

**Control Chart Analysis:**

```
Mean of week 1: 8.10
Std Dev: 0.08
UCL = 8.10 + (3 × 0.08) = 8.34
LCL = 8.10 - (3 × 0.08) = 7.86

Chart:
              UCL = 8.34 ━━━━━━●← Day 9 approaches limit
              CL = 8.10 ───●─●─●
                         ●─●
              LCL = 7.86 ━━━━━━

Day:    1   2   3   4   5   6   7   8   9
```

**What this tells you:**

```
Days 1-3: Process is stable
Days 4-6: Process is trending upward (watch!)
Days 7-9: Process is definitely out of control

Investigation reveals:
- Charger getting hotter over time
- Fan on charger isn't working properly
- Higher heat = faster battery degradation = longer "life" (bad!)

Fix: Replace fan in charger
Result: Days 10+ return to normal ~8.1 hours
```

---

## Creating Control Charts in Practice

### By Hand

1. Calculate mean and std dev
2. Calculate UCL and LCL
3. Draw graph:
   - X-axis = Time (day, run, etc.)
   - Y-axis = Measurement value
   - Draw center line, UCL, LCL as horizontal lines
   - Plot each point
   - Connect points with lines

### With Spreadsheet

**Setup:**

```
Column A: Day (1, 2, 3, ...)
Column B: Measurement (5.0, 5.1, 5.2, ...)
Column C: Mean =AVERAGE($B$1:$B$30)
Column D: UCL =AVERAGE($B$1:$B$30) + 3*STDEV($B$1:$B$30)
Column E: LCL =AVERAGE($B$1:$B$30) - 3*STDEV($B$1:$B$30)
```

**Charting:**
1. Select columns A, B, D, E
2. Insert Line Chart
3. Format as needed

---

## Different Types of Control Charts

### Individual-X Chart (What We've Been Showing)

Best for: One measurement per day/run

**What you plot:** Each individual measurement

### Moving Range Chart

Best for: Detecting smaller changes

**What you plot:** Range between consecutive measurements

### Average-Range Chart (X-bar, R Chart)

Best for: Multiple measurements per day

**When you have:**
```
Day 1: 5.0, 5.1, 5.2 (take average = 5.1)
Day 2: 5.1, 5.0, 5.1 (take average = 5.07)
Day 3: 5.2, 5.1, 5.2 (take average = 5.17)

Plot the daily averages: 5.1, 5.07, 5.17
```

This smooths out random variation and catches real trends better.

**How to set up:**

```
For each day, calculate:
1. Average of that day's measurements
2. Range (max - min) of that day's measurements

Plot the averages on one chart
Plot the ranges on another chart

Both tell you about process health
```

---

## Common Questions About Control Charts

### Q: What if I don't have many data points?

**A:** You need at least 20-30 points to calculate reliable limits. Less than that and your UCL/LCL won't be accurate.

**Solution:** Collect more data before setting up the chart.

### Q: What should I do when I see a red flag?

**A:** The classic procedure:

```
STOP
↓
INVESTIGATE
- Check the equipment
- Check the sample/material
- Check the procedure
- Check the conditions
↓
FIND THE ROOT CAUSE
↓
FIX IT
↓
VERIFY THE FIX WORKED
(measurements return to normal)
↓
DOCUMENT WHAT HAPPENED
(so you can avoid it next time)
```

### Q: Should I always use Mean ± 3 × Std Dev?

**A:** For starting out, yes. This is standard.

For advanced users:
- Some industries use ± 2 × Std Dev (more sensitive, more false alarms)
- Some use different calculations (EWMA, Cumulative Sum)
- But stick with ± 3 × Std Dev until you understand the basics

### Q: What if my measurements are not normally distributed?

**A:** The ± 3 × Std Dev method assumes a bell-shaped distribution. If your data is very skewed, you might need different limits.

For now: Assume normal distribution. Once you understand this, you can learn about other approaches.

---

## Real Example: Manufacturing Control Chart

**Scenario:** Factory produces springs. Each spring should be 10cm ± 0.2cm.

**Measurements over 10 days (daily average of 5 springs):**

```
Day 1: 10.02
Day 2: 10.01
Day 3: 10.00
Day 4: 10.03
Day 5: 10.02
Day 6: 10.15 ← Slightly high
Day 7: 10.25 ← Getting higher!
Day 8: 10.35 ← Higher still!
Day 9: 10.42 ← Much too high!
Day 10: 10.48 ← Way too high!
```

**Analysis:**

```
Mean of days 1-5: 10.016
Std Dev: 0.011
UCL: 10.016 + (3 × 0.011) = 10.05
LCL: 10.016 - (3 × 0.011) = 9.98

Control Chart:
          10.20 ━━━━━━━━━━━●───●───●
          10.10 ────────────●──────
          10.05 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ UCL
          10.01 ●────●───●──●──●
          9.98 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ LCL
          9.90 ━━━━━━━━━━━━━━━━━━

Day:      1   2   3   4   5   6   7   8   9   10
```

**What's happening:**

```
Days 1-5: Normal operation
Days 6-10: Clear upward trend
Day 9-10: Out of control!

Investigation reveals:
- Machine temperature was rising
- Heat expands the spring steel
- Longer springs being produced

Fix: Replace cooling fan
Result: Next batch returns to 10.0-10.02
```

---

## Summary: Control Charts in One Page

**Purpose:** Detect when a process goes out of control

**Setup:**
- Center Line (CL) = Mean
- Upper Control Limit (UCL) = Mean + 3 × Std Dev
- Lower Control Limit (LCL) = Mean - 3 × Std Dev

**Plot:** Measurements over time

**Watch for:**
1. Points beyond limits
2. Trends (6+ points going up/down)
3. Clustering (points mostly above/below center)
4. High variation (bouncing all over)

**Action:** When you see red flags, investigate and fix

**Benefit:** Catch problems early, before they ruin products

---

## Practice: Build Your Own

**Data: Temperature readings from a room (°C)**

```
Hour 1: 22.1
Hour 2: 22.0
Hour 3: 21.9
Hour 4: 22.1
Hour 5: 22.0
Hour 6: 22.2
Hour 7: 22.1
Hour 8: 22.0
Hour 9: 23.5 ← Spike!
Hour 10: 23.8 ← Higher!
```

**Questions:**
1. Calculate the mean of hours 1-8
2. Calculate the std dev of hours 1-8
3. Calculate UCL and LCL
4. Are hours 9 and 10 out of control?
5. What might have happened at hour 9?

**Answers:**
```
1. Mean = (22.1+22.0+21.9+22.1+22.0+22.2+22.1+22.0)/8 = 22.05°C

2. Std Dev ≈ 0.1°C

3. UCL = 22.05 + 3(0.1) = 22.35°C
   LCL = 22.05 - 3(0.1) = 21.75°C

4. Hour 9 (23.5°C) and Hour 10 (23.8°C) are way above UCL!
   YES, out of control

5. Possible causes:
   - Someone left a heater on
   - Sun came through a window
   - HVAC system failed
   - Someone opened a door to outside
```

---

## Next Steps

Move to **Part 5: Specifications & Capability** to learn how to compare your measurements against requirements.

---

**Last updated:** May 2026
**Difficulty level:** High School
**Time to read:** 20-25 minutes
**Prerequisite:** Part 3 (Basic Statistics)
