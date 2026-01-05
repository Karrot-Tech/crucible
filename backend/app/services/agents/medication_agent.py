from typing import Dict, Any, List
from .base import BaseAgent
import asyncio
import json

class MedicationManagementAgent(BaseAgent):
    def __init__(self, priority: int = 3):
        super().__init__(
            agent_id="medication_management",
            name="Medication Management Agent",
            priority=priority,
            dependencies=["clinical_entity"],
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        transcript = input_data.get("transcript", "")
        
        return f"""
You are a Medication Management Specialist.
Identify medications and changes.

**PEER REVIEW MODE**:
You are collaborating with a Diagnosis Agent.
1. Check the 'diagnosis_mapping' in the context.
2. Does the currently proposed Diagnosis match the medications you see?
3. IF NO (e.g., Diagnosis is "Anxiety" but patient is on "Risperidone"), you must FLAG this in your findings.
4. Explicitly state: "Potential Mismatch: Medications suggest [Other Condition]."

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "clarification_needed": boolean,
  "clarification_question": "string (optional)",
  "suggested_answer": "string (optional - e.g. '50mg daily' if inferred)",
  "medications": [
    {{
      "name": "string",
      "generic_name": "string",
      "brand_name": "string (or null)",
      "strength": "string",
      "form": "string",
      "route": "string",
      "frequency": "string",
      "indication": "string",
      "response": "string",
      "adherence": "string",
      "side_effects": ["string"]
    }}
  ],
  "changes_made": [
    {{
      "medication": "string",
      "change_type": "New Start" | "Discontinue" | "Increase Dose" | "Decrease Dose" | "No Change",
      "rationale": "string"
    }}
  ]
}}

IMPORTANT:
- If a medication is discussed but the DOSE or FREQUENCY is validly unclear (and required for a prescription), set "clarification_needed" to true and ask.
- Provide a `suggested_answer` if context hints at it (e.g. "Standard starting dose is 50mg?").
- Example: "Patient is taking Sertraline but didn't say how much. Ask for dose."
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "What is the specific dose of..." or "Please confirm frequency...".
- **DO NOT** ask "Sarah, how much are you taking?".

TRANSCRIPT:
{transcript}
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        meds = data.get("medications", [])
        changes = data.get("changes_made", [])
        
        summary = ""
        if meds:
            names = [f"*{m['name'].title()}*" for m in meds[:2]]
            summary += f"Monitoring {len(meds)} active medications, including {', '.join(names)}. "
        
        if changes:
            active_changes = [c for c in changes if c.get("change_type") != "No Change"]
            if active_changes:
                change_desc = [f"*{c['medication'].title()}* ({c['change_type']})" for c in active_changes[:2]]
                summary += f"**ADJUSTMENTS**: {', '.join(change_desc)}."
                
        return summary.strip() or "Medication review complete."
