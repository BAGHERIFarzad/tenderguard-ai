from agent_models import AgentFinding, AgentVote, ReviewContext
from local_band_room import LocalBandRoom


class LegalAgent:
    name = "Legal Agent"

    def review(self, context: ReviewContext, room: LocalBandRoom) -> None:
        text = context.contract_text.lower()

        if "unlimited liability" in text or "liability is unlimited" in text:
            room.post_message(
                context,
                self.name,
                "@FinanceAgent",
                "Unlimited liability exposure found. Please evaluate financial impact.",
                "Agent Handoff",
            )

            context.findings.append(
                AgentFinding(
                    agent_name=self.name,
                    category="Contract Liability",
                    severity="High",
                    finding="The contract includes unlimited liability language without a clear liability cap.",
                    recommendation="Add a liability cap equal to 12 months of service fees.",
                )
            )

            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Approve with conditions",
                    confidence=84,
                    reason="Legal risk can be reduced with contract amendments.",
                )
            )
        else:
            context.votes.append(
                AgentVote(
                    agent_name=self.name,
                    vote="Approve",
                    confidence=76,
                    reason="No major legal blocker detected.",
                )
            )