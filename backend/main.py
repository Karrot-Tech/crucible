from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.core.socket_manager import manager
from app.services.orchestrator import orchestrator

app = FastAPI(title="Crucible API")

# Configure CORS
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    patient_id: str
    session_date: str
    transcript: str
    soap_notes: Optional[str] = None

@app.get("/")
async def root():
    return {"message": "Crucible API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

class ClarificationRequest(BaseModel):
    session_id: str
    agent_id: str
    answer: str

@app.post("/api/analyze")
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Starts the agentic analysis in the background.
    """
    # Generate session ID here or let Orchestrator do it. 
    # For consistency, we'll let Orchestrator handle it but pass a known one if we want.
    # Actually, simpler to just start it and let Orchestrator return it if we awaited? 
    # But run_workflow is async background.
    # Let's generate it here.
    import uuid
    session_id = str(uuid.uuid4())
    background_tasks.add_task(orchestrator.run_workflow, request.dict(), session_id)
    return {"status": "analysis_started", "message": "Agents are running...", "session_id": session_id}

@app.post("/api/clarify")
async def submit_clarification(request: ClarificationRequest, background_tasks: BackgroundTasks):
    """
    Submits user clarification to a paused agent.
    """
    background_tasks.add_task(orchestrator.submit_clarification, request.session_id, request.agent_id, request.answer)
    return {"status": "clarification_submitted", "message": "Agent workflow resuming..."}
@app.post("/api/terminate/{session_id}")
async def terminate_analysis(session_id: str):
    """
    Kills the agent workflow for a given session.
    """
    await orchestrator.terminate_session(session_id)
    return {"status": "terminated", "session_id": session_id}
