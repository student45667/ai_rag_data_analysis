# Test Data Analysis: A High School Guide
## Part 8: Common Mistakes - What NOT to Do

---

## Why This Matters

Making a mistake in analysis is worse than doing no analysis.

**Why?** Because you'll be confident in the wrong answer. You'll make decisions based on bad data.

This part teaches you what can go wrong.

---

## Mistake 1: Trusting One Measurement

### The Problem

```
You test one chip: Leakage = 0.8 µA
Spec is 0.1-5.0 µA
Conclusion: "We're fine!"

But you have no idea if this is typical or an outlier.
```

### Why It's Wrong

**One data point tells you NOTHING about your process.**

```
One measurement could be:
- Typical (the process is fine)
- An outlier (the process has a problem hidden by luck)
- A measurement error (you read it wrong)
- Affected by conditions (temperature was off)
```

### What to Do Instead

**Always collect multiple measurements:**

```
❌ Bad: Test one item
✓ Good: Test at least 5-10 items

❌ Bad: One test run
✓ Good: Test over multiple days/runs

❌ Bad: One batch of material
✓ Good: Test across multiple batches
```

**Minimum sample size:**
- 5 measurements = barely acceptable
- 10 measurements = minimum
- 20+ measurements = good
- 100+ measurements = excellent

**Real consequence:**
```
One chip passes: "Ship it!"
Test 100 chips: 10 fail
This is the difference between success and disaster.
```

---

## Mistake 2: Ignoring Trends

### The Problem

```
Day 1: 2.0, 2.1, 2.0
Day 2: 2.2, 2.1, 2.2
Day 3: 2.4, 2.5, 2.3
Day 4: 2.6, 2.7, 2.5

Observation: "Every measurement is within 2.0-2.7. 
             This is within our 1.5-3.0 spec. We're okay!"

WRONG!
```

### Why It's Wrong

The data is TRENDING UPWARD. If this continues:

```
Day 5: 2.8, 2.9, 2.8
Day 6: 3.0, 3.1, 3.0
Day 7: 3.2 → OUT OF SPEC!
```

**You had warning on Day 2 or 3!** But you ignored it.

### What to Do Instead

**Watch for trends:**

```
✓ Plot measurements over time
✓ Look for: Going up, going down, gradually changing
✓ Calculate weekly/daily average to see the trend better
✓ Don't just look at individual numbers
✓ Act when trend is 25% toward the limit, not 90%
```

**Real example:**

```
Temperature control system drifting upward:
Day 1: 22.0°C (target = 22, spec = 20-24)
Day 3: 22.5°C (trend visible?)
Day 5: 23.0°C (clear trend!)
Day 7: 23.5°C (problem getting worse)
Day 8: 24.0°C (at limit)
Day 9: 24.5°C (OUT OF SPEC!)

If you caught it on Day 5, you have 2-3 days to fix.
If you wait until Day 9, you have a disaster.
```

---

## Mistake 3: Using the Wrong Statistic

### The Problem

```
Salaries: $30,000, $32,000, $35,000, $1,000,000

Mean: ($30k + $32k + $35k + $1M) / 4 = $274,250

Conclusion: "Average salary is $274k!"

MISLEADING! Three people make ~$32k, one person 
makes $1M. That's not representative.
```

### Why It's Wrong

The mean was pulled way off by one outlier.

### What to Do Instead

**Know which statistic to use:**

```
✓ Use MEAN when: Data is roughly normal, no big outliers
✓ Use MEDIAN when: There are outliers, skewed data
✓ Use STD DEV when: Comparing consistency (spread)
✓ Use MIN/MAX when: Checking limits, extremes
✓ Use PERCENTILE when: Risk assessment, worst-case
```

**Real example:**

```
Test scores: 45, 50, 55, 60, 65, 70, 75, 80, 85, 95, 98, 100

Mean: 72.1
Median: 67.5

Which is more "typical"?
MEDIAN! Most students scored in 50-80 range.
The high scorers (95-100) pulled the mean up.

Report both: "Median score 67, with range 45-100"
Much better than: "Average score 72"
```

---

## Mistake 4: Cherry-Picking Data

### The Problem

```
You test 20 samples:
10 pass, 10 fail (50% yield)

But in your report, you only show the 10 that pass.
"All samples passed!"

This is LYING.
```

### Why It's Wrong

You're misrepresenting the truth. This can lead to:
- Shipping bad products
- Harming customers
- Legal liability
- Loss of trust
- Your own reputation destroyed

### What to Do Instead

**Report the TRUTH, even if it's bad:**

```
✓ Include all data (good and bad)
✓ Be honest about failures
✓ Say what went wrong
✓ Explain the investigation
✓ Show what you'll do to fix it

✗ Don't hide failures
✗ Don't exclude data you don't like
✗ Don't manipulate to look good
```

**Real consequence:**

```
A company knew their product sometimes failed.
Instead of fixing it, they hid the failures in reports.
When products failed in the field, people got hurt.
The company faced: lawsuits, fines, prison time.
Reputation destroyed forever.

All because they didn't report test failures honestly.
```

---

## Mistake 5: No Documentation

### The Problem

```
You do tests on Monday.
Friday someone asks: "Why did Tuesday's batch fail?"
You can't remember. No notes.

Or: It's 3 months later. What was the temperature
during testing? You don't know.
```

### Why It's Wrong

**Without documentation:**
- Can't explain why something happened
- Can't reproduce the test later
- Can't spot patterns
- Can't prove you did it correctly
- Legal issues if something goes wrong

### What to Do Instead

**Document EVERYTHING:**

```
What to record:
✓ Date and time
✓ Who did the test
✓ What equipment was used
✓ All measurements
✓ Any unusual observations
✓ Environmental conditions (temp, humidity, time of day)
✓ Procedure followed exactly as written
✓ Any deviations from procedure
✓ Equipment calibration status
✓ Lot/batch numbers of materials

Where to record:
✓ Lab notebook (physical, dated, signed)
✓ Or digital spreadsheet with timestamps
✓ Or both (belt and suspenders)
```

**Real example of good documentation:**

```
Date: May 27, 2026
Time: 08:00-11:45
Technician: Sarah Chen
Equipment: pH meter #5 (last calibrated May 26)
Location: Building 3, Lab A
Room temp: 21.8-22.2°C
Humidity: 45-50%

Sample #1:
  Time: 08:00
  pH: 7.2
  Notes: Clear, normal appearance

Sample #2:
  Time: 08:15
  pH: 7.1
  Notes: Clear, normal appearance

...

Equipment status: Working normally throughout
Procedure: Followed SOP-pH-001 exactly
No deviations noted
Data checked: All values reasonable, no obvious errors
```

---

## Mistake 6: Not Checking Data Quality First

### The Problem

```
You collect 100 measurements.
You immediately calculate statistics.
You don't notice:
- One measurement is 0.5 (measurement error, dropped on floor?)
- Three measurements are identical 2.00 (not possible)
- Time of day varies wildly (changed conditions?)

Your statistics are wrong.
```

### Why It's Wrong

**Bad data in = Bad statistics out**

It's called GIGO (Garbage In, Garbage Out).

### What to Do Instead

**Before analyzing, check:**

```
✓ Do you have all measurements?
✓ Are values in reasonable range?
✓ Are there obvious typos?
✓ Are there suspicious patterns?
✓ Did conditions vary?
✓ Any outliers? (if yes, investigate)
✓ Data collection method consistent?
```

**Real example:**

```
Testing battery lifespan:
You get: 8, 8, 8, 8, 8, 9, 9, 9, 9, 50

STOP! Something is wrong:
- Why are five exactly 8?
- Why is one 50 (much higher)?

Investigate:
- First five: Probably were rounded to nearest hour
- One 50: Maybe data entry error (0.5 typed as 50)?
- Or maybe one test ran for 50 hours and others were cut short

Fix before analyzing!
```

---

## Mistake 7: Small Sample Size

### The Problem

```
You test 3 samples: All pass
Conclusion: "100% yield!"

You test 1000 samples: 50 fail
Actual yield: 95%
```

**Why is there a difference?**
Small samples are lucky/unlucky.

### Why It's Wrong

With only 3 samples, you have no idea if they're representative.

```
By chance alone, you might pick:
- The three best samples
- The three worst samples
- Or get an unrepresentative mix
```

### What to Do Instead

**Use larger sample sizes:**

```
Sample Size | Confidence | Use For
-----------|-----------|---------
3-5        | Low       | Quick check only
10-20      | Medium    | Lab experiments
50-100     | High      | Quality control
1000+      | Very high | Manufacturing
```

**Real rule of thumb:**

```
"At least 10 samples per group being compared"

Bad: Test 3 new units, 3 old units. Compare.
Good: Test 30 new units, 30 old units. Compare.

Bad: One-day sample
Good: One-week sample

Bad: One batch of material
Good: Multiple batches
```

---

## Mistake 8: Changing the Procedure

### The Problem

```
Procedure says: Use glass thermometer
Day 1: Use glass thermometer ✓
Day 2: Glass one is broken, use digital ✗
Day 3: Back to glass ✓
Day 4: Try laser thermometer for fun ✗

Now your measurements aren't comparable!
Different methods give different results.
```

### Why It's Wrong

If you change how you measure, you don't know if variation is from:
- The process (real problem)
- Or your measurement method (fake variation)

### What to Do Instead

**Standardize and stick with it:**

```
✓ Write a procedure
✓ Use the same equipment (or identical equipment)
✓ Same person (if possible, or train others identically)
✓ Same location, conditions
✓ Don't change mid-test
✓ If you must change, document it clearly
```

**Real example:**

```
Testing water pH:
- Equipment A (calibrated): reads 7.2
- Equipment B (not calibrated): reads 7.4
- Equipment C (broken): reads 8.1

Your data looks terrible! High variation!
But it's not the water—it's your equipment.

Solution: Use Equipment A only, keep it calibrated
```

---

## Mistake 9: Ignoring Outliers

### The Problem

```
Test results: 2.0, 2.1, 2.0, 2.2, 100

"That 100 is clearly wrong. I'll delete it."

Final data: 2.0, 2.1, 2.0, 2.2

But what if the 100 was REAL?
What if something really went wrong?
```

### Why It's Wrong

**Two extremes:**

```
Extreme 1: Delete outliers too easily
- Hides real problems
- Your analysis is false
- You miss important issues

Extreme 2: Never delete outliers
- One measurement error ruins everything
- Mean is distorted
- Statistics are wrong
```

### What to Do Instead

**Investigate, don't delete:**

```
When you see an outlier:

1. Don't automatically delete it
2. Investigate: "Why is it different?"
3. Check: Was it a measurement error?
4. Look: Was something different about that sample?
5. Decide: Is it real or a mistake?
6. Document: Either way, record why
7. Calculate: Statistics with AND without it

If it's a measurement error: Remove it, explain why
If it's real: Keep it, but note it
```

**Real example:**

```
Testing semiconductor lifespan:
Results: 1000 hrs, 1100 hrs, 900 hrs, 50 hrs

That 50 is way low!

Investigate:
- "Was equipment working?" Equipment was fine
- "Was testing wrong?" Test procedure was correct
- "Was sample different?" Yes! That sample had defect

Conclusion: The 50 is REAL. That sample failed early.
This is important! It shows a potential defect mode.

Don't delete it. Report it. Investigate why it failed.
```

---

## Mistake 10: Not Communicating Results

### The Problem

```
You do great analysis.
You find important results.
But you don't tell anyone.
Nobody knows.
Nothing changes.
```

### Why It's Wrong

Analysis only matters if people USE the results.

### What to Do Instead

**Communicate clearly:**

```
✓ Write a report (or email)
✓ Include key findings (not every detail)
✓ Make charts (pictures are worth 1000 words)
✓ State your conclusion clearly
✓ Recommend action
✓ Be honest (good news or bad)
✓ Use simple language (not jargon)
```

**Bad report:**

```
"Cpk = 1.23, std dev = 0.08, mean = 50.2, 
P95 = 50.3, process capability in acceptable range..."
```

**Good report:**

```
"GOOD NEWS: Our process is working well.
- 100% of products pass specification
- Process is stable over time
- Safe margin to limits
RECOMMENDATION: Continue current procedure"
```

---

## Quick Checklist: Before You Conclude Anything

```
□ Do I have enough data? (At least 10 measurements)
□ Is the data quality good? (No obvious errors)
□ Did I use consistent methods? (Same procedure, equipment)
□ Did I collect data fairly? (Representative sample)
□ Am I using the right statistics? (Mean vs median)
□ Am I ignoring trends? (Looking over time?)
□ Did I investigate outliers? (Instead of deleting?)
□ Did I document everything? (Can someone repeat this?)
□ Is my conclusion supported by data? (Or am I guessing?)
□ Will I communicate findings? (To people who need to know)
```

If you can answer YES to all of these, you're doing good analysis.

---

## Real Consequence: A Bad Analysis Destroyed a Company

**Story (simplified):**

```
A food company tested their product.
They found some batches had contamination.
Instead of reporting it, they:
✗ Hid the test results
✗ Didn't retrain workers
✗ Shipped the contaminated product anyway

Customers got sick.
People died.

Investigation revealed: They knew about the problem!
Result:
- Product recalled
- Criminal charges
- Lawsuits (millions)
- Company shut down
- Executives went to prison
- Thousands lost jobs

All because they didn't honestly report test results.
```

**Lesson:** Report your analysis honestly, even if it's bad news.

---

## Summary: The Top 10 Mistakes

1. **Trusting one measurement** → Collect multiple samples
2. **Ignoring trends** → Plot over time, watch for drift
3. **Using wrong statistics** → Know when to use mean vs median
4. **Cherry-picking data** → Report all results, good and bad
5. **No documentation** → Write everything down
6. **Bad data quality** → Check before analyzing
7. **Small sample size** → Collect at least 10
8. **Changing procedure** → Standardize and stick with it
9. **Deleting outliers** → Investigate before deleting
10. **Not communicating** → Tell people what you found

---

## Final Wisdom

**Analysis is only as good as your integrity.**

Equipment and math can lie. You can make mistakes.
But if you're honest, transparent, and thorough,
your analysis will be trusted and valuable.

---

## Next Steps

You've learned:
1. What test data is (Part 2)
2. Basic statistics (Part 3)
3. Control charts (Part 4)
4. Specifications (Part 5)
5. Visualization (Part 6)
6. Practical workflow (Part 7)
7. Common mistakes (Part 8)

**Now go apply this to YOUR work.**

Start with one experiment. Collect data carefully.
Analyze it thoroughly. Report it honestly.

You'll be amazed how much you can understand
from data if you analyze it right.

---

**Last updated:** May 2026
**Difficulty level:** High School
**Time to read:** 20-25 minutes
**Prerequisite:** Parts 1-7
**Most important:** Read and remember this part!
