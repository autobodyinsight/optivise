from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import tempfile
import os

from pdf_parser import parse_pdf
from rule_engine import run_rules
from feedback_trainer import log_feedback

app = FastAPI(title="Optivise Audit Engine")

# Optional: allow frontend or external tools to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class FeedbackRequest(BaseModel):
    pdf_id: str
    missed_item: str
    context_lines: List[str]

# ---------- Endpoints ----------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        parsed = parse_pdf(tmp_path)
        suggestions = run_rules(parsed["raw_lines"])

        os.remove(tmp_path)  # Optional cleanup

        return {"suggestions": suggestions, "parts": parsed["parts"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    log_feedback(
        pdf_id=feedback.pdf_id,
        missed_item=feedback.missed_item,
        context_lines=feedback.context_lines
    )
    return {"status": "feedback logged"}