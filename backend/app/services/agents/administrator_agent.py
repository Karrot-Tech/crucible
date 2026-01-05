from typing import Dict, Any, List
from .base import BaseAgent
from ...core.event_bus import Event
import asyncio

class AdministratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="administrator",
            name="Workflow Administrator",
            priority=0,
            dependencies=[]
        )
        self.max_loops = 3
        self.interaction_history: List[str] = [] # Track sender_ids
        
    async def monitor(self, event: Event, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates the event stream for loops or completion.
        Returns a directive: 'CONTINUE', 'PAUSE', 'STOP', 'RESOLVED'.
        """
        # 0. Ignore system events to prevent noise
        if event.sender_id in ["system", "supervisor"]:
            return {"directive": "CONTINUE"}

        # 1. Update History with Priority
        self.interaction_history.append({"id": event.sender_id, "priority": event.sender_priority})
        
        # 2. Check for Infinite Loops (A -> B -> A -> B pattern)
        if self._detect_loop():
            # JUDGE MODE: Resolve by Rank
            # Identify the loop participants
            last_4 = self.interaction_history[-4:] # [{'id': 'A', 'p': 1}, {'id': 'B', 'p': 5}...]
            unique_participants = list({x["id"]: x for x in last_4}.values())
            
            # Find winner (Highest Priority)
            winner = max(unique_participants, key=lambda x: x["priority"])
            
            return {
                "directive": "RESOLVED",
                "reason": f"Infinite debate detected. Resolving by Authority.",
                "winner_id": winner["id"],
                "winner_priority": winner["priority"],
                "action": "ACCEPT_WINNER_STATE"
            }

        # 3. Check for Global Completion (Basic Heuristic)
        # In a real mesh, this would be a complex goal predicate
        required_keys = ["clinical", "diagnosis", "medication", "output"]
        if all(k in context for k in required_keys) and event.topic == "OUTPUT_GENERATED":
             return {"directive": "STOP", "reason": "All goals met."}

        return {"directive": "CONTINUE"}

    def _detect_loop(self) -> bool:
        """
        Simple heuristic: Check if the last 4 senders form a repetitive ABAB pattern.
        """
        if len(self.interaction_history) < 4:
            return False
        
        last_4 = [x["id"] for x in self.interaction_history[-4:]]
        # Pattern: A, B, A, B
        if last_4[0] == last_4[2] and last_4[1] == last_4[3] and last_4[0] != last_4[1]:
            return True
        
        return False

    # Standard/mock implementation for abstract methods
    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        return "" 
    
    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        return "👀 Monitoring workflow..."
