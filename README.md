# TenderGuard AI

TenderGuard AI is an enterprise multi-agent supplier review system built for the **Band of Agents Hackathon**.

It helps procurement, legal, finance, compliance, and operations teams review supplier contracts faster, with traceable agent collaboration, human approval, partner AI reasoning, and an audit-ready decision packet.

## Problem

Enterprise supplier reviews are slow and fragmented.

A single supplier contract can involve:

- Legal risk review
- Finance exposure analysis
- GDPR and compliance checks
- Operational/SLA validation
- Human manager approval
- Audit traceability

In many organizations, this process happens across emails, spreadsheets, chat messages, and disconnected tools. Context is lost, handoffs are unclear, and approval decisions are difficult to audit.

## Solution

TenderGuard AI turns supplier review into a coordinated multi-agent workflow.

Specialized agents collaborate through a Band-powered room:

- Orchestrator Agent assigns the review
- Legal Agent checks liability and contract risk
- Finance Agent checks payment and financial exposure
- Compliance Agent checks GDPR, DPA, and data protection risk
- Operations Agent checks SLA and delivery feasibility
- Human Manager approves, rejects, or approves with conditions

The system generates:

- Risk score
- Risk level
- Agent timeline
- Agent findings
- Agent votes
- Executive summary
- Human decision state
- Audit hash
- Final audit decision packet

## Why Band Matters

Band is used as the collaboration layer.

The project does not only run agents locally. It connects the Python Agent API to a Band chat room through a Band adapter. Agent messages are sent into the Band room so the collaboration is visible and traceable.

Current integration mode shown in the app:

```txt
Python Agent API + Band Adapter
```

## Agent Workflow

1. User submits supplier contract text from the React dashboard.
2. React frontend sends the review request to the .NET backend.
3. .NET backend delegates the review to the Python Agent API.
4. Python Orchestrator Agent starts the workflow.
5. Specialized agents analyze the contract.
6. Agent-to-agent handoffs are posted to the timeline and Band room.
7. Featherless AI supports compliance reasoning.
8. AI/ML API supports executive summary generation.
9. .NET backend normalizes the response and assigns an audit hash.
10. React frontend displays the audit-ready decision packet.
11. Human manager records a final decision.

## Architecture

```txt
React Frontend
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
Specialized Agents
   ├── Orchestrator Agent
   ├── Legal Agent
   ├── Finance Agent
   ├── Compliance Agent
   └── Operations Agent
```

## Technologies Used

### Frontend

- React
- TypeScript
- Vite
- CSS
- Lucide React icons

### Backend

- .NET 8 Web API
- C#
- Swagger / OpenAPI
- HttpClient integration

### Agent Layer

- Python
- FastAPI
- Uvicorn
- Pydantic
- Python dotenv
- Requests
- OpenAI-compatible client

### AI / Partner Tools

- Band
- AI/ML API
- Featherless AI

## Key Features

- Band-powered multi-agent collaboration
- 5 specialized enterprise agents
- Agent-to-agent timeline
- Risk scoring
- Compliance escalation
- Partner AI reasoning
- AI-generated/fallback executive summary
- Audit hash generation
- Human-in-the-loop approval
- Final decision packet
- Copy report button
- Safe fallback mode if external services are unavailable

## Demo Scenario

The demo uses a supplier contract with several risks:

```txt
The supplier may process customer data.
Liability is unlimited.
Payment is due within 15 days.
SLA penalties are not clearly defined.
No Data Processing Agreement is attached.
```

Expected output:

- Risk Score: 98
- Risk Level: High
- Compliance finding: Critical
- Legal finding: High
- Finance finding: Medium
- Operations finding: Medium
- Human Decision: Pending or Approved with conditions
- Integration Mode: Python Agent API + Band Adapter
- AI Providers: Featherless enabled, AI/ML API enabled

## Running Locally

### 1. Start Python Agent API

```powershell
cd agents
.venv\Scripts\activate
uvicorn agent_api:app --reload --port 8001
```

### 2. Start .NET Backend

```powershell
cd backend/TenderGuard.Api
dotnet run
```

### 3. Start React Frontend

```powershell
cd frontend/tenderguard-ui
npm run dev
```

## Environment Variables

Create:

```txt
agents/.env
```

Use `agents/.env.example` as a template.

Important: never commit real API keys.

```env
AGENT_ROOM_MODE=band

BAND_BASE_URL=https://app.band.ai
BAND_CHAT_ID=your_band_chat_id
BAND_ORCHESTRATOR_API_KEY=your_band_agent_api_key
BAND_ORCHESTRATOR_AGENT_ID=your_band_agent_uuid
BAND_VERIFY_SSL=false

BAND_OWNER_USER_ID=your_band_user_uuid
BAND_OWNER_NAME=your_name
BAND_OWNER_HANDLE=your_band_handle

AIML_API_KEY=your_aiml_api_key
AIML_BASE_URL=https://api.aimlapi.com/v1
AIML_MODEL=gpt-4o-mini

FEATHERLESS_API_KEY=your_featherless_api_key
FEATHERLESS_BASE_URL=https://api.featherless.ai/v1
FEATHERLESS_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct

BACKEND_API_URL=http://localhost:5196/api
```

## Security

The project uses `.gitignore` to avoid committing:

- `.env`
- API keys
- build folders
- local virtual environments
- node_modules
- bin/obj folders

## Hackathon Value

TenderGuard AI demonstrates:

- Real enterprise workflow
- More than 3 agents
- Meaningful agent-to-agent collaboration
- Band as the coordination layer
- Human approval
- Traceable audit output
- Partner AI usage
- Practical business value for procurement and compliance teams
