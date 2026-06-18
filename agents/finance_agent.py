from agent_models import AgentFinding, AgentVote, ReviewContext
from local_band_room import LocalBandRoom


class FinanceAgent:
    name = "Finance Agent"

    def review(self, context: ReviewContext, room: LocalBandRoom) -> None:
        text = context.contract_text.lower()

        if "payment is due within 15 days" in text or "15 days" in text:
            room.post_message(
                context,
                self.name,
                "@LegalAgent",
                "Payment terms are aggressive. Please verify whether penalties and liability terms increase financial exposure.",
                "Risk Review",
            )

            context.findings.append(
                AgentFinding(
                    agent_name=self.name,
                    category="Payment Terms",
                    severity="Medium",
                    finding="The payment deadline is short and may create cash-flow pressure.",
                    recommendation="Negotiate payment due within 30 days instead of 15 days.",
                )
            )

            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Approve with conditions",
                    confidence=78,
                    reason="Financial exposure should be reduced before signature.",
                )
            )
        else:
            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Approve",
                    confidence=74,
                    reason="No major finance blocker detected.",
                )
            )