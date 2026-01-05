from typing import Dict, Any, List
from .base import BaseAgent
import asyncio
import json

class RiskAssessmentAgent(BaseAgent):
    def __init__(self, priority: int = 2):
        super().__init__(
            agent_id="risk_assessment",
            name="Risk Assessment Agent (C-SSRS)",
            priority=priority, # High priority but after triage
            dependencies=["transcript"],
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        transcript = input_data.get("transcript", "")
        return f"""
You are a psychiatric risk assessment specialist trained in the Columbia-Suicide Severity Rating Scale (C-SSRS). Your task is to analyze the session transcript and complete a structured suicide risk assessment.

C-SSRS FRAMEWORK:
1. SUICIDAL IDEATION (Categories 1-5):
   - Wish to be dead
   - Non-specific active thoughts
   - Active ideation w/o intent
   - Active ideation w/ intent
   - Active ideation w/ plan & intent
2. SUICIDAL BEHAVIOR (Categories 6-10):
   - Preparatory acts
   - Aborted/Interrupted/Actual attempts

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "clarification_needed": boolean,
  "clarification_question": "string (optional)",
  "suggested_answer": "string (optional - best guess based on context)",
  "risk_level": "Low" | "Moderate" | "High" | "Imminent",
  "suicidal_ideation_present": boolean,
  "max_ideation_severity": int (0-5),
  "suicidal_behavior_present": boolean,
  "protective_factors": ["string"],
  "risk_factors": ["string"],
  "clinical_actions": ["string"],
  "cssrs_detail": {{
      "wish_to_be_dead": boolean,
      "active_thoughts": boolean,
      "specific_plan": boolean,
      "intent": boolean
  }}
}}

IMPORTANT:
- If C-SSRS questions were NOT asked and key information is missing to determine risk, set "clarification_needed" to true.
- Provide a `suggested_answer` if you can infer a likely response (e.g. "No active intent mentioned"), otherwise "Unknown".
- E.g., if a patient says "I want to die" but intent/plan wasn't queried, you MUST ask.
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "Did the patient mention..." or "Please confirm if..." or "What is the..."
- **DO NOT** ask "Sarah, do you..." or "How are you feeling?".

TRANSCRIPT:
{transcript}
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        risk_level = data.get("risk_level", "Unknown")
        ideation = "PRESENT" if data.get("suicidal_ideation_present") else "NOT PRESENT"
        
        status_color = "**HIGH RISK**" if risk_level in ["High", "Imminent"] else "**STABLE**"
        return f"{status_color}: C-SSRS Level *{risk_level}*. Suicidal ideation is *{ideation}*."
