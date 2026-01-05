from typing import Dict, Any, List
from .base import BaseAgent
import asyncio
import json

class ProcedureCodingAgent(BaseAgent):
    def __init__(self, priority: int = 4):
        super().__init__(
            agent_id="procedure_coding",
            name="Procedure Coding Agent",
            priority=priority,
            dependencies=["clinical_entity", "diagnosis_mapping"],
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        transcript = input_data.get("transcript", "")
        clinical_data = context.get("clinical", {})
        diagnosis_data = context.get("diagnosis", {})
        
        # We need session date and patient info if available, but primarily transcript and clinical info for time/complexity
        
        return f"""
You are a psychiatric billing and coding specialist. Your task is to analyze the session and assign appropriate CPT codes for reimbursement.

INFORMATION REQUIRED:
1. Session Type (Initial vs Follow-up)
2. Provider Type (Prescribing vs Non-prescribing)
3. Services Provided (Eval, Therapy, Med Management, Crisis)
4. Time Documentation (Total time, Face-to-face time)
5. Modality (In-person, Telehealth)

CPT CODE LOGIC:
- Initial: 90791 (Non-MD), 90792 (MD)
- Therapy: 90832 (30m), 90834 (45m), 90837 (60m)
- Med Management (E/M): 99212-99215 (Established), 99202-99205 (New)
- Combined: E/M + Therapy Add-on (90833, 90836, 90838)
- Crisis: 90839 + 90840

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "clarification_needed": boolean,
  "clarification_question": "string (optional)",
  "suggested_answer": "string (optional)",
  "primary_code": {{
    "code": "string",
    "description": "string",
    "rationale": "string"
  }},
  "addon_codes": [
    {{
      "code": "string",
      "description": "string",
      "rationale": "string"
    }}
  ],
  "modifiers": ["string"],
  "medical_necessity": "string",
  "confidence": "High" | "Medium" | "Low"
}}

IMPORTANT:
- If session duration is NOT mentioned in the transcript (e.g., "start time", "end time", or "we've been talking for X minutes"), you MUST set "clarification_needed" to true and ask for the session duration. Time is critical for coding.
- Provide a `suggested_answer` if standard duration applies (e.g. "53 minutes (Standard 90837)?").
- Determine Provider Type from context or ask if unclear.
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "What was the total session time?" or "Please specify the duration...".
- **DO NOT** ask the patient directly.

TRANSCRIPT START:
{transcript[:2000]}... (truncated for brevity if long)
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        primary = data.get("primary_code")
        if primary:
            return f"**CODE ASSIGNED**: *{primary.get('code')}* (*{primary.get('description', 'Procedure')}*)."
        
        if data.get("clarification_needed"):
            return "**PAUSED**: Time/Duration missing. *Manual verification* required for CPT mapping."
            
        return "Procedure analysis complete."
