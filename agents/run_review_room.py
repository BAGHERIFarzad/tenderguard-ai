from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_models import ReviewContext
from room_factory import create_room
from orchestrator_agent import OrchestratorAgent

console = Console()

sample_contract = """
The supplier may process customer data.
Liability is unlimited.
Payment is due within 15 days.
SLA penalties are not clearly defined.
No Data Processing Agreement is attached.
The supplier will provide cloud software services for a 24-month period.
Termination rights require 90 days notice.
"""


def main():
    context = ReviewContext(
        project_name="Cloud Software Supplier Review",
        supplier_name="Nexora Cloud Ltd",
        contract_text=sample_contract,
    )

    room = create_room("TenderGuard Supplier Review Room")
    orchestrator = OrchestratorAgent()
    result = orchestrator.run(context, room)

    console.print(
        Panel.fit(
            "[bold cyan]TenderGuard AI[/bold cyan]\nLocal Band-style multi-agent review room",
            border_style="cyan",
        )
    )

    console.print("\n[bold]Agent Collaboration Timeline[/bold]")

    for message in result.messages:
        console.print(
            f"[cyan]{message.from_agent}[/cyan] → [green]{message.to_agent}[/green] "
            f"[dim]({message.message_type})[/dim]\n{message.message}\n"
        )

    findings_table = Table(title="Agent Findings")
    findings_table.add_column("Agent")
    findings_table.add_column("Category")
    findings_table.add_column("Severity")
    findings_table.add_column("Recommendation")

    for finding in result.findings:
        findings_table.add_row(
            finding.agent_name,
            finding.category,
            finding.severity,
            finding.recommendation,
        )

    console.print(findings_table)

    votes_table = Table(title="Agent Votes")
    votes_table.add_column("Agent")
    votes_table.add_column("Vote")
    votes_table.add_column("Confidence")
    votes_table.add_column("Reason")

    for vote in result.votes:
        votes_table.add_row(
            vote.agent_name,
            vote.vote,
            f"{vote.confidence}%",
            vote.reason,
        )

    console.print(votes_table)


if __name__ == "__main__":
    main()