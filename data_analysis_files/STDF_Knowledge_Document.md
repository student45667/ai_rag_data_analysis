# STDF Knowledge Document — Standard Test Data Format V4
## Purpose: RAG Reference for Semiconductor Wafer Test Analysis

---

## 1. OVERVIEW

### What is STDF?

STDF (Standard Test Data Format) is a binary file format for storing semiconductor test data produced by Automated Test Equipment (ATE). Originally developed by Teradyne in 1985, it is now a de facto industry standard used by all major ATE vendors including Advantest (V93k), Teradyne (J750, UltraFLEX), Cohu, SPEA, and Roos Instruments.

STDF V4 is the current specification. An updated variant, STDF V4-2007, adds scan test records (STR) for IJTAG/JTAG patterns.

### Key Characteristics

- Binary format (compact, fast to write during test — critical since test time = cost)
- Sequential stream of typed records — written in real time as test runs
- ASCII equivalent: ATDF (human-readable, same structure)
- Supports wafer probe (wafer-level) and final test (package-level)
- One lot per file is the convention, though the format allows flexibility
- A partial STDF file may still contain usable data (file is written record-by-record during test)

### Why Engineers Use STDF

- Universal compatibility across ATE vendors
- Compact binary reduces write overhead on tester computers
- Structured hierarchy: lot → wafer → die → test → result
- Supports parametric (analog), functional (pass/fail), and multi-result test types
- Enables yield analysis, wafer maps, bin summaries, and trend monitoring

---

## 2. FILE STRUCTURE AND RECORD HIERARCHY

### Record Organization

STDF is organized in a strict hierarchy of record types. Every record has a 4-byte header:

```
[REC_LEN: 2 bytes] [REC_TYP: 1 byte] [REC_SUB: 1 byte] [DATA: REC_LEN bytes]
```

REC_TYP + REC_SUB uniquely identify each record type.

### Complete Record Type Table

| REC_TYP | REC_SUB | Abbreviation | Full Name | Frequency |
|---------|---------|--------------|-----------|-----------|
| 0 | 10 | FAR | File Attributes Record | Once, first record in file |
| 0 | 20 | ATR | Audit Trail Record | Optional, once per modification |
| 1 | 10 | MIR | Master Information Record | Once per lot |
| 1 | 20 | MRR | Master Results Record | Once, last record in file |
| 1 | 30 | PCR | Part Count Record | Once per site or lot total |
| 1 | 40 | HBR | Hardware Bin Record | Once per hardware bin |
| 1 | 50 | SBR | Software Bin Record | Once per software bin |
| 1 | 60 | PMR | Pin Map Record | Once per pin used |
| 1 | 62 | PGR | Pin Group Record | Optional, once per group |
| 1 | 63 | PLR | Pin List Record | Optional |
| 1 | 70 | RDR | Retest Data Record | Optional, once if retest |
| 1 | 80 | SDR | Site Description Record | Once per site group |
| 2 | 10 | WIR | Wafer Information Record | Once per wafer (open) |
| 2 | 20 | WRR | Wafer Results Record | Once per wafer (close) |
| 2 | 30 | WCR | Wafer Configuration Record | Once per file (wafer probe only) |
| 5 | 10 | PIR | Part Information Record | Once per die (open) |
| 5 | 20 | PRR | Part Results Record | Once per die (close) |
| 10 | 30 | TSR | Test Synopsis Record | Once per test in program |
| 15 | 10 | PTR | Parametric Test Record | One per parametric test per die |
| 15 | 15 | MPR | Multiple-Result Parametric Record | One per multi-pin test per die |
| 15 | 20 | FTR | Functional Test Record | One per functional test per die |
| 20 | 10 | BPS | Begin Program Section | Optional |
| 20 | 20 | EPS | End Program Section | Optional |
| 50 | 10 | GDR | Generic Data Record | Optional, custom data |
| 50 | 30 | DTR | Datalog Text Record | Optional, text comments |

### Canonical File Structure for Wafer Probe

```
FAR                          ← always first
MIR                          ← lot-level info
SDR                          ← site/handler config
WCR                          ← wafer geometry (diameter, flat orientation)
  [HBR, SBR]                 ← bin definitions (may appear here or after MRR)

  WIR                        ← begin wafer 1
    PIR                      ← begin die at (X=3, Y=5)
      PTR                    ← test 1000: VDD_CURRENT = 45.3mA
      PTR                    ← test 1010: LEAKAGE = 0.02uA
      FTR                    ← test 2000: SCAN_CHAIN_1 = PASS
      MPR                    ← test 3000: PIN_CONTINUITY[1..8]
    PRR                      ← die result: PASS, HARD_BIN=1, X=3, Y=5
    PIR                      ← begin die at (X=3, Y=6)
      PTR ...
    PRR ...
  WRR                        ← end wafer 1, yield summary

  WIR                        ← begin wafer 2
    ...
  WRR                        ← end wafer 2

PCR                          ← total part counts
HBR                          ← hardware bin summary counts
SBR                          ← software bin summary counts
MRR                          ← always last
```

---

## 3. RECORD FIELD DEFINITIONS

### 3.1 FAR — File Attributes Record

**Purpose:** Identifies the CPU type and STDF version. Must be the very first record.

| Field | Type | Description |
|-------|------|-------------|
| CPU_TYPE | U1 | CPU that wrote the file (1=Sun/Motorola big-endian, 2=x86 little-endian) |
| STDF_VER | U1 | STDF version number (4 = V4) |

**Note:** CPU_TYPE=2 (little-endian) is most common in modern testers.

---

### 3.2 MIR — Master Information Record

**Purpose:** Lot-level identification. Contains device, program, facility, and operator information. Appears once, immediately after FAR.

| Field | Type | Description |
|-------|------|-------------|
| SETUP_T | U4 | Setup time (Unix timestamp) |
| START_T | U4 | Lot start time (Unix timestamp) |
| STAT_NUM | U1 | Tester station number |
| MODE_COD | C1 | Test mode: A=AEL/Production, D=Debug, E=Engineering, Q=QA |
| RTST_COD | C1 | Lot retest code |
| PROT_COD | C1 | Data protection code |
| BURN_TIM | U2 | Burn-in time (minutes) |
| CMOD_COD | C1 | Command mode code |
| LOT_ID | Cn | Lot ID string (primary identifier) |
| PART_TYP | Cn | Device/part type name |
| NODE_NAM | Cn | Tester node name (hostname) |
| TSTR_TYP | Cn | Tester type (e.g., "V93000") |
| JOB_NAM | Cn | Test program name |
| JOB_REV | Cn | Test program revision |
| SBLOT_ID | Cn | Sublot ID |
| OPER_NAM | Cn | Operator name or ID |
| EXEC_TYP | Cn | Test executive software type |
| EXEC_VER | Cn | Test executive software version |
| TEST_COD | Cn | Test phase code (e.g., "WAT", "EWS", "FT") |
| TST_TEMP | Cn | Test temperature as string (e.g., "25C", "-40C", "125C") |
| USER_TXT | Cn | User-defined text |
| AUX_FILE | Cn | Auxiliary data file name |
| PKG_TYP | Cn | Package type |
| FAMLY_ID | Cn | Product family ID |
| DATE_COD | Cn | Date code |
| FACIL_ID | Cn | Facility ID |
| FLOOR_ID | Cn | Test floor ID |
| PROC_ID | Cn | Process ID |
| OPER_FRQ | Cn | Operation frequency |
| SPEC_NAM | Cn | Test specification name |
| SPEC_VER | Cn | Test specification version |
| FLOW_ID | Cn | Test flow ID |
| SETUP_ID | Cn | Setup ID |
| DSGN_REV | Cn | Design revision |
| ENG_ID | Cn | Engineering lot ID |
| ROM_COD | Cn | ROM code ID |
| SERL_NUM | Cn | Tester serial number |
| SUPR_NAM | Cn | Supervisor name |

---

### 3.3 MRR — Master Results Record

**Purpose:** Closes the file. Always the last record written.

| Field | Type | Description |
|-------|------|-------------|
| FINISH_T | U4 | Lot finish time (Unix timestamp) |
| DISP_COD | C1 | Lot disposition code |
| USR_DESC | Cn | User description of lot disposition |
| EXC_DESC | Cn | Executive description |

---

### 3.4 SDR — Site Description Record

**Purpose:** Describes the test hardware configuration for each site group (handler, DIB, cables, etc.).

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Test head number |
| SITE_GRP | U1 | Site group number |
| SITE_CNT | U1 | Number of test sites in this group |
| SITE_NUM | kxU1 | Array of site numbers |
| HAND_TYP | Cn | Handler type |
| HAND_ID | Cn | Handler ID |
| CARD_TYP | Cn | Probe card type |
| CARD_ID | Cn | Probe card ID |
| LOAD_TYP | Cn | Load board type |
| LOAD_ID | Cn | Load board ID |
| DIB_TYP | Cn | DIB (Device Interface Board) type |
| DIB_ID | Cn | DIB ID |
| CABL_TYP | Cn | Cable type |
| CABL_ID | Cn | Cable ID |
| CONT_TYP | Cn | Contactor type |
| CONT_ID | Cn | Contactor ID |
| LASR_TYP | Cn | Laser type (for laser marking) |
| LASR_ID | Cn | Laser ID |
| EXTR_TYP | Cn | Extracter type |
| EXTR_ID | Cn | Extracter ID |

---

### 3.5 WCR — Wafer Configuration Record

**Purpose:** Defines wafer geometry and die layout. One per STDF file when wafer probing is used.

| Field | Type | Description |
|-------|------|-------------|
| WAFR_SIZ | R4 | Wafer diameter in WF_UNITS |
| DIE_HT | R4 | Die height in WF_UNITS |
| DIE_WID | R4 | Die width in WF_UNITS |
| WF_UNITS | U1 | Units: 1=inches, 2=cm, 3=mm, 4=mils |
| WF_FLAT | C1 | Wafer flat orientation: U=up, D=down, L=left, R=right |
| CENTER_X | I2 | X coordinate of center die |
| CENTER_Y | I2 | Y coordinate of center die |
| POS_X | C1 | Direction of X axis increase: L=left, R=right |
| POS_Y | C1 | Direction of Y axis increase: U=up, D=down |

---

### 3.6 WIR — Wafer Information Record

**Purpose:** Opens a wafer section. Paired with WRR. All die records for this wafer appear between WIR and WRR.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Test head number |
| SITE_GRP | U1 | Site group (refers to SDR) |
| START_T | U4 | Wafer test start time (Unix timestamp) |
| WAFER_ID | Cn | Wafer ID string |

---

### 3.7 WRR — Wafer Results Record

**Purpose:** Closes a wafer section. Summarizes results for one wafer.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Test head number |
| SITE_GRP | U1 | Site group |
| FINISH_T | U4 | Wafer test finish time (Unix timestamp) |
| PART_CNT | U4 | Total parts tested on wafer |
| RTST_CNT | U4 | Number of retested parts |
| ABRT_CNT | U4 | Number of aborted tests |
| GOOD_CNT | U4 | Number of good (passing) parts |
| FUNC_CNT | U4 | Number of functionally tested parts |
| WAFER_ID | Cn | Wafer ID |
| FABWF_ID | Cn | Fab wafer ID (ID during fabrication — for correlation with fab data) |
| FRAME_ID | Cn | Frame ID (post-saw, when wafer ID is no longer readable) |
| MASK_ID | Cn | Mask set ID |
| USR_DESC | Cn | User description |
| EXC_DESC | Cn | Executive description |

**Key yield fields:** PART_CNT, GOOD_CNT, ABRT_CNT, RTST_CNT. Wafer yield = GOOD_CNT / PART_CNT.

---

### 3.8 PIR — Part Information Record

**Purpose:** Opens a die (part) test sequence. One PIR per die. Paired with PRR.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Test head number |
| SITE_NUM | U1 | Test site number (for parallel/multi-site testing) |

---

### 3.9 PRR — Part Results Record

**Purpose:** Closes a die test sequence. Contains die coordinates, bin assignment, and pass/fail.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Test head number |
| SITE_NUM | U1 | Test site number |
| PART_FLG | B1 | Part flags (bit field — see below) |
| NUM_TEST | U2 | Number of tests executed for this part |
| HARD_BIN | U2 | Hardware bin number (0–32767) |
| SOFT_BIN | U2 | Software bin number (0–32767, 65535=missing) |
| X_COORD | I2 | Die X coordinate (-32767 to 32767) |
| Y_COORD | I2 | Die Y coordinate (-32767 to 32767) |
| TEST_T | U4 | Elapsed test time in milliseconds |
| PART_ID | Cn | Part serial number |
| PART_TXT | Cn | Part description text |
| PART_FIX | Bn | Repair information (application-specific) |

**PART_FLG bit definitions:**
- Bit 0: 1 = Die retest (supersedes prior record with same X,Y)
- Bit 1: 1 = Die retested due to previous failure
- Bit 2: 1 = Abnormal end of testing
- Bit 3: 0 = Pass, 1 = Fail
- Bit 4: 1 = Pass/fail not determined (bit 3 invalid)

**Bin conventions (common industry practice):**
- HARD_BIN 1 = Pass
- HARD_BIN 2–9 = Functional fail categories
- HARD_BIN 10+ = Parametric fail categories
- SOFT_BIN provides finer-grained classification within hardware bins

---

### 3.10 PTR — Parametric Test Record

**Purpose:** Stores a single numeric measurement result for one parametric test on one die. This is the most important record for yield and trend analysis. One PTR per test per die.

| Field | Type | Description |
|-------|------|-------------|
| TEST_NUM | U4 | Test number (unique ID in test program) |
| HEAD_NUM | U1 | Test head number |
| SITE_NUM | U1 | Test site number |
| TEST_FLG | B1 | Test flags (bit field — see below) |
| PARM_FLG | B1 | Parametric test flags (bit field — see below) |
| RESULT | R4 | Measured value (float, in units of UNITS field) |
| TEST_TXT | Cn | Test name/description (max 255 chars) |
| ALARM_ID | Cn | Alarm ID if alarm triggered |
| OPT_FLAG | B1 | Optional data flag (indicates which optional fields are valid) |
| RES_SCAL | I1 | Result scaling exponent (e.g., -3 = milli, -6 = micro) |
| LLM_SCAL | I1 | Low limit scaling exponent |
| HLM_SCAL | I1 | High limit scaling exponent |
| LO_LIMIT | R4 | Low test limit |
| HI_LIMIT | R4 | High test limit |
| UNITS | Cn | Units string (e.g., "mA", "V", "MHz", "ohm") |
| C_RESFMT | Cn | Result printf format string |
| C_LLMFMT | Cn | Low limit printf format string |
| C_HLMFMT | Cn | High limit printf format string |
| LO_SPEC | R4 | Low specification limit (design spec, may differ from test limit) |
| HI_SPEC | R4 | High specification limit |

**TEST_FLG bit definitions:**
- Bit 0: 1 = Alarm condition
- Bit 1: 1 = Result is unreliable
- Bit 2: 1 = Timeout occurred
- Bit 3: 1 = Test not executed
- Bit 4: 1 = Test aborted
- Bit 5: 1 = Pass/fail flag invalid
- Bit 6: 1 = Test failed

**PARM_FLG bit definitions:**
- Bit 0: 1 = Alarm triggered
- Bit 1: 1 = Result is outside limits but test flag shows pass (overridden)
- Bit 2: 1 = Result is zero
- Bit 3: 1 = Result negative (for unsigned format strings)
- Bit 4: 1 = Low limit value is equal to high limit value
- Bit 5: 1 = Low limit is not strict (>=  vs >)
- Bit 6: 1 = High limit is not strict (<=  vs <)

**Result scaling:** Actual value = RESULT × 10^RES_SCAL
Example: RESULT=45.3, RES_SCAL=-3, UNITS="A" → actual = 45.3 mA

**Important note:** The first PTR occurrence for each TEST_NUM in the file contains the test definition (limits, name, units). Subsequent PTRs for the same TEST_NUM may omit these optional fields to save space.

---

### 3.11 MPR — Multiple-Result Parametric Record

**Purpose:** Stores an array of parametric results from a single test execution where the same test is applied to multiple pins or repeated structures. Common for continuity tests, leakage sweeps, frequency sweeps.

| Field | Type | Description |
|-------|------|-------------|
| TEST_NUM | U4 | Test number |
| HEAD_NUM | U1 | Test head number |
| SITE_NUM | U1 | Test site number |
| TEST_FLG | B1 | Test flags (same as PTR) |
| RTN_ICNT | U2 | Count of PMR indexes with return states |
| RSLT_CNT | U2 | Count of result values |
| RTN_STAT | kxN1 | Array of return states (one per pin) |
| RTN_RSLT | kxR4 | Array of measured values (one per pin) |
| TEST_TXT | Cn | Test description |
| ALARM_ID | Cn | Alarm ID |
| OPT_FLAG | B1 | Optional data flag |
| RES_SCAL | I1 | Result scaling exponent |
| LLM_SCAL | I1 | Low limit scaling exponent |
| HLM_SCAL | I1 | High limit scaling exponent |
| LO_LIMIT | R4 | Low limit (same for all results) |
| HI_LIMIT | R4 | High limit (same for all results) |
| UNITS | Cn | Units string |
| UNITS_IN | Cn | Input units (for sweeps) |
| C_RESFMT | Cn | Result format string |
| LO_SPEC | R4 | Low spec limit |
| HI_SPEC | R4 | High spec limit |
| RTN_INDX | kxU2 | Array of PMR indexes (pin numbers being tested) |

---

### 3.12 FTR — Functional Test Record

**Purpose:** Stores pass/fail result for one functional test (pattern-based test, scan test, BIST). No measured value — only pass/fail status and failure address information.

| Field | Type | Description |
|-------|------|-------------|
| TEST_NUM | U4 | Test number |
| HEAD_NUM | U1 | Test head number |
| SITE_NUM | U1 | Test site number |
| TEST_FLG | B1 | Test flags (same as PTR) |
| OPT_FLAG | B1 | Optional data flag |
| CYCL_CNT | U4 | Cycle count of vector where failure occurred |
| REL_VADR | U4 | Relative vector address of first failure |
| REPT_CNT | U4 | Number of times the test was repeated |
| NUM_FAIL | U4 | Number of failures in the test |
| XFAIL_AD | I4 | X coordinate of failure (for memory/array tests) |
| YFAIL_AD | I4 | Y coordinate of failure (for memory/array tests) |
| VECT_OFF | I2 | Vector offset from CYCL_CNT |
| RTN_ICNT | U2 | Number of pins with return data |
| PGM_ICNT | U2 | Number of programmed state entries |
| RTN_INDX | kxU2 | Array of PMR indexes of failing pins |
| RTN_STAT | kxN1 | Return states of failing pins |
| PGM_INDX | kxU2 | Array of programmed PMR indexes |
| PGM_STAT | kxN1 | Programmed states |
| FAIL_PIN | Dn | Bit-encoded failing pin map |
| VECT_NAM | Cn | Vector pattern name |
| TIME_SET | Cn | Timeset name |
| OP_CODE | Cn | Operation code |
| TEST_TXT | Cn | Test description |
| ALARM_ID | Cn | Alarm ID |
| PROG_TXT | Cn | Additional programmed info |
| RSLT_TXT | Cn | Additional result info |
| PATG_NUM | U1 | Pattern generator number |
| SPIN_MAP | Dn | Bit-encoded map of pins with strobe information |

---

### 3.13 TSR — Test Synopsis Record

**Purpose:** Provides a statistical summary of all executions of a single test across the entire lot. Appears once per test, after all die data.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Head number (255 = summary across all heads) |
| SITE_NUM | U1 | Site number (255 = summary across all sites) |
| TEST_TYP | C1 | Test type: P=Parametric, F=Functional, M=Multiple-result |
| TEST_NUM | U4 | Test number |
| EXEC_CNT | U4 | Total executions |
| FAIL_CNT | U4 | Total failures |
| ALRM_CNT | U4 | Total alarms |
| TEST_NAM | Cn | Test name |
| SEQ_NAME | Cn | Sequence name |
| TEST_LBL | Cn | Test label |
| OPT_FLAG | B1 | Optional field validity flag |
| TEST_TIM | R4 | Average test time per execution (seconds) |
| TEST_MIN | R4 | Minimum result value |
| TEST_MAX | R4 | Maximum result value |
| TST_SUMS | R4 | Sum of all result values |
| TST_SQRS | R4 | Sum of squares of all result values |

**Note:** Mean = TST_SUMS / EXEC_CNT. Variance = (TST_SQRS / EXEC_CNT) - Mean². TSR records provide lot-level statistics without re-reading all PTRs.

---

### 3.14 PCR — Part Count Record

**Purpose:** Summarizes part counts per site or overall. Multiple PCRs may appear — one per site and one for the total (HEAD_NUM=255, SITE_NUM=255).

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Head number (255 = all heads) |
| SITE_NUM | U1 | Site number (255 = all sites) |
| PART_CNT | U4 | Total parts tested |
| RTST_CNT | U4 | Retested parts |
| ABRT_CNT | U4 | Aborted parts |
| GOOD_CNT | U4 | Passing parts |
| FUNC_CNT | U4 | Functionally tested parts |

---

### 3.15 HBR — Hardware Bin Record

**Purpose:** Counts parts assigned to each physical hardware bin after test. In wafer probe, "physical" binning means ink dot or wafer map entry — not physical movement.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Head (255 = total for all heads) |
| SITE_NUM | U1 | Site (255 = total for all sites) |
| HBIN_NUM | U2 | Hardware bin number (0–32767) |
| HBIN_CNT | U4 | Count of parts in this bin |
| HBIN_PF | C1 | Pass/fail indicator: P=pass, F=fail |
| HBIN_NAM | Cn | Bin name/description |

---

### 3.16 SBR — Software Bin Record

**Purpose:** Same structure as HBR but for logical software bins. Software bins provide finer classification than hardware bins.

| Field | Type | Description |
|-------|------|-------------|
| HEAD_NUM | U1 | Head number |
| SITE_NUM | U1 | Site number |
| SBIN_NUM | U2 | Software bin number |
| SBIN_CNT | U4 | Count of parts |
| SBIN_PF | C1 | P=pass, F=fail |
| SBIN_NAM | Cn | Bin name/description |

---

### 3.17 PMR — Pin Map Record

**Purpose:** Maps a logical PMR index to a physical pin/channel. Required when using MPR or FTR records that reference pins by index.

| Field | Type | Description |
|-------|------|-------------|
| PMR_INDX | U2 | PMR index number (1–32767, unique) |
| CHAN_TYP | U2 | Channel type |
| CHAN_NAM | Cn | Channel name (tester channel identifier) |
| PHY_NAM | Cn | Physical pin name on device |
| LOG_NAM | Cn | Logical pin name (from netlist) |
| HEAD_NUM | U1 | Head number |
| SITE_NUM | U1 | Site number |

---

### 3.18 GDR — Generic Data Record

**Purpose:** Stores custom, non-standard data in a variable-format record. Used for application-specific extensions.

| Field | Type | Description |
|-------|------|-------------|
| FLD_CNT | U2 | Number of data fields |
| GEN_DATA | Vn | Array of typed data fields (each field is self-describing) |

---

### 3.19 DTR — Datalog Text Record

**Purpose:** Stores a free-text string. Used for tester print statements, comments, or debug messages during test.

| Field | Type | Description |
|-------|------|-------------|
| TEXT_DAT | Cn | Text string (max 255 chars) |

---

## 4. DATA TYPES

| Code | Size | Description |
|------|------|-------------|
| U1 | 1 byte | Unsigned integer (0–255) |
| U2 | 2 bytes | Unsigned integer (0–65535) |
| U4 | 4 bytes | Unsigned integer (0–4,294,967,295) |
| I1 | 1 byte | Signed integer (-128 to 127) |
| I2 | 2 bytes | Signed integer (-32768 to 32767) |
| I4 | 4 bytes | Signed integer |
| R4 | 4 bytes | IEEE 754 single-precision float |
| R8 | 8 bytes | IEEE 754 double-precision float |
| C1 | 1 byte | Single character |
| Cn | 1+n bytes | Variable-length string (first byte = length, then chars) |
| Bn | 1+n bytes | Variable-length bit-encoded string |
| Dn | 2+n bytes | Bit-encoded array (first 2 bytes = bit count) |
| N1 | 0.5 bytes | Nibble (4-bit value, two packed per byte) |
| kxT | k × size | Array of k items of type T |

**Byte order:** Determined by CPU_TYPE in FAR. CPU_TYPE=2 (most common modern testers) = little-endian (x86 style).

**Timestamps:** All time fields (SETUP_T, START_T, FINISH_T, etc.) are U4 Unix timestamps (seconds since Jan 1, 1970 00:00:00 local time).

**Missing values:**
- U1: 255, U2: 65535, U4: 4,294,967,295
- I2: -32768
- R4: depends on OPT_FLAG bits
- Cn: empty string (length byte = 0)

---

## 5. WAFER TEST CONCEPTS

### Multi-Site Testing

Modern probers test multiple dice simultaneously using parallel probe cards. Each die is tested at a different site. HEAD_NUM identifies the test head (usually 1), SITE_NUM identifies which die position (1–N) within that head. PIR/PRR pairs are written per site. All sites share the same WIR/WRR bracket.

### X,Y Coordinates

Die coordinates in PRR (X_COORD, Y_COORD) are in die-step units, not physical millimeters. The center die is typically (0,0) or defined by CENTER_X, CENTER_Y in WCR. Legal range: -32767 to 32767. Coordinates are used to build the wafer map.

### Binning in Wafer Probe

In final package test, binning physically moves the part to a bin. In wafer probe, binning is represented by an ink dot on the die (for failing parts) or a wafer map entry. The ATE writes HARD_BIN in the PRR; the wafer map system reads this to know which die are pass/fail.

### Test Temperature

TST_TEMP in MIR is a string (e.g., "25C", "-40C", "125C"). A full lot may be tested at multiple temperatures — each temperature generates a separate STDF file.

### EWS vs WAT

TEST_COD in MIR identifies the test phase:
- EWS (Electrical Wafer Sort) = production wafer probe, full test program, all dice
- WAT (Wafer Acceptance Test) = process control structures, not product dice
- CP (Circuit Probe) = alternative term for EWS at some fabs

---

## 6. MINIMAL EXAMPLE: GENERATING AN STDF FILE IN PYTHON

```python
"""
Minimal STDF V4 generator for wafer probe data.
Produces: FAR, MIR, WCR, WIR, PIR, PTR (x2), PRR, WRR, PCR, HBR, MRR
Requires: Python standard library only (struct module)
"""

import struct
import time

def write_record(f, rec_typ, rec_sub, data: bytes):
    """Write one STDF record with 4-byte header."""
    header = struct.pack('<HBB', len(data), rec_typ, rec_sub)
    f.write(header + data)

def cn(s: str) -> bytes:
    """Encode a variable-length string (Cn type)."""
    if s is None or s == '':
        return b'\x00'
    encoded = s.encode('ascii')
    return bytes([len(encoded)]) + encoded

def u1(v): return struct.pack('<B', v)
def u2(v): return struct.pack('<H', v)
def u4(v): return struct.pack('<I', v)
def i2(v): return struct.pack('<h', v)
def r4(v): return struct.pack('<f', v)
def c1(v): return v.encode('ascii') if v else b' '
def timestamp(t=None): return u4(int(t or time.time()))

# ─── Open output file ───────────────────────────────────────────────
with open('example_wafer.stdf', 'wb') as f:

    # FAR — File Attributes Record (REC_TYP=0, REC_SUB=10)
    # CPU_TYPE=2 (little-endian/x86), STDF_VER=4
    write_record(f, 0, 10, u1(2) + u1(4))

    # MIR — Master Information Record (REC_TYP=1, REC_SUB=10)
    now = int(time.time())
    mir_data = (
        u4(now - 3600) +   # SETUP_T
        u4(now) +          # START_T
        u1(1) +            # STAT_NUM
        c1('P') +          # MODE_COD (Production)
        c1(' ') +          # RTST_COD
        c1(' ') +          # PROT_COD
        u2(0) +            # BURN_TIM
        c1(' ') +          # CMOD_COD
        cn('LOT2024A') +   # LOT_ID
        cn('CHIP_XYZ') +   # PART_TYP
        cn('TESTER01') +   # NODE_NAM
        cn('V93000') +     # TSTR_TYP
        cn('prog_v1.tf') + # JOB_NAM
        cn('1.0') +        # JOB_REV
        cn('') +           # SBLOT_ID
        cn('OPER1') +      # OPER_NAM
        cn('SmarTest') +   # EXEC_TYP
        cn('8.0') +        # EXEC_VER
        cn('EWS') +        # TEST_COD
        cn('25C')          # TST_TEMP
    )
    write_record(f, 1, 10, mir_data)

    # WCR — Wafer Configuration Record (REC_TYP=2, REC_SUB=30)
    wcr_data = (
        r4(300.0) +  # WAFR_SIZ (300mm wafer)
        r4(5.0) +    # DIE_HT (5mm)
        r4(5.0) +    # DIE_WID (5mm)
        u1(3) +      # WF_UNITS (3=mm)
        c1('D') +    # WF_FLAT (flat at bottom)
        i2(0) +      # CENTER_X
        i2(0) +      # CENTER_Y
        c1('R') +    # POS_X (X increases right)
        c1('U')      # POS_Y (Y increases up)
    )
    write_record(f, 2, 30, wcr_data)

    # WIR — Wafer Information Record (REC_TYP=2, REC_SUB=10)
    wir_data = u1(1) + u1(255) + u4(now) + cn('W01')
    write_record(f, 2, 10, wir_data)

    # ── Die 1: (X=3, Y=5) ───────────────────────────────────────────

    # PIR — Part Information Record (REC_TYP=5, REC_SUB=10)
    write_record(f, 5, 10, u1(1) + u1(1))  # HEAD=1, SITE=1

    # PTR — Test 1000: VDD_CURRENT (REC_TYP=15, REC_SUB=10)
    ptr_data = (
        u4(1000) +         # TEST_NUM
        u1(1) +            # HEAD_NUM
        u1(1) +            # SITE_NUM
        u1(0b00000000) +   # TEST_FLG (pass, all flags clear)
        u1(0b00000000) +   # PARM_FLG
        r4(45.3) +         # RESULT (45.3 mA)
        cn('VDD_CURRENT') +# TEST_TXT
        cn('') +           # ALARM_ID
        u1(0b00000010) +   # OPT_FLAG (bit1: LO_LIMIT valid, bit0: HI_LIMIT valid)
        u1(0xFD) +         # RES_SCAL = -3 (milli)
        u1(0xFD) +         # LLM_SCAL = -3
        u1(0xFD) +         # HLM_SCAL = -3
        r4(30.0) +         # LO_LIMIT (30 mA)
        r4(60.0) +         # HI_LIMIT (60 mA)
        cn('mA')           # UNITS
    )
    write_record(f, 15, 10, ptr_data)

    # PTR — Test 1010: LEAKAGE
    ptr2_data = (
        u4(1010) +
        u1(1) + u1(1) +
        u1(0) +            # TEST_FLG (pass)
        u1(0) +            # PARM_FLG
        r4(0.018) +        # RESULT (18 nA — within 50nA limit)
        cn('LEAKAGE') +
        cn('') +
        u1(0b00000010) +
        u1(0xFA) +         # RES_SCAL = -6 (micro)
        u1(0xFA) +
        u1(0xFA) +
        r4(0.0) +          # LO_LIMIT (0)
        r4(0.05) +         # HI_LIMIT (50 nA)
        cn('uA')
    )
    write_record(f, 15, 10, ptr2_data)

    # PRR — Part Results Record (REC_TYP=5, REC_SUB=20)
    prr_data = (
        u1(1) +            # HEAD_NUM
        u1(1) +            # SITE_NUM
        u1(0b00000000) +   # PART_FLG (bit3=0: PASS)
        u2(2) +            # NUM_TEST (2 tests run)
        u2(1) +            # HARD_BIN (1 = pass bin)
        u2(1) +            # SOFT_BIN (1 = pass)
        i2(3) +            # X_COORD
        i2(5) +            # Y_COORD
        u4(150) +          # TEST_T (150 ms)
        cn('DIE_3_5')      # PART_ID
    )
    write_record(f, 5, 20, prr_data)

    # ── Die 2: (X=4, Y=5) — FAIL on LEAKAGE ────────────────────────

    write_record(f, 5, 10, u1(1) + u1(1))  # PIR

    # PTR 1000 — pass
    ptr3_data = (
        u4(1000) + u1(1) + u1(1) +
        u1(0) + u1(0) +
        r4(47.1) +         # RESULT (pass)
        cn('VDD_CURRENT') + cn('') +
        u1(0b00000010) +
        u1(0xFD) + u1(0xFD) + u1(0xFD) +
        r4(30.0) + r4(60.0) + cn('mA')
    )
    write_record(f, 15, 10, ptr3_data)

    # PTR 1010 — FAIL (0.08 uA exceeds 0.05 uA limit)
    ptr4_data = (
        u4(1010) + u1(1) + u1(1) +
        u1(0b01000000) +   # TEST_FLG bit6=1: FAIL
        u1(0) +
        r4(0.08) +         # RESULT (fail — above HI_LIMIT)
        cn('LEAKAGE') + cn('') +
        u1(0b00000010) +
        u1(0xFA) + u1(0xFA) + u1(0xFA) +
        r4(0.0) + r4(0.05) + cn('uA')
    )
    write_record(f, 15, 10, ptr4_data)

    # PRR — FAIL, bin 5
    prr2_data = (
        u1(1) + u1(1) +
        u1(0b00001000) +   # PART_FLG bit3=1: FAIL
        u2(2) +
        u2(5) +            # HARD_BIN 5 (leakage fail bin)
        u2(10) +           # SOFT_BIN 10
        i2(4) + i2(5) +
        u4(155) +
        cn('DIE_4_5')
    )
    write_record(f, 5, 20, prr2_data)

    # WRR — Wafer Results Record (REC_TYP=2, REC_SUB=20)
    wrr_data = (
        u1(1) +            # HEAD_NUM
        u1(255) +          # SITE_GRP
        u4(now + 600) +    # FINISH_T
        u4(2) +            # PART_CNT
        u4(0) +            # RTST_CNT
        u4(0) +            # ABRT_CNT
        u4(1) +            # GOOD_CNT (1 pass out of 2)
        u4(2) +            # FUNC_CNT
        cn('W01')          # WAFER_ID
    )
    write_record(f, 2, 20, wrr_data)

    # PCR — Part Count Record (REC_TYP=1, REC_SUB=30)
    pcr_data = (
        u1(255) + u1(255) +  # HEAD=255, SITE=255 (total)
        u4(2) +              # PART_CNT
        u4(0) +              # RTST_CNT
        u4(0) +              # ABRT_CNT
        u4(1) +              # GOOD_CNT
        u4(2)                # FUNC_CNT
    )
    write_record(f, 1, 30, pcr_data)

    # HBR — Hardware Bin Records (REC_TYP=1, REC_SUB=40)
    hbr_pass = (
        u1(255) + u1(255) +
        u2(1) +          # HBIN_NUM (bin 1 = pass)
        u4(1) +          # HBIN_CNT
        c1('P') +        # HBIN_PF
        cn('PASS')       # HBIN_NAM
    )
    write_record(f, 1, 40, hbr_pass)

    hbr_fail = (
        u1(255) + u1(255) +
        u2(5) +          # HBIN_NUM (bin 5 = leakage fail)
        u4(1) +          # HBIN_CNT
        c1('F') +        # HBIN_PF
        cn('LEAKAGE_FAIL')
    )
    write_record(f, 1, 40, hbr_fail)

    # MRR — Master Results Record (REC_TYP=1, REC_SUB=20)
    mrr_data = u4(now + 700) + c1('U') + cn('') + cn('')
    write_record(f, 1, 20, mrr_data)

print("STDF file written: example_wafer.stdf")
```

---

## 7. PARSING STDF IN PYTHON (READING BACK)

```python
import pystdf.V4 as stdf
import pandas as pd

TESTS_OF_INTEREST = {1000, 1010}  # filter to specific test numbers

records = []

with open('example_wafer.stdf', 'rb') as f:
    parser = stdf.Parser(inp=f)
    for rec in parser:
        name = rec.__class__.__name__
        
        if name == 'Ptr':  # PTR record
            test_num = rec.fields[0][1]
            if test_num not in TESTS_OF_INTEREST:
                continue
            records.append({
                'record':    'PTR',
                'test_num':  test_num,
                'head':      rec.fields[1][1],
                'site':      rec.fields[2][1],
                'test_flg':  rec.fields[3][1],
                'result':    rec.fields[5][1],
                'test_name': rec.fields[6][1],
                'lo_limit':  rec.fields[13][1],
                'hi_limit':  rec.fields[14][1],
                'units':     rec.fields[15][1],
                'pass':      not bool(rec.fields[3][1] & 0b01000000),
            })
        
        elif name == 'Prr':  # PRR record
            records.append({
                'record':    'PRR',
                'head':      rec.fields[0][1],
                'site':      rec.fields[1][1],
                'part_flg':  rec.fields[2][1],
                'hard_bin':  rec.fields[4][1],
                'soft_bin':  rec.fields[5][1],
                'x_coord':   rec.fields[6][1],
                'y_coord':   rec.fields[7][1],
            })

df = pd.DataFrame(records)
print(df)
```

---

## 8. COMMON ANALYSIS PATTERNS

### Yield Calculation
```python
# From WRR or PCR
yield_pct = (good_cnt / part_cnt) * 100

# From parsed PRR records
df_prr = df[df.record == 'PRR']
yield_pct = (df_prr.hard_bin == 1).mean() * 100
```

### Cpk Calculation per Test
```python
from scipy import stats
import numpy as np

def cpk(values, lo_limit, hi_limit):
    mean = np.mean(values)
    std  = np.std(values, ddof=1)
    if std == 0:
        return float('inf')
    cpu = (hi_limit - mean) / (3 * std)
    cpl = (mean - lo_limit) / (3 * std)
    return min(cpu, cpl)

for test_num, group in df[df.record == 'PTR'].groupby('test_num'):
    results = group['result'].dropna()
    lo = group['lo_limit'].iloc[0]
    hi = group['hi_limit'].iloc[0]
    print(f"Test {test_num}: Cpk={cpk(results, lo, hi):.3f}")
```

### Trend Detection Across Wafers
```python
# Assumes 'wafer_id' column available (correlate from WIR context during parse)
from scipy import stats

for test_num, group in df[df.record == 'PTR'].groupby('test_num'):
    wafer_means = group.groupby('wafer_id')['result'].mean()
    x = np.arange(len(wafer_means))
    slope, intercept, r, p, se = stats.linregress(x, wafer_means.values)
    if p < 0.05:
        print(f"Test {test_num}: SIGNIFICANT TREND slope={slope:.4f} p={p:.4f}")
```

### Site-to-Site Variation
```python
for test_num, group in df[df.record == 'PTR'].groupby('test_num'):
    site_means = group.groupby('site')['result'].mean()
    site_range = site_means.max() - site_means.min()
    print(f"Test {test_num}: site range = {site_range:.4f}")
```

---

## 9. KEY LIMITATIONS AND GOTCHAS

**TEST_TXT is max 255 characters.** Engineers use naming conventions like prefixes and codes because descriptions are length-limited.

**First PTR carries the definition.** For any given TEST_NUM, the first PTR in the file includes limits, units, and format strings. Subsequent PTRs for the same test may omit these fields (OPT_FLAG marks them absent). Always look up the first occurrence for test metadata.

**Scaling exponents.** RES_SCAL is a signed byte. Value 0xFD = -3 (milli), 0xFA = -6 (micro), 0xF7 = -9 (nano). Actual value = RESULT × 10^RES_SCAL.

**Endianness.** CPU_TYPE in FAR determines byte order. Always check this before parsing numeric fields.

**Missing values.** Fields not written by the tester show as maximum unsigned values (U2 → 65535, U1 → 255). Always check OPT_FLAG before trusting optional fields.

**Binary format.** STDF cannot be read with a text editor. Use pystdf (Python), libstdf (C/C++), or STDFUtils (Java).

**File size.** A single lot with 25 wafers, 2000 dice/wafer, and 500 tests = 25M PTR records. Files can reach several hundred MB.

**One lot per file** is convention, but the format technically allows more. Some fabs merge lots — always check MIR.LOT_ID.

---

## 10. GLOSSARY

| Term | Meaning |
|------|---------|
| ATE | Automated Test Equipment |
| Die | Individual chip on a wafer (also: part, DUT) |
| DUT | Device Under Test |
| EWS | Electrical Wafer Sort (production wafer probe) |
| WAT | Wafer Acceptance Test (process control, not product) |
| CP | Circuit Probe (alternative term for EWS) |
| Bin | Category assigned to a die after test |
| Hard bin | Physical hardware bin assignment |
| Soft bin | Logical software bin (finer classification) |
| Probe card | PCB with needles that contacts wafer die pads |
| Prober | Robot that moves the wafer to bring each die under the probe card |
| Site | One position under the probe card (multi-site = parallel testing of N dice) |
| Cpk | Process capability index: how well process fits within limits |
| PTR | Parametric Test Record (one numeric measurement) |
| FTR | Functional Test Record (pass/fail for pattern-based test) |
| MPR | Multiple-Result Parametric (array of measurements, one per pin) |
| PIR/PRR | Part Info/Results Record (brackets one die's test data) |
| WIR/WRR | Wafer Info/Results Record (brackets one wafer's test data) |
| MIR/MRR | Master Info/Results Record (lot-level, first and last records) |
| STDF | Standard Test Data Format |
| ATDF | ASCII Test Data Format (human-readable version of STDF) |

---

*Document version: 1.0 — Based on STDF V4 specification (Teradyne) and STDF V4-2007 specification.*
*Primary sources: STDF V4 Spec, pystdf library, yieldHUB, Semiconductor Engineering.*
