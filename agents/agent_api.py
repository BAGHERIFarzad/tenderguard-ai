import os
from dataclasses import asdict
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent_models import ReviewContext
from room_factory import create_room
from orchestrator_agent import OrchestratorAgent


class StartReviewRequest(BaseModel):
    projectName: str
    supplierName: str
    contractText: str


app = FastAPI(
    title="TenderGuard AI Agent API",
    description="Local Band-style multi-agent collaboration service.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {
        "service": "TenderGuard AI Agent API",
        "status": "running",
        "agents": [
            "Orchestrator Agent",
            "Legal Agent",
            "Finance Agent",
            "Compliance Agent",
            "Operations Agent",
        ],
    }


@app.post("/agent-review")
def run_agent_review(request: StartReviewRequest):
    context = ReviewContext(
        project_name=request.projectName,
        supplier_name=request.supplierName,
        contract_text=request.contractText,
    )

    room = create_room("TenderGuard Supplier Review Room")
    orchestrator = OrchestratorAgent()
    result = orchestrator.run(context, room)

    risk_score = calculate_risk_score(result.findings)
    risk_level = get_risk_level(risk_score)
    final_recommendation = build_final_recommendation(result.findings, risk_score)
    
    room_mode = os.getenv("AGENT_ROOM_MODE", "local").lower().strip()
    
    featherless_enabled = bool(os.getenv("FEATHERLESS_API_KEY", "").strip())
    aiml_enabled = bool(os.getenv("AIML_API_KEY", "").strip())

    ai_provider_status = {
        "featherless": "enabled" if featherless_enabled else "fallback-ready",
        "aimlApi": "enabled" if aiml_enabled else "fallback-ready",
    }

    integration_mode = (
        "Python Agent API + Band Adapter"
        if room_mode == "band"
        else "Python Agent API + Local Band Room"
    )

    return {
        "projectName": result.project_name,
        "supplierName": result.supplier_name,
        "contractText": result.contract_text,
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "integrationMode": integration_mode,
        "roomMode": room_mode,
        "aiProviderStatus": ai_provider_status,
        "executiveSummary": result.executive_summary,
        "timeline": [asdict(message) for message in result.messages],
        "findings": [asdict(finding) for finding in result.findings],
        "votes": [asdict(vote) for vote in result.votes],
        "finalRecommendation": final_recommendation,
    }


def calculate_risk_score(findings: List) -> int:
    if not findings:
        return 35

    score = 20

    for finding in findings:
        severity = finding.severity.lower()

        if severity == "critical":
            score += 28
        elif severity == "high":
            score += 22
        elif severity == "medium":
            score += 14
        else:
            score += 6

    return min(score, 100)


def get_risk_level(score: int) -> str:
    if score >= 80:
        return "High"
    if score >= 55:
        return "Medium"
    return "Low"


def build_final_recommendation(findings: List, risk_score: int) -> str:
    has_critical = any(finding.severity.lower() == "critical" for finding in findings)
    has_high = any(finding.severity.lower() == "high" for finding in findings)

    if has_critical:
        return "Do not approve as-is. Human approval is required after critical issues are corrected, especially compliance and data protection requirements."

    if has_high:
        return "Approve only with conditions. High-risk contract terms must be amended before signature."

    if risk_score >= 55:
        return "Proceed with caution. Medium-risk items should be clarified before final approval."

    return "Low-risk review. The contract can proceed to normal approval."