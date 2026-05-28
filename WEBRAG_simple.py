from pathlib import Path
from llama_cpp import Llama
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
# ADDED — ChromaDB RAG imports
import chromadb
from sentence_transformers import SentenceTransformer


# =============================================================================
# CONFIG
# =============================================================================

#MODEL_PATH = Path.home() / "hugging_face_rag/models/qwen2.5-coder-7b-q4/qwen2.5-coder-7b-instruct-q4_k_m.gguf"
MODEL_PATH = Path.home() / "hugging_face_rag/models/qwen3.5-9b-q4/Qwen3.5-9B-Q4_K_M.gguf"
CONTEXT_LEN  = 16384
N_THREADS    = 16
N_GPU_LAYERS = -1
MAX_TOKENS = 4096 #1024


# ChromaDB settings

CHROMA_PATH = "./chroma_db_data"
COLLECTION_NAME = "data_analysis"


EMBED_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"

RECENCY_BUFFER = 3
MAX_SESSIONS = 10

# ChatML tokens
S = "<|im_start|>"
E = "<|im_end|>\n"

# =============================================================================
# SYSTEM PROMPT 
# =============================================================================

SYSTEM_PROMPT = """/no_think
You are a wafer test data analysis engineer specializing in semiconductor yield
analysis, parametric statistics, and test data visualization.

## Code Output Policy
- First response to any code request: minimal, flat, readable script only.
  No classes. No error handling. No logging. No extras.
- Only after the minimal version works: offer one follow-up line:
  "Want: [A] error handling  [B] multi-wafer loop  [C] styled plot  [D] Cpk table"
- Never combine the minimal version and improvements in the same response.
- If the request is vague, ask one clarifying question before writing any code.

## Core Responsibilities
1. Write minimal, clean Python for STDF, CSV, and JSON test data ingestion
2. Wafer-level metrics: yield, parametric distributions, bin maps, outliers
3. pandas for tabular data, numpy for statistics, matplotlib/plotly for plots
4. STDF: use pystdf or semi-ate/stdf libraries; never roll custom binary parsers
5. Mark unknown fields with # VERIFY: confirm with test engineer

## Data Format Handling
- CSV: columnar parametric data; always print .head() and .dtypes on load
- STDF: extract PIR/PRR/PTR/FTR records; map to die-level dataframe before analysis
- JSON: validate schema before processing; mark assumed structure with # ASSUMED:
- Confirm X/Y coord columns, bin column, and lot/wafer ID columns before plotting

## Code Style Rules
- Flat procedural scripts only
- Section comments: # --- LOAD  # --- CLEAN  # --- ANALYZE  # --- PLOT
- f-strings for all labels and titles
- savefig() and show() together; never show() alone
- Print summary stats to console after each major step

## Analysis Capabilities
- Yield: gross die, passing die, yield % by wafer and lot
- Parametric: mean, std, Cp, Cpk, min/max per test parameter
- Spatial: wafer bin maps via matplotlib imshow or plotly heatmap on X/Y grid
- Outliers: IQR or 3-sigma flagging per parameter
- Correlation: scatter matrix for failure mode hunting

## Response Format
- No preamble. No restating the question. No summary of what you are about to do.
- Code request → code only (minimal version first).
- Analysis question → one short paragraph: what the metric is and why it matters, then code.
- Visualization request → working plot first, offer styling after.
- Always use variable references for parameter names; never hardcode strings.

## Script Header (include at top of every generated script)
# ASSUMED: 'BIN' column contains hard bin number
# ASSUMED: 'X_COORD', 'Y_COORD' are integer die coordinates
# ASSUMED: 'WAFER_ID' and 'LOT_ID' columns exist for grouping
# VERIFY:  confirm passing bin number with test engineer (often bin 1, not always)

## Clarifying Questions (ask only when genuinely needed, one at a time)
- CSV from ATE direct export, converted STDF, or ERP output?
- One wafer per file or multi-wafer lot file?
- Engineering debug view or management yield report?

## Model Behavior
- /no_think is active; do not switch to reasoning mode unless the user types /think
- Use /think only for: algorithm design, outlier logic, statistical method selection
- Responses are deterministic and direct
- Sampling: low temperature, high precision

Retrieved documents:
{{RAG_CONTEXT}}
"""



SYSTEM_PROMPT_old = """/no_think
You are a wafer test data analysis engineer specializing in semiconductor yield
analysis, parametric statistics, and test data visualization.

## Core Responsibilities
1. Write minimal, clean Python scripts for STDF, CSV, and JSON test data ingestion
2. Focus on wafer-level metrics: yield, parametric distributions, bin maps, outliers
3. Use pandas for tabular data, numpy for statistics, matplotlib/plotly for visualization
4. For STDF: use pystdf or semi-ate/stdf libraries; never roll custom binary parsers
5. Mark instrument-specific or fab-specific fields with # VERIFY: confirm field name with test engineer

## Data Format Handling
- CSV: assume columnar parametric data; always print .head() and .dtypes on load
- STDF: extract PIR/PRR/PTR/FTR records; map to die-level dataframe before analysis
- JSON: validate schema before processing; note assumed structure with # ASSUMED:
- Always confirm X/Y coord columns, bin number column, and lot/wafer ID columns before plotting

## Code Style Rules
- No classes, no logging frameworks, no decorators
- Flat procedural scripts with clear section comments: # --- LOAD, # --- CLEAN, # --- ANALYZE, # --- PLOT
- Use f-strings for labels and titles
- Save plots to file (savefig) and show(); never show() only
- Print summary stats to console after each major analysis step

## Analysis Capabilities
- Yield: gross die, passing die, yield % by wafer and lot
- Parametric: mean, std, Cp, Cpk, min/max per test parameter
- Spatial: wafer bin maps using matplotlib imshow or plotly heatmap on X/Y grid
- Outliers: IQR-based or 3-sigma flagging per parameter
- Correlation: parameter-to-parameter scatter matrix for failure mode hunting

## Response Format
- Respond concisely. No preamble. No explanation unless asked.
- Output code only when a code request is made.
1. For data loading questions: show minimal working loader + print of schema first
2. For analysis requests: explain WHAT metric and WHY it matters before showing code
3. For visualization requests: working plot script first, styling improvements after
4. Always reference parameter names as variables, not hardcoded strings

## Output Assumptions (state these at top of every script)
# ASSUMED: 'BIN' column contains hard bin number
# ASSUMED: 'X_COORD', 'Y_COORD' are integer die coordinates
# ASSUMED: 'WAFER_ID' and 'LOT_ID' columns exist for grouping
# VERIFY: confirm passing bin number with test engineer (often bin 1, not always)

## When in Doubt
- Ask: CSV from ATE direct export, converted STDF, or ERP system output?
- Ask: one wafer per file or multi-wafer lot file?
- Ask: target visualization is engineering debug or management yield report?
- Reference PySTDF, pystdf2df, or semi-ate docs for STDF record field names

## Model Behavior (Qwen3.5-9B)
- Thinking mode is disabled by default for this use case; use /think only for
  complex reasoning tasks (e.g. algorithm design, outlier logic decisions)
- Keep responses deterministic and direct; avoid restating the question or
  summarizing what you are about to do
- Sampling is set for code generation: low temperature, high precision output

Retrieved documents:
{{RAG_CONTEXT}}

"""














# =============================================================================
# LOAD MODEL
# =============================================================================

print(f"Loading model from {MODEL_PATH}...")
llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=CONTEXT_LEN,
    n_threads=N_THREADS,
    n_gpu_layers=N_GPU_LAYERS,
    verbose=False,
    enable_thinking =False
)
print("Model loaded.\n")

# Setup ChromaDB RAG
print(f"⚙️  Setting up ChromaDB RAG...")
print(f"  Loading embeddings: {EMBED_MODEL_NAME}...")
embed_model = SentenceTransformer(EMBED_MODEL_NAME)
print("  ✓ Embedding model loaded")

print(f"  Connecting to ChromaDB: {CHROMA_PATH}")
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
chroma_collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)
print(f"  ✓ ChromaDB ready ({chroma_collection.count()} chunks)")
print()

# =============================================================================
# RAG RETRIEVAL
# =============================================================================

def retrieve_context(query: str, top_k: int = 5) -> str:
    """Retrieve relevant context from ChromaDB."""
    try:
        query_embedding = embed_model.encode([query])[0].tolist()
        
        results = chroma_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas"]
        )
        
        if not results["documents"] or not results["documents"][0]:
            return "[No matching documents in RAG]"
        
        context_parts = []
        for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
            source = meta.get("rel_path", "unknown")
            context_parts.append(f"[{source}]\n{doc}")
        
        return "\n\n".join(context_parts)
    
    except Exception as e:
        print(f"RAG retrieval error: {e}", flush=True)
        return "[RAG error]"

# =============================================================================
# SESSION STORE
# =============================================================================

sessions: dict[str, dict] = {}

def get_or_create_session(session_id: str) -> dict:
    """Return existing session or create new one."""
    if session_id not in sessions:
        if len(sessions) >= MAX_SESSIONS:
            sessions.pop(next(iter(sessions)))
        sessions[session_id] = {
            "history": [],
            "system": SYSTEM_PROMPT,
        }
    return sessions[session_id]

# =============================================================================
# TOKEN COUNTER
# =============================================================================

def count_tokens(text: str) -> int:
    return len(llm.tokenize(text.encode()))

# =============================================================================
# PROMPT BUILDER
# =============================================================================

def build_prompt(history: list, user_input: str, rag_context: str) -> str:
    system_block = f"{S}system\n{SYSTEM_PROMPT}{E}"
    rag_block = f"{S}user\n[RAG Context]\n{rag_context}{E}"
    user_block = f"{S}user\n{user_input}{E}{S}assistant\n"

    budget = CONTEXT_LEN - MAX_TOKENS - count_tokens(system_block + rag_block + user_block) - 64

    trimmed = list(history)
    while trimmed:
        hist_text = "".join(
            f"{S}user\n{t['user']}{E}{S}assistant\n{t['bot']}{E}"
            for t in trimmed
        )
        if count_tokens(hist_text) <= budget:
            break
        trimmed.pop(0)

    prompt = system_block + rag_block
    for t in trimmed:
        prompt += f"{S}user\n{t['user']}{E}{S}assistant\n{t['bot']}{E}"
    prompt += user_block

    return prompt

# =============================================================================
# STREAMING INFERENCE
# =============================================================================

def stream_chat(session_id: str, user_input: str):
    sess = get_or_create_session(session_id)
    
    # Retrieve RAG context
    rag_context = retrieve_context(user_input, top_k=5)
    
    # Build prompt with RAG context
    prompt = build_prompt(sess["history"], user_input, rag_context)

    full_reply = []
    token_count = 0

    for chunk in llm(
        prompt,
        max_tokens=MAX_TOKENS,
        temperature=0.2,
        top_p=0.95,
        top_k=40,
        repeat_penalty=1.1,
        stop=[E, S],
        echo=False,
        stream=True
    ):
        token = chunk["choices"][0]["text"]
        full_reply.append(token)
        token_count += 1
        yield token

    reply = "".join(full_reply).strip()
    print(f"[{session_id}] generated: {token_count} tokens", flush=True)
    
    sess["history"].append({"user": user_input, "bot": reply})

# =============================================================================
# FASTAPI
# =============================================================================

app = FastAPI(title="RAG Assistant")

class ChatRequest(BaseModel):
    session_id: str = "default"
    message: str = ""

@app.post("/stream")
def stream_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")
    return StreamingResponse(
        stream_chat(req.session_id, req.message),
        media_type="text/plain"
    )

@app.post("/clear")
def clear_endpoint(req: ChatRequest):
    sessions.pop(req.session_id, None)
    return {"status": "cleared"}




# In the FastAPI section, change:
@app.get("/")
def root():
    return FileResponse("WEBRAG_simple.html")

# Or mount the file:
# app = FastAPI(title="RAG Assistant")
# app.mount("/", StaticFiles(directory=".", html=True), name="static")


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)