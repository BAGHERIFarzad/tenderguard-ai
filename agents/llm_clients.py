import json
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class FeatherlessClient:
    def __init__(self):
        self.api_key = os.getenv("FEATHERLESS_API_KEY", "").strip()
        self.base_url = os.getenv("FEATHERLESS_BASE_URL", "https://api.featherless.ai/v1").strip()
        self.model = os.getenv(
            "FEATHERLESS_MODEL",
            "meta-llama/Meta-Llama-3.1-8B-Instruct",
        ).strip()

        self.client = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )

    def is_configured(self) -> bool:
        return self.client is not None

    def analyze_compliance_risk(self, contract_text: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None

        system_prompt = """
You are a strict enterprise compliance review agent.
Analyze supplier contract text for GDPR, data protection, DPA, privacy, sanctions, and approval risks.

Return ONLY valid JSON with this structure:
{
  "riskDetected": true,
  "severity": "Low | Medium | High | Critical",
  "category": "Compliance / Data Protection",
  "finding": "short finding",
  "recommendation": "short recommendation",
  "confidence": 0-100
}
"""

        user_prompt = f"""
Contract text:
{contract_text}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt.strip()},
                ],
                temperature=0.1,
                max_tokens=450,
            )

            content = response.choices[0].message.content or ""

            return self._safe_json_parse(content)

        except Exception as exc:
            print(f"[FeatherlessClient] Compliance analysis failed: {exc}")
            return None

    @staticmethod
    def _safe_json_parse(content: str) -> Optional[Dict[str, Any]]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        start = content.find("{")
        end = content.rfind("}")

        if start == -1 or end == -1 or end <= start:
            return None

        try:
            return json.loads(content[start : end + 1])
        except json.JSONDecodeError:
            return None
        
class AimlApiClient:
    def __init__(self):
        self.api_key = os.getenv("AIML_API_KEY", "").strip()
        self.base_url = os.getenv("AIML_BASE_URL", "https://api.aimlapi.com/v1").strip()
        self.model = os.getenv("AIML_MODEL", "gpt-4o-mini").strip()

        self.client = None

        if self.api_key:
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )

    def is_configured(self) -> bool:
        return self.client is not None

    def generate_executive_summary(
        self,
        project_name: str,
        supplier_name: str,
        risk_score: int,
        risk_level: str,
        findings: list,
        votes: list,
    ) -> str | None:
        if not self.client:
            return None

        findings_text = "\n".join(
            [
                f"- [{finding.severity}] {finding.category}: {finding.finding} Recommendation: {finding.recommendation}"
                for finding in findings
            ]
        )

        votes_text = "\n".join(
            [
                f"- {vote.agent_name}: {vote.vote} ({vote.confidence}% confidence). Reason: {vote.reason}"
                for vote in votes
            ]
        )

        system_prompt = """
You are an enterprise procurement review orchestrator.
Write a concise executive decision summary for a procurement manager.
Be direct, risk-aware, and business-oriented.
Do not use markdown tables.
"""

        user_prompt = f"""
Project: {project_name}
Supplier: {supplier_name}
Risk Score: {risk_score}
Risk Level: {risk_level}

Agent Findings:
{findings_text}

Agent Votes:
{votes_text}

Write:
1. One-sentence executive summary.
2. Main blockers.
3. Recommended decision.
4. Required conditions before approval.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt.strip()},
                    {"role": "user", "content": user_prompt.strip()},
                ],
                temperature=0.2,
                max_tokens=550,
            )

            return response.choices[0].message.content

        except Exception as exc:
            print(f"[AimlApiClient] Executive summary generation failed: {exc}")
            return None