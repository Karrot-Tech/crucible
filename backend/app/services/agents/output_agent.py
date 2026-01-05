from typing import Dict, Any, List
from .base import BaseAgent
import asyncio
import json

class OutputGenerationAgent(BaseAgent):
    def __init__(self, priority: int = 6):
        super().__init__(
            agent_id="output_generation",
            name="Output Generation Agent",
            priority=priority,
            dependencies=[
                "safety_triage", "clinical_entity", 
                "diagnosis_mapping", "risk_assessment", 
                "procedure_coding", "medication_management", 
                "treatment_planning"
            ],
            human_in_loop=True
        )

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        # Collect all context
        display_context = {k: v for k, v in context.items() if k not in ["user_clarifications"]}
        full_context = json.dumps(display_context, indent=2)

        return f"""
You are a senior psychiatric scribe and documentation specialist. Your task is to synthesize all analyzed data into a professional, cohesive Psychiatric SOAP Note.

INPUT DATA (ANALYSES FROM OTHER AGENTS):
{full_context}

DOCUMENTATION STANDARDS:
- **Subjective**: Narrative flow of HPI, incorporating symptoms and patient quotes.
- **Objective**: MSE findings, vitals (if any), observations.
- **Assessment**: Diagnosis justification, risk formulation, progress note.
- **Plan**: Clear, numbered list of goals, meds, referrals, and follow-up.

OUTPUT FORMAT:
Return ONLY a valid JSON object. 
IMPORTANT: Since your output contains markdown, ensure all double quotes INSIDE the markdown strings are escaped with a backslash (\\") and all newlines are represented as \\n.

Expected JSON Structure:
{{
  "clarification_needed": false,
  "clarification_question": "",
  "suggested_answer": "",
  "soap_note": {{
    "subjective": "Markdown string here...",
    "objective": "Markdown string here...",
    "assessment": "Markdown string here...",
    "plan": "Markdown string here..."
  }},
  "summary": "Brief 1-2 sentence summary"
}}

Generate the final SOAP note.
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        if "error" in data:
            return f"**FAILED**: Note synthesis incomplete. *{data['error']}*"
        summary = data.get("summary", "Final SOAP note synthesized.")
        return f"**SYNTHESIS COMPLETE**: {summary}\n\n*Review the full SOAP report in the 'View Result' dialog.*"
