from fastapi import APIRouter, Request
from engine.audit import run_audit

router = APIRouter()

@router.post("/audit")
async def audit_endpoint(request: Request):
    payload = await request.json()
    lines = payload.get("lines", [])
    result = run_audit(lines)
    return {"result": result}