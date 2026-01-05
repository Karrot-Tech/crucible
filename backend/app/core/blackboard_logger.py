"""
Blackboard Logger - Complete audit trail for the agentic network.

This module captures every event, agent output, context mutation, and decision
in a structured, timestamped format for detailed post-session analysis.

Log Structure (per session):
logs/
  sessions/
    {session_id}/
      blackboard.jsonl       # Append-only log of all events
      context_snapshots/     # Full context dumps at key moments
      agent_outputs/         # Raw agent outputs per execution
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Any, Dict, Optional, Literal
from pathlib import Path


LogLevel = Literal["EVENT", "AGENT_START", "AGENT_COMPLETE", "CONTEXT_UPDATE", 
                   "CLARIFICATION", "ADMINISTRATOR", "SYSTEM", "ERROR"]


class BlackboardLogger:
    """
    Comprehensive logger for the agentic network blackboard.
    Captures raw data in organized, analyzable format.
    """
    
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Default to logs directory in backend root
            backend_root = Path(__file__).parent.parent.parent
            base_path = backend_root / "logs" / "sessions"
        
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._locks: Dict[str, asyncio.Lock] = {}
    
    def _get_session_path(self, session_id: str) -> Path:
        """Get or create session directory."""
        session_path = self.base_path / session_id
        session_path.mkdir(parents=True, exist_ok=True)
        (session_path / "context_snapshots").mkdir(exist_ok=True)
        (session_path / "agent_outputs").mkdir(exist_ok=True)
        return session_path
    
    def _get_lock(self, session_id: str) -> asyncio.Lock:
        """Get or create a lock for a session (thread-safe writes)."""
        if session_id not in self._locks:
            self._locks[session_id] = asyncio.Lock()
        return self._locks[session_id]
    
    async def log_event(
        self,
        session_id: str,
        level: LogLevel,
        event_type: str,
        data: Dict[str, Any],
        agent_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Append an event to the session's blackboard log.
        
        Args:
            session_id: Unique session identifier
            level: Log level category
            event_type: Specific event name (e.g., "TRANSCRIPT_READY", "SAFETY_STOP")
            data: Raw event data/payload
            agent_id: Optional agent identifier
            metadata: Optional additional metadata
        """
        session_path = self._get_session_path(session_id)
        log_file = session_path / "blackboard.jsonl"
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "sequence": await self._get_next_sequence(session_id),
            "level": level,
            "event_type": event_type,
            "agent_id": agent_id,
            "data": data,
            "metadata": metadata or {}
        }
        
        async with self._get_lock(session_id):
            with open(log_file, "a") as f:
                f.write(json.dumps(entry, default=str) + "\n")
    
    async def log_agent_execution(
        self,
        session_id: str,
        agent_id: str,
        phase: Literal["start", "complete", "error"],
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
        prompt: Optional[str] = None,
        llm_response: Optional[str] = None,
        duration_ms: Optional[int] = None,
        error: Optional[str] = None
    ) -> None:
        """
        Log detailed agent execution data.
        Saves both to the main blackboard and a separate agent output file.
        """
        session_path = self._get_session_path(session_id)
        timestamp = datetime.now()
        
        # Detailed agent output file
        agent_file = session_path / "agent_outputs" / f"{agent_id}_{timestamp.strftime('%H%M%S_%f')}.json"
        
        detailed_entry = {
            "timestamp": timestamp.isoformat(),
            "agent_id": agent_id,
            "phase": phase,
            "input_data": input_data,
            "prompt": prompt,
            "llm_response": llm_response,
            "output_data": output_data,
            "duration_ms": duration_ms,
            "error": error
        }
        
        async with self._get_lock(session_id):
            with open(agent_file, "w") as f:
                json.dump(detailed_entry, f, indent=2, default=str)
        
        # Also log summary to main blackboard
        level = "ERROR" if phase == "error" else f"AGENT_{phase.upper()}"
        await self.log_event(
            session_id=session_id,
            level=level,
            event_type=f"AGENT_{phase.upper()}",
            data={
                "output_file": str(agent_file.name),
                "output_summary": self._summarize_output(output_data) if output_data else None,
                "duration_ms": duration_ms,
                "error": error
            },
            agent_id=agent_id
        )
    
    async def log_context_snapshot(
        self,
        session_id: str,
        context: Dict[str, Any],
        trigger: str,
        agent_id: Optional[str] = None
    ) -> None:
        """
        Save a complete snapshot of the blackboard context.
        Useful for debugging and replaying agent decisions.
        """
        session_path = self._get_session_path(session_id)
        timestamp = datetime.now()
        
        snapshot_file = session_path / "context_snapshots" / f"{timestamp.strftime('%H%M%S_%f')}_{trigger}.json"
        
        snapshot = {
            "timestamp": timestamp.isoformat(),
            "trigger": trigger,
            "agent_id": agent_id,
            "context": context
        }
        
        async with self._get_lock(session_id):
            with open(snapshot_file, "w") as f:
                json.dump(snapshot, f, indent=2, default=str)
        
        # Log reference to main blackboard
        await self.log_event(
            session_id=session_id,
            level="CONTEXT_UPDATE",
            event_type="CONTEXT_SNAPSHOT",
            data={"snapshot_file": str(snapshot_file.name), "trigger": trigger},
            agent_id=agent_id
        )
    
    async def log_administrator_decision(
        self,
        session_id: str,
        directive: str,
        reason: str,
        winner_id: Optional[str] = None,
        loser_id: Optional[str] = None,
        loop_detected: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log administrator/judge decisions for conflict resolution."""
        await self.log_event(
            session_id=session_id,
            level="ADMINISTRATOR",
            event_type=f"ADMINISTRATOR_{directive}",
            data={
                "directive": directive,
                "reason": reason,
                "winner_id": winner_id,
                "loser_id": loser_id,
                "loop_detected": loop_detected
            },
            metadata=metadata
        )
    
    async def log_clarification(
        self,
        session_id: str,
        agent_id: str,
        question: str,
        suggested_answer: Optional[str] = None,
        user_answer: Optional[str] = None,
        triggering_agent_id: Optional[str] = None
    ) -> None:
        """Log human-in-the-loop clarification exchanges."""
        await self.log_event(
            session_id=session_id,
            level="CLARIFICATION",
            event_type="CLARIFICATION_REQUEST" if user_answer is None else "CLARIFICATION_RESPONSE",
            data={
                "question": question,
                "suggested_answer": suggested_answer,
                "user_answer": user_answer,
                "triggering_agent_id": triggering_agent_id
            },
            agent_id=agent_id
        )
    
    async def log_workflow_event(
        self,
        session_id: str,
        event_type: str,
        data: Dict[str, Any]
    ) -> None:
        """Log workflow lifecycle events (start, pause, resume, complete)."""
        await self.log_event(
            session_id=session_id,
            level="SYSTEM",
            event_type=event_type,
            data=data
        )
    
    async def _get_next_sequence(self, session_id: str) -> int:
        """Get next sequence number for ordering."""
        session_path = self._get_session_path(session_id)
        log_file = session_path / "blackboard.jsonl"
        
        if not log_file.exists():
            return 1
        
        with open(log_file, "r") as f:
            return sum(1 for _ in f) + 1
    
    def _summarize_output(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Create a brief summary of agent output for the main log."""
        summary = {}
        
        # Key fields to always include
        key_fields = ["risk_detected", "clarification_needed", "error", "summary"]
        for field in key_fields:
            if field in output:
                summary[field] = output[field]
        
        # Count of items for list fields
        for key, value in output.items():
            if isinstance(value, list):
                summary[f"{key}_count"] = len(value)
        
        return summary
    
    def get_session_log(self, session_id: str) -> list:
        """Read all log entries for a session (for analysis)."""
        session_path = self._get_session_path(session_id)
        log_file = session_path / "blackboard.jsonl"
        
        if not log_file.exists():
            return []
        
        entries = []
        with open(log_file, "r") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        
        return entries


# Singleton instance
blackboard_logger = BlackboardLogger()
