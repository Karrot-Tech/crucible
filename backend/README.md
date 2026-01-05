# Crucible Backend

FastAPI backend powering the Crucible agent mesh system.

## Tech Stack
- **Python 3.10+**
- **FastAPI** with WebSocket support
- **Google Gemini** for LLM inference
- **Event-driven architecture** with custom Event Bus

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env

# Run server
python -m uvicorn main:app --reload --port 8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/ws` | WebSocket | Real-time agent updates |
| `/api/analyze` | POST | Start agent mesh analysis |
| `/api/clarify/{session_id}` | POST | Submit clarification response |
| `/api/terminate/{session_id}` | POST | Kill active session |

## Project Structure

```
backend/
├── app/
│   ├── core/
│   │   ├── event_bus.py      # Pub/Sub event system
│   │   ├── socket_manager.py # WebSocket broadcast
│   │   └── blackboard_logger.py
│   └── services/
│       ├── agents/           # Individual agent implementations
│       │   ├── base.py
│       │   ├── safety_agent.py
│       │   ├── clinical_agent.py
│       │   └── ...
│       ├── orchestrator.py   # Main workflow coordinator
│       └── administrator_agent.py
├── main.py                   # FastAPI entry point
└── requirements.txt
```

## Agents

| Agent | Priority | Role |
|-------|----------|------|
| safety_triage | 100 | Safety monitoring (supreme authority) |
| user_assist | 10 | Session orientation |
| clinical_entity | 9 | Clinical data extraction |
| diagnosis_mapping | 8 | ICD-10 mapping |
| risk_assessment | 8 | C-SSRS evaluation |
| procedure_coding | 6 | CPT coding |
| medication_management | 5 | Medication review |
| treatment_planning | 5 | Treatment plans |
| output_generation | 1 | SOAP note synthesis |
