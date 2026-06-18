from typing import Any

from agent_models import ReviewContext
from compliance_agent import ComplianceAgent
from finance_agent import FinanceAgent
from legal_agent import LegalAgent
from llm_clients import AimlApiClient
from operations_agent import OperationsAgent


class OrchestratorAgent:
    name = "Orchestrator Agent"

    def __init__(self):
        self.agents = [
            LegalAgent(),
            FinanceAgent(),
            ComplianceAgent(),
            OperationsAgent(),
        ]
        self.aiml = AimlApiClient()

    def run(self, context: ReviewContext, room: Any) -> ReviewContext:
        room.post_message(
            context,
            self.name,
            "@LegalAgent @FinanceAgent @ComplianceAgent @OperationsAgent",
            "New supplier review started. Please analyze legal, financial, compliance, and operational risks.",
            "Task Assignment",
        )

        for agent in self.agents:
            agent.review(context, room)

        if not context.findings:
            room.post_message(
                context,
                self.name,
                "@AllAgents",
                "No major risk keyword was detected. Preparing normal approval packet.",
                "Coordination",
            )

        risk_score = self._calculate_risk_score(context)
        risk_level = self._get_risk_level(risk_score)

        executive_summary = self.aiml.generate_executive_summary(
            project_name=context.project_name,
            supplier_name=context.supplier_name,
            risk_score=risk_score,
            risk_level=risk_level,
            findings=context.findings,
            votes=context.votes,
        )

        if executive_summary:
            context.executive_summary = executive_summary

            room.post_message(
                context,
                self.name,
                "@HumanManager",
                "AI/ML API generated an executive decision summary from all agent findings and votes.",
                "Partner AI Summary",
            )
        else:
            context.executive_summary = self._build_fallback_executive_summary(
                risk_score,
                risk_level,
                context,
            )

        room.post_message(
            context,
            self.name,
            "@AllAgents",
            "All agent reviews completed. Final decision packet is ready for human approval.",
            "Coordination",
        )

        return context

    def _calculate_risk_score(self, context: ReviewContext) -> int:
        if not context.findings:
            return 35

        score = 20

        for finding in context.findings:
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

    def _get_risk_level(self, score: int) -> str:
        if score >= 80:
            return "High"

        if score >= 55:
            return "Medium"

        return "Low"

    def _build_fallback_executive_summary(
        self,
        risk_score: int,
        risk_level: str,
        context: ReviewContext,
    ) -> str:
        critical_findings = [
            finding
            for finding in context.findings
            if finding.severity.lower() == "critical"
        ]

        if critical_findings:
            return (
                f"{context.supplier_name} is a {risk_level.lower()}-risk supplier review "
                f"with a score of {risk_score}. The main blocker is a critical compliance issue. "
                "The supplier should not be approved as-is. Required conditions must be completed "
                "before human approval."
            )

        if risk_score >= 80:
            return (
                f"{context.supplier_name} is a high-risk supplier review with a score of {risk_score}. "
                "Approval should only proceed with strong contractual, financial, and operational conditions."
            )

        if risk_score >= 55:
            return (
                f"{context.supplier_name} is a medium-risk supplier review. "
                "The manager should clarify open conditions before approval."
            )

        return (
            f"{context.supplier_name} is a low-risk supplier review. "
            "The contract can proceed to normal approval."
        )