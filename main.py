from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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
    lines = parse_pdf(file)
    suggestions = run_rules(lines)
    return {"suggestions": suggestions}

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    log_feedback(
        pdf_id=feedback.pdf_id,
        missed_item=feedback.missed_item,
        context_lines=feedback.context_lines
    )
    return {"status": "feedback logged"}