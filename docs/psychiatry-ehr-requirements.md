# Psychiatry-Specific EHR Data Mapping & Structured Documentation Requirements

## Executive Summary

Psychiatric practice has unique EHR requirements that differ significantly from general medical specialties. Behavioral health and primary care differ in their language, classifications, codes, data reporting requirements, and regulations. This report details the specific structured data formats, coding systems, discrete data fields, and documentation templates required for psychiatric medical scribe applications to integrate successfully with psychiatric EHR systems.

## 1. Psychiatric Diagnosis Coding (ICD-10-CM F Codes)

### Overview of Mental Health Diagnosis Coding

While DSM-5 and ICD-10 are maintained by different organizations, the diagnostic codes you find in DSM-5 are actually ICD-10 codes. The relationship between these two systems is critical for psychiatric documentation:

**DSM-5 (Diagnostic and Statistical Manual of Mental Disorders)**:
- Maintained by the American Psychiatric Association (APA)
- Provides comprehensive diagnostic criteria for mental disorders
- References ICD-10-CM codes for billing and documentation
- Updated periodically with coding changes

**ICD-10-CM Coding for Psychiatry**:
- ICD-10-CM is an alpha-numeric system that contains approximately 68,000 codes; each code starts with a letter followed by anywhere from 2 to 7 numbers
- Mental health diagnoses primarily use F codes (F00-F99)
- Required by HIPAA for all insurance claims and billing

### Structure of ICD-10-CM F Codes

F codes are further broken up into the following categories: F00–F09: codes for organic, including symptomatic, mental disorders; F10–F19: codes for mental and behavioral disorders due to psychoactive substance abuse

**Complete F Code Categories**:

| Code Range | Category | Examples |
|------------|----------|----------|
| F00-F09 | Organic mental disorders | Dementia, delirium |
| F10-F19 | Substance-related disorders | Alcohol use disorder, opioid dependence |
| F20-F29 | Schizophrenia spectrum | Schizophrenia, schizoaffective disorder |
| F30-F39 | Mood disorders | Major depressive disorder, bipolar disorder |
| F40-F48 | Anxiety and stress-related disorders | Generalized anxiety disorder, PTSD, OCD |
| F50-F59 | Behavioral syndromes | Eating disorders, sleep disorders |
| F60-F69 | Personality disorders | Borderline, antisocial, narcissistic PD |
| F70-F79 | Intellectual disabilities | Mild to profound intellectual disability |
| F80-F89 | Developmental disorders | Autism spectrum disorder, ADHD |
| F90-F98 | Behavioral/emotional disorders of childhood | Conduct disorder, oppositional defiant disorder |
| F99 | Unspecified mental disorder | When specific diagnosis cannot be determined |

### Common Psychiatric Diagnoses and Their Codes

**Mood Disorders**:
- F32.0-F32.9: Major depressive disorder, single episode (severity variants)
- F33.0-F33.9: Major depressive disorder, recurrent
- F34.1: Dysthymia (persistent depressive disorder)
- F31.0-F31.9: Bipolar disorder (with various episode specifiers)

**Anxiety Disorders**:
- F41.0: Panic disorder
- F41.1: Generalized anxiety disorder
- F40.10: Social anxiety disorder (social phobia)
- F42.2-F42.9: Obsessive-compulsive disorder

**Trauma and Stress-Related**:
- F43.10: Post-traumatic stress disorder (PTSD)
- F43.21-F43.23: Adjustment disorders

**Psychotic Disorders**:
- F20.0-F20.9: Schizophrenia (with various specifiers)
- F25.0-F25.9: Schizoaffective disorder

**Substance Use Disorders**:
- The ICD-10-CM coding system requires the clinician to combine substance use disorder diagnoses (e.g., substance dependence) with substance-induced diagnoses (e.g., substance-induced depressive disorder)
- Format: F1x.xxx where x specifies substance type and use pattern
- Example: F10.20 (Alcohol dependence, uncomplicated)

### Z Codes for Mental Health

Z codes for mental health include codes for factors influencing health status and contact with health services (includes the 2018 No Diagnosis or Condition code)

Common Z Codes:
- Z03.89: No diagnosis or condition
- Z13.89: Encounter for screening for other disorder
- Z71.3: Dietary counseling
- Z63.0: Problems in relationship with spouse or partner

### Coding Challenges Specific to Psychiatry

**Challenge 1: DSM-5 and ICD-10-CM Discrepancies**

For instance, DSM-5 uses F40.10 for Social Anxiety Disorder which maps to "Social Phobia, Unspecified" in the ICD-10-CM. Social phobia, generalized is coded as F40.11, which may be a more appropriate diagnostic code for different presentations

Psychiatrists may need to choose between:
- Using the DSM-5 recommended code (simpler, consistent with diagnostic manual)
- Selecting a more specific ICD-10-CM code (more accurate, better reimbursement)

**Challenge 2: Specifiers and Severity Levels**

Most psychiatric diagnoses require additional coding for:
- Severity (mild, moderate, severe)
- Episode type (current, in partial remission, in full remission)
- Specific features (with anxious distress, with psychotic features, etc.)

**Challenge 3: Comorbidity**

Psychiatric patients often have multiple diagnoses requiring:
- Primary diagnosis determination
- Multiple ICD-10-CM codes on single claim
- Accurate representation of symptom complexity

## 2. Psychiatric Procedure Coding (CPT Codes)

### Psychiatric Diagnostic Evaluation Codes

90791: Psychiatric diagnostic evaluation without medical services, typically used for an initial diagnostic evaluation, usually covered once per client; 90792: Psychiatric diagnostic evaluation with medical services, including medical services in addition to the diagnostic evaluation

**Key Differences**:
- **90791**: Used by therapists, psychologists, social workers (non-prescribing clinicians)
- **90792**: Used by psychiatrists, psychiatric nurse practitioners (prescribing clinicians performing medical assessment)

### Psychotherapy CPT Codes

90832: 30-minute psychotherapy session (16-37 minutes), for individual sessions lasting up to 37 minutes; 90834: 45-minute psychotherapy session (38-52 minutes), for individual sessions lasting up to 52 minutes

**Time-Based Psychotherapy Codes**:

| CPT Code | Duration | Minimum Time Required |
|----------|----------|----------------------|
| 90832 | 30 minutes | 16-37 minutes |
| 90834 | 45 minutes | 38-52 minutes |
| 90837 | 60 minutes | 53+ minutes |

**Important**: Each CPT code includes specific time frames. For example, 90834 (45-minute therapy) requires at least 38 minutes spent face-to-face with the client; 90837 (60-minute therapy) requires at least 53 minutes

### Psychotherapy with Evaluation & Management (E/M)

For psychiatrists providing both medication management and therapy:

**Add-on Codes** (used with E/M codes):
- 90833: Psychotherapy add-on, 30 minutes (used with 99212-99215)
- 90836: Psychotherapy add-on, 45 minutes
- 90838: Psychotherapy add-on, 60 minutes

**Usage Example**:
- Psychiatrist sees patient for 15-minute medication check + 30 minutes therapy
- Bill: 99213 (established patient E/M) + 90833 (therapy add-on)
- Modifier -25 must be added to E/M code to indicate separate service

### Specialized Therapy Codes

**Family and Group Therapy**:
- 90846: Family psychotherapy without patient present
- 90847: Family psychotherapy with patient present
- 90853: Group psychotherapy

**Crisis Intervention**:
- 90839: Psychotherapy for crisis, first 60 minutes
- 90840: Each additional 30 minutes (add-on code)

### New 2025 Psychiatric CPT Codes

Mental health billing codes 2025 include a new code – 90868 – introduced for ultra-brief psychotherapy sessions (sessions lasting less than 20 minutes)

**Collaborative Care Model (CoCM) Codes**:

99492: Initial psychiatric collaborative care management (70 minutes in the first month); 99493: Subsequent management services (60 minutes per month); 99494: Additional 30 minutes of care management beyond the primary time blocks

**2025 Update**: In 2025, CMS expanded who can deliver some of these services – for example, licensed counselors and marriage/family therapists can now participate in collaborative care teams for CoCM codes

### Evaluation & Management (E/M) Codes for Medication Management

Psychiatrists commonly use standard medical E/M codes for medication management visits:

**Outpatient Visits**:
- 99202-99205: New patient office visits (time-based or complexity-based)
- 99212-99215: Established patient office visits

**Typical Use**:
- 99212: Brief medication check (10 minutes)
- 99213: Standard medication management (15 minutes)
- 99214: Complex medication management (25 minutes)
- 99215: Very complex cases (40 minutes)

### Telehealth Modifiers for Psychiatry

Psychiatrists and other prescribers also use telehealth extensively. Psychiatry telehealth CPT codes 2025 usage follows the same rules – you use the normal E/M or psychotherapy codes and append telehealth modifiers

**Key Modifiers**:
- **-95**: Synchronous telemedicine service (video)
- **-93**: Audio-only service (when video not available)
- **GT**: Via interactive audio/video (alternative to -95)

After March 2025, Medicare permanently defined "interactive telecommunications system" to include audio-only for mental health, as long as the provider could use video but the patient cannot or doesn't consent to video

**Place of Service Codes**:
- POS 02: Telehealth (patient's home)
- POS 10: Patient's home (for in-person home visits)

## 3. Psychiatric Assessment Scales and LOINC Codes

### Overview of Standardized Assessment Tools

Psychiatrists use validated screening and assessment tools to:
- Screen for mental health conditions
- Measure symptom severity
- Track treatment response over time
- Document clinical decision-making
- Support quality reporting and value-based care

These assessments must be coded using both:
- **CPT codes** for billing (96127, 96160, etc.)
- **LOINC codes** for the specific instrument and results

### Patient Health Questionnaire-9 (PHQ-9)

**Purpose**: Depression screening and severity measurement

**LOINC Codes**:
- 44249-1: PHQ-9 quick depression assessment panel [Reported.PHQ]
- 44261-6: Patient Health Questionnaire 9 item (PHQ-9) total score [Reported]

**Scoring System**:
Add up all checked boxes on PHQ-9. For every check: Not at all = 0; Several days = 1; More than half the days = 2; Nearly every day = 3. Interpretation: 1-4 = Minimal depression; 5-9 = Mild depression; 10-14 = Moderate depression; 15-19 = Moderately severe depression; 20-27 = Severe depression

**Structure**:
- The PHQ-9 is the nine-item depression scale. Each of the nine items reflects a DSM-5 symptom of depression
- Time frame: Past 2 weeks
- Self-administered or clinician-administered
- Takes less than 3 minutes to complete

**Clinical Use**:
- Primary care providers can use the PHQ-9 to screen for possible depression in patients. Clinicians may use the PHQ-9 to evaluate the efficacy of treatments for depression. A change of PHQ-9 score to less than 10 is considered a "partial response" to treatment and a change of PHQ-9 score to less than 5 is considered to be "remission"

**Related Versions**:
- PHQ-2: Brief 2-item screener (first 2 questions only)
- PHQ-A: Adolescent version
- PHQ-15: Somatic symptom scale

### Generalized Anxiety Disorder-7 (GAD-7)

**Purpose**: Anxiety screening and severity measurement

**LOINC Code**:
- 69737-5: Generalized anxiety disorder 7 item (GAD-7)

**Scoring System**:
The GAD-7 score is calculated by assigning scores of 0, 1, 2, and 3, to the response categories of 'not at all', 'several days', 'more than half the days', and 'nearly every day', respectively, and adding together the scores for the seven questions. Scores of 5, 10, and 15 are taken as the cut-off points for mild, moderate and severe anxiety, respectively

**Structure**:
- 7 items assessing anxiety symptoms
- Same response format as PHQ-9
- Time frame: Past 2 weeks
- Total score range: 0-21

**Clinical Use**:
Unlike the PHQ-9, the GAD-7 does not generate provisional diagnoses. Clinicians use the GAD-7 to assess the severity of anxiety only

### Combined Assessment: PHQ-SADS

**LOINC Code**:
- 69729-2: Patient Health Questionnaire - Somatic, Anxiety, and Depressive Symptoms (PHQ-SADS) [Reported] - PHQ-9, GAD-7, and PHQ-15 measures, plus panic measure from original PHQ

This comprehensive tool combines multiple assessments for efficient screening.

### Billing for Psychiatric Assessment Scales

**CPT Code 96127**: Brief emotional/behavioral assessment

96127 is a time-based code which require documentation of start and stop time. Assessment tools may include the Behavior Assessment System for Children-Second Edition (BASC-2), Behavior Rating Profile-Second Edition (BRP-2), Child Behavior Checklist (CBCL), Conners' Rating Scale, Pervasive Developmental Disorder Behavior Inventory (PDDBI), Brief Infant Toddler Social Emotional Assessment (BITSEA) and the Patient Health Questionnaire for Depression and Anxiety (PHQ-4, PHQ-9)

**CPT Code 96160**: Administration of patient-focused health risk assessment

**Billing Multiple Assessments**:
- When administering both PHQ-9 and GAD-7, can bill 96127 with units of 2
- Must document time spent on administration and scoring
- Results must be documented in structured format

### Other Common Psychiatric Assessment Scales

**Mood Disorders**:
- Beck Depression Inventory (BDI)
- Hamilton Depression Rating Scale (HAM-D)
- Young Mania Rating Scale (YMRS)
- Mood Disorder Questionnaire (MDQ)

**Anxiety Disorders**:
- Hamilton Anxiety Rating Scale (HAM-A)
- Beck Anxiety Inventory (BAI)
- Yale-Brown Obsessive Compulsive Scale (Y-BOCS)

**Psychotic Disorders**:
- Brief Psychiatric Rating Scale (BPRS)
- Positive and Negative Syndrome Scale (PANSS)
- Scale for the Assessment of Negative Symptoms (SANS)

**ADHD**:
- Conners Rating Scales
- ADHD Rating Scale
- Vanderbilt Assessment Scale

**Substance Use**:
- CAGE Questionnaire (alcohol)
- Drug Abuse Screening Test (DAST)
- Alcohol Use Disorders Identification Test (AUDIT)

**Personality Assessment**:
- Minnesota Multiphasic Personality Inventory (MMPI)
- Personality Assessment Inventory (PAI)

**Cognitive Function**:
- Mini-Mental State Examination (MMSE)
- Montreal Cognitive Assessment (MoCA)

## 4. Mental Status Examination (MSE) Documentation

### Overview of Mental Status Examination

The Mental Status Exam (MSE) is a systematic way of describing a patient's mental state at the time you were doing a psychiatric assessment. An observant clinician can do a comprehensive mental status exam that helps guide them towards a diagnosis

The MSE is NOT coded separately but is an essential component of:
- Psychiatric diagnostic evaluations (90791, 90792)
- Progress notes
- Discharge summaries
- Court-ordered evaluations

### Standard Components of MSE

Commonly utilised components do exist, typically: appearance, behaviour, mood and affect, speech, thought process, thought content, perception, cognition and insight

**Complete MSE Structure** (10 domains):

1. **Appearance and Behavior**
   - General appearance (grooming, hygiene, dress)
   - Level of consciousness and alertness
   - Eye contact
   - Psychomotor activity (agitation, retardation, tremor, tics)
   - Attitude toward examiner (cooperative, guarded, hostile)

2. **Speech**
   - Rate (rapid, slow, normal)
   - Volume (loud, soft, normal)
   - Fluency and articulation
   - Spontaneity
   - Prosody (tone, inflection)

3. **Mood** (subjective)
   - Patient's self-reported emotional state
   - Document in patient's own words: "I feel depressed," "I'm anxious," "I'm fine"

4. **Affect** (objective)
   - Range (full, restricted, blunted, flat)
   - Intensity (normal, heightened, diminished)
   - Appropriateness (congruent with mood and situation)
   - Mobility (labile vs. stable)

5. **Thought Process** (how patient thinks)
   - Organization (logical, coherent, tangential, circumstantial)
   - Flow (goal-directed, flight of ideas, thought blocking)
   - Associations (loose, intact)

6. **Thought Content** (what patient thinks about)
   - Obsessions or preoccupations
   - Delusions (persecutory, grandiose, referential, somatic)
   - Overvalued ideas
   - Suicidal or homicidal ideation
   - Phobias

7. **Perception**
   - Hallucinations are perceptions in the absence of sensory stimuli in any of the five senses (auditory, visual, gustatory, olfactory, and tactile). The two most commonly asked in psychiatry are auditory and visual
   - Illusions (misperceptions of real stimuli)
   - Depersonalization (feeling detached from self)
   - Derealization (feeling surroundings are unreal)

8. **Cognition**
   - Level of consciousness
   - Orientation (person, place, time, situation)
   - Attention and concentration
   - Memory (immediate, recent, remote)
   - Fund of knowledge
   - Abstract reasoning
   - Calculations

9. **Insight**
   - Awareness of having a mental illness
   - Understanding of need for treatment
   - Levels: absent, poor, fair, good, excellent

10. **Judgment**
    - Ability to make appropriate decisions
    - Problem-solving capacity
    - Risk assessment
    - Impulse control

### Structured MSE Templates in EHRs

A semi-structured assessment template significantly improves the quality of MSE recording by junior doctors within EHRs. Whereas 100% of the OPCRIT+ MSEs used structured headings, only 86% of the normal MSEs did

**Benefits of Structured Templates**:
- Ensures completeness (all domains covered)
- Improves consistency across providers
- Reduces documentation time
- Facilitates data extraction for research
- Supports quality improvement initiatives

**Template Design Considerations**:
- Drop-down menus for common descriptors
- Free-text fields for detailed observations
- Ability to indicate "not assessed" vs. "normal"
- Auto-population of normal findings
- Customization for different clinical settings

### MSE Descriptive Terminology

**Common MSE Descriptors by Domain**:

**Appearance**:
- Well-groomed, disheveled, unkempt, bizarre
- Appropriate for age/weather, incongruent
- Good hygiene, poor hygiene, malodorous

**Behavior**:
- Cooperative, uncooperative, guarded, hostile
- Calm, agitated, restless, fidgety
- Appropriate, inappropriate, bizarre
- Normal eye contact, poor eye contact, avoids eye contact

**Speech**:
- Normal rate/volume/tone
- Rapid, pressured, slow, hesitant
- Loud, soft, monotonous
- Fluent, slurred, mumbled

**Mood**:
- "Depressed," "anxious," "angry," "happy," "fine," "okay"
- Document patient's exact words

**Affect**:
- Range: Full, restricted, blunted, flat
- Intensity: Normal, increased, decreased
- Appropriateness: Congruent, incongruent
- Quality: Euthymic, dysthymic, anxious, euphoric, irritable
- Stability: Stable, labile

**Thought Process**:
- Linear, logical, coherent, goal-directed
- Tangential, circumstantial, loose associations
- Flight of ideas, thought blocking
- Perseveration, echolalia

**Thought Content**:
- No suicidal/homicidal ideation
- Denies delusions, hallucinations
- Obsessive thoughts about...
- Paranoid ideation
- Ideas of reference

**Perception**:
- No hallucinations or illusions
- Auditory hallucinations: command, conversing, commenting
- Visual hallucinations: formed, unformed
- No depersonalization or derealization

**Cognition**:
- Alert and oriented x 4 (person, place, time, situation)
- Attention/concentration: intact, impaired
- Memory: intact for immediate, recent, and remote events
- Insight: poor, fair, good
- Judgment: poor, fair, good

### MSE Documentation Standards

**Key Principles**:
1. Document what you observe, not your interpretation
2. Use specific, objective language
3. Avoid jargon or vague terms like "WNL" (within normal limits)
4. Compare to previous assessments when relevant
5. Note changes over time or response to treatment

**Documentation Requirements**:
- MSE should be completed at every diagnostic evaluation
- Brief MSE in routine follow-up visits
- Comprehensive MSE when clinical status changes
- Document inability to assess specific domains

## 5. Suicide Risk Assessment

### Columbia Suicide Severity Rating Scale (C-SSRS)

**Overview**:

The Columbia-Suicide Severity Rating Scale (C-SSRS) is a unique suicide risk assessment tool that supports suicide risk assessment through a series of simple, plain-language questions that anyone can ask

**Key Features**:
The C-SSRS is: Simple - Ask all the questions in a few moments or minutes—with no mental health training required to ask them; Efficient - Use of the scale redirects resources to where they're needed most

**Free to Use**:
You do not need special permission from us to take the Columbia Protocol tools and use them in your setting, create your own unique triage next steps, or embed the Columbia Protocol in your electronic health record keeping systems (EHR)

### C-SSRS Components

**Four Main Constructs**:
The C-SSRS attempted to separate ideation and behavior by using 4 constructs (severity of ideation, intensity of ideation, behavior, and lethality), based on factors identified in previous studies as predictive of suicide attempts and completed suicide

**Categories of Assessment**:

The C-SSRS is made up of ten categories, all of which maintain binary responses (yes/no) to indicate a presence or absence of the behavior: Category 1 – Wish to be Dead; Category 2 – Non-specific Active Suicidal Thoughts; Category 3 – Active Suicidal Ideation with Any Methods (Not Plan) without Intent to Act; Category 4 – Active Suicidal Ideation with Some Intent to Act, without Specific Plan; Category 5 – Active Suicidal Ideation with Specific Plan and Intent

**Additional Categories**:
- Category 6-10: Various types of suicidal behavior (preparatory acts, aborted attempts, interrupted attempts, actual attempts, completed suicide)

### C-SSRS Question Examples

The Columbia Protocol questions use plain and direct language, which is most effective in eliciting honest and clear responses. For example, the questioner may ask: "Have you wished you were dead or wished you could go to sleep and not wake up?"; "Have you been thinking about how you might kill yourself?"; "Have you taken any steps toward making a suicide attempt or preparing to kill yourself (such as collecting pills, getting a gun, giving valuables away, or writing a suicide note)?"

### C-SSRS Versions

**Multiple Formats Available**:
- Lifetime/Recent: Gathers lifetime history plus recent suicidality
- Since Last Visit: Assesses changes since previous appointment
- Screener: Brief version for rapid assessment
- Self-Report: Patient-completed version

**Setting-Specific Versions**:
- Emergency department
- Primary care
- Inpatient psychiatric
- Outpatient mental health
- School-based

### Integration with EHR Systems

**Documentation Requirements**:
- Record all C-SSRS responses (yes/no for each category)
- Document recency of suicidal thoughts/behaviors
- Note intensity ratings
- Include risk formulation and safety plan

**Structured Data Fields**:
- Binary flags for each category
- Date/time of last suicidal ideation
- Date/time of last suicidal behavior
- Severity level (low, moderate, high risk)
- Protective factors present
- Risk factors present

**Clinical Actions Triggered**:
Based on C-SSRS results, EHR should support:
- Automated safety protocols
- Referral workflows
- Notification to supervisors/crisis teams
- Safety planning documentation
- Follow-up scheduling

### Safety Planning

**Safety Plan Components** (commonly stored as structured template):
1. Warning signs (thoughts, images, mood, situation, behavior)
2. Internal coping strategies (activities without contacting another person)
3. People and social settings that provide distraction
4. People to ask for help
5. Professional or agency contacts
6. Making environment safe (removing lethal means)

**EHR Integration**:
- Structured template with discrete fields
- Patient and provider co-create plan
- Printable for patient to take home
- Accessible to all care team members
- Updated at regular intervals

## 6. Psychiatric Medications and RxNorm Coding

### Psychotropic Medication Classes

Psychiatrists prescribe medications across multiple classes:

**Antidepressants**:
- SSRIs: Fluoxetine, Sertraline, Escitalopram, Paroxetine
- SNRIs: Venlafaxine, Duloxetine, Desvenlafaxine
- Atypical: Bupropion, Mirtazapine, Trazodone
- TCAs: Amitriptyline, Nortriptyline, Desipramine
- MAOIs: Phenelzine, Tranylcypromine

**Antipsychotics**:
- Atypical (Second-generation): Risperidone, Olanzapine, Quetiapine, Aripiprazole, Clozapine, Lurasidone
- Typical (First-generation): Haloperidol, Chlorpromazine, Fluphenazine

**Mood Stabilizers**:
- Lithium
- Anticonvulsants: Valproic acid, Lamotrigine, Carbamazepine

**Anxiolytics**:
- Benzodiazepines: Lorazepam, Clonazepam, Alprazolam, Diazepam
- Non-benzodiazepines: Buspirone, Hydroxyzine

**Stimulants** (for ADHD):
- Methylphenidate, Amphetamine salts, Lisdexamfetamine

**Sedative-Hypnotics**:
- Zolpidem, Eszopiclone, Zaleplon

### RxNorm Coding for Psychiatric Medications

**Structure**: Each medication has multiple RxNorm concepts:
- Ingredient (IN)
- Clinical Drug (strength + form): Semantic Clinical Drug (SCD)
- Branded versions: Semantic Branded Drug (SBD)

**Example - Sertraline**:
- RxCUI 36437: Sertraline (ingredient)
- RxCUI 312940: Sertraline 50 MG Oral Tablet (SCD)
- RxCUI 310385: Zoloft 50 MG Oral Tablet (SBD)

**Example - Aripiprazole**:
- RxCUI 89013: Aripiprazole (ingredient)
- RxCUI 616916: Aripiprazole 10 MG Oral Tablet
- RxCUI 616917: Abilify 10 MG Oral Tablet

### Medication Management in Psychiatric EHR

**Required Structured Fields**:
- Medication name (RxNorm code)
- Strength and dosage
- Route of administration
- Frequency (with structured timing)
- Start date
- Indication (linked to diagnosis)
- Prescribing clinician
- Pharmacy information

**Psychiatric-Specific Documentation**:
- **Response to medication**: Improvement, no change, worsening
- **Side effects**: Using SNOMED CT or free text
- **Adherence**: Good, partial, poor, non-adherent
- **Reason for change**: Lack of efficacy, side effects, patient preference
- **Target symptoms**: Which symptoms medication addresses

**Special Considerations**:

1. **Clozapine REMS Program**:
   - Requires absolute neutrophil count (ANC) monitoring
   - Structured documentation of labs
   - REMS enrollment status
   - Prescriber certification

2. **Controlled Substances**:
   - DEA number required
   - State prescription monitoring program (PDMP) integration
   - Controlled substance agreements
   - Pill counts and urine drug screens

3. **Long-Acting Injectables**:
   - Administration date and site
   - Next due date
   - Lot number and expiration

4. **Lithium Monitoring**:
   - Serum lithium levels
   - Thyroid function tests
   - Renal function tests
   - Therapeutic range (0.6-1.2 mEq/L)

5. **Medication Interactions**:
   - Automated alerts for drug-drug interactions
   - QTc prolongation warnings
   - CYP450 enzyme interactions

## 7. Treatment Planning and Progress Notes

### Psychiatric Treatment Plans

**Required Components**:
1. **Problems/Diagnoses**: Linked to ICD-10-CM codes
2. **Goals**: Short-term and long-term, measurable
3. **Interventions**: Specific therapeutic approaches
4. **Frequency**: How often patient will be seen
5. **Modalities**: Individual, family, group therapy; medication management
6. **Target dates**: When goals should be achieved
7. **Responsible providers**: Who delivers each intervention

**Structured Format Example**:

```
Problem: Major Depressive Disorder, moderate (F32.1)

Goal 1: Patient will report decreased depressive symptoms as measured by PHQ-9 score <10 within 8 weeks
- Intervention: Cognitive Behavioral Therapy, 1x/week
- Intervention: Medication management (Sertraline 50mg daily)
- Responsible: Dr. Smith (psychiatrist), Jane Doe, LCSW (therapist)
- Target date: [8 weeks from now]

Goal 2: Patient will return to work within 12 weeks
- Intervention: Work-related stress management techniques
- Intervention: Collaborative discussion with employer
- Target date: [12 weeks from now]
```

### Psychotherapy Progress Notes

**Standard Elements**:
- **Subjective**: Patient's self-report of symptoms, functioning
- **Objective**: Clinical observations (brief MSE)
- **Assessment**: Clinical impression, progress toward goals
- **Plan**: Next steps, medication changes, homework

**Measurement-Based Care**:
- Regular administration of standardized scales (PHQ-9, GAD-7)
- Tracking scores over time
- Adjusting treatment based on objective data
- Documentation of clinical decision-making

### Documentation of Therapeutic Modalities

**Evidence-Based Psychotherapies Requiring Documentation**:
- **Cognitive Behavioral Therapy (CBT)**: Thought records, behavioral experiments
- **Dialectical Behavior Therapy (DBT)**: Skills taught, diary cards
- **Exposure Therapy**: Exposure hierarchy, SUDS ratings
- **Motivational Interviewing**: Change talk, commitment language
- **Psychodynamic Therapy**: Transference, defense mechanisms
- **EMDR**: Processing targets, validity of cognition

**Structured Documentation Elements**:
- Session number
- Therapeutic techniques used
- Homework assigned
- Patient participation and engagement
- Progress toward treatment goals

## 8. Unique EHR Requirements for Psychiatry

### Privacy and Confidentiality (42 CFR Part 2)

**Special Protections for Mental Health Records**:

A common indirect way that sensitive information was raised as an issue was by sectioning mental health records in the EHR. By sectioning the record, nonpsychiatric clinicians could not access mental health notes or could only access them with a password or if they were willing to break the glass and have their access recorded

**"Break the Glass" Functionality**:
- Mental health notes separated from general medical record
- Requires explicit consent or emergency override
- Audit trail of who accessed psychiatric notes

**Psychotherapy Notes vs. Progress Notes**:
- **Psychotherapy notes**: Provider's personal process notes, highly protected under HIPAA
- **Progress notes**: Standard medical record, required for continuity of care
- EHRs must distinguish between these two types

### Coordination with Primary Care

Psychiatry practices overwhelmingly serve patients who are receiving care from other providers. Thus, the ability to share clinical information seamlessly is vital

**Integration Challenges**:
- EHRs inadequately capture mental health diagnoses, visits, specialty care, hospitalizations, and medications. Patients with depression and bipolar disorder, respectively, averaged 8.4 and 14.0 days of outpatient behavioral care per year; 60% and 54% of these, respectively, were missing from the EHR because they occurred offsite

**Required Capabilities**:
- Bi-directional data exchange
- Medication reconciliation
- Lab result sharing
- Care coordination workflows

### Telepsychiatry Requirements

The American Psychiatric Association notes that the use of video-based telepsychiatry not only addresses the problem of provider shortages it also serves as an "convenient, affordable and readily-accessible mental health services," that leads to improved outcomes and higher patient satisfaction ratings

**EHR Telepsychiatry Features**:
- Integrated video conferencing (HIPAA-compliant)
- Virtual waiting room
- E-prescribing (including controlled substances in some states)
- Digital consent forms
- Screen sharing for assessments
- Recording capabilities (with consent)

### Outcome Tracking and Quality Measures

**CMS Quality Measures for Mental Health**:
- Depression screening and follow-up (PHQ-9)
- Alcohol and drug screening
- Metabolic monitoring for antipsychotics
- Follow-up after hospitalization for mental illness
- Suicide risk assessment

**Population Health Management**:
- Registries of patients by diagnosis
- Medication adherence tracking
- Appointment no-show rates
- Crisis utilization (ED, hospitalization)
- Outcome measurement over time

## 9. Data Mapping Workflow for Psychiatric Scribe Applications

### Natural Language to Structured Data Pipeline

**Step 1: Clinical Narrative Capture**
- Voice or text transcription of psychiatric interview
- Preservation of patient's exact words (for mood, suicidal ideation)
- Timestamp and provider identification

**Step 2: Named Entity Recognition (NER)**
- Identify symptoms: "feeling depressed," "can't sleep," "anxious"
- Extract medications: "taking Prozac 20mg daily"
- Recognize temporal information: "for the past two weeks"
- Identify behaviors: "stopped going to work," "isolating from friends"

**Step 3: Symptom-to-Diagnosis Mapping**
- Map symptom clusters to potential diagnoses
- Consider diagnostic criteria (DSM-5)
- Suggest appropriate ICD-10-CM F codes
- Flag need for additional information

**Step 4: Therapy Content Extraction**
- Identify therapeutic modality used (CBT, DBT, supportive)
- Extract homework assigned
- Note coping skills taught
- Recognize progress toward goals

**Step 5: Mental Status Examination Parsing**
- Extract MSE observations from narrative
- Map to standard MSE terminology
- Populate structured MSE template
- Flag abnormal findings

**Step 6: Risk Assessment Processing**
- Detect suicidal/homicidal ideation
- Identify protective/risk factors
- Map to C-SSRS framework
- Trigger safety protocols

**Step 7: Treatment Plan Generation**
- Link problems to diagnoses (ICD-10)
- Generate measurable goals
- Map interventions to CPT codes
- Assign responsible providers

**Step 8: Code Assignment**
- Select appropriate CPT code based on service type and time
- Assign primary ICD-10-CM diagnosis
- Add comorbid diagnoses
- Verify medical necessity

**Step 9: Structured Data Output**
- FHIR resources (Condition, Observation, MedicationStatement, Procedure)
- Discrete data fields populated
- Codes embedded in appropriate locations
- Ready for EHR import

### Validation and Quality Assurance

**Automated Checks**:
- Code validity (current ICD-10/CPT codes)
- Diagnosis-procedure pairing (medical necessity)
- Time documentation matches CPT code
- Suicide risk assessment completed
- Required modifiers present

**Clinical Review Prompts**:
- Ambiguous symptoms require clarification
- Multiple diagnoses - confirm hierarchy
- High-risk situations flagged
- Medication interactions detected

## 10. Implementation Considerations

### Psychiatry-Specific NLP Challenges

**Challenge 1: Symptom Ambiguity**
- "I'm hearing voices" → Auditory hallucinations OR normal expression?
- Context needed: patient history, diagnosis, other symptoms

**Challenge 2: Negation Detection**
- "No suicidal ideation" vs. "Patient denies, but..." vs. "denies passive SI but endorses active"
- Critical for risk assessment accuracy

**Challenge 3: Temporal Complexity**
- "Has been feeling better this week after increasing Zoloft last month"
- Multiple timeframes in single statement
- Need to track medication changes over time

**Challenge 4: Subjective vs. Objective**
- Patient's mood (subjective): "I feel sad"
- Provider's observation of affect (objective): "Appears tearful"
- Must distinguish for MSE documentation

**Challenge 5: Treatment Response Tracking**
- "PHQ-9 was 18 at last visit, now 12"
- Requires access to previous scores
- Context for current assessment

### Recommended Data Architecture

**Core Database Tables**:

1. **Patients**
   - Demographics
   - Insurance information
   - Consent status (for information sharing)

2. **Diagnoses**
   - ICD-10-CM code
   - Diagnosis description
   - Status (active, in remission, resolved)
   - Onset date, resolution date

3. **Encounters**
   - Date/time
   - Provider
   - Encounter type (initial eval, follow-up, crisis)
   - CPT code
   - Location/modality (in-person, telehealth)

4. **Mental Status Exams**
   - Structured fields for all 10 domains
   - Free-text details
   - Link to encounter

5. **Risk Assessments**
   - C-SSRS responses
   - Risk level determination
   - Safety plan
   - Link to encounter

6. **Assessment Scales**
   - Scale type (PHQ-9, GAD-7, etc.)
   - LOINC code
   - Individual item responses
   - Total score
   - Interpretation
   - Link to encounter

7. **Medications**
   - RxNorm code
   - Dosing details
   - Indication
   - Start/stop dates
   - Response/side effects

8. **Progress Notes**
   - Subjective findings
   - Objective findings (MSE)
   - Assessment
   - Plan
   - Time spent
   - Link to encounter

9. **Treatment Plans**
   - Problems/diagnoses
   - Goals (measurable)
   - Interventions
   - Target dates
   - Progress status

### Integration Testing Scenarios

**Test Case 1: New Patient Evaluation**
- Input: 60-minute initial psychiatric evaluation transcript
- Expected Output:
  - CPT code 90792
  - 3-5 ICD-10-CM codes
  - Complete MSE with all domains
  - C-SSRS documentation
  - Initial treatment plan
  - Time documentation (60 minutes)

**Test Case 2: Medication Management Follow-Up**
- Input: 15-minute follow-up visit transcript
- Expected Output:
  - CPT code 99213
  - Updated medication list with changes
  - Side effects documented
  - PHQ-9 or GAD-7 score
  - Brief MSE
  - Updated problem list

**Test Case 3: Psychotherapy Session**
- Input: 45-minute therapy session transcript
- Expected Output:
  - CPT code 90834
  - Time documentation (45 minutes)
  - Therapeutic modality identified
  - Progress toward goals
  - Homework assigned
  - MSE if indicated

**Test Case 4: Crisis Intervention**
- Input: 90-minute crisis session transcript
- Expected Output:
  - CPT codes 90839 + 90840
  - High suicide risk detected and documented
  - C-SSRS completed
  - Safety plan created
  - Disposition (hospitalization, intensive outpatient, follow-up)

### Success Metrics

**Coding Accuracy**:
- 95%+ accuracy for primary diagnosis
- 90%+ accuracy for procedure codes
- 98%+ accuracy for time-based codes

**Documentation Completeness**:
- 100% MSE completion for initial evaluations
- 100% risk assessment when indicated
- 95%+ treatment plan elements present

**Clinical Safety**:
- 100% detection of suicidal ideation mentions
- 100% detection of homicidal ideation
- Automated alerts for high-risk situations

**Efficiency Gains**:
- 50% reduction in documentation time
- 30% increase in patient contact time
- 20% improvement in coding compliance

## Conclusion

Psychiatric EHR integration for medical scribe applications requires deep understanding of psychiatry-specific coding systems, assessment tools, documentation requirements, and clinical workflows. Success depends on:

1. **Accurate Code Mapping**: ICD-10-CM F codes, psychiatric CPT codes, LOINC codes for assessments
2. **Structured Templates**: MSE, risk assessments, treatment plans
3. **Safety Focus**: Suicide risk detection, crisis protocols
4. **Privacy Protection**: Enhanced confidentiality for mental health records
5. **Outcome Tracking**: Standardized scales, measurement-based care
6. **Integration**: Coordination with primary care, telepsychiatry support

A medical scribe application focused on psychiatry must go beyond general medical documentation to address the unique complexities of mental health practice, while maintaining the highest standards of clinical accuracy and patient safety.