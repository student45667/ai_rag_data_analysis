# Wafer Sort: Statistical Tools, Setups & Data Analysis Overview

## 1. Core Statistical Concepts & Tools

### Descriptive Statistics
- **Mean, Median, Std Dev**: Baseline metrics for test parameter distributions
- **Percentiles (P10, P50, P90, P99)**: Identify tails of population; compare against spec limits
- **Histogram Analysis**: Visualize test parameter distributions; detect bimodal/skewed populations
- **Box Plots**: Quickly assess spread, outliers, and shifts across wafers/lots

### Process Capability Analysis
- **Cpk/Ppk**: Measure how well test data fits within spec limits (goal: Cpk > 1.33)
- **Yield Analysis**: Pass/fail rates by wafer position, lot, reticle, design block
- **Binning Analysis**: Categorize devices into functional/speed bins; track yield per bin
- **Fallout Analysis**: Identify failing tests and rank by frequency/impact

### Statistical Testing
- **T-tests / ANOVA**: Compare means across wafers, lots, process conditions
- **Chi-square**: Test for independence (e.g., does die position affect yield?)
- **Trend Analysis**: Detect systematic shifts (voltage drift, temperature effects)
- **Control Charts (X-bar, moving range)**: Monitor process stability; detect out-of-control conditions

---

## 2. Data Collection & Ingestion

### Test Equipment Setup
- **ATE (Automatic Test Equipment)**: Generates raw test data per device
  - **Handler**: Loads/unloads die; manages parallelism
  - **Probe Card**: Makes electrical contact to die pads
  - **Tester Channels**: Apply stimulus, measure response (current, voltage, timing, etc.)
- **Data Logging**: Test results → STDF (Standard Test Data Format) files
- **Parametric vs. Functional Tests**: Leakage, supply current, timing specs, functional patterns

### Data Pipeline
1. **Raw STDF Export**: Per-wafer test logs
2. **Parsing & Extraction**: Convert STDF → structured tables (pandas, SQL)
3. **Cleaning**: Remove duplicates, flag incomplete tests, handle missing data
4. **Feature Engineering**: Derived metrics (speed bin, power rank, thermal gradient)

---

## 3. Visualization & Graphical Methods

### Standard Plots
- **Wafer Maps**: Color-coded die positions; highlight pass/fail, bin assignment, or parametric value
  - Reveals spatial patterns (edge effects, reticle artifacts, thermal gradients)
- **Test Distribution Histograms**: Parameter vs. frequency; overlay spec limits and process mean
- **Scatter Plots**: Parameter A vs. Parameter B (e.g., leakage vs. frequency); detect correlation
- **Time Series / Trend Plots**: Parameter drift over lot sequence or wafer position

### Advanced Visualization
- **Heatmaps**: Multi-parameter correlation matrix (Pearson, Spearman)
- **Violin/Ridge Plots**: Overlaid distributions across wafers/lots/conditions
- **3D Surface Plots**: Die position (X, Y) vs. parametric value (Z); visualize spatial effects
- **Control Limit Overlays**: Historical limits, specification limits, control limits on same plot

### Statistical Plots
- **Q-Q Plots**: Test for normality; assess tail behavior
- **Probability Plots**: Weibull, lognormal fits for reliability analysis
- **Pareto Charts**: Rank failing tests by frequency (80/20 rule)

---

## 4. Key Data Analysis Workflows

### Yield & Quality Analysis
- **Yield by Wafer/Lot**: Track pass rates; identify outliers
- **Yield by Die Position**: Detect edge loss, reticle misalignment, thermal gradients
- **Bin Yield Tracking**: Monitor shifts in speed/power distribution over time
- **First-Pass Yield (FPY)**: Devices that pass on first test (no retest)

### Parametric Analysis
- **Distribution Fitting**: Fit histograms to normal, Weibull, or lognormal; estimate tail probabilities
- **Shift & Drift Detection**: Compare early vs. late wafers in lot; detect process trend
- **Corner/Temperature Dependency**: Analyze data by applied voltage/temperature during test
- **Correlation Studies**: Leakage vs. delay, power vs. speed (design trade-offs)

### Test Effectiveness & Diagnostics
- **Test Coverage**: Which tests are most discriminating? (high fail rate, wide distribution)
- **Redundancy Analysis**: Tests with identical results; potential candidates for elimination
- **Escape Rate Estimation**: False-pass risk; compare incoming vs. final test results
- **Debug Correlation**: Link failing parametric tests to functional fails

### Comparative Analysis
- **Lot-to-Lot**: Identify process drifts between manufacturing runs
- **Wafer-to-Wafer**: Intra-lot variation; thermal, spatial patterns
- **Reticle-to-Reticle**: Multi-patterning effects; lithography uniformity
- **Design Block Comparison**: Different IP blocks on same wafer; identify susceptibilities

---

## 5. Statistical Tools & Platforms

### Standard Platforms
- **Spreadsheet Tools** (Excel, LibreOffice): Quick histograms, basic stats; limited for large datasets
- **Statistical Software** (R, JMP, Minitab, SPSS): Full capability; Cpk, control charts, DOE
- **Python Stack** (pandas, numpy, scipy, matplotlib, seaborn): Flexible, scriptable; RAG-friendly for semiconductor analysis
- **SQL Databases** (PostgreSQL, SQLite): Store/query large STDF datasets; enable filtering & aggregation

### Semiconductor-Specific Tools
- **Yield Analysis Software** (Xcur, Dft, Yield Sentinel, others): Purpose-built for wafer test data
- **EDA Tools** (Cadence, Synopsys): Simulation correlation; predict test fail mechanisms
- **Custom Scripts**: Internal ETL; wafer map generation; process trend dashboards

---

## 6. Common Statistical Metrics & KPIs

| Metric | Definition | Use Case |
|--------|-----------|----------|
| **Cpk** | Process capability index | Assess spec centering & spread |
| **Yield (%)** | Passing devices / Total devices | Overall health; lot acceptance |
| **Bin Yield (%)** | Devices in each speed/power bin | Market grading; revenue impact |
| **Escapes (ppm)** | False passes reaching customer | Quality risk; test tightness |
| **FPY (%)** | First-pass yield (no retest) | Production efficiency |
| **Fallout (%)** | Devices failing any test | Identify limiting tests |
| **Wafer Edge Loss (%)** | Dies lost due to edge effect | Process/design quality |
| **Thermal Gradient (°C)** | Temperature variation across wafer | Probe card, chuck, chuck temp control |
| **Retest Rate (%)** | Devices requiring second pass | Handler, tester, or test stability |

---

## 7. Example Analysis Workflow

1. **Ingest STDF** → Parse all test records for wafer set
2. **Generate Descriptive Stats** → Mean, Cpk, fallout rate per test
3. **Visualize Distributions** → Histograms with spec limits overlaid
4. **Wafer Map Analysis** → Spatial patterns (edge loss, gradient, defects)
5. **Compare Across Lots** → Trend plots; identify process shift
6. **Identify Root Cause** → Correlation analysis, design block analysis, retest data
7. **Document Findings** → Summary report with actionable recommendations

---

## 8. Expansion Opportunities

- **Machine Learning**: Anomaly detection (outlier wafers); predictive models (escape rate)
- **Design of Experiments (DOE)**: Optimize test conditions (temperature, voltage, timing)
- **Reliability Modeling**: Weibull analysis, failure rate estimation from tail data
- **Test Program Optimization**: Identify redundant tests; tighten limits on key discriminators
- **Integration with CAD/Simulation**: Correlate measured data with simulation predictions
- **Real-time Dashboards**: Live yield monitoring; automated alerts for out-of-spec conditions

---

## Notes for Your Use Case

- **STDF as data source**: You already have structured test records; focus on efficient parsing & feature extraction
- **Offline/Local deployment**: Python stack (pandas, scipy, matplotlib) works well on `ai.local`
- **RAG integration**: Embedding test pattern specs, ATE docs, and historical analysis → wafer data analysis agent
- **Consulting value**: Clients often lack bandwidth for in-depth statistical analysis; offer Cpk reports, root cause analysis, trend dashboards

