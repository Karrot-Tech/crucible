from typing import Dict, Any, List
from .base import BaseAgent
import asyncio
import json

class DiagnosisMappingAgent(BaseAgent):
    def __init__(self, priority: int = 3):
        super().__init__(
            agent_id="diagnosis_mapping",
            name="Diagnosis Mapping Agent",
            priority=priority,
            dependencies=["clinical_entity"], # Depends on clinical entities
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        # Get extracted entities from context (output of ClinicalEntityAgent)
        clinical_data = context.get("clinical", {})
        
        # Format the clinical data for the prompt
        entities_str = json.dumps(clinical_data, indent=2)

        return f"""
You are a psychiatric diagnosis coding specialist with deep knowledge of DSM-5 criteria and ICD-10-CM F codes. Your task is to analyze clinical information and assign appropriate psychiatric diagnosis codes.

INPUT DATA:
{entities_str}

DIAGNOSTIC PROCESS:
1. SYMPTOM CLUSTER ANALYSIS: Group symptoms into diagnostic categories.
2. DSM-5 CRITERIA MATCHING: Check criteria for potential diagnoses.
3. ICD-10-CM CODE SELECTION: Select most specific code (with severity specifiers).
4. DIAGNOSIS HIERARCHY: Determine Primary, Secondary, and Rule-out diagnoses.

COMMON ICD-10-CM F CODE RANGES:
F32.x (MDD Single), F33.x (MDD Recurrent), F31.x (Bipolar), F41.1 (GAD), F43.10 (PTSD), etc.

**PEER REVIEW MODE**:
You are collaborating with a Medication Management Agent.
1. Check if 'medication_management' data exists in the context.
2. IF the Medication Agent suggests a medication that contradicts your diagnosis (e.g., Lithium for Unipolar Depression), you MUST RE-EVALUATE.
3. If you change your mind, update the diagnosis and explain why in the 'reasoning' field.
4. If you stand by your diagnosis despite the mismatch, explain why the medication might be off-label or secondary.

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "clarification_needed": boolean,
  "clarification_question": "string (optional question if critical info for diagnosis is missing)",
  "suggested_answer": "string (proactive answer if clarification_needed is true)",
  "primary_diagnosis": {{
    "code": "string (e.g., F32.1)",
    "description": "string",
    "justification": "string",
    "dsm_criteria_met": ["string"],
    "confidence": float (0.0-1.0)
  }},
  "secondary_diagnoses": [
    {{
      "code": "string",
      "description": "string",
      "justification": "string",
      "dsm_criteria_met": ["string"],
      "confidence": float
    }}
  ],
  "ruled_out": [
    {{
      "code": "string",
      "description": "string",
      "reason": "string"
    }}
  ]
}}

IMPORTANT:
- If there is insufficient information to confirm a primary diagnosis (e.g. uncertain duration, missing key criteria), set "clarification_needed" to true and ask.
- **MANDATORY**: If "clarification_needed" is true, you MUST provide a "suggested_answer" based on your best inference from the transcript.
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "Does the patient meet criteria for..." or "Please confirm duration of...".
- **DO NOT** ask the patient directly.
- Do NOT hallucinate criteria that are not present in the input.

Analyze this clinical information and provide diagnosis codes.
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        primary = data.get("primary_diagnosis", {})
        code = primary.get("code")
        desc = primary.get("description")
        
        if code and desc:
            return f"**DIAGNOSIS PROPOSED**: *{code}* (*{desc}*)"
        
        if data.get("clarification_needed"):
            return "**PAUSED**: Insufficient data for definitive diagnosis. Clarification requested."
            
        return "Diagnosis analysis complete."
