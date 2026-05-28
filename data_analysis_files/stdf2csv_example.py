#!/usr/bin/env python3
"""
stdf_to_csv.py — Parse STDF file and export die-level parametric data to CSV
Requirements: pip install pystdf pandas
Usage: python3 stdf_to_csv.py <file.stdf> [output.csv]
"""

import sys
import pandas as pd
import pystdf.IO as IO
import pystdf.V4 as V4

# ASSUMED: passing hard bin = 1
# ASSUMED: PTR TEST_TXT is the unique test name
# VERIFY: confirm HARD_BIN pass value with test engineer


DIES_AMOUNT = 10000 # dies amount  to parse

# --- LOAD -------------------------------------------------------------------

#stdf_file = sys.argv[1] if len(sys.argv) > 1 else "wafer_200dies.stdf"
stdf_file = "wafer.stdf"
#csv_file  = sys.argv[2] if len(sys.argv) > 2 else stdf_file.replace(".stdf", ".csv")
csv_file  = "wafer.csv"
# --- PARSE ------------------------------------------------------------------

class StdfSink:
    """Collect PIR/PTR/PRR records into a flat list of die rows."""

    def __init__(self):
        self.rows     = []       # final output rows
        self.lot_id   = ""
        self.wafer_id = ""
        self._die     = {}       # current die accumulator

    def after_send(self, parser, data):
        rec = data[0]
        fields = data[1]

        if isinstance(rec, V4.Mir):
            fmap = {f[0]: i for i, f in enumerate(V4.Mir.fieldMap)}
            self.lot_id = fields[fmap["LOT_ID"]]

        elif isinstance(rec, V4.Wir):
            fmap = {f[0]: i for i, f in enumerate(V4.Wir.fieldMap)}
            self.wafer_id = fields[fmap["WAFER_ID"]]

        elif isinstance(rec, V4.Pir):
            self._die = {"LOT_ID": self.lot_id, "WAFER_ID": self.wafer_id}

        elif isinstance(rec, V4.Ptr):
            fmap = {f[0]: i for i, f in enumerate(V4.Ptr.fieldMap)}
            name   = fields[fmap["TEST_TXT"]] or f"TEST_{fields[fmap['TEST_NUM']]}"
            result = fields[fmap["RESULT"]]
            passed = (fields[fmap["TEST_FLG"]] == 0)
            self._die[name]              = round(result, 6)
            self._die[f"{name}_PASS"]   = int(passed)

        elif isinstance(rec, V4.Prr):
            fmap = {f[0]: i for i, f in enumerate(V4.Prr.fieldMap)}
            self._die["X_COORD"]  = fields[fmap["X_COORD"]]
            self._die["Y_COORD"]  = fields[fmap["Y_COORD"]]
            self._die["HARD_BIN"] = fields[fmap["HARD_BIN"]]
            self._die["SOFT_BIN"] = fields[fmap["SOFT_BIN"]]
            self._die["PART_ID"]  = fields[fmap["PART_ID"]]
            self._die["PASS"]     = int(fields[fmap["HARD_BIN"]] == 1)
            self.rows.append(self._die.copy())


            

sink = StdfSink()

with open(stdf_file, "rb") as f:
    p = IO.Parser(inp=f)
    p.addSink(sink)
    p.parse()

# --- CLEAN ------------------------------------------------------------------

df = pd.DataFrame(sink.rows[:DIES_AMOUNT])



# Reorder: metadata first, then test results
meta_cols = ["LOT_ID", "WAFER_ID", "PART_ID", "X_COORD", "Y_COORD",
             "HARD_BIN", "SOFT_BIN", "PASS"]
test_cols = [c for c in df.columns if c not in meta_cols]
df = df[meta_cols + test_cols]

print(df.head())
print(f"\nShape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")

# --- ANALYZE ----------------------------------------------------------------

total = len(df)
passing = df["PASS"].sum()
print(f"\nYield: {passing}/{total} = {passing/total*100:.1f}%")
print(f"Hard bins:\n{df['HARD_BIN'].value_counts().sort_index()}")

# --- SAVE -------------------------------------------------------------------

df.to_csv(csv_file, index=False)
print(f"\nSaved: {csv_file}  ({len(df)} rows x {len(df.columns)} cols)")