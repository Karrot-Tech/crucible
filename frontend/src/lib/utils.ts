import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const AGENT_PERSONAS: Record<string, string> = {
  "safety_triage": "Safety Guardian",
  "clinical_entity": "Clinical Analyst",
  "diagnosis_mapping": "Lead Diagnostician",
  "risk_assessment": "Risk Monitor",
  "procedure_coding": "Medical Coder",
  "medication_management": "Pharmacologist",
  "treatment_planning": "Care Planner",
  "output_generation": "Scribe Architect",
  "user_assist": "Intake Coordinator",
  "administrator": "Administrator",
  "supervisor": "Administrator" // Legacy fallback
};

export const getAgentPersona = (id: string): string => {
  const key = id.toLowerCase();
  // Handle specific hardcoded 'System' or 'User' if needed
  if (key === 'system') return 'System';
  if (key === 'user') return 'Physician';

  // Check direct match
  if (AGENT_PERSONAS[key]) return AGENT_PERSONAS[key];

  // Normalize key (replace spaces with underscores) to try matching snake_case keys
  const normalizedKey = key.replace(/ /g, '_');
  if (AGENT_PERSONAS[normalizedKey]) return AGENT_PERSONAS[normalizedKey];

  // Check partial match (e.g. 'safety_triage_agent' or 'safety triage agent')
  const match = Object.keys(AGENT_PERSONAS).find(k => normalizedKey.includes(k));
  if (match) return AGENT_PERSONAS[match];

  // Fallback: format snake_case or whatever came in
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
};

export const replaceAgentNames = (text: string): string => {
  let newText = text;
  Object.entries(AGENT_PERSONAS).forEach(([key, persona]) => {
    // Create regex for loose matching (spaces or underscores) AND optional " agent" suffix
    // e.g. "safety_triage" matches "SAFETY TRIAGE", "safety_triage", "SAFETY TRIAGE AGENT"
    const regex = new RegExp(`${key.replace(/_/g, '[\\s_]')}(?:\\s+agent)?`, 'gi');
    newText = newText.replace(regex, persona);
  });
  return newText;
};
