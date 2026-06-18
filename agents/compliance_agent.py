from agent_models import AgentFinding, AgentVote, ReviewContext
from llm_clients import FeatherlessClient
from local_band_room import LocalBandRoom


class ComplianceAgent:
    name = "Compliance Agent"

    def __init__(self):
        self.featherless = FeatherlessClient()

    def review(self, context: ReviewContext, room: LocalBandRoom) -> None:
        text = context.contract_text.lower()

        has_dpa_problem = (
            "no data processing agreement" in text
            or "no dpa" in text
            or "without dpa" in text
        )

        llm_result = self.featherless.analyze_compliance_risk(context.contract_text)

        if llm_result:
            room.post_message(
                context,
                self.name,
                "@OrchestratorAgent",
                "Featherless AI completed an independent compliance reasoning pass.",
                "Partner AI Reasoning",
            )

        if has_dpa_problem:
            room.post_message(
                context,
                self.name,
                "@OrchestratorAgent",
                "GDPR risk detected. Data Processing Agreement is missing. Human approval required.",
                "Escalation",
            )

            context.findings.append(
                AgentFinding(
                    agent_name=self.name,
                    category="GDPR / Data Protection",
                    severity="Critical",
                    finding="The supplier may process personal data, but no Data Processing Agreement is attached.",
                    recommendation="Block final approval until a DPA is added.",
                )
            )

            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Reject until fixed",
                    confidence=93,
                    reason="Missing DPA creates a serious compliance issue.",
                )
            )

            return

        if llm_result and llm_result.get("riskDetected"):
            severity = str(llm_result.get("severity", "Medium"))
            finding = str(
                llm_result.get(
                    "finding",
                    "Featherless AI detected a potential compliance risk.",
                )
            )
            recommendation = str(
                llm_result.get(
                    "recommendation",
                    "Request compliance review before approval.",
                )
            )
            confidence = int(llm_result.get("confidence", 82))

            room.post_message(
                context,
                self.name,
                "@OrchestratorAgent",
                f"Featherless AI detected compliance risk: {finding}",
                "Partner AI Finding",
            )

            context.findings.append(
                AgentFinding(
                    agent_name=self.name,
                    category="AI-Assisted Compliance Review",
                    severity=severity,
                    finding=finding,
                    recommendation=recommendation,
                )
            )

            vote = "Reject until fixed" if severity.lower() in ["critical", "high"] else "Approve with conditions"

            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote=vote,
                    confidence=confidence,
                    reason="Compliance decision supported by Featherless AI reasoning.",
                )
            )

            return

        context.votes.append(
            AgentVote(
                agent_name=self.name,
                vote="Approve",
                confidence=80,
                reason="No critical compliance blocker detected.",
            )
        )