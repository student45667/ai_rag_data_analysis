# RAG Wafer Test Data Analysis Assistant

Local, offline AI assistant for semiconductor wafer test data analysis.

Wafer test data is IP. Yield numbers, parametric distributions, bin maps, and failure signatures are proprietary — they should never leave the building. This system runs entirely on your own hardware. No cloud API. No subscription. No data transmitted. The model loads from a local GGUF file, the vector database lives on your disk, and the browser UI talks only to `localhost`.

You describe what you want in plain English. The system retrieves relevant context from your ingested knowledge base — analysis guides, STDF references, JMP documentation, your own scripts — and returns a working answer grounded in that material. For code requests, you get a flat, readable Python or JSL script you can run immediately. For analysis questions, you get a direct answer with the metric explained and the reasoning shown. For visualization requests, you get a script that saves to file and displays — not a description of one.

The assistant covers the full analysis workflow: loading ATE exports, calculating yield and Cpk, generating wafer bin maps, flagging spatial outliers, building parametric correlation matrices, and producing JMP scripts for distribution reports and control charts. What takes an engineer two to four hours of repetitive scripting takes the system under a minute.

---

## What It Does

- **Python code generation** — yield analysis, Cpk, bin maps, outliers, correlation
- **JMP script generation** — JSL for distribution reports, control charts, scatter plots
- **Graph generation** — wafer heatmaps, histograms, box plots, Pareto, CDF, scatter matrix
- **RAG-grounded answers** — retrieves from your ingested knowledge base before every response
- **Streaming UI** — markdown + syntax-highlighted code rendered in browser as model generates

---

## Demo

```
> "Load circular_grid_params.csv and show yield % where BIN==1"

# ASSUMED: 'BIN' column contains hard bin number
# ASSUMED: 'X_COORD', 'Y_COORD' are integer die coordinates
# VERIFY:  confirm passing bin number with test engineer (often bin 1, not always)

import pandas as pd

# --- LOAD
df = pd.read_csv("circular_grid_params.csv")
print(df.head())
print(df.dtypes)

# --- ANALYZE
total = len(df)
passing = (df["BIN"] == 1).sum()
yield_pct = passing / total * 100
print(f"Yield: {passing}/{total} = {yield_pct:.1f}%")
```

```
> "Write a JMP script for a Cpk table of LEAKAGE_UA by wafer"

dt = Data Table("circular_grid_params");
col = Column(dt, "LEAKAGE_UA");
...
```

---

## Architecture

```
Browser (WEBRAG_simple.html)
    ↓  POST /stream
FastAPI  (WEBRAG_simple.py)
    ↓
ChromaDB query → top-5 chunks from data_analysis_files/
    ↓
Prompt builder → injects RAG context into system prompt
    ↓
Qwen3.5-9B-Q4_K_M  (llama-cpp-python, local GGUF)
    ↓  streaming tokens
Browser → marked.js + highlight.js + mermaid
```

---

## Project Structure

```
├── data_analysis_files/          ← RAG knowledge base
│   ├── 00-test-data-index.md
│   ├── 01-test-data-analysis-intro.md
│   ├── 02-test-data-understanding.md
│   ├── 03-test-data-statistics.md
│   ├── 04-test-data-control-charts.md
│   ├── 05-test-data-specifications.md
│   ├── 06-test-data-visualization.md
│   ├── 07-test-data-workflow.md
│   ├── 08-test-data-mistakes.md
│   ├── CIRCULAR_GRID_CODE_EXPLAINED.md
│   ├── FIXING_ATTRIBUTEERROR_EXPLAINED.md
│   ├── JMP_SCRIPTING_LANGUAGE_GUIDE.md
│   ├── JMP_USER_MANUAL_BEGINNERS.md
│   ├── STDF_Knowledge_Document.md
│   ├── STDF_Python_Scripts_RAG.md
│   ├── WAFER_ANALYSIS_COMPLETE_GUIDE.md
│   ├── wafer_comprehensive_charts.md
│   ├── wafer_sort_statistical_overview.md
│   ├── wafer_visualization_guide.md
│   ├── wafer_data_example.txt
│   ├── create_stdf.py
│   ├── stdf2csv_example.py
│   └── pdf2md.py
├── WEBRAG_INGEST.py              ← run once to populate ChromaDB
├── WEBRAG_simple.py              ← FastAPI server
└── WEBRAG_simple.html            ← browser UI
```

---

## Knowledge Base

The `data_analysis_files/` folder is what the model reads from — not its training data. Every answer is grounded in these documents.

| Category | Files |
|---|---|
| Analysis theory | `01–08` series — statistics, control charts, Cpk, visualization, workflow |
| Wafer analysis | Complete guide, chart library, statistical overview, visualization guide |
| STDF | Format spec, Python parsing scripts, record field reference |
| JMP | JSL syntax guide, UI manual, analysis workflows |
| Code examples | Circular grid generator, STDF creation, CSV conversion |
| Sample data | `wafer_data_example.txt` — grounds column name assumptions |

Add your own files (test plans, datasheets, ATE export samples, existing scripts) and re-ingest. The model learns your conventions.

---

## Setup

### Requirements

```bash
pip install llama-cpp-python fastapi uvicorn chromadb sentence-transformers
```

GPU build (recommended):
```bash
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python --force-reinstall
```

### Model

Download `Qwen3.5-9B-Q4_K_M.gguf` from HuggingFace and place at:
```
~/hugging_face_rag/models/qwen3.5-9b-q4/Qwen3.5-9B-Q4_K_M.gguf
```

Or edit `MODEL_PATH` in `WEBRAG_simple.py` to match your path.

### Ingest

```bash
python3 WEBRAG_INGEST.py ./data_analysis_files/
```

Output:
```
Found 23 file(s) to process
✅ DONE!
   Files processed:  23
   Total chunks:     1847
   Database:         ./chroma_db_data/
```

### Run

```bash
python3 WEBRAG_simple.py
```

Open browser: `http://localhost:8000`  
From another machine: `http://ai.local:8000`

---

## Configuration

All settings in `WEBRAG_simple.py`:

| Variable | Default | Description |
|---|---|---|
| `MODEL_PATH` | `~/hugging_face_rag/...` | Path to GGUF model |
| `CONTEXT_LEN` | `16384` | Context window tokens |
| `N_GPU_LAYERS` | `-1` | GPU layers (-1 = all) |
| `N_THREADS` | `16` | CPU threads |
| `MAX_TOKENS` | `4096` | Max output tokens |
| `CHROMA_PATH` | `./chroma_db_data` | Vector DB location |
| `COLLECTION_NAME` | `data_analysis` | ChromaDB collection |
| `RECENCY_BUFFER` | `3` | Recent turns kept in prompt |

---

## Supported File Types (Ingestion)

```
Code:           .c  .h  .cpp  .ino  .py  .js  .java
Documentation:  .md  .txt
Config:         .xml  .json
V93K SmarTest:  .tf  .lim  .spec  .pin  .lvl  .tim  .vec
```

---

## Hardware

Tested on:
- GPU: RTX 3070 8GB — all layers offloaded (`N_GPU_LAYERS = -1`)
- CPU: AMD Ryzen 7 5800X 16 threads
- RAM: 16 GB
- OS: Ubuntu

Minimum: 6 GB VRAM for Q4 7B model. 8 GB VRAM recommended for Q4 9B.

| Model | Quant | VRAM |
|---|---|---|
| Qwen3.5-9B | Q4_K_M | ~6.5 GB |
| Qwen2.5-Coder-7B | Q4_K_M | ~5.5 GB |

---

## Model Behavior

Thinking mode disabled by default (`/no_think` in system prompt).  
Type `/think` in your query to enable reasoning mode for complex tasks.

**Code output policy:**
- First response: minimal flat script only — no classes, no error handling
- After working code: one follow-up line offering improvements
- Vague request: one clarifying question before writing code

**Every generated script includes:**
```python
# ASSUMED: 'BIN' column contains hard bin number
# ASSUMED: 'X_COORD', 'Y_COORD' are integer die coordinates
# ASSUMED: 'WAFER_ID' and 'LOT_ID' columns exist for grouping
# VERIFY:  confirm passing bin number with test engineer (often bin 1, not always)
```

---

## Update Knowledge Base

Add new files to `data_analysis_files/` and re-run ingest:

```bash
python3 WEBRAG_INGEST.py ./data_analysis_files/
```

Chunks are keyed by file path — existing chunks are not duplicated on re-run.

---

## Stack

| Component | Library |
|---|---|
| LLM inference | llama-cpp-python (GGUF) |
| Model | Qwen3.5-9B-Q4_K_M |
| Embeddings | nomic-ai/nomic-embed-text-v1.5 |
| Vector store | ChromaDB (persistent, local) |
| Server | FastAPI + uvicorn |
| UI | Vanilla HTML/JS |
| Markdown | marked.js |
| Syntax highlight | highlight.js (VS2015 theme) |
| Diagrams | mermaid.js |

---

## License

MIT
