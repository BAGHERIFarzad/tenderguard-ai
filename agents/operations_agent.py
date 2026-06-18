from agent_models import AgentFinding, AgentVote, ReviewContext
from local_band_room import LocalBandRoom


class OperationsAgent:
    name = "Operations Agent"

    def review(self, context: ReviewContext, room: LocalBandRoom) -> None:
        text = context.contract_text.lower()

        if "sla penalties are not clearly defined" in text or "sla" in text:
            room.post_message(
                context,
                self.name,
                "@OrchestratorAgent",
                "Delivery is feasible, but SLA penalties and operational guarantees must be clarified.",
                "Operational Review",
            )

            context.findings.append(
                AgentFinding(
                    agent_name=self.name,
                    category="Delivery / SLA",
                    severity="Medium",
                    finding="SLA penalties are vague and may create ambiguity during service incidents.",
                    recommendation="Clarify SLA metrics, uptime obligations, response times, and penalty conditions.",
                )
            )

            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Approve with conditions",
                    confidence=88,
                    reason="Operational conditions must be clarified.",
                )
            )
        else:
            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Approve",
                    confidence=77,
                    reason="Delivery appears feasible.",
                )
            )