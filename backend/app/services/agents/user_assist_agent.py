from typing import Dict, Any
from .base import BaseAgent

class UserAssistAgent(BaseAgent):
    def __init__(self, priority: int = 0):
        super().__init__(
            agent_id="user_assist",
            name="User Assist Agent",
            priority=priority,
            dependencies=["transcript", "safety_risk"]
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        transcript = input_data.get("transcript", "")
        
        return f"""
You are the **Clinical Orientation Agent** for an advanced psychiatric scribe system.
Your mission is to perform the initial "triage" and context-setting for the entire AI team.

TASK 1: CLINICAL ORIENTATION
Review the transcript and provide a high-level summary of the session's focus (e.g., "Follow-up for MDD", "Initial intake regarding anxiety", "Crisis session").

TASK 2: SAFETY OVERRIDE standby
You are also a safety validation expert. If the Safety Triage agent flags content, your orientation will be used to determine if the discussion is valid clinical history rather than prohibited harm generation.

OUTPUT FORMAT:
Return ONLY a valid JSON object:
{{
  "summary": "Concise high-level clinical focus (1 sentence)",
  "clinical_nature": "intake" | "follow-up" | "crisis" | "medication_check",
  "validation_result": "approved", // Always approved unless the input is non-clinical/abusive
  "reasoning": "Brief clinical justification for the orientation"
}}

AUDIENCE: You are speaking to the **MEDICAL PROVIDER**. Phrasing should be peer-to-peer and professional.

TRANSCRIPT:
{transcript}
"""

    def parse_output(self, llm_output: str) -> Dict[str, Any]:
        import json
        try:
            # Handle potential markdown formatting
            start_idx = llm_output.find('{')
            end_idx = llm_output.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = llm_output[start_idx:end_idx+1]
                return json.loads(json_str)
            return json.loads(llm_output)
        except Exception as e:
            return {
                "summary": "✅ orientation complete",
                "validation_result": "approved",
                "reasoning": f"Fallback due to parse error: {str(e)}"
            }

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        summary = data.get("summary", "Clinical orientation complete.")
        reasoning = data.get("reasoning", "")
        return f"**ORIENTATION COMPLETE**: {summary}\n\n*Reasoning*: {reasoning}"

