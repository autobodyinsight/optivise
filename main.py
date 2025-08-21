from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import tempfile
import os
import logging

from pdf_parser import parse_pdf
from rule_engine import run_rules
from report_formatter import format_report_html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/audit", response_class=HTMLResponse)
async def audit_estimate(file: UploadFile = File(...)):
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        parsed_data = parse_pdf(tmp_path)
        logger.info("🔍 Parsed PDF data: %s", parsed_data)

        results = run_rules(parsed_data)
        logger.info("🧠 Rule results: %s", results)

        report_html = format_report_html(results)
        return report_html

    except Exception as e:
        logger.error("❌ Internal Server Error: %s", str(e))
        return HTMLResponse(content="Internal Server Error", status_code=500)

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)