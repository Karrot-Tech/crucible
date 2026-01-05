from typing import Dict, Any
from .base import BaseAgent
import asyncio

class ClinicalEntityAgent(BaseAgent):
    def __init__(self, priority: int = 2):
        super().__init__(
            agent_id="clinical_entity",
            name="Clinical Entity Extraction",
            priority=priority,
            dependencies=["transcript"] # Implicit dependency on input
        )

    async def consult(self, question: str, context: Dict[str, Any]) -> str | None:
        """
        Acts as a 'Knowledge Base' consultant. 
        It has seen the raw transcript and extracted entities, so it can answer factual questions.
        """
        # If we have extracted data, use it. Otherwise use raw transcript.
        input_data = context.get("input_data", {})
        
        transcript = ""
        # Try to find transcript in session input
        if "transcript" in input_data:
             transcript = input_data["transcript"]
        
        if not transcript:
            return None

        prompt = f"""
        You are the Clinical Entity Agent. A peer agent needs help with this question:
        "{question}"

        Please check the transcript below. If the answer is explicitly stated, provide it concisely (e.g., "50mg", "20 minutes"). 
        If NOT stated, return "NONE".

        TRANSCRIPT:
        {transcript}
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            answer = response.text.strip()
            if "NONE" in answer or "None" in answer:
                return None
            return answer
        except:
            return None

    def build_prompt(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> str:
        transcript = input_data.get("transcript", "")
        return f"""
You are a psychiatric clinical entity extraction specialist. Extract all clinically relevant information from this psychiatric session transcript and organize it into structured categories.

EXTRACTION CATEGORIES:
1. PRESENTING SYMPTOMS (symptom, onset, duration, frequency, severity, context, impact)
2. MENTAL STATUS OBSERVATIONS (appearance, behavior, speech, mood, affect, thought_process, thought_content, perception, cognition, insight, judgment)
3. CURRENT MEDICATIONS (name, dose, frequency, start_date, response, adherence)
4. SUBSTANCE USE (alcohol, tobacco, drugs)
5. PAST PSYCHIATRIC HISTORY
6. MEDICAL HISTORY
7. SOCIAL HISTORY
8. FAMILY PSYCHIATRIC HISTORY
9. FUNCTIONAL ASSESSMENT
10. ASSESSMENT SCALE RESULTS

OUTPUT FORMAT:
Return ONLY a valid JSON object with this structure:
{{
  "clarification_needed": boolean,
  "clarification_question": "string (optional question to ask the user)",
  "suggested_answer": "string (proactive answer if clarification_needed is true)",
  "presenting_symptoms": [
    {{
      "symptom": "string",
      "onset": "string",
      "duration": "string",
      "severity": "string",
      "context": "string",
      "impact": "string"
    }}
  ],
  "mental_status_exam": {{
    "appearance": "string",
    "behavior": "string",
    "speech": "string",
    "mood": "string",
    "affect": "string",
    "thought_process": "string",
    "thought_content": "string",
    "perception": "string",
    "cognition": "string",
    "insight": "string",
    "judgment": "string"
  }},
  "current_medications": [],
  "substance_use": {{}},
  "past_psychiatric_history": {{}},
  "medical_history": {{}},
  "social_history": {{}},
  "family_psychiatric_history": {{}},
  "functional_assessment": {{}},
  "assessment_scales": []
}}

IMPORTANT: 
- If critical information for coding is missing (e.g., medication dose, duration of symptoms), set "clarification_needed" to true and ask.
- **MANDATORY**: If "clarification_needed" is true, you MUST provide a "suggested_answer" based on your best inference from the transcript.
- **AUDIENCE**: You are speaking to the **MEDICAL PROVIDER** (the user), NOT the patient.
- **PHRASING**: Ask "Did the patient mention..." or "Please clarify if...".
- **DO NOT** ask the patient directly (e.g., "Sarah, what dose are you on?").
- Use "not assessed" if element not addressed.

TRANSCRIPT:
{transcript}
"""

    def get_chat_summary(self, data: Dict[str, Any]) -> str:
        symptoms = data.get("presenting_symptoms", [])
        meds = data.get("current_medications", [])
        
        summary = ""
        if symptoms:
            names = [f"*{s['symptom'].title()}*" for s in symptoms[:3]]
            summary += f"Extracted {len(symptoms)} symptoms, including {', '.join(names)}. "
        if meds:
            names = [f"*{m['name'].title()}*" for m in meds[:3]]
            summary += f"Identified {len(meds)} medications, including {', '.join(names)}. "
            
        return summary.strip() or "Clinical entities extracted."
