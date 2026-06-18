# Architecture

TenderGuard AI is designed as a multi-service enterprise application.

The system has four main layers:

1. React frontend
2. .NET backend
3. Python Agent API
4. Band collaboration layer

## High-Level Architecture

```txt
User
 ↓
React Dashboard
 ↓
.NET 8 Backend API
 ↓
Python FastAPI Agent API
 ↓
Room Factory
 ├── LocalBandRoom
 └── BandRoomAdapter
       ↓
     Band Chat Room
 ↓
Specialized Agent Team
```

## Frontend

The frontend is a React + TypeScript application.

It provides:

- Supplier review form
- Risk summary cards
- Integration mode status
- AI provider status
- Agent room cards
- Band collaboration timeline
- Risk findings
- Agent votes
- Human decision panel
- Final audit decision packet
- Copy report button

The frontend communicates with the .NET backend through API calls.

## Backend

The backend is a .NET 8 Web API.

Responsibilities:

- Receive supplier review requests
- Call the Python Agent API
- Normalize agent responses
- Assign audit hash
- Store reviews in memory
- Handle human decisions
- Return structured review data to React

Important backend components:

- `ReviewsController.cs`
- `ReviewService.cs`
- `AgentApiClient.cs`
- `ReviewModels.cs`
- `AgentApiModels.cs`

## Python Agent API

The Python Agent API is built with FastAPI.

Responsibilities:

- Receive review request from .NET
- Create shared review context
- Create room adapter
- Run Orchestrator Agent
- Run specialized agents
- Return timeline, findings, votes, risk score, and summary

Important files:

- `agent_api.py`
- `agent_models.py`
- `orchestrator_agent.py`
- `legal_agent.py`
- `finance_agent.py`
- `compliance_agent.py`
- `operations_agent.py`
- `room_factory.py`
- `local_band_room.py`
- `band_room_adapter.py`
- `llm_clients.py`

## Agent Roles

### Orchestrator Agent

Coordinates the review, assigns work, collects outputs, and prepares the final decision packet.

### Legal Agent

Reviews:

- Liability
- Contractual exposure
- Termination risk

### Finance Agent

Reviews:

- Payment terms
- Cash-flow exposure
- Financial approval needs

### Compliance Agent

Reviews:

- GDPR
- Data Processing Agreement
- Privacy risk
- Compliance blockers

Uses Featherless AI for an independent compliance reasoning pass when configured.

### Operations Agent

Reviews:

- Delivery feasibility
- SLA clarity
- Operational obligations

## Band Integration

TenderGuard AI uses a room adapter pattern:

```txt
room.post_message(...)
```

Agents do not know whether the room is local or Band-backed.

The room is selected through:

```env
AGENT_ROOM_MODE=local
```

or:

```env
AGENT_ROOM_MODE=band
```

### Local Mode

Uses `LocalBandRoom`.

Good for local development and fallback safety.

### Band Mode

Uses `BandRoomAdapter`.

Sends agent collaboration messages to a Band chat room.

## Partner AI Integration

### Featherless AI

Used inside the Compliance Agent.

Purpose:

- Independent compliance reasoning
- Additional high-stakes review intelligence

### AI/ML API

Used inside the Orchestrator Agent.

Purpose:

- Executive summary generation
- Business-oriented final recommendation support

If keys are unavailable, the system falls back safely.
