from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class AgentMessage:
    from_agent: str
    to_agent: str
    message: str
    message_type: str
    timestamp_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


@dataclass
class AgentFinding:
    agent_name: str
    category: str
    severity: str
    finding: str
    recommendation: str


@dataclass
class AgentVote:
    agent_name: str
    vote: str
    confidence: int
    reason: str


@dataclass
class ReviewContext:
    project_name: str
    supplier_name: str
    contract_text: str
    messages: List[AgentMessage] = field(default_factory=list)
    findings: List[AgentFinding] = field(default_factory=list)
    votes: List[AgentVote] = field(default_factory=list)
    executive_summary: str = ""