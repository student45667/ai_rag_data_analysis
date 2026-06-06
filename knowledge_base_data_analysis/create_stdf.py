#!/usr/bin/env python3
"""
generate_wafer_stdf.py — Dummy STDF wafer file, 200 dies, 3 parametric tests
Requirements: pip install pystdf4 numpy
"""

import time, random, os
import numpy as np
from pystdf4 import Stdf4Writer

# --- SETTINGS ---------------------------------------------------------------

OUTPUT_FILE  = "wafer.stdf"
LOT_ID       = "LOT12345"
WAFER_ID     = "WAFER001"
NUM_DIES     = 16000
YIELD_TARGET = 0.85

# (test_num, name, lo_limit, hi_limit, mean, std, units)
TESTS = [
    (100, "VCC_TEST",   0.95, 1.15, 1.05, 0.03, "V"),
    (200, "ICC_TEST",   0.00, 0.50, 0.25, 0.05, "A"),
    (300, "FREQ_TEST", 95.0, 105.0, 100.0, 2.0, "MHz"),
]

BIN_PASS = 1
BIN_FAIL = {100: 2, 200: 3, 300: 4}

random.seed(42)
np.random.seed(42)

# --- HELPERS ----------------------------------------------------------------

def make_result(mean, std, lo, hi, force_fail=False):
    if force_fail:
        val = hi + abs(np.random.normal(0, std)) if random.random() > 0.5 \
              else lo - abs(np.random.normal(0, std))
    else:
        val = np.random.normal(mean, std)
    return round(val, 4), lo <= val <= hi

# --- DIE COORDINATES --------------------------------------------------------

coords = [(x, y) for x in range(-7, 8) for y in range(-7, 8)]
random.shuffle(coords)
die_coords = coords[:NUM_DIES]

# --- WRITE STDF -------------------------------------------------------------

now = int(time.time())
pass_count = fail_count = 0

with Stdf4Writer(OUTPUT_FILE) as stdf:

    stdf.FAR(CPU_TYPE=2, STDF_VER=4)

    stdf.MIR(
        SETUP_T=now, START_T=now, STAT_NUM=1,
        LOT_ID=LOT_ID, PART_TYP="ASIC_TEST_CHIP",
        NODE_NAM="ATE_NODE_01", TSTR_TYP="T2000",
        JOB_NAM="PROBE_WAFER_V1", MODE_COD="P",
        JOB_REV="1.0", OPER_NAM="OPERATOR1", TST_TEMP="25",
    )

    stdf.WIR(HEAD_NUM=1, START_T=now, SITE_GRP=1, WAFER_ID=WAFER_ID)

    for die_num, (x, y) in enumerate(die_coords, start=1):
        force_fail = random.random() > YIELD_TARGET
        fail_test  = random.choice([t[0] for t in TESTS]) if force_fail else None

        stdf.PIR(HEAD_NUM=1, SITE_NUM=1)

        die_passed = True
        hard_bin   = BIN_PASS
        num_tests  = 0

        for test_num, test_name, lo, hi, mean, std, units in TESTS:
            result, passed = make_result(mean, std, lo, hi,
                                         force_fail=(fail_test == test_num))
            if not passed:
                die_passed = False
                hard_bin   = BIN_FAIL[test_num]

            stdf.PTR(
                TEST_NUM=test_num, HEAD_NUM=1, SITE_NUM=1,
                TEST_FLG=b'\x00' if passed else b'\x08',
                PARM_FLG=b'\x00', OPT_FLAG=b'\x00',
                RESULT=result, TEST_TXT=test_name,
                LO_LIMIT=lo, HI_LIMIT=hi, UNITS=units,
            )
            num_tests += 1

        stdf.PRR(
            HEAD_NUM=1, SITE_NUM=1,
            PART_FLG=b'\x00' if die_passed else b'\x08',
            NUM_TEST=num_tests, HARD_BIN=hard_bin,
            SOFT_BIN=1 if die_passed else 10,
            X_COORD=x, Y_COORD=y,
            PART_ID=f"DIE_{die_num:03d}",
        )

        if die_passed: pass_count += 1
        else:          fail_count += 1

    stdf.WRR(HEAD_NUM=1, FINISH_T=now, PART_CNT=NUM_DIES,
             GOOD_CNT=pass_count, WAFER_ID=WAFER_ID)

    for bin_num, name, cnt, pf in [
        (BIN_PASS,    "PASS",      pass_count, 'P'),
        (BIN_FAIL[100], "FAIL_VCC",  0,        'F'),
        (BIN_FAIL[200], "FAIL_ICC",  0,        'F'),
        (BIN_FAIL[300], "FAIL_FREQ", fail_count,'F'),
    ]:
        stdf.HBR(HEAD_NUM=255, SITE_NUM=255, HBIN_NUM=bin_num,
                 HBIN_CNT=cnt, HBIN_PF=pf, HBIN_NAM=name)

    stdf.SBR(HEAD_NUM=255, SITE_NUM=255, SBIN_NUM=1,  SBIN_CNT=pass_count, SBIN_PF='P', SBIN_NAM="PASS")
    stdf.SBR(HEAD_NUM=255, SITE_NUM=255, SBIN_NUM=10, SBIN_CNT=fail_count, SBIN_PF='F', SBIN_NAM="FAIL")

    stdf.MRR(FINISH_T=now)

# --- SUMMARY ----------------------------------------------------------------

print(f"Written: {OUTPUT_FILE} ({os.path.getsize(OUTPUT_FILE):,} bytes)")
print(f"Dies: {NUM_DIES}  Pass: {pass_count} ({pass_count/NUM_DIES*100:.1f}%)  Fail: {fail_count}")