from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# --- Clinical Entities ---

class Symptom(BaseModel):
    symptom: str
    onset: Optional[str] = None
    duration: Optional[str] = None
    frequency: Optional[str] = None
    severity: Optional[str] = None
    context: Optional[str] = None
    impact: Optional[str] = None

class Medication(BaseModel):
    name: str
    dose_frequency: Optional[str] = Field(None, alias="dose_and_frequency")
    start_date: Optional[str] = None
    prescriber: Optional[str] = None
    response: Optional[str] = None
    adherence: Optional[str] = None

class MentalStatusExam(BaseModel):
    appearance: Optional[str] = None
    behavior: Optional[str] = None
    speech: Optional[str] = None
    mood: Optional[str] = None
    affect: Optional[str] = None
    thought_process: Optional[str] = None
    thought_content: Optional[str] = None
    perception: Optional[str] = None
    cognition: Optional[str] = None
    insight: Optional[str] = None
    judgment: Optional[str] = None

class AssessmentScale(BaseModel):
    scale_name: str
    score: int
    interpretation: Optional[str] = None
    comparison: Optional[str] = None

# --- Diagnosis ---

class DiagnosisCandidate(BaseModel):
    code: str
    description: str
    justification: str
    dsm_criteria_met: List[str]
    confidence: float
    type: str # Primary, Secondary, RuleOut

class DiagnosisOutput(BaseModel):
    primary_diagnosis: Optional[DiagnosisCandidate] = None
    secondary_diagnoses: List[DiagnosisCandidate] = []
    ruled_out: List[DiagnosisCandidate] = []
    required_clarifications: List[str] = []

# --- Risk Assessment ---

class RiskAssessment(BaseModel):
    risk_level: str # Low, Moderate, High, Imminent
    suicidal_ideation: bool
    suicidal_behavior: bool
    homicidal_ideation: bool
    protective_factors: List[str] = []
    clinical_actions: List[str] = []
    cssrs_categories_present: List[int] = [] # 1-5 for ideation, 6-10 for behavior

# --- Agent IO ---

class AgentOutput(BaseModel):
    agent_id: str
    status: str # completed, needs_review, error, needs_clarification
    confidence: float
    data: Dict[str, Any]
    reasoning: str
    timestamp: datetime
    clarification_needed: bool = False
    clarification_question: Optional[str] = None
