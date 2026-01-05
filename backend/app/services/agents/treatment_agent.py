from typing import Dict, Any, List
from .base import BaseAgent
import asyncio
import json

class TreatmentPlanningAgent(BaseAgent):
    def __init__(self, priority: int = 5):
        super().__init__(
            agent_id="treatment_planning",
            name="Treatment Planning Agent",
            priority=priority,
            dependencies=["diagnosis_mapping", "risk_assessment", "medication_management"],
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        diagnosis_data = context.get("diagnosis", {})
        risk_data = context.get("risk", {})
        medication_data = context.get("medication", {})
        clinical_data = context.get("clinical", {})
        
        # Format context for the LLM
        context_str = json.dumps({
            "diagnosis": diagnosis_data,
            "risk_assessment": risk_data,
            "medications": medication_data,
            "clinical_entities": clinical_data
        }, indent=2)

        return f"""
You are a psychiatric treatment planning specialist. Your task is to develop a comprehensive, actionable treatment plan based on the clinical analysis provided.

INPUT CONTEXT:
{context_str}

PLANNING REQUIREMENTS:
1. **Goals**: Specific, measurable, achievable, relevant, and time-bound (SMART) goals based on the Diagnosis.
2. **Interventions**: Specific clinical actions (e.g., CBT techniques, medication adjustments, safety planning).
3. **Follow-up**: Determine appropriate follow-up interval based on Risk and Severity.

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "clarification_needed": boolean,
  "clarification_question": "string (optional)",
  "suggested_answer": "string (proactive answer if clarification_needed is true)",
  "treatment_goals": [
    {{
      "goal": "string",
      "target_date": "string (e.g., '3 months')",
      "status": "New" | "Ongoing" | "Met"
    }}
  ],
  "interventions": [
    "string (e.g., 'Initiate Sertraline 50mg')",
    "string (e.g., 'Safety plan developed')"
  ],
  "referrals": ["string"],
  "follow_up_plan": "string (e.g., 'Return in 2 weeks')"
}}

IMPORTANT:
- Align interventions with the Medication Management Agent's output.
- If Risk is High/Imminent, ensuring safety is the PRIORITY goal.
- If the plan implies an action (e.g., referral) that wasn't discussed, do NOT hallucinate it. Only reflect what likely occurred or is standard of care if implied.
- **MANDATORY**: If "clarification_needed" is true, you MUST provide a "suggested_answer" based on your best inference from the transcript.
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "What is the intended follow-up for..." or "Please confirm the goal for...".
- **DO NOT** ask the patient directly.

Develop the treatment plan.
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        goals = data.get("treatment_goals", [])
        interventions = data.get("interventions", [])
        follow_up = data.get("follow_up_plan", "TBD")
        
        return f"**PLAN DEVELOPED**: {len(goals)} *Clinical Goals* and {len(interventions)} *Interventions*. **FOLLOW-UP**: *{follow_up}*."
