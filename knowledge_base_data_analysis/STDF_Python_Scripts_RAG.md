# STDF Python Analysis & Visualization Scripts
## RAG Reference — Parsing, Analysis, and Presentation Tools

---

## 1. PYTHON LIBRARY ECOSYSTEM FOR STDF

### Available Libraries (Install via pip)

| Library | pip install | Purpose |
|---------|-------------|---------|
| **pystdf** | `pip install pystdf` | Event-based STDF V4 parser (most common, GPL) |
| **Semi-ATE-STDF** | `pip install Semi-ATE-STDF` | Modern read/write API, field-level access |
| **pystdf4** | `pip install pystdf4` | Modern STDF4 reader/writer (MIT license) |
| **pandas** | `pip install pandas` | DataFrames for tabular analysis |
| **numpy** | `pip install numpy` | Numerical operations, array math |
| **scipy** | `pip install scipy` | Statistics: linregress, pearsonr, normaltest |
| **matplotlib** | `pip install matplotlib` | Core plotting library |
| **seaborn** | `pip install seaborn` | Statistical plots (histograms, boxplots, heatmaps) |
| **plotly** | `pip install plotly` | Interactive charts (HTML output) |
| **wfmap** | `pip install wfmap` | Wafer heatmap + defect pareto (matplotlib-based) |

### Which Parser to Use

**pystdf** — battle-tested, widely used in industry, event-driven model. Best for streaming large files.
**Semi-ATE-STDF** — cleaner API, supports both read and write, good for smaller files and scripting.
**Raw struct** — no dependencies, full control, best for embedded/offline deployment.

---

## 2. SCRIPT 1 — UNIVERSAL STDF PARSER (struct-based, no dependencies)

This parser reads STDF without any third-party library. Works offline.

```python
"""
stdf_parser.py — Zero-dependency STDF V4 parser using Python struct
Reads PTR, PRR, WIR, WRR records and returns a pandas DataFrame
"""

import struct
import pandas as pd
from pathlib import Path


def read_cn(data, offset):
    """Read a Cn (variable-length string) field. Returns (string, new_offset)."""
    length = data[offset]
    offset += 1
    if length == 0:
        return '', offset
    s = data[offset:offset + length].decode('ascii', errors='replace')
    return s, offset + length


def read_u1(data, offset): return data[offset], offset + 1
def read_u2(data, offset): return struct.unpack_from('<H', data, offset)[0], offset + 2
def read_u4(data, offset): return struct.unpack_from('<I', data, offset)[0], offset + 4
def read_i2(data, offset): return struct.unpack_from('<h', data, offset)[0], offset + 2
def read_r4(data, offset): return struct.unpack_from('<f', data, offset)[0], offset + 4
def read_b1(data, offset): return data[offset], offset + 1


def parse_stdf(filepath, test_filter=None):
    """
    Parse STDF file and return a dict of DataFrames.

    Parameters:
        filepath    : str or Path to .stdf file
        test_filter : set of test numbers to keep (None = keep all)

    Returns dict with keys:
        'ptr'  : DataFrame of parametric test results
        'prr'  : DataFrame of part results (die pass/fail, X, Y, bins)
        'wir'  : DataFrame of wafer info
        'wrr'  : DataFrame of wafer results
        'mir'  : dict of lot-level info
    """
    ptr_records = []
    prr_records = []
    wir_records = []
    wrr_records = []
    mir_info    = {}

    # Track context state
    current_wafer_id = None
    current_head     = None
    current_site     = None

    # Cache first PTR definition per test_num (limits, name, units)
    ptr_defs = {}

    with open(filepath, 'rb') as f:
        raw = f.read()

    pos = 0
    total = len(raw)

    while pos < total - 4:
        # Read 4-byte record header
        try:
            rec_len = struct.unpack_from('<H', raw, pos)[0]
            rec_typ = raw[pos + 2]
            rec_sub = raw[pos + 3]
        except struct.error:
            break

        rec_data = raw[pos + 4: pos + 4 + rec_len]
        pos += 4 + rec_len

        # ── FAR (0/10) ──────────────────────────────────────────────
        if rec_typ == 0 and rec_sub == 10:
            pass  # just validates byte order

        # ── MIR (1/10) ──────────────────────────────────────────────
        elif rec_typ == 1 and rec_sub == 10:
            try:
                o = 8  # skip timestamps and stat fields
                lot_id, o  = read_cn(rec_data, o)
                part_typ, o = read_cn(rec_data, o)
                node_nam, o = read_cn(rec_data, o)
                tstr_typ, o = read_cn(rec_data, o)
                job_nam, o  = read_cn(rec_data, o)
                mir_info = {
                    'lot_id': lot_id,
                    'part_typ': part_typ,
                    'node_nam': node_nam,
                    'tstr_typ': tstr_typ,
                    'job_nam': job_nam,
                }
            except Exception:
                pass

        # ── WIR (2/10) — wafer open ──────────────────────────────────
        elif rec_typ == 2 and rec_sub == 10:
            try:
                o = 0
                head, o      = read_u1(rec_data, o)
                site_grp, o  = read_u1(rec_data, o)
                start_t, o   = read_u4(rec_data, o)
                wafer_id, o  = read_cn(rec_data, o)
                current_wafer_id = wafer_id
                wir_records.append({
                    'head': head,
                    'site_grp': site_grp,
                    'start_t': start_t,
                    'wafer_id': wafer_id,
                })
            except Exception:
                pass

        # ── WRR (2/20) — wafer close ─────────────────────────────────
        elif rec_typ == 2 and rec_sub == 20:
            try:
                o = 0
                head, o      = read_u1(rec_data, o)
                site_grp, o  = read_u1(rec_data, o)
                finish_t, o  = read_u4(rec_data, o)
                part_cnt, o  = read_u4(rec_data, o)
                rtst_cnt, o  = read_u4(rec_data, o)
                abrt_cnt, o  = read_u4(rec_data, o)
                good_cnt, o  = read_u4(rec_data, o)
                func_cnt, o  = read_u4(rec_data, o)
                wafer_id, o  = read_cn(rec_data, o)
                yield_pct = (good_cnt / part_cnt * 100) if part_cnt > 0 else 0
                wrr_records.append({
                    'wafer_id': wafer_id,
                    'part_cnt': part_cnt,
                    'good_cnt': good_cnt,
                    'abrt_cnt': abrt_cnt,
                    'rtst_cnt': rtst_cnt,
                    'yield_pct': round(yield_pct, 2),
                })
            except Exception:
                pass

        # ── PTR (15/10) — parametric test result ─────────────────────
        elif rec_typ == 15 and rec_sub == 10:
            try:
                o = 0
                test_num, o = read_u4(rec_data, o)

                # Apply test filter
                if test_filter and test_num not in test_filter:
                    continue

                head, o     = read_u1(rec_data, o)
                site, o     = read_u1(rec_data, o)
                test_flg, o = read_b1(rec_data, o)
                parm_flg, o = read_b1(rec_data, o)
                result, o   = read_r4(rec_data, o)
                test_txt, o = read_cn(rec_data, o)
                alarm_id, o = read_cn(rec_data, o)

                passed = not bool(test_flg & 0b01000000)  # bit6 = fail flag

                # Read optional fields if present
                lo_limit = hi_limit = None
                units    = ''
                if o < len(rec_data):
                    opt_flag, o = read_b1(rec_data, o)
                    res_scal, o = read_b1(rec_data, o)
                    llm_scal, o = read_b1(rec_data, o)
                    hlm_scal, o = read_b1(rec_data, o)
                    lo_limit, o = read_r4(rec_data, o)
                    hi_limit, o = read_r4(rec_data, o)
                    if o < len(rec_data):
                        units, o = read_cn(rec_data, o)

                # Cache first definition for this test
                if test_num not in ptr_defs:
                    ptr_defs[test_num] = {
                        'test_name': test_txt,
                        'lo_limit':  lo_limit,
                        'hi_limit':  hi_limit,
                        'units':     units,
                    }
                else:
                    # Fill from cache if not present in this record
                    if not test_txt:
                        test_txt = ptr_defs[test_num]['test_name']
                    if lo_limit is None:
                        lo_limit = ptr_defs[test_num]['lo_limit']
                    if hi_limit is None:
                        hi_limit = ptr_defs[test_num]['hi_limit']
                    if not units:
                        units = ptr_defs[test_num]['units']

                ptr_records.append({
                    'wafer_id':  current_wafer_id,
                    'test_num':  test_num,
                    'test_name': test_txt,
                    'head':      head,
                    'site':      site,
                    'result':    result,
                    'lo_limit':  lo_limit,
                    'hi_limit':  hi_limit,
                    'units':     units,
                    'passed':    passed,
                    'test_flg':  test_flg,
                })
            except Exception:
                pass

        # ── PRR (5/20) — part result record ──────────────────────────
        elif rec_typ == 5 and rec_sub == 20:
            try:
                o = 0
                head, o      = read_u1(rec_data, o)
                site, o      = read_u1(rec_data, o)
                part_flg, o  = read_b1(rec_data, o)
                num_test, o  = read_u2(rec_data, o)
                hard_bin, o  = read_u2(rec_data, o)
                soft_bin, o  = read_u2(rec_data, o)
                x_coord, o   = read_i2(rec_data, o)
                y_coord, o   = read_i2(rec_data, o)
                test_t, o    = read_u4(rec_data, o)
                part_id, o   = read_cn(rec_data, o)

                die_passed = not bool(part_flg & 0b00001000)  # bit3 = fail

                prr_records.append({
                    'wafer_id':  current_wafer_id,
                    'head':      head,
                    'site':      site,
                    'x_coord':   x_coord,
                    'y_coord':   y_coord,
                    'hard_bin':  hard_bin,
                    'soft_bin':  soft_bin,
                    'num_test':  num_test,
                    'test_t_ms': test_t,
                    'passed':    die_passed,
                    'part_id':   part_id,
                })
            except Exception:
                pass

    return {
        'ptr': pd.DataFrame(ptr_records),
        'prr': pd.DataFrame(prr_records),
        'wir': pd.DataFrame(wir_records),
        'wrr': pd.DataFrame(wrr_records),
        'mir': mir_info,
    }


# ── USAGE ────────────────────────────────────────────────────────────
if __name__ == '__main__':
    data = parse_stdf('wafer.stdf', test_filter={1000, 1010, 2000})
    print("MIR:", data['mir'])
    print("Wafer yields:\n", data['wrr'][['wafer_id', 'part_cnt', 'good_cnt', 'yield_pct']])
    print("PTR sample:\n", data['ptr'].head())
```

---

## 3. SCRIPT 2 — pystdf EVENT-DRIVEN PARSER WITH DATAFRAME SINK

pystdf uses an event/sink pattern. Create a Sink class that catches record events and accumulates data.

```python
"""
stdf_pystdf_sink.py — pystdf-based parser using DataFrameSink pattern
Install: pip install pystdf pandas
"""

import pystdf.V4 as stdf
from pystdf.Pipeline import DataSource
import pandas as pd


class STDFDataSink:
    """
    Accumulates PTR, PRR, WIR, WRR data into lists during parse.
    Attach to pystdf Parser as a sink (receiver of record events).
    """
    def __init__(self, test_filter=None):
        self.test_filter     = test_filter  # set of test_num ints or None
        self.ptr_rows        = []
        self.prr_rows        = []
        self.wir_rows        = []
        self.wrr_rows        = []
        self._current_wafer  = None
        self._ptr_defs       = {}

    def before_send(self, data_source, record_type):
        pass

    def after_send(self, data_source, rec):
        name = rec.__class__.__name__

        if name == 'Wir':
            self._current_wafer = rec.fields[3][1]  # WAFER_ID
            self.wir_rows.append({
                'wafer_id': self._current_wafer,
                'start_t':  rec.fields[2][1],
            })

        elif name == 'Wrr':
            part_cnt = rec.fields[3][1] or 0
            good_cnt = rec.fields[6][1] or 0
            self.wrr_rows.append({
                'wafer_id': rec.fields[8][1],
                'part_cnt': part_cnt,
                'good_cnt': good_cnt,
                'yield_pct': round((good_cnt / part_cnt * 100) if part_cnt else 0, 2),
            })

        elif name == 'Ptr':
            test_num = rec.fields[0][1]
            if self.test_filter and test_num not in self.test_filter:
                return
            test_flg = rec.fields[3][1] or 0
            passed   = not bool(test_flg & 0b01000000)
            test_txt = rec.fields[6][1] or ''
            result   = rec.fields[5][1]
            lo_limit = rec.fields[13][1]
            hi_limit = rec.fields[14][1]
            units    = rec.fields[15][1] or ''

            if test_num not in self._ptr_defs:
                self._ptr_defs[test_num] = (test_txt, lo_limit, hi_limit, units)
            else:
                cached = self._ptr_defs[test_num]
                if not test_txt: test_txt = cached[0]
                if lo_limit is None: lo_limit = cached[1]
                if hi_limit is None: hi_limit = cached[2]
                if not units: units = cached[3]

            self.ptr_rows.append({
                'wafer_id':  self._current_wafer,
                'test_num':  test_num,
                'test_name': test_txt,
                'site':      rec.fields[2][1],
                'result':    result,
                'lo_limit':  lo_limit,
                'hi_limit':  hi_limit,
                'units':     units,
                'passed':    passed,
            })

        elif name == 'Prr':
            part_flg = rec.fields[2][1] or 0
            self.prr_rows.append({
                'wafer_id': self._current_wafer,
                'site':     rec.fields[1][1],
                'x_coord':  rec.fields[6][1],
                'y_coord':  rec.fields[7][1],
                'hard_bin': rec.fields[4][1],
                'soft_bin': rec.fields[5][1],
                'passed':   not bool(part_flg & 0b00001000),
            })

    def to_dataframes(self):
        return {
            'ptr': pd.DataFrame(self.ptr_rows),
            'prr': pd.DataFrame(self.prr_rows),
            'wir': pd.DataFrame(self.wir_rows),
            'wrr': pd.DataFrame(self.wrr_rows),
        }


def parse_with_pystdf(filepath, test_filter=None):
    sink   = STDFDataSink(test_filter=test_filter)
    parser = stdf.Parser()
    parser.addSink(sink)
    with open(filepath, 'rb') as f:
        parser.parse(f)
    return sink.to_dataframes()


# ── USAGE ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    dfs = parse_with_pystdf('wafer.stdf', test_filter={1000, 1010})
    print(dfs['ptr'].describe())
    print(dfs['wrr'])
```

---

## 4. SCRIPT 3 — STATISTICAL ANALYSIS (Cpk, Yield, Trends, Correlation)

```python
"""
stdf_analysis.py — Statistical analysis of parsed STDF data
Requires: pandas, numpy, scipy
Input: DataFrames from parse_stdf() or parse_with_pystdf()
"""

import numpy as np
import pandas as pd
from scipy import stats


# ── 4.1 CPK CALCULATION ───────────────────────────────────────────

def cpk(values, lo_limit, hi_limit):
    """
    Process capability index — how well distribution fits between limits.
    Cpk < 1.0  : process failing or at risk
    Cpk 1.0–1.33 : marginal
    Cpk >= 1.33 : capable
    Cpk >= 1.67 : highly capable
    """
    arr  = np.array(values, dtype=float)
    arr  = arr[~np.isnan(arr)]
    if len(arr) < 2:
        return np.nan
    mean = np.mean(arr)
    std  = np.std(arr, ddof=1)
    if std == 0:
        return np.inf
    cpu = (hi_limit - mean) / (3 * std)
    cpl = (mean - lo_limit) / (3 * std)
    return min(cpu, cpl)


def analyze_all_tests(ptr_df):
    """
    Compute per-test statistics: mean, std, min, max, Cpk, yield.

    Returns a summary DataFrame sorted by Cpk (worst first).
    """
    results = []
    for test_num, grp in ptr_df.groupby('test_num'):
        vals     = grp['result'].dropna()
        lo       = grp['lo_limit'].iloc[0]
        hi       = grp['hi_limit'].iloc[0]
        test_name = grp['test_name'].iloc[0]
        units    = grp['units'].iloc[0]

        cp = cpk(vals, lo, hi) if (lo is not None and hi is not None) else np.nan
        results.append({
            'test_num':  test_num,
            'test_name': test_name,
            'units':     units,
            'n':         len(vals),
            'mean':      round(vals.mean(), 4),
            'std':       round(vals.std(ddof=1), 4),
            'min':       round(vals.min(), 4),
            'max':       round(vals.max(), 4),
            'lo_limit':  lo,
            'hi_limit':  hi,
            'cpk':       round(cp, 3) if not np.isnan(cp) else np.nan,
            'pass_rate': round(grp['passed'].mean() * 100, 2),
        })

    df = pd.DataFrame(results).sort_values('cpk')  # worst Cpk first
    return df


# ── 4.2 YIELD TREND ACROSS WAFERS ────────────────────────────────

def yield_trend(wrr_df):
    """
    Detect linear yield trend across wafers in a lot.
    Returns slope (yield%/wafer) and p-value.
    p < 0.05 means statistically significant trend.
    """
    wafers = wrr_df.reset_index(drop=True)
    if len(wafers) < 3:
        return {'slope': None, 'p_value': None, 'message': 'Too few wafers'}

    x = np.arange(len(wafers))
    y = wafers['yield_pct'].values

    slope, intercept, r, p, se = stats.linregress(x, y)

    direction = 'INCREASING' if slope > 0 else 'DECREASING'
    significant = p < 0.05

    return {
        'slope':       round(slope, 4),
        'r_squared':   round(r ** 2, 4),
        'p_value':     round(p, 5),
        'significant': significant,
        'direction':   direction,
        'message':     f'Yield {direction} by {abs(slope):.2f}%/wafer (p={p:.4f})'
                       if significant else 'No significant yield trend',
    }


# ── 4.3 PARAMETRIC TREND ACROSS WAFERS (per test) ─────────────────

def parametric_trend(ptr_df, test_num):
    """
    For a specific test, compute mean per wafer and check for drift.
    Returns slope, p-value, and wafer means.
    """
    grp = ptr_df[ptr_df['test_num'] == test_num].copy()
    wafer_means = grp.groupby('wafer_id')['result'].mean()

    if len(wafer_means) < 3:
        return {'message': 'Too few wafers for trend analysis'}

    x = np.arange(len(wafer_means))
    slope, intercept, r, p, se = stats.linregress(x, wafer_means.values)

    lo_limit = grp['lo_limit'].iloc[0]
    hi_limit = grp['hi_limit'].iloc[0]
    test_name = grp['test_name'].iloc[0]
    units    = grp['units'].iloc[0]

    return {
        'test_num':    test_num,
        'test_name':   test_name,
        'units':       units,
        'wafer_means': wafer_means.to_dict(),
        'slope':       round(slope, 6),
        'r_squared':   round(r ** 2, 4),
        'p_value':     round(p, 5),
        'significant': p < 0.05,
        'lo_limit':    lo_limit,
        'hi_limit':    hi_limit,
        'message':     (f'TEST {test_num} ({test_name}): Drift {slope:+.4f} '
                        f'{units}/wafer — {"SIGNIFICANT" if p < 0.05 else "not significant"}'),
    }


# ── 4.4 CROSS-TEST CORRELATION ────────────────────────────────────

def test_correlation_matrix(ptr_df, test_nums=None):
    """
    Compute Pearson correlation between all selected tests.
    Returns correlation DataFrame (tests × tests).
    """
    if test_nums:
        sub = ptr_df[ptr_df['test_num'].isin(test_nums)]
    else:
        sub = ptr_df.copy()

    # Pivot: one row per die-site, one column per test
    pivot = sub.pivot_table(
        index=['wafer_id', 'site'],
        columns='test_num',
        values='result',
        aggfunc='first'
    )

    corr = pivot.corr(method='pearson')

    # Rename columns to test names if available
    name_map = (
        sub.drop_duplicates('test_num')
           .set_index('test_num')['test_name']
           .to_dict()
    )
    corr.columns = [f"{n} ({name_map.get(n, '')})" for n in corr.columns]
    corr.index   = corr.columns

    return corr


# ── 4.5 SITE-TO-SITE UNIFORMITY ───────────────────────────────────

def site_uniformity(ptr_df, test_num):
    """
    Compare mean and std across test sites for a specific test.
    Large variation between sites indicates probe card or handler issue.
    """
    grp = ptr_df[ptr_df['test_num'] == test_num]
    site_stats = grp.groupby('site')['result'].agg(['mean', 'std', 'count'])
    site_stats.columns = ['mean', 'std', 'count']
    site_range  = site_stats['mean'].max() - site_stats['mean'].min()
    overall_std = grp['result'].std(ddof=1)
    between_pct = (site_range / overall_std * 100) if overall_std > 0 else 0
    return {
        'test_num':    test_num,
        'site_stats':  site_stats,
        'site_range':  round(site_range, 6),
        'between_pct': round(between_pct, 1),
        'flag':        between_pct > 30,  # >30% between-site variation is concerning
    }


# ── 4.6 OUTLIER DETECTION (Z-SCORE AND GRUBBS) ───────────────────

def detect_outliers(ptr_df, test_num, z_threshold=3.0):
    """
    Detect statistical outliers in a test result set using Z-score.
    Returns DataFrame of outlier die records.
    """
    grp     = ptr_df[ptr_df['test_num'] == test_num].copy()
    mean    = grp['result'].mean()
    std     = grp['result'].std(ddof=1)
    grp['z_score'] = (grp['result'] - mean) / std
    outliers = grp[grp['z_score'].abs() > z_threshold]
    return outliers[['wafer_id', 'site', 'result', 'z_score', 'passed']]


# ── 4.7 GENERATE LLM SUMMARY TEXT ────────────────────────────────

def generate_llm_summary(stats_df, trend_results, corr_matrix, lot_info):
    """
    Convert analysis results to a concise text summary for LLM prompt injection.
    Keeps token count small — suitable for 7B model context windows.
    """
    lines = [
        f"=== STDF Lot Analysis Summary ===",
        f"Lot: {lot_info.get('lot_id', 'N/A')}  "
        f"Device: {lot_info.get('part_typ', 'N/A')}  "
        f"Tester: {lot_info.get('tstr_typ', 'N/A')}",
        "",
        "--- Test Statistics (sorted by Cpk, worst first) ---",
    ]

    for _, row in stats_df.iterrows():
        flag = '⚠ ' if (not np.isnan(row['cpk']) and row['cpk'] < 1.33) else '✓ '
        lines.append(
            f"{flag}Test {row['test_num']} ({row['test_name']}) {row['units']}: "
            f"mean={row['mean']}, std={row['std']}, "
            f"Cpk={row['cpk']}, pass={row['pass_rate']}%, "
            f"limits=[{row['lo_limit']}, {row['hi_limit']}]"
        )

    lines += ["", "--- Trend Findings ---"]
    for t in trend_results:
        lines.append(t.get('message', ''))

    lines += ["", "--- High Correlations (|r| > 0.7) ---"]
    seen = set()
    for t1 in corr_matrix.columns:
        for t2 in corr_matrix.columns:
            if t1 != t2 and (t2, t1) not in seen:
                r = corr_matrix.loc[t1, t2]
                if abs(r) > 0.7:
                    lines.append(f"  {t1} ↔ {t2}: r={r:.3f}")
                seen.add((t1, t2))

    return '\n'.join(lines)
```

---

## 5. SCRIPT 4 — WAFER MAP VISUALIZATION (matplotlib, no extra libs)

```python
"""
stdf_wafermap.py — Wafer map plots using only matplotlib + numpy
Visualizes: bin map, parametric heatmap, pass/fail overlay
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap


def _circular_mask(grid, cx, cy, radius_die):
    """Mask numpy array to circle. Returns masked array."""
    rows, cols = grid.shape
    y_idx, x_idx = np.ogrid[:rows, :cols]
    dist = np.sqrt((x_idx - cx) ** 2 + (y_idx - cy) ** 2)
    masked = grid.astype(float).copy()
    masked[dist > radius_die] = np.nan
    return masked


def plot_bin_wafermap(prr_df, wafer_id=None, title=None, ax=None):
    """
    Plot hard bin wafer map colored by bin number.

    prr_df must have: x_coord, y_coord, hard_bin, passed columns.
    wafer_id: filter to specific wafer (None = all data).
    """
    df = prr_df[prr_df['wafer_id'] == wafer_id] if wafer_id else prr_df.copy()

    x = df['x_coord'].values
    y = df['y_coord'].values
    bins = df['hard_bin'].values

    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    cols = x_max - x_min + 1
    rows = y_max - y_min + 1

    grid = np.full((rows, cols), np.nan)
    for xi, yi, b in zip(x - x_min, y - y_min, bins):
        grid[yi, xi] = b

    # Apply circular mask
    cx = (x_max - x_min) / 2
    cy = (y_max - y_min) / 2
    radius = min(cx, cy) * 1.05
    grid_masked = _circular_mask(grid, cx, cy, radius)

    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))

    # Color map: bin 1 = green (pass), others = red shades
    cmap = plt.get_cmap('RdYlGn_r', int(bins.max()) + 1)
    cmap.set_bad(color='white')

    im = ax.imshow(grid_masked, cmap=cmap, origin='lower', interpolation='nearest')
    plt.colorbar(im, ax=ax, label='Hard Bin')

    ax.set_title(title or f'Bin Wafer Map — {wafer_id or "All"}')
    ax.set_xlabel('X Die Coordinate')
    ax.set_ylabel('Y Die Coordinate')

    # Add wafer circle outline
    circle = plt.Circle((cx, cy), radius, color='black', fill=False, linewidth=1.5)
    ax.add_patch(circle)

    # Add pass rate text
    pass_rate = df['passed'].mean() * 100
    ax.text(0.02, 0.98, f'Yield: {pass_rate:.1f}%',
            transform=ax.transAxes, va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    return ax


def plot_parametric_wafermap(ptr_df, test_num, wafer_id=None, ax=None):
    """
    Plot parametric heatmap — die color = measured value for a specific test.
    """
    df = ptr_df[ptr_df['test_num'] == test_num]
    if wafer_id:
        df = df[df['wafer_id'] == wafer_id]

    if df.empty:
        print(f"No data for test {test_num}")
        return None

    test_name = df['test_name'].iloc[0]
    units     = df['units'].iloc[0]
    lo_limit  = df['lo_limit'].iloc[0]
    hi_limit  = df['hi_limit'].iloc[0]

    # Merge with PRR for coordinates — assumes caller provides merged df
    # Here we assume ptr_df has x_coord, y_coord (merged from PRR)
    if 'x_coord' not in df.columns:
        print("ptr_df needs x_coord, y_coord columns — merge with prr_df first")
        return None

    x = df['x_coord'].values
    y = df['y_coord'].values
    vals = df['result'].values

    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    cols = x_max - x_min + 1
    rows = y_max - y_min + 1

    grid = np.full((rows, cols), np.nan)
    for xi, yi, v in zip(x - x_min, y - y_min, vals):
        grid[yi, xi] = v

    cx = (x_max - x_min) / 2
    cy = (y_max - y_min) / 2
    radius = min(cx, cy) * 1.05
    grid_masked = _circular_mask(grid, cx, cy, radius)

    if ax is None:
        fig, ax = plt.subplots(figsize=(7, 7))

    cmap = plt.get_cmap('RdYlGn')
    cmap.set_bad(color='lightgray')

    # Clip colormap to limits for visual reference
    vmin = lo_limit if lo_limit is not None else np.nanmin(grid_masked)
    vmax = hi_limit if hi_limit is not None else np.nanmax(grid_masked)

    im = ax.imshow(grid_masked, cmap=cmap, origin='lower',
                   interpolation='nearest', vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=ax, label=f'{test_name} [{units}]')
    ax.set_title(f'Test {test_num}: {test_name}\nWafer: {wafer_id or "All"}')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    circle = plt.Circle((cx, cy), radius, color='black', fill=False, linewidth=1.5)
    ax.add_patch(circle)
    return ax


def plot_wafer_gallery(wrr_df, prr_df, ncols=5):
    """
    Plot pass/fail wafer maps for all wafers in a lot (gallery view).
    """
    wafers = wrr_df['wafer_id'].tolist()
    nrows  = int(np.ceil(len(wafers) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 3, nrows * 3))
    axes = axes.flatten()

    for i, wid in enumerate(wafers):
        df = prr_df[prr_df['wafer_id'] == wid]
        if df.empty:
            axes[i].axis('off')
            continue
        plot_bin_wafermap(prr_df, wafer_id=wid, ax=axes[i])
        axes[i].set_title(wid, fontsize=8)
        axes[i].set_xticks([])
        axes[i].set_yticks([])

    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    fig.suptitle('Wafer Gallery — Bin Map', fontsize=13, y=1.02)
    plt.tight_layout()
    return fig
```

---

## 6. SCRIPT 5 — STATISTICAL PLOT SUITE (Histogram, Boxplot, Trend, Correlation)

```python
"""
stdf_plots.py — Full statistical visualization suite for STDF data
Requires: matplotlib, seaborn, numpy, pandas
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns


# ── 6.1 HISTOGRAM WITH CPK AND LIMITS ───────────────────────────

def plot_histogram(ptr_df, test_num, wafer_id=None, bins=40, ax=None):
    """
    Distribution histogram for one parametric test.
    Overlays: KDE curve, lo/hi limits, mean line, Cpk annotation.
    """
    df = ptr_df[ptr_df['test_num'] == test_num]
    if wafer_id:
        df = df[df['wafer_id'] == wafer_id]

    vals      = df['result'].dropna()
    lo_limit  = df['lo_limit'].iloc[0]
    hi_limit  = df['hi_limit'].iloc[0]
    test_name = df['test_name'].iloc[0]
    units     = df['units'].iloc[0]

    mean = vals.mean()
    std  = vals.std(ddof=1)
    cpk_val = min(
        (hi_limit - mean) / (3 * std),
        (mean - lo_limit) / (3 * std)
    ) if (lo_limit is not None and hi_limit is not None and std > 0) else np.nan

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(vals, bins=bins, color='steelblue', alpha=0.7,
            density=True, edgecolor='white', label='Distribution')

    # KDE overlay
    from scipy.stats import gaussian_kde
    kde_x = np.linspace(vals.min(), vals.max(), 300)
    kde   = gaussian_kde(vals)
    ax.plot(kde_x, kde(kde_x), 'navy', lw=2, label='KDE')

    # Spec limits
    if lo_limit is not None:
        ax.axvline(lo_limit, color='red', linestyle='--', lw=1.5, label=f'LO={lo_limit}')
    if hi_limit is not None:
        ax.axvline(hi_limit, color='red', linestyle='--', lw=1.5, label=f'HI={hi_limit}')

    # Mean
    ax.axvline(mean, color='orange', linestyle='-', lw=1.5, label=f'Mean={mean:.4f}')

    # Annotation box
    info = (f'n={len(vals)}\nMean={mean:.4f}\nStd={std:.4f}'
            f'\nCpk={cpk_val:.3f}' if not np.isnan(cpk_val) else
            f'n={len(vals)}\nMean={mean:.4f}\nStd={std:.4f}')
    ax.text(0.98, 0.97, info, transform=ax.transAxes,
            va='top', ha='right', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    ax.set_xlabel(f'{units}')
    ax.set_ylabel('Density')
    ax.set_title(f'Test {test_num}: {test_name}')
    ax.legend(fontsize=8)
    return ax


# ── 6.2 BOXPLOT ACROSS WAFERS ────────────────────────────────────

def plot_boxplot_by_wafer(ptr_df, test_num, ax=None):
    """
    Boxplot of results grouped by wafer. Shows wafer-to-wafer variation.
    Highlights out-of-trend wafers visually.
    """
    df = ptr_df[ptr_df['test_num'] == test_num].copy()
    if df.empty:
        print(f"No data for test {test_num}")
        return None

    test_name = df['test_name'].iloc[0]
    units     = df['units'].iloc[0]
    lo_limit  = df['lo_limit'].iloc[0]
    hi_limit  = df['hi_limit'].iloc[0]

    if ax is None:
        fig, ax = plt.subplots(figsize=(max(8, len(df['wafer_id'].unique()) * 0.6), 5))

    sns.boxplot(data=df, x='wafer_id', y='result', ax=ax,
                color='steelblue', width=0.5, fliersize=3)

    if lo_limit is not None:
        ax.axhline(lo_limit, color='red', linestyle='--', lw=1.2, label='Low limit')
    if hi_limit is not None:
        ax.axhline(hi_limit, color='red', linestyle='--', lw=1.2, label='High limit')

    ax.set_title(f'Test {test_num}: {test_name} — By Wafer')
    ax.set_xlabel('Wafer ID')
    ax.set_ylabel(f'Result [{units}]')
    ax.tick_params(axis='x', rotation=45)
    if lo_limit or hi_limit:
        ax.legend(fontsize=8)
    return ax


# ── 6.3 TREND CHART WITH CONTROL LIMITS ─────────────────────────

def plot_trend_chart(ptr_df, test_num, ax=None):
    """
    Wafer mean trend chart (run chart) with ±3sigma control limits.
    Each point = mean of all sites on that wafer.
    """
    df = ptr_df[ptr_df['test_num'] == test_num]
    if df.empty:
        return None

    test_name = df['test_name'].iloc[0]
    units     = df['units'].iloc[0]
    lo_limit  = df['lo_limit'].iloc[0]
    hi_limit  = df['hi_limit'].iloc[0]

    wafer_means = df.groupby('wafer_id')['result'].mean()
    wafer_stds  = df.groupby('wafer_id')['result'].std()
    x = np.arange(len(wafer_means))

    overall_mean = wafer_means.mean()
    overall_std  = wafer_means.std(ddof=1)
    ucl = overall_mean + 3 * overall_std
    lcl = overall_mean - 3 * overall_std

    # Trend line
    from scipy import stats as sp_stats
    slope, intercept, r, p, _ = sp_stats.linregress(x, wafer_means.values)
    trend_line = slope * x + intercept

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(x, wafer_means.values, 'o-', color='steelblue', ms=5, label='Wafer mean')
    ax.fill_between(x, wafer_means - wafer_stds, wafer_means + wafer_stds,
                    alpha=0.15, color='steelblue', label='±1σ band')
    ax.plot(x, trend_line, 'r--', lw=1.2, label=f'Trend (slope={slope:+.4f})')
    ax.axhline(overall_mean, color='gray', lw=1, linestyle='-', label='Mean')
    ax.axhline(ucl, color='orange', lw=1, linestyle='--', label='UCL (+3σ)')
    ax.axhline(lcl, color='orange', lw=1, linestyle='--', label='LCL (-3σ)')

    if lo_limit is not None:
        ax.axhline(lo_limit, color='red', lw=1.2, linestyle=':', label='Spec Lo')
    if hi_limit is not None:
        ax.axhline(hi_limit, color='red', lw=1.2, linestyle=':', label='Spec Hi')

    ax.set_xticks(x)
    ax.set_xticklabels(wafer_means.index, rotation=45, fontsize=7)
    ax.set_title(f'Test {test_num}: {test_name} — Wafer Trend\n'
                 f'Slope={slope:+.4f} {units}/wafer, p={p:.4f}')
    ax.set_xlabel('Wafer')
    ax.set_ylabel(f'Mean [{units}]')
    ax.legend(fontsize=7, loc='upper right')
    return ax


# ── 6.4 YIELD TREND CHART ────────────────────────────────────────

def plot_yield_trend(wrr_df, ax=None):
    """
    Plot lot yield trend across wafers with control limits.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    y = wrr_df['yield_pct'].values
    x = np.arange(len(y))
    labels = wrr_df['wafer_id'].values

    mean_y = y.mean()
    std_y  = y.std(ddof=1)

    from scipy import stats as sp_stats
    slope, intercept, r, p, _ = sp_stats.linregress(x, y)
    trend = slope * x + intercept

    ax.plot(x, y, 'o-', color='green', ms=6, label='Yield %')
    ax.plot(x, trend, 'r--', lw=1.2, label=f'Trend (p={p:.3f})')
    ax.axhline(mean_y, color='gray', lw=1, label=f'Mean={mean_y:.1f}%')
    ax.axhline(mean_y + 3 * std_y, color='orange', lw=1, linestyle='--', label='UCL')
    ax.axhline(mean_y - 3 * std_y, color='orange', lw=1, linestyle='--', label='LCL')

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, fontsize=7)
    ax.set_ylabel('Yield %')
    ax.set_title(f'Lot Yield Trend — Slope={slope:+.2f}%/wafer')
    ax.set_ylim(max(0, y.min() - 5), min(100, y.max() + 5))
    ax.legend(fontsize=8)
    return ax


# ── 6.5 CORRELATION SCATTER PLOT ────────────────────────────────

def plot_scatter_correlation(ptr_df, test_num_x, test_num_y, ax=None):
    """
    Scatter plot of two parametric tests. Shows correlation and fit line.
    """
    df_x = ptr_df[ptr_df['test_num'] == test_num_x][['wafer_id', 'site', 'result']].rename(columns={'result': 'x'})
    df_y = ptr_df[ptr_df['test_num'] == test_num_y][['wafer_id', 'site', 'result']].rename(columns={'result': 'y'})
    merged = pd.merge(df_x, df_y, on=['wafer_id', 'site'])

    name_x = ptr_df[ptr_df['test_num'] == test_num_x]['test_name'].iloc[0]
    name_y = ptr_df[ptr_df['test_num'] == test_num_y]['test_name'].iloc[0]
    units_x = ptr_df[ptr_df['test_num'] == test_num_x]['units'].iloc[0]
    units_y = ptr_df[ptr_df['test_num'] == test_num_y]['units'].iloc[0]

    from scipy import stats as sp_stats
    r, p = sp_stats.pearsonr(merged['x'], merged['y'])
    slope, intercept, *_ = sp_stats.linregress(merged['x'], merged['y'])
    fit_x = np.linspace(merged['x'].min(), merged['x'].max(), 100)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(merged['x'], merged['y'], alpha=0.4, s=15, color='steelblue')
    ax.plot(fit_x, slope * fit_x + intercept, 'r-', lw=1.5,
            label=f'r={r:.3f}, p={p:.4f}')

    ax.set_xlabel(f'Test {test_num_x}: {name_x} [{units_x}]')
    ax.set_ylabel(f'Test {test_num_y}: {name_y} [{units_y}]')
    ax.set_title(f'Correlation: T{test_num_x} vs T{test_num_y}')
    ax.legend(fontsize=9)
    return ax


# ── 6.6 CORRELATION HEATMAP ─────────────────────────────────────

def plot_correlation_heatmap(corr_df, ax=None):
    """
    Seaborn heatmap of test-test correlation matrix.
    """
    if ax is None:
        n = len(corr_df)
        fig, ax = plt.subplots(figsize=(max(6, n), max(5, n - 1)))

    mask = np.triu(np.ones_like(corr_df, dtype=bool), k=1)
    sns.heatmap(
        corr_df, annot=True, fmt='.2f', cmap='RdBu_r',
        center=0, vmin=-1, vmax=1,
        mask=mask, ax=ax, square=True,
        annot_kws={'size': 8},
        linewidths=0.5
    )
    ax.set_title('Test Correlation Matrix (Pearson r)')
    ax.tick_params(axis='x', rotation=45, labelsize=7)
    ax.tick_params(axis='y', rotation=0, labelsize=7)
    return ax


# ── 6.7 SITE-TO-SITE BOXPLOT ────────────────────────────────────

def plot_site_boxplot(ptr_df, test_num, ax=None):
    """
    Boxplot grouped by site number. Reveals probe card or pin issues.
    """
    df = ptr_df[ptr_df['test_num'] == test_num]
    if df.empty:
        return None

    test_name = df['test_name'].iloc[0]
    units     = df['units'].iloc[0]
    lo_limit  = df['lo_limit'].iloc[0]
    hi_limit  = df['hi_limit'].iloc[0]

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))

    sns.boxplot(data=df, x='site', y='result', ax=ax,
                palette='Set2', width=0.5)

    if lo_limit is not None:
        ax.axhline(lo_limit, color='red', linestyle='--', lw=1.2)
    if hi_limit is not None:
        ax.axhline(hi_limit, color='red', linestyle='--', lw=1.2)

    ax.set_title(f'Test {test_num}: {test_name} — By Site')
    ax.set_xlabel('Site Number')
    ax.set_ylabel(f'Result [{units}]')
    return ax


# ── 6.8 MULTI-PANEL DASHBOARD FOR ONE TEST ──────────────────────

def plot_test_dashboard(ptr_df, prr_df, test_num, wafer_id=None):
    """
    4-panel dashboard for a single test:
    [Histogram] [Trend chart]
    [Boxplot by wafer] [Site boxplot]
    """
    fig = plt.figure(figsize=(16, 10))
    gs  = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.35)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])

    plot_histogram(ptr_df, test_num, wafer_id=wafer_id, ax=ax1)
    plot_trend_chart(ptr_df, test_num, ax=ax2)
    plot_boxplot_by_wafer(ptr_df, test_num, ax=ax3)
    plot_site_boxplot(ptr_df, test_num, ax=ax4)

    test_name = ptr_df[ptr_df['test_num'] == test_num]['test_name'].iloc[0]
    fig.suptitle(f'Test {test_num}: {test_name} — Full Dashboard', fontsize=14, y=1.01)
    return fig
```

---

## 7. SCRIPT 6 — LLM INTEGRATION (Ollama / Local Model)

```python
"""
stdf_llm.py — Pipe STDF analysis results into a local Ollama model
Requires: requests (or ollama Python SDK), analysis results as text
"""

import requests
import json


OLLAMA_URL   = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'llama3.1:8b'   # or qwen2.5-coder:7b for code tasks


def ask_ollama(prompt, model=OLLAMA_MODEL, system=None):
    """
    Send a prompt to local Ollama server. Returns streamed response text.
    """
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': True,
    }
    if system:
        payload['system'] = system

    response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
    response.raise_for_status()

    full_text = ''
    for line in response.iter_lines():
        if line:
            chunk = json.loads(line)
            token = chunk.get('response', '')
            print(token, end='', flush=True)
            full_text += token
            if chunk.get('done'):
                break
    print()
    return full_text


def interpret_analysis(summary_text, question=None):
    """
    Ask local model to interpret STDF analysis results.
    """
    system = (
        "You are an expert semiconductor test engineer with deep knowledge of "
        "wafer probe, STDF data, parametric analysis, ATE systems, and failure analysis. "
        "Analyze the test data summary provided and give actionable insights. "
        "Focus on root cause hypotheses, process implications, and recommended actions."
    )

    q = question or (
        "Based on this wafer test data analysis, identify: "
        "1) Tests at risk (low Cpk), "
        "2) Any significant trends (drift, shift), "
        "3) Possible correlations and their physical meaning, "
        "4) Recommended investigation actions."
    )

    prompt = f"""
Here is a wafer sort analysis summary for your review:

{summary_text}

{q}
"""
    return ask_ollama(prompt, system=system)


def ask_specific_question(summary_text, question):
    """
    Ask a targeted question about specific findings in the summary.
    """
    system = (
        "You are a semiconductor test engineer expert. "
        "Answer questions about wafer test data concisely and technically."
    )
    prompt = f"""
STDF Analysis Data:
{summary_text}

Question: {question}
"""
    return ask_ollama(prompt, system=system)


# ── EXAMPLE QUESTIONS TO ASK THE LLM ────────────────────────────
EXAMPLE_QUESTIONS = [
    "Which test shows the most concerning drift trend and what could cause it?",
    "The LEAKAGE test has Cpk=0.8 — what are the likely physical root causes?",
    "Tests 1000 and 1010 show r=0.85 correlation — what does this mean physically?",
    "Site 3 consistently reads 5% low on VDD_CURRENT — what should we check?",
    "Wafer 15 shows 20% yield drop vs lot average — what are the likely causes?",
    "Should we tighten the test limit for test 2000 given the current distribution?",
    "What fab process parameters typically correlate with leakage current drift?",
]
```

---

## 8. SCRIPT 7 — COMPLETE PIPELINE (Parse → Analyze → Plot → LLM)

```python
"""
stdf_pipeline.py — Full end-to-end pipeline
Parse STDF → run statistics → generate plots → ask LLM to interpret

Usage:
    python stdf_pipeline.py wafer.stdf --tests 1000 1010 2000
"""

import sys
import argparse
import matplotlib.pyplot as plt

# Import from our other scripts
from stdf_parser   import parse_stdf
from stdf_analysis import (analyze_all_tests, yield_trend,
                            parametric_trend, test_correlation_matrix,
                            site_uniformity, generate_llm_summary)
from stdf_plots    import (plot_yield_trend, plot_test_dashboard,
                            plot_correlation_heatmap, plot_wafer_gallery)
from stdf_wafermap import plot_bin_wafermap
from stdf_llm      import interpret_analysis


def run_pipeline(stdf_file, test_filter=None, ask_llm=True, save_plots=False):
    print(f"\n=== STDF Pipeline: {stdf_file} ===")

    # ── 1. PARSE ──────────────────────────────────────────────────
    print("Parsing STDF...")
    data = parse_stdf(stdf_file, test_filter=test_filter)
    ptr  = data['ptr']
    prr  = data['prr']
    wrr  = data['wrr']
    mir  = data['mir']

    print(f"  Lot: {mir.get('lot_id', 'N/A')}  Device: {mir.get('part_typ', 'N/A')}")
    print(f"  Wafers: {len(wrr)}  Tests recorded: {ptr['test_num'].nunique()}")
    print(f"  Total PTR records: {len(ptr)}")

    # ── 2. STATISTICS ─────────────────────────────────────────────
    print("\nRunning statistics...")
    stats_df = analyze_all_tests(ptr)
    yt       = yield_trend(wrr)

    print("\n--- Yield ---")
    print(wrr[['wafer_id', 'yield_pct']].to_string(index=False))
    print(f"\nYield trend: {yt['message']}")

    print("\n--- Test Stats (worst Cpk first) ---")
    print(stats_df[['test_num', 'test_name', 'mean', 'std', 'cpk', 'pass_rate']].to_string(index=False))

    # Parametric trends
    trend_results = []
    for tn in ptr['test_num'].unique():
        tr = parametric_trend(ptr, tn)
        trend_results.append(tr)
        if tr.get('significant'):
            print(f"  ⚠  {tr['message']}")

    # Correlation
    corr = test_correlation_matrix(ptr)

    # ── 3. PLOTS ──────────────────────────────────────────────────
    print("\nGenerating plots...")

    # Yield trend
    fig1, ax = plt.subplots(figsize=(10, 4))
    plot_yield_trend(wrr, ax=ax)
    if save_plots:
        fig1.savefig('yield_trend.png', dpi=150, bbox_inches='tight')
    plt.show()

    # Wafer gallery
    if len(prr) > 0:
        fig2 = plot_wafer_gallery(wrr, prr)
        if save_plots:
            fig2.savefig('wafer_gallery.png', dpi=150, bbox_inches='tight')
        plt.show()

    # Dashboard for each test
    for test_num in ptr['test_num'].unique():
        fig = plot_test_dashboard(ptr, prr, test_num)
        if save_plots:
            fig.savefig(f'test_{test_num}_dashboard.png', dpi=150, bbox_inches='tight')
        plt.show()

    # Correlation heatmap
    if len(corr) > 1:
        fig3, ax = plt.subplots(figsize=(8, 7))
        plot_correlation_heatmap(corr, ax=ax)
        if save_plots:
            fig3.savefig('correlation_heatmap.png', dpi=150, bbox_inches='tight')
        plt.show()

    # ── 4. LLM INTERPRETATION ────────────────────────────────────
    if ask_llm:
        print("\nGenerating LLM summary...")
        summary = generate_llm_summary(stats_df, trend_results, corr, mir)
        print("\n--- LLM Summary Input ---")
        print(summary[:1000], '...' if len(summary) > 1000 else '')

        print("\n--- LLM Interpretation ---")
        interpret_analysis(summary)

    return data, stats_df, corr


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='STDF Analysis Pipeline')
    parser.add_argument('stdf_file', help='Path to .stdf file')
    parser.add_argument('--tests', nargs='+', type=int, default=None,
                        help='Test numbers to include (e.g. --tests 1000 1010)')
    parser.add_argument('--no-llm', action='store_true', help='Skip LLM step')
    parser.add_argument('--save', action='store_true', help='Save plots as PNG')
    args = parser.parse_args()

    test_filter = set(args.tests) if args.tests else None
    run_pipeline(args.stdf_file,
                 test_filter=test_filter,
                 ask_llm=not args.no_llm,
                 save_plots=args.save)
```

---

## 9. SCRIPT 8 — RAG CHUNKER FOR STDF DATA

```python
"""
stdf_rag_chunker.py — Convert parsed STDF data into ChromaDB-ready text chunks
For use with nomic-embed-text + ChromaDB in your ai-workspace RAG pipeline
"""

import json
import chromadb
import requests
from stdf_parser import parse_stdf
from stdf_analysis import analyze_all_tests, parametric_trend, site_uniformity


EMBED_MODEL = 'nomic-embed-text'
OLLAMA_URL  = 'http://localhost:11434/api/embeddings'


def embed_text(text):
    """Get embedding from local Ollama nomic-embed-text model."""
    resp = requests.post(OLLAMA_URL, json={'model': EMBED_MODEL, 'prompt': text})
    return resp.json()['embedding']


def build_rag_chunks(stdf_file, test_filter=None):
    """
    Parse STDF and build a list of text chunks for embedding.
    Each chunk = one coherent unit of knowledge about the test data.
    """
    data     = parse_stdf(stdf_file, test_filter=test_filter)
    ptr      = data['ptr']
    wrr      = data['wrr']
    mir      = data['mir']
    stats_df = analyze_all_tests(ptr)

    chunks = []
    lot_id = mir.get('lot_id', 'UNKNOWN')

    # Chunk 1: Lot metadata
    chunks.append({
        'id':   f'{lot_id}_lot_info',
        'text': (
            f"Lot {lot_id} on device {mir.get('part_typ','?')} "
            f"tested on {mir.get('tstr_typ','?')} using program {mir.get('job_nam','?')}. "
            f"Wafer count: {len(wrr)}. "
            f"Average yield: {wrr['yield_pct'].mean():.1f}%."
        ),
        'meta': {'lot_id': lot_id, 'chunk_type': 'lot_info'},
    })

    # Chunk 2: Yield per wafer
    for _, row in wrr.iterrows():
        chunks.append({
            'id':   f"{lot_id}_{row['wafer_id']}_yield",
            'text': (
                f"Wafer {row['wafer_id']} in lot {lot_id}: "
                f"{row['good_cnt']} good out of {row['part_cnt']} total. "
                f"Yield = {row['yield_pct']:.1f}%. "
                f"Aborted: {row['abrt_cnt']}, Retested: {row['rtst_cnt']}."
            ),
            'meta': {'lot_id': lot_id, 'wafer_id': row['wafer_id'],
                     'chunk_type': 'wafer_yield'},
        })

    # Chunk 3: Per-test statistics
    for _, row in stats_df.iterrows():
        cpk_str = f"Cpk={row['cpk']:.3f}" if row['cpk'] == row['cpk'] else "Cpk=N/A"
        flag = "AT RISK — " if (row['cpk'] == row['cpk'] and row['cpk'] < 1.33) else ""
        chunks.append({
            'id':   f"{lot_id}_test_{row['test_num']}_stats",
            'text': (
                f"{flag}Test {row['test_num']} ({row['test_name']}) for lot {lot_id}: "
                f"mean={row['mean']} {row['units']}, std={row['std']}, "
                f"min={row['min']}, max={row['max']}, {cpk_str}, "
                f"pass rate={row['pass_rate']}%, n={row['n']}, "
                f"limits=[{row['lo_limit']}, {row['hi_limit']}]."
            ),
            'meta': {'lot_id': lot_id, 'test_num': int(row['test_num']),
                     'test_name': row['test_name'], 'chunk_type': 'test_stats',
                     'cpk': float(row['cpk']) if row['cpk'] == row['cpk'] else -1},
        })

    # Chunk 4: Per-test trend
    for test_num in ptr['test_num'].unique():
        tr = parametric_trend(ptr, test_num)
        if 'message' in tr:
            chunks.append({
                'id':   f"{lot_id}_test_{test_num}_trend",
                'text': f"Lot {lot_id}: {tr['message']}",
                'meta': {'lot_id': lot_id, 'test_num': int(test_num),
                         'chunk_type': 'trend',
                         'significant': tr.get('significant', False)},
            })

    # Chunk 5: Site uniformity per test
    for test_num in ptr['test_num'].unique():
        su = site_uniformity(ptr, test_num)
        flag = "WARNING: " if su['flag'] else ""
        chunks.append({
            'id':   f"{lot_id}_test_{test_num}_site_uniformity",
            'text': (
                f"{flag}Test {test_num} site uniformity for lot {lot_id}: "
                f"between-site range={su['site_range']:.4f}, "
                f"between-site variation={su['between_pct']:.1f}% of total std. "
                f"{'High site variation — check probe card or handler.' if su['flag'] else 'Site uniformity acceptable.'}"
            ),
            'meta': {'lot_id': lot_id, 'test_num': int(test_num),
                     'chunk_type': 'site_uniformity', 'flag': su['flag']},
        })

    return chunks


def load_to_chromadb(chunks, collection_name='stdf_knowledge'):
    """Embed chunks and store in ChromaDB."""
    client     = chromadb.Client()
    collection = client.get_or_create_collection(collection_name)

    for chunk in chunks:
        embedding = embed_text(chunk['text'])
        collection.add(
            ids=[chunk['id']],
            embeddings=[embedding],
            documents=[chunk['text']],
            metadatas=[chunk['meta']],
        )

    print(f"Loaded {len(chunks)} chunks into ChromaDB collection '{collection_name}'")
    return collection


def query_rag(collection, question, n_results=5):
    """Query ChromaDB and return relevant chunks for LLM context."""
    embedding = embed_text(question)
    results   = collection.query(query_embeddings=[embedding], n_results=n_results)
    docs      = results['documents'][0]
    return '\n'.join(docs)


# ── USAGE ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    chunks     = build_rag_chunks('wafer.stdf', test_filter={1000, 1010, 2000})
    collection = load_to_chromadb(chunks)

    question = "Which tests are drifting and what is the Cpk for test 1000?"
    context  = query_rag(collection, question)
    print("Retrieved context:\n", context)
```

---

## 10. KEY PATTERNS AND BEST PRACTICES

### Parsing Pattern: Filter Early, Reduce Always
```python
# Never load all records into memory — filter during parse
data = parse_stdf('big_lot.stdf', test_filter={1000, 1010, 2000})
# A 200MB STDF reduces to a few MB DataFrame in memory
```

### Merge PTR + PRR for Spatial Analysis
```python
# ptr_df has test results; prr_df has X,Y coordinates
# Join them to enable spatial (wafer map) analysis
ptr_with_coords = ptr_df.merge(
    prr_df[['wafer_id', 'site', 'x_coord', 'y_coord']],
    on=['wafer_id', 'site'],
    how='left'
)
```

### LLM Token Budget Management
```python
# Keep summaries under 2KB for 7B models
# Include: lot ID, test name, mean, std, Cpk, pass rate per test
# Flag only anomalies — don't feed raw numbers for all 500 tests
summary = generate_llm_summary(stats_df[stats_df['cpk'] < 1.5], ...)
```

### Typical Analysis Workflow
```
1. parse_stdf()           → get ptr, prr, wrr DataFrames
2. analyze_all_tests()    → Cpk, mean, std, pass_rate per test
3. yield_trend()          → is yield drifting across wafers?
4. parametric_trend()     → which tests are drifting?
5. test_correlation()     → which tests are related?
6. site_uniformity()      → probe card / handler issues?
7. generate_llm_summary() → text block for LLM
8. interpret_analysis()   → LLM explains root causes
```

### Tool Reference Summary

| Script | Function | Use Case |
|--------|----------|----------|
| stdf_parser.py | parse_stdf() | Read STDF → DataFrames (no deps) |
| stdf_pystdf_sink.py | parse_with_pystdf() | Read STDF via pystdf library |
| stdf_analysis.py | analyze_all_tests() | Cpk, stats, yields |
| stdf_analysis.py | yield_trend() | Lot yield drift |
| stdf_analysis.py | parametric_trend() | Per-test drift |
| stdf_analysis.py | test_correlation_matrix() | Cross-test correlation |
| stdf_analysis.py | site_uniformity() | Site variation |
| stdf_analysis.py | generate_llm_summary() | LLM-ready text |
| stdf_wafermap.py | plot_bin_wafermap() | Pass/fail wafer map |
| stdf_wafermap.py | plot_parametric_wafermap() | Value heatmap |
| stdf_wafermap.py | plot_wafer_gallery() | All wafers in lot |
| stdf_plots.py | plot_histogram() | Distribution + Cpk |
| stdf_plots.py | plot_trend_chart() | Run chart + UCL/LCL |
| stdf_plots.py | plot_boxplot_by_wafer() | Wafer-to-wafer variation |
| stdf_plots.py | plot_correlation_heatmap() | r-matrix heatmap |
| stdf_plots.py | plot_test_dashboard() | 4-panel per test |
| stdf_plots.py | plot_yield_trend() | Lot yield chart |
| stdf_plots.py | plot_site_boxplot() | Site-to-site variation |
| stdf_llm.py | ask_ollama() | Call local model |
| stdf_llm.py | interpret_analysis() | LLM explains findings |
| stdf_rag_chunker.py | build_rag_chunks() | Build ChromaDB chunks |
| stdf_rag_chunker.py | load_to_chromadb() | Store embeddings |
| stdf_rag_chunker.py | query_rag() | Retrieve context |
| stdf_pipeline.py | run_pipeline() | Full end-to-end run |

---

*Document version: 1.0 — Python scripts for STDF parsing, analysis, and visualization.*
*Libraries: pystdf, Semi-ATE-STDF, pandas, numpy, scipy, matplotlib, seaborn, ChromaDB, Ollama.*
