# TenderGuard AI Agents

This folder contains the multi-agent collaboration layer for TenderGuard AI.

## Current mode

The current implementation runs a local Band-style collaboration room to validate the enterprise workflow:

- Orchestrator Agent assigns work
- Legal Agent reviews liability
- Finance Agent reviews payment and financial exposure
- Compliance Agent reviews GDPR and DPA risks
- Operations Agent reviews SLA and delivery feasibility

## Why this matters for the hackathon

The Band of Agents Hackathon requires at least 3 agents collaborating through Band. This folder defines the agent roles, message handoffs, shared context model, and review workflow before connecting the live Band SDK/API.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install python-dotenv requests rich
python run_review_room.py