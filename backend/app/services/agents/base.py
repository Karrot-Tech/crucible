import google.generativeai as genai
import os
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
from app.models.schemas import AgentOutput

# Configure Gemini
# NOTE: In production, use os.environ.get("GEMINI_API_KEY")
# For the prototype, we expect the key to be set in the environment.
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)

TEAM_ROSTER = """
THE MEDICAL AI TEAM:
1. Safety Triage Agent: Monitors for emergency risks (Self-Harm, Violence).
2. Clinical Entity Agent: Extracts key medical terms (Symptoms, Meds, Conditions).
3. Diagnosis Mapping Agent: Maps symptoms to ICD-10 codes.
4. Risk Assessment Agent: Performs C-SSRS suicide risk assessment.
5. Procedure Coding Agent: Assigns CPT codes for billing.
6. Medication Management Agent: details current medications and changes.
7. Treatment Planning Agent: Develops goals and interventions.
8. Output Generation Agent: Synthesizes the final SOAP note.

FORMATTING GUIDELINES FOR TEAM CHAT:
- Use *asterisks* to highlight clinical entities (e.g. *Fluoxetine*, *Major Depression*).
- Use **double asterisks** for high-level decisions or status (e.g. **SAFE**, **HALTED**, **DIAGNOSIS PROPOSED**).
- Be conversational but clinical. Your "get_chat_summary" output is what the provider sees.
"""

class BaseAgent(ABC):
    def __init__(
        self, 
        agent_id: str, 
        name: str, 
        priority: int = 1,
        dependencies: List[str] = [],
        human_in_loop: bool = False,
        model_name: str = "gemini-flash-latest"
    ):
        self.agent_id = agent_id
        self.name = name
        self.priority = priority
        self.dependencies = dependencies
        self.human_in_loop = human_in_loop
        self.listen_for: List[str] = [] # Topics to subscribe to
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
    
    async def react(self, event, context: Dict[str, Any]) -> bool:
        """
        Base logic: If the event topic matches one of our 'listen_for' topics,
        we return True to signal we want to wake up.
        """
        if event.topic in self.listen_for:
            return True
        return False

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentOutput:
        """
        Main execution flow for the agent.
        """
        # 1. Validate Input
        if not self.validate_input(input_data):
            return self.create_error_output("Invalid input data")

        # 2. Build Shared Collaborative Context
        shared_context = self._build_collaborative_context(context)

        # 3. Build Specific Prompt
        specific_prompt = self.build_prompt(input_data, context)
        
        # Combine
        prompt = f"{TEAM_ROSTER}\n\n{shared_context}\n\nYOUR SPECIFIC TASK:\n{specific_prompt}"

        # Check for User Clarifications in context (Specific to THIS agent)
        user_clarifications = context.get("user_clarifications", {})
        if self.agent_id in user_clarifications:
            clarification_text = f"\n\n*** DIRECT USER FEEDBACK FOR {self.agent_id.upper()} ***:\n"
            clarification_text += f"USER: {user_clarifications[self.agent_id]}\n"
            clarification_text += "INSTRUCTION: Incorporate this feedback immediately. If this answers your previous doubt, set 'clarification_needed' to false."
            prompt += clarification_text

        # 4. Call LLM
        try:
             # Always use call_llm so subclasses can override/mock it easily
             llm_response = await self.call_llm(prompt)
        except Exception as e:
            print(f"Error calling LLM for {self.agent_id}: {e}")
            return self.create_error_output(str(e))

        # 4. Parse Output
        parsed_data = self.parse_output(llm_response)

        # 5. Calculate Confidence
        confidence = self.assess_confidence(parsed_data)

        # 6. Return Structured Output
        return AgentOutput(
            agent_id=self.agent_id,
            status="completed", # or needs_review based on confidence
            confidence=confidence,
            data=parsed_data,
            reasoning="Steps taken by Gemini Agent.",
            timestamp=datetime.now()
        )

    def _build_collaborative_context(self, context: Dict[str, Any]) -> str:
        """
        Constructs a history of what other agents have asked and what the user replied.
        """
        user_clarifications = context.get("user_clarifications", {})
        if not user_clarifications:
            return "NO PRIOR HUMAN-IN-THE-LOOP INTERACTIONS."

        history = "SHARED TRANSCRIPT OF CLARIFICATIONS (Use this context):\n"
        
        # Iterate through clarifications to build history
        # Note: In a real DB this would be ordered. In Dict, hopefully ordered by insertion.
        for agent_id, answer in user_clarifications.items():
            # Try to find the original question from the agent's output in context
            question = "Unknown Question"
            if agent_id in context and "clarification_question" in context[agent_id]:
                question = context[agent_id]["clarification_question"]
            
            history += f"- [Agent: {agent_id.replace('_', ' ').title()}]\n"
            history += f"  Q: \"{question}\"\n"
            history += f"  A: \"{answer}\"\n"
        
        return history

    async def consult(self, question: str, context: Dict[str, Any]) -> str | None:
        """
        Optional: Allows this agent to act as a consultant for other agents.
        Returns a suggestion string or None if it has no helpful input.
        Default implementation returns None.
        """
        return None

    @abstractmethod
    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        pass

    async def call_llm(self, prompt: str) -> str:
        """
        Wrapper for the LLM call. Can be overridden for mocking.
        """
        if not API_KEY:
            print(f"WARNING: No GEMINI_API_KEY found for {self.agent_id}. Returning empty JSON.")
            return "{}"
        
        # Use asyncio.to_thread for the synchronous SDK call
        response = await asyncio.to_thread(self.model.generate_content, prompt)
        return response.text

    def parse_output(self, llm_output: str) -> Dict[str, Any]:
        """
        Parses LLM string output into a dictionary.
        Handles common markdown wrapping and common JSON syntax errors.
        """
        import json
        import re

        clean_output = llm_output.strip()
        
        # 1. Try direct parse
        try:
            return json.loads(clean_output)
        except:
            pass

        # 2. Extract from markdown code blocks
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', clean_output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass

        # 3. Last resort: find any { ... }
        match = re.search(r'(\{.*\})', clean_output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError as e:
                print(f"JSON subset parse failed for {self.agent_id}: {e}")
        
        return {
            "error": "Failed to parse JSON",
            "raw": llm_output,
            "clarification_question": "I encountered a formatting error while processing the analysis. Could you please provide a brief update or re-state the last point of the session to help me re-sync?"
        }

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        """Returns a summary of the agent's findings for the team chat."""
        # 1. Check for explicit summary/thought in data
        summary = data.get("summary", "")
        thought = data.get("reasoning", "")
        
        if summary:
            return summary
            
        # 2. Try to build a summary from other fields
        if data.get("clarification_needed"):
            return f"**PAUSED**: Clarification requested for agent *{self.agent_id}*."
            
        # 3. Use reasoning as fallback if summary is missing
        if thought:
             return thought

        return f"Agent *{self.agent_id}* processing complete."

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        return True

    def assess_confidence(self, data: Dict[str, Any]) -> float:
        return 0.95 # Default high confidence for mock

    def create_error_output(self, message: str) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            status="error",
            confidence=0.0,
            data={"error": message},
            reasoning="Error occurred during execution",
            timestamp=datetime.now()
        )
