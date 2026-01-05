from typing import Dict, Any, List
from .base import BaseAgent
import asyncio

class SafetyTriageAgent(BaseAgent):
    def __init__(self, priority: int = 1):
        super().__init__(
            agent_id="safety_triage",
            name="Safety Triage Agent",
            priority=priority,
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        transcript = input_data.get("transcript", "")
        return f"""
You are a psychiatric safety specialist. Your CRITICAL task is to immediately identify any safety concerns in this session transcript that require urgent clinical attention.

PRIORITY SAFETY CONCERNS:
1. SUICIDE RISK INDICATORS (ideation, intent, plan, preparatory behaviors)
2. HOMICIDAL RISK INDICATORS (threats, violence)
3. ABUSE/NEGLECT (child, elder, domestic)
4. ACUTE PSYCHIATRIC EMERGENCIES (psychosis, mania, delirium)

ANALYSIS REQUIRED:
For each safety concern detected, provide the details.

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "risk_detected": boolean,
  "clarification_needed": boolean,
  "clarification_question": "string (optional question to ask the user)",
  "suggested_answer": "string (proactive answer if clarification_needed is true)",
  "concerns": [
    {{
      "type": "Suicide Risk" | "Homicide Risk" | "Abuse" | "Acute Emergency",
      "severity": "Low" | "Moderate" | "High" | "Imminent",
      "evidence": "string (quote)",
      "recommended_action": "string"
    }}
  ],
  "summary": "string"
}}

IMPORTANT:
- If there is ambiguity or a potential risk is hinted at but not clear, set "clarification_needed" to true and ask a specific question in "clarification_question".
- **MANDATORY**: If "clarification_needed" is true, you MUST provide a "suggested_answer" based on your best inference from the transcript.
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "Did the patient mention..." or "Please clarify if the patient..." or "Is there evidence for...".
- **DO NOT** ask the patient directly (e.g., "How are you feeling?", "Are you safe?").
- DO NOT HALLUCINATE risks. If it's unclear, ask.

If NO safety concerns are detected, return "risk_detected": false and an empty concerns list.

TRANSCRIPT:
{transcript}
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        if data.get("risk_detected"):
            summary = data.get('summary', 'Safety concerns detected.')
            return f"**SAFETY RISK DETECTED**: {summary}\n\n*Action required immediately.*"
        
        return "**SAFE**: No immediate safety risks identified in the *transcript*."
