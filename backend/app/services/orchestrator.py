from typing import Dict, Any, List
import asyncio
import time
from app.core.socket_manager import manager
from app.core.blackboard_logger import blackboard_logger
from app.services.agents.base import BaseAgent
from app.services.agents.safety_agent import SafetyTriageAgent
from app.services.agents.clinical_agent import ClinicalEntityAgent
from app.services.agents.diagnosis_agent import DiagnosisMappingAgent
from app.services.agents.risk_agent import RiskAssessmentAgent
from app.services.agents.procedure_agent import ProcedureCodingAgent
from app.services.agents.medication_agent import MedicationManagementAgent
from app.services.agents.treatment_agent import TreatmentPlanningAgent
from app.services.agents.output_agent import OutputGenerationAgent
from app.services.agents.user_assist_agent import UserAssistAgent

class Orchestrator:
    def __init__(self):
        # Register available agents
        self.agents:Dict[str, BaseAgent] = {
            "safety_triage": SafetyTriageAgent(priority=100),  # SUPREME++: God-tier authority
            "clinical_entity": ClinicalEntityAgent(priority=9),
            "diagnosis_mapping": DiagnosisMappingAgent(priority=8),
            "risk_assessment": RiskAssessmentAgent(priority=8),
            "procedure_coding": ProcedureCodingAgent(priority=6),
            "medication_management": MedicationManagementAgent(priority=5),
            "treatment_planning": TreatmentPlanningAgent(priority=5),
            "output_generation": OutputGenerationAgent(priority=1),
            "user_assist": UserAssistAgent(priority=10) # Orientation is high priority
        }
        self.active_sessions: Dict[str, Any] = {}
        self.terminated_sessions: set = set()

    async def run_workflow(self, input_data: Dict[str, Any], session_id: str = None):
        if not session_id:
             import uuid
             session_id = str(uuid.uuid4())

        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = {
                "input_data": input_data,
                "context": {},
                "status": "running"
            }
        
        session_state = self.active_sessions[session_id]
        context = session_state["context"]

        # --- EVENT MESH INITIALIZATION ---
        from app.core.event_bus import EventBus, Event
        from app.services.agents.administrator_agent import AdministratorAgent
        
        bus = EventBus()
        administrator = AdministratorAgent()
        
        # Subscribe Agents (Dynamic)
        # DEBATE MODE ACTIVATED: Diagnosis & Medication listen to each other
        self.agents["user_assist"].listen_for = ["TRANSCRIPT_READY"]
        self.agents["safety_triage"].listen_for = ["ORIENTATION_COMPLETE"]
        self.agents["clinical_entity"].listen_for = ["SAFETY_CLEARED"]
        
        self.agents["diagnosis_mapping"].listen_for = ["CLINICAL_EXTRACTED", "MEDICATION_CHECKED"] # Listens to Meds!
        
        self.agents["risk_assessment"].listen_for = ["DIAGNOSIS_PROPOSED"]
        self.agents["procedure_coding"].listen_for = ["RISK_ASSESSED"]
        
        self.agents["medication_management"].listen_for = ["DIAGNOSIS_PROPOSED", "PROCEDURE_CODED"] # Listens to Dx!
        
        self.agents["treatment_planning"].listen_for = ["MEDICATION_CHECKED"]
        self.agents["output_generation"].listen_for = ["TREATMENT_PLANNED"]

        # Helper to run an agent in the mesh
        async def run_agent_task(event: Event):
            # Check for termination
            if session_id in self.terminated_sessions:
                print(f"DEBUG: Session {session_id} TERMINATED. Skipping task for {event.topic}")
                return

            print(f"DEBUG: run_agent_task triggered for event {event.topic}")
            # Log incoming event
            await blackboard_logger.log_event(
                session_id=session_id,
                level="EVENT",
                event_type=event.topic,
                data={"sender_id": event.sender_id, "payload_keys": list(event.data.keys()) if event.data else []}
            )
            
            # Find agents listening to this topic
            for agent_id, agent in self.agents.items():
                should_run = await agent.react(event, context)
                if should_run:
                    print(f"DEBUG: Agent {agent_id} WAKING UP for {event.topic}")
                    # Log agent start
                    start_time = time.time()
                    await blackboard_logger.log_agent_execution(
                        session_id=session_id,
                        agent_id=agent_id,
                        phase="start",
                        input_data=input_data
                    )
                    
                    # Execute Agent
                    await manager.broadcast({"type": "chat_message", "text": f"{agent.name} reacting to {event.topic}...", "sender": "System", "variant": "system"})
                    await self._broadcast_agent_status(agent.agent_id, "running")
                    
                    try:
                        output = await agent.execute(input_data, context)
                        print(f"DEBUG: Agent {agent_id} COMPLETED with status {output.status}")
                    except Exception as e:
                        print(f"ERROR: Agent {agent_id} failed during execution: {e}")
                        import traceback
                        traceback.print_exc()
                        return
                    duration_ms = int((time.time() - start_time) * 1000)
                    
                    # Log agent completion
                    await blackboard_logger.log_agent_execution(
                        session_id=session_id,
                        agent_id=agent_id,
                        phase="complete",
                        output_data=output.data,
                        duration_ms=duration_ms
                    )
                    
                    # Update Context
                    context[agent_id] = output.data
                    
                    # --- BROADCAST AGENT SUMMARY TO TEAM CHAT ---
                    # Use the agent's get_chat_summary method
                    chat_text = agent.get_chat_summary(output.data)
                    await manager.broadcast({
                        "type": "chat_message", 
                        "text": chat_text, 
                        "sender": agent.name, 
                        "agent_id": agent.agent_id,
                        "variant": "agent"
                    })
                    
                    # Log context snapshot after significant agents
                    await blackboard_logger.log_context_snapshot(
                        session_id=session_id,
                        context=context,
                        trigger=f"after_{agent_id}",
                        agent_id=agent_id
                    )
                    
                    # Handle Clarification (Pause Mesh)
                    if output.data.get("clarification_needed"):
                        # Log clarification request
                        await blackboard_logger.log_clarification(
                            session_id=session_id,
                            agent_id=agent.agent_id,
                            question=output.data.get("clarification_question"),
                            suggested_answer=output.data.get("suggested_answer")
                        )
                        
                        await manager.broadcast({
                            "type": "workflow_pause",
                            "reason": "Clarification Requested",
                            "session_id": session_id,
                            "agent_id": agent.agent_id,
                            "question": output.data.get("clarification_question"),
                            "suggested_answer": output.data.get("suggested_answer"),
                            "data": output.data
                        })
                        return # Stop this branch

                    # Success: Publish next event
                    # Map agent to output topic (Simplified for MVP)
                    topic_map = {
                        "user_assist": "ORIENTATION_COMPLETE",
                        "safety_triage": "SAFETY_CLEARED", # Assuming safety pass
                        "clinical_entity": "CLINICAL_EXTRACTED",
                        "diagnosis_mapping": "DIAGNOSIS_PROPOSED",
                        "risk_assessment": "RISK_ASSESSED",
                        "procedure_coding": "PROCEDURE_CODED",
                        "medication_management": "MEDICATION_CHECKED",
                        "treatment_planning": "TREATMENT_PLANNED",
                        "output_generation": "OUTPUT_GENERATED"
                    }
                    
                    next_topic = topic_map.get(agent_id, "UNKNOWN_EVENT")
                    
                    # Special Safety Check Override Logic
                    if agent_id == "safety_triage" and output.data.get("risk_detected"):
                         # Check Orientation for Override
                         orientation = context.get("user_assist", {})
                         if orientation.get("validation_result") == "approved":
                             await manager.broadcast({"type": "chat_message", "text": "Safety Override: Clinical Context confirmed.", "sender": "Supervisor", "variant": "consultant"})
                             next_topic = "SAFETY_CLEARED" # Force proceed
                         else:
                             # HARD STOP - Track who triggered the safety check for debate
                             triggering_agent_id = event.sender_id if event.sender_id != "system" else "user_assist"
                             await manager.broadcast({
                                 "type": "workflow_pause", 
                                 "reason": "SAFETY STOP", 
                                 "session_id": session_id, 
                                 "agent_id": "safety_triage", 
                                 "triggering_agent_id": triggering_agent_id,  # Debate owner
                                 "data": output.data, 
                                 "question": "Safety Risk Detected. Verify?"
                             })
                             return

                    new_event = Event(
                        topic=next_topic, 
                        sender_id=agent_id, 
                        data=output.data,
                        sender_priority=agent.priority
                    )
                    
                    # Check with Administrator before publishing
                    directive = await administrator.monitor(new_event, context)
                    
                    # Log administrator decision
                    await blackboard_logger.log_administrator_decision(
                        session_id=session_id,
                        directive=directive["directive"],
                        reason=directive.get("reason", ""),
                        winner_id=directive.get("winner_id"),
                        loop_detected=directive.get("loop_detected", False)
                    )
                    
                    if directive["directive"] == "STOP":
                        await blackboard_logger.log_workflow_event(session_id, "WORKFLOW_COMPLETE", {"reason": "administrator_stop"})
                        await manager.broadcast({"type": "workflow_complete", "data": context, "session_id": session_id})
                        return
                    elif directive["directive"] == "PAUSE":
                        await manager.broadcast({"type": "chat_message", "text": f"**ADMIN PAUSE**: {directive['reason']}", "sender": "Administrator", "variant": "system"})
                        return
                    elif directive["directive"] == "RESOLVED":
                        await manager.broadcast({
                            "type": "chat_message", 
                            "text": f"👨‍⚖️ **ADMIN RULING**: {directive['reason']} Target: *{directive['winner_id']}*.", 
                            "sender": "Administrator", 
                            "variant": "consultant"
                        })
                        
                        # FORCE WINNER: Only publish if this agent IS the winner
                        if agent_id == directive['winner_id']:
                             await bus.publish(new_event)
                        else:
                             # LOSER: Silenced. Do not publish.
                             await manager.broadcast({"type": "chat_message", "text": f"Agent *{agent.name}* silenced by Administrator.", "sender": "System", "variant": "system"})
                        
                        return
                    
                    # DEFAULT: CONTINUE
                    await bus.publish(new_event)
                    # Note: Agent status is set to 'idle' by frontend when chat_message is received

        # Wire the helper to the bus (Wildcard listener for simulator)

        # Wire the helper to the bus (Wildcard listener for simulator)
        # In real mesh, agents bind their own specific handlers.
        # Here, we bind the generic runner to ALL topics to dispatch to agents.
        bus.subscribe("*", run_agent_task)

        # Kickoff
        await blackboard_logger.log_workflow_event(session_id, "WORKFLOW_START", {"input_keys": list(input_data.keys())})
        await manager.broadcast({"type": "workflow_start", "message": "Agent Mesh Activated", "session_id": session_id})
        start_event = Event(topic="TRANSCRIPT_READY", sender_id="system", data=input_data)
        await bus.publish(start_event)

    async def submit_clarification(self, session_id: str, agent_id: str, answer: str):
        if session_id not in self.active_sessions:
            raise ValueError("Session not found")
        
        session_state = self.active_sessions[session_id]
        context = session_state["context"]
        
        # Store clarification
        if "user_clarifications" not in context:
            context["user_clarifications"] = {}
        context["user_clarifications"][agent_id] = answer
        
        # Log clarification response
        await blackboard_logger.log_clarification(
            session_id=session_id,
            agent_id=agent_id,
            question="(previous question)",
            user_answer=answer
        )
        
        # Chat Event: User Answer
        await manager.broadcast({
            "type": "chat_message",
            "text": f"{answer}",
            "sender": "User",
            "variant": "user"
        })

        # Resume Workflow
        session_state["status"] = "running"
        await self.run_workflow(session_state["input_data"], session_id)

        # 4. Finish
        await blackboard_logger.log_workflow_event(session_id, "WORKFLOW_COMPLETE", {"reason": "normal_completion"})
        await manager.broadcast({
            "type": "workflow_complete",
            "data": context
        })
    async def _broadcast_agent_status(self, agent_id: str, status: str, data: Any = None):
        await manager.broadcast({
            "type": "agent_update",
            "agent_id": agent_id,
            "status": status,
            "data": data
        })

    async def terminate_session(self, session_id: str):
        if session_id in self.active_sessions:
            self.terminated_sessions.add(session_id)
            self.active_sessions[session_id]["status"] = "terminated"
            
            # Broadcast termination
            await manager.broadcast({
                "type": "chat_message",
                "text": "🛑 **NETWORK TERMINATED**: Administrator has issued a hard-kill signal. All process threads halted.",
                "sender": "System",
                "variant": "system"
            })
            
            # Log it
            await blackboard_logger.log_workflow_event(session_id, "WORKFLOW_TERMINATED", {"reason": "user_kill_switch"})

orchestrator = Orchestrator()
