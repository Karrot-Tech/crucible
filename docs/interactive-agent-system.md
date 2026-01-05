# Interactive Psychiatric Scribe: User Interaction Model & System Architecture

## 1. User Interaction Model

### 1.1 Main Interface Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  🏥 Psychiatric Scribe AI    Patient: John Doe (ID: 12345)  👤 Dr. Smith │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  📁 Session: Nov 15, 2024 - Follow-up Visit                         │
│  ⏱️  Duration: 45 minutes  |  📊 Status: Transcript Ready            │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐ │
│  │  📝 Transcript   │  │  🩺 SOAP Notes   │  │  🤖 Agent View   │ │
│  │  (Validated)     │  │  (Your Notes)    │  │  (AI Analysis)   │ │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘ │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

### 1.2 Three-Panel Workspace

**LEFT PANEL: Source Documents**
- Validated transcript (collapsible sections)
- Your SOAP notes (editable)
- Previous session summaries
- Patient history quick reference

**CENTER PANEL: Agent Workflow Visualizer**
- Interactive agent tree/network
- Real-time processing status
- Agent outputs and reasoning
- Human intervention points

**RIGHT PANEL: Structured Output**
- Generated documentation
- Codes and billing
- Alerts and recommendations
- Export options

### 1.3 Agent Workflow Visualizer (Center Panel)

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENT WORKFLOW CONTROL                     🔄 Auto-run: [OFF]  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    ┌──────────────────┐                          │
│                    │  ORCHESTRATOR    │                          │
│                    │  ✓ Completed     │                          │
│                    └────────┬─────────┘                          │
│                             │                                     │
│              ┌──────────────┴──────────────┐                     │
│              ↓                             ↓                     │
│     ┌─────────────────┐          ┌──────────────────┐          │
│     │ TRANSCRIPTION   │          │  SAFETY TRIAGE   │          │
│     │ ✓ Complete      │─────→    │  ⚠️  Needs Review│          │
│     │ [View Output]   │          │  [Review Alerts] │←─ 👤     │
│     └─────────────────┘          └────────┬─────────┘          │
│                                            │                     │
│     ┌──────────────────────────────────────┴─────────┐         │
│     ↓              ↓              ↓                   ↓         │
│  ┌─────────┐  ┌─────────┐  ┌──────────┐  ┌────────────────┐  │
│  │CLINICAL │  │DIAGNOSIS│  │ MENTAL   │  │ RISK           │  │
│  │ENTITY   │  │MAPPING  │  │ STATUS   │  │ ASSESSMENT     │  │
│  │⏳ Running│  │⏸️ Paused│  │⏸️ Paused │  │⚠️ Needs Review │  │
│  │         │  │[OFF]    │  │         │  │[Review C-SSRS] │←─ 👤│
│  └────┬────┘  └────┬────┘  └────┬─────┘  └────────┬───────┘  │
│       │            │             │                   │          │
│       └────────────┴─────────────┴───────────────────┘          │
│                            ↓                                     │
│                   [Continue Pipeline]                            │
│                                                                   │
│  Legend:                                                          │
│  ✓ Complete  ⏳ Running  ⏸️ Paused  ⚠️ Needs Review  ❌ Error    │
│  [OFF] = Agent disabled by user                                  │
│  👤 = Human-in-the-loop intervention point                       │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐│
│  │ Quick Actions:                                               ││
│  │ [▶️ Run Selected] [⏸️ Pause All] [🔄 Run All] [💾 Save State]││
│  └────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

### 1.4 Individual Agent Card Interface

When clicking on any agent node, a detailed card expands:

```
┌─────────────────────────────────────────────────────────────────┐
│  🔍 DIAGNOSIS MAPPING AGENT                          [✕] Close   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Status: ⏸️ Paused - Awaiting Your Review                        │
│  Controls: [▶️ Run] [⏭️ Skip] [🔄 Reset] [⚙️ Settings]           │
│                                                                   │
│  ┌─── AGENT INPUT ────────────────────────────────────────────┐│
│  │ Source: Clinical Entity Extraction Agent                    ││
│  │ • Presenting symptoms: 7 identified                          ││
│  │ • Mental status observations: Complete                       ││
│  │ • Past psychiatric history: Available                        ││
│  │ [View Full Input] ────────────────────────────────────────  ││
│  └──────────────────────────────────────────────────────────────┘│
│                                                                   │
│  ┌─── AI REASONING ───────────────────────────────────────────┐│
│  │ The agent analyzed symptom clusters and identified:          ││
│  │                                                               ││
│  │ Primary Diagnosis Candidate:                                 ││
│  │ • F32.1 - Major Depressive Disorder, single episode, moderate││
│  │   Confidence: 85%                                             ││
│  │   Evidence: Meets 7/9 DSM-5 criteria, PHQ-9 score = 14       ││
│  │                                                               ││
│  │ Secondary Diagnosis Candidate:                               ││
│  │ • F41.1 - Generalized Anxiety Disorder                       ││
│  │   Confidence: 72%                                             ││
│  │   Evidence: GAD-7 score = 12, excessive worry present        ││
│  │                                                               ││
│  │ Differential Diagnoses Considered:                           ││
│  │ • F33.1 - Recurrent MDD (ruled out: no prior episodes)       ││
│  │ • F34.1 - Dysthymia (ruled out: acute onset, not chronic)    ││
│  │ [View Full Reasoning] ─────────────────────────────────────  ││
│  └──────────────────────────────────────────────────────────────┘│
│                                                                   │
│  ┌─── YOUR INPUT ────────────────────────────────────────────┐ │
│  │                                                              │ │
│  │ ☑️ I agree with AI's primary diagnosis                      │ │
│  │ ☑️ I agree with AI's secondary diagnosis                    │ │
│  │ ☐ I want to modify the diagnosis                            │ │
│  │                                                              │ │
│  │ Additional Notes:                                            │ │
│  │ ┌──────────────────────────────────────────────────────┐   │ │
│  │ │ Patient also shows signs of seasonal pattern.         │   │ │
│  │ │ Consider specifier "with seasonal pattern"            │   │ │
│  │ └──────────────────────────────────────────────────────┘   │ │
│  │                                                              │ │
│  │ Diagnosis Override (if needed):                              │ │
│  │ [Select ICD-10 Code ▼]                                      │ │
│  │                                                              │ │
│  │         [✓ Approve & Continue]  [✏️ Modify]                  │ │
│  └──────────────────────────────────────────────────────────── │ │
│                                                                   │
│  ┌─── AGENT OUTPUT ──────────────────────────────────────────┐ │
│  │ Will be available after approval                             │ │
│  └──────────────────────────────────────────────────────────────┘│
│                                                                   │
│  Dependencies: Clinical Entity Extraction → THIS AGENT → CPT Coding│
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.5 Workflow Execution Modes

**Mode 1: Manual Step-by-Step**
- Psychiatrist controls each agent execution
- Review and approve each stage
- Highest control, slower workflow

**Mode 2: Semi-Automated with Checkpoints**
- System runs agents automatically
- Pauses at critical decision points flagged by orchestrator
- Balanced control and efficiency

**Mode 3: Fully Automated (Review at End)**
- All agents run automatically
- Psychiatrist reviews final output
- Fastest workflow, less granular control

**Mode 4: Smart Intervention**
- System only pauses when:
  - Confidence scores below threshold (e.g., <70%)
  - Safety alerts detected
  - Multiple conflicting outputs
  - Unusual patterns detected

### 1.6 Critical Intervention Points

The system automatically requests human review for:

**🔴 MANDATORY REVIEW (System Pauses):**
1. **Safety Triage Agent** - Any suicide/homicide risk detected
2. **Risk Assessment Agent** - C-SSRS indicates moderate-high risk
3. **Diagnosis Mapping** - Confidence <60% or conflicting diagnoses
4. **Medication Management** - New medication recommendations or major changes

**🟡 SUGGESTED REVIEW (Flagged but Continues):**
1. **Mental Status Exam** - Unusual findings detected
2. **Assessment Scales** - Scores indicate significant change
3. **Procedure Coding** - Complex billing scenarios
4. **Treatment Planning** - Major treatment direction changes

**🟢 OPTIONAL REVIEW (Available but Not Flagged):**
- All other agents
- Can be reviewed if psychiatrist wants to see reasoning

## 2. Key User Workflows

### 2.1 Standard Session Documentation Workflow

```
START
  ↓
1. Upload/Select Session
   - Transcript (auto-loaded or uploaded)
   - Add SOAP notes (optional)
   ↓
2. Configure Agent Pipeline
   - Select execution mode
   - Toggle specific agents ON/OFF
   - Set intervention preferences
   ↓
3. Click [🚀 Start Analysis]
   ↓
4. Monitor Progress in Real-Time
   - Visual workflow updates
   - Agent status changes
   - Notifications for review needed
   ↓
5. Intervene When Prompted
   - Review agent reasoning
   - Approve/Modify/Override
   - Add clinical notes
   ↓
6. Review Final Output
   - Complete documentation
   - ICD-10 and CPT codes
   - Structured data
   ↓
7. Export/Save
   - Push to EHR
   - Save PDF
   - Update patient record
   ↓
END
```

### 2.2 Crisis Session Fast Track

```
START (Urgent Session)
  ↓
1. Upload Transcript
   ↓
2. [⚡ CRISIS MODE] - Auto-enables:
   - Safety Triage (Priority 1)
   - Risk Assessment (Priority 2)
   - Mental Status Exam (Priority 3)
   ↓
3. IMMEDIATE SAFETY REVIEW
   - Safety alerts displayed prominently
   - C-SSRS auto-completed
   - Risk level determined
   ↓
4. Psychiatrist Reviews & Acts
   - Approve safety plan
   - Document interventions
   - Initiate protocols
   ↓
5. Complete Documentation Later
   - Other agents run in background
   - Full documentation available for review
   ↓
END
```

### 2.3 Medication Management Focus

```
START
  ↓
1. Select "Medication Management" Template
   ↓
2. System Auto-Configures:
   - Medication Management Agent (ON)
   - Diagnosis Mapping (ON - for medical necessity)
   - Assessment Scales (ON - for outcome measurement)
   - Procedure Coding (ON - for E/M coding)
   - Other agents (OFF or background)
   ↓
3. Run Pipeline
   ↓
4. Review Medication Recommendations
   - Current meds with responses
   - Suggested changes with rationale
   - Drug interaction warnings
   ↓
5. Approve/Modify Prescriptions
   ↓
6. Auto-Generate:
   - Prescription orders
   - Patient education materials
   - Pharmacy communication
   ↓
END
```

## 3. Technical Architecture

### 3.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Web App    │  │  Desktop App │  │  Mobile App  │          │
│  │   (React)    │  │  (Electron)  │  │  (React Native)│         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         └──────────────────┴────────────────┘                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ WebSocket (Real-time) + REST API
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Authentication & Authorization (JWT + RBAC)                │ │
│  │  Rate Limiting | Request Validation | HIPAA Compliance     │ │
│  └────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  ORCHESTRATION  │  │  USER SESSION   │  │   WORKFLOW      │
│    SERVICE      │  │    MANAGER      │  │   CONTROLLER    │
│                 │  │                 │  │                 │
│ • Workflow exec │  │ • State mgmt    │  │ • Agent routing │
│ • Agent coord   │  │ • User inputs   │  │ • Dependencies  │
│ • Error handling│  │ • Checkpoints   │  │ • Parallel exec │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                     │
         └────────────────────┴─────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                     AGENT EXECUTION LAYER                        │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              MESSAGE QUEUE (RabbitMQ / Kafka)             │  │
│  │          Task Distribution | Priority Queuing             │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  AGENT POD  │  │  AGENT POD  │  │  AGENT POD  │  ... x N   │
│  │  (Container)│  │  (Container)│  │  (Container)│            │
│  │             │  │             │  │             │            │
│  │ • AI Model  │  │ • AI Model  │  │ • AI Model  │            │
│  │ • Prompt    │  │ • Prompt    │  │ • Prompt    │            │
│  │ • Context   │  │ • Context   │  │ • Context   │            │
│  │ • I/O       │  │ • I/O       │  │ • I/O       │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│                                                                   │
└──────────────────────┬────────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   AI/ML     │  │  KNOWLEDGE  │  │   CODING    │
│  SERVICES   │  │    BASE     │  │  SERVICES   │
│             │  │             │  │             │
│ Claude API  │  │ ICD-10-CM   │  │ CPT Lookup  │
│ GPT-4       │  │ SNOMED CT   │  │ RxNorm      │
│ Local Models│  │ LOINC       │  │ Crosswalks  │
│ Embeddings  │  │ DSM-5       │  │ Validators  │
└─────────────┘  └─────────────┘  └─────────────┘
                                               
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  POSTGRESQL  │  │    MONGODB   │  │    REDIS     │          │
│  │              │  │              │  │              │          │
│  │• Patient data│  │• Transcripts │  │• Session cache│         │
│  │• Structured  │  │• Unstructured│  │• Agent state │         │
│  │  records     │  │  notes       │  │• Real-time   │         │
│  │• Codes       │  │• SOAP notes  │  │  updates     │         │
│  │• Audit logs  │  │• Agent outputs│ │• Temp storage│         │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            VECTOR DATABASE (Pinecone / Weaviate)          │  │
│  │    • Patient embeddings  • Clinical pattern matching     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   INTEGRATION LAYER                              │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  EHR SYSTEMS │  │   PHARMACY   │  │   BILLING    │          │
│  │              │  │   SYSTEMS    │  │   SYSTEMS    │          │
│  │• Epic (FHIR) │  │• e-Prescribe │  │• Claims mgmt │          │
│  │• Cerner      │  │• SureScripts │  │• Revenue     │          │
│  │• Athena      │  │              │  │  cycle       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Agent Execution Framework

**Agent Container Structure:**

```python
class PsychiatricAgent:
    def __init__(self, agent_id, config):
        self.agent_id = agent_id
        self.name = config['name']
        self.prompt_template = config['prompt']
        self.model = config['model']  # Claude, GPT-4, etc.
        self.dependencies = config['dependencies']
        self.human_in_loop = config['human_in_loop']
        self.confidence_threshold = config['confidence_threshold']
        
    async def execute(self, input_data, session_context):
        """Main execution method"""
        # 1. Validate input
        self.validate_input(input_data)
        
        # 2. Check if human review needed
        if self.requires_human_review(input_data, session_context):
            await self.request_human_review()
            # Wait for human input
            human_input = await self.wait_for_human_input()
            input_data = self.merge_human_input(input_data, human_input)
        
        # 3. Construct prompt with context
        prompt = self.build_prompt(input_data, session_context)
        
        # 4. Call AI model
        response = await self.call_ai_model(prompt)
        
        # 5. Parse and validate output
        output = self.parse_output(response)
        confidence = self.calculate_confidence(output)
        
        # 6. Check if output needs review
        if confidence < self.confidence_threshold:
            output = await self.request_output_review(output)
        
        # 7. Save intermediate results
        await self.save_results(output, confidence)
        
        # 8. Emit events for dependent agents
        await self.notify_dependent_agents(output)
        
        return {
            'agent_id': self.agent_id,
            'output': output,
            'confidence': confidence,
            'reasoning': response['reasoning'],
            'timestamp': datetime.now()
        }
    
    def requires_human_review(self, input_data, context):
        """Determine if human review needed before execution"""
        # Check session settings
        if context['execution_mode'] == 'manual':
            return True
        
        # Check agent configuration
        if self.human_in_loop == 'always':
            return True
        
        # Check for risk factors
        if self.detect_risk_factors(input_data):
            return True
            
        return False
    
    async def request_human_review(self):
        """Send request to UI for human review"""
        await websocket.emit('agent_pause', {
            'agent_id': self.agent_id,
            'reason': 'Human review required',
            'status': 'awaiting_input'
        })
```

### 3.3 Workflow Orchestration Engine

```python
class WorkflowOrchestrator:
    def __init__(self):
        self.agents = {}
        self.workflow_state = {}
        self.dependency_graph = {}
        
    def register_agent(self, agent):
        """Register agent and its dependencies"""
        self.agents[agent.agent_id] = agent
        self.dependency_graph[agent.agent_id] = agent.dependencies
    
    async def execute_workflow(self, session_id, input_data, config):
        """Execute complete workflow"""
        # 1. Initialize session
        session = self.create_session(session_id, config)
        
        # 2. Determine execution order
        execution_plan = self.build_execution_plan(config['enabled_agents'])
        
        # 3. Execute agents in order
        for stage in execution_plan:
            # Check for parallel execution opportunities
            if len(stage) > 1:
                results = await asyncio.gather(*[
                    self.execute_agent(agent_id, session)
                    for agent_id in stage
                ])
            else:
                results = [await self.execute_agent(stage[0], session)]
            
            # 4. Store results in session context
            session.update_context(results)
            
            # 5. Check for workflow interruptions
            if session.should_pause():
                await self.pause_workflow(session)
                await self.wait_for_continuation(session)
        
        # 6. Compile final output
        final_output = self.compile_output(session)
        
        return final_output
    
    def build_execution_plan(self, enabled_agents):
        """Build DAG-based execution plan"""
        # Topological sort of dependency graph
        plan = []
        visited = set()
        
        def resolve_dependencies(agent_id):
            if agent_id in visited:
                return
            
            # Visit dependencies first
            for dep in self.dependency_graph[agent_id]:
                if dep in enabled_agents:
                    resolve_dependencies(dep)
            
            visited.add(agent_id)
            
            # Find agents that can run in parallel
            stage = self.find_parallel_agents(agent_id, visited)
            if stage not in plan:
                plan.append(stage)
        
        for agent_id in enabled_agents:
            resolve_dependencies(agent_id)
        
        return plan
    
    async def execute_agent(self, agent_id, session):
        """Execute individual agent"""
        agent = self.agents[agent_id]
        
        # Get input from dependencies
        input_data = self.gather_input(agent_id, session)
        
        try:
            # Execute agent
            result = await agent.execute(input_data, session.context)
            
            # Update UI in real-time
            await self.emit_progress({
                'agent_id': agent_id,
                'status': 'completed',
                'result': result
            })
            
            return result
            
        except Exception as e:
            # Handle errors
            await self.handle_agent_error(agent_id, e, session)
            return None
```

### 3.4 Real-Time Communication Architecture

```javascript
// Frontend WebSocket Handler
class AgentWorkflowClient {
  constructor(sessionId) {
    this.sessionId = sessionId;
    this.socket = new WebSocket(`wss://api.example.com/ws/${sessionId}`);
    this.agentStates = new Map();
    this.setupEventHandlers();
  }
  
  setupEventHandlers() {
    // Agent status updates
    this.socket.on('agent_status', (data) => {
      this.updateAgentCard(data.agent_id, data.status);
    });
    
    // Agent pause (human review needed)
    this.socket.on('agent_pause', (data) => {
      this.showReviewModal(data.agent_id, data.reason);
    });
    
    // Agent completed
    this.socket.on('agent_complete', (data) => {
      this.displayAgentOutput(data.agent_id, data.result);
      this.enableDependentAgents(data.agent_id);
    });
    
    // Workflow completed
    this.socket.on('workflow_complete', (data) => {
      this.displayFinalOutput(data);
    });
    
    // Safety alerts
    this.socket.on('safety_alert', (data) => {
      this.showCriticalAlert(data);
    });
  }
  
  // User actions
  async approveAgentOutput(agentId, modifications = {}) {
    await this.socket.emit('agent_approve', {
      agent_id: agentId,
      modifications: modifications,
      approved_by: this.psychiatristId,
      timestamp: Date.now()
    });
  }
  
  async runAgent(agentId) {
    await this.socket.emit('run_agent', {
      agent_id: agentId,
      session_id: this.sessionId
    });
  }
  
  async pauseWorkflow() {
    await this.socket.emit('pause_workflow', {
      session_id: this.sessionId
    });
  }
}
```

### 3.5 State Management System

```python
class SessionState:
    """Manages workflow state for persistence and recovery"""
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.state = {
            'transcript': None,
            'soap_notes': None,
            'execution_mode': 'semi_automated',
            'enabled_agents': [],
            'agent_states': {},
            'agent_outputs': {},
            'human_inputs': {},
            'checkpoint': None,
            'final_output': None
        }
    
    async def save_checkpoint(self):
        """Save current state to database"""
        await redis.set(
            f'session:{self.session_id}:state',
            json.dumps(self.state),
            ex=86400  # 24 hour expiry
        )
    
    async def restore_from_checkpoint(self):
        """Restore state from last checkpoint"""
        state_data = await redis.get(f'session:{self.session_id}:state')
        if state_data:
            self.state = json.loads(state_data)
            return True
        return False
    
    def update_agent_state(self, agent_id, status, output=None):
        """Update individual agent state"""
        self.state['agent_states'][agent_id] = {
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'output': output
        }
        
        # Auto-save on state change
        asyncio.create_task(self.save_checkpoint())
    
    def get_agent_input(self, agent_id):
        """Gather input data for agent from dependencies"""
        agent = self.agents[agent_id]
        input_data = {}
        
        for dep_id in agent.dependencies:
            if dep_id in self.state['agent_outputs']:
                input_data[dep_id] = self.state['agent_outputs'][dep_id]
        
        # Include human inputs if available
        if agent_id in self.state['human_inputs']:
            input_data['human_input'] = self.state['human_inputs'][agent_id]
        
        # Include source documents
        input_data['transcript'] = self.state['transcript']
        input_data['soap_notes'] = self.state['soap_notes']
        
        return input_data
```

## 4. Key Technical Components

### 4.1 Agent Configuration System

```yaml
# agents_config.yaml

agents:
  - id: safety_triage
    name: "Safety Triage Agent"
    type: critical
    priority: 1
    model: claude-sonnet-4
    human_in_loop: always  # always | on_alert | never
    confidence_threshold: 0.95
    dependencies: []
    prompt_template: "safety_triage_prompt.txt"
    output_schema: "safety_triage_schema.json"
    
  - id: clinical_entity_extraction
    name: "Clinical Entity Extraction Agent"
    type: standard
    priority: 3
    model: claude-sonnet-4
    human_in_loop: never
    confidence_threshold: 0.80
    dependencies: []
    prompt_template: "entity_extraction_prompt.txt"
    output_schema: "entity_extraction_schema.json"
    
  - id: diagnosis_mapping
    name: "Diagnosis Mapping Agent"
    type: critical
    priority: 5
    model: claude-sonnet-4
    human_in_loop: on_low_confidence
    confidence_threshold: 0.75
    dependencies: [clinical_entity_extraction]
    prompt_template: "diagnosis_mapping_prompt.txt"
    output_schema: "diagnosis_schema.json"
    validation_rules:
      - check_dsm5_criteria
      - verify_icd10_format
      - require_justification
    
  - id: risk_assessment
    name: "Risk Assessment Agent (C-SSRS)"
    type: critical
    priority: 2
    model: claude-sonnet-4
    human_in_loop: on_risk_detected
    confidence_threshold: 0.90
    dependencies: [clinical_entity_extraction]
    prompt_template: "risk_assessment_prompt.txt"
    output_schema: "cssrs_schema.json"
    triggers:
      - suicide_ideation_mentioned
      - self_harm_behavior
      - hopelessness_expressed

workflow_templates:
  standard_followup:
    enabled_agents:
      - safety_triage
      - clinical_entity_extraction
      - diagnosis_mapping
      - mental_status_exam
      - assessment_scales
      - medication_management
      - procedure_coding
      - treatment_planning
    execution_mode: semi_automated
    
  crisis_session:
    enabled_agents:
      - safety_triage
      - risk_assessment
      - mental_status_exam
      - procedure_coding
    execution_mode: manual
    priority_override: true
    
  medication_only:
    enabled_agents:
      - medication_management
      - assessment_scales
      - diagnosis_mapping
      - procedure_coding
    execution_mode: automated
```

### 4.2 Human-in-the-Loop Integration Points

```python
class HumanReviewManager:
    """Manages human intervention in agent workflow"""
    
    async def request_review(self, agent_id, review_type, data):
        """Send review request to psychiatrist"""
        review_id = self.generate_review_id()
        
        review_request = {
            'review_id': review_id,
            'agent_id': agent_id,
            'type': review_type,  # approve, modify, override
            'data': data,
            'urgency': self.determine_urgency(agent_id, data),
            'timestamp': datetime.now()
        }
        
        # Store review request
        await self.save_review_request(review_request)
        
        # Notify UI
        await websocket.emit('review_requested', review_request)
        
        # Wait for response (with timeout)
        response = await self.wait_for_review(review_id, timeout=3600)
        
        return response
    
    def determine_urgency(self, agent_id, data):
        """Determine review urgency level"""
        if agent_id == 'safety_triage':
            if data.get('risk_level') == 'high':
                return 'critical'
            return 'high'
        
        if agent_id == 'risk_assessment':
            return 'high'
        
        if data.get('confidence', 1.0) < 0.5:
            return 'high'
        
        return 'normal'
    
    async def process_review_response(self, review_id, response):
        """Process psychiatrist's review response"""
        review = await self.get_review_request(review_id)
        
        action = response['action']  # approve | modify | override
        
        if action == 'approve':
            # Continue with agent output
            result = review['data']
        
        elif action == 'modify':
            # Merge modifications with agent output
            result = self.merge_modifications(
                review['data'],
                response['modifications']
            )
        
        elif action == 'override':
            # Use psychiatrist's input entirely
            result = response['override_data']
        
        # Add audit trail
        result['reviewed_by'] = response['psychiatrist_id']
        result['review_action'] = action
        result['review_timestamp'] = datetime.now()
        
        # Resume workflow
        await self.resume_agent(review['agent_id'], result)
        
        return result
```

### 4.3 Output Generation and Export

```python
class OutputGenerator:
    """Generates final documentation in various formats"""
    
    async def generate_clinical_note(self, session_state):
        """Generate complete clinical note"""
        
        note = {
            'patient_id': session_state['patient_id'],
            'session_date': session_state['session_date'],
            'provider': session_state['provider'],
            
            'chief_complaint': self.extract_chief_complaint(session_state),
            
            'subjective': {
                'history_present_illness': session_state.get_output('clinical_entity_extraction')['symptoms'],
                'mood': session_state.get_output('mental_status_exam')['mood'],
                'review_of_symptoms': session_state.get_output('clinical_entity_extraction')['ros']
            },
            
            'objective': {
                'mental_status_exam': session_state.get_output('mental_status_exam'),
                'vital_signs': session_state['soap_notes'].get('vitals'),
                'assessment_scales': session_state.get_output('assessment_scales')
            },
            
            'assessment': {
                'diagnoses': session_state.get_output('diagnosis_mapping'),
                'risk_assessment': session_state.get_output('risk_assessment'),
                'clinical_formulation': self.generate_formulation(session_state)
            },
            
            'plan': {
                'treatment_plan': session_state.get_output('treatment_planning'),
                'medications': session_state.get_output('medication_management'),
                'psychotherapy': self.extract_therapy_plan(session_state),
                'follow_up': self.determine_followup(session_state)
            },
            
            'billing': {
                'cpt_codes': session_state.get_output('procedure_coding'),
                'icd10_codes': session_state.get_output('diagnosis_mapping')['codes'],
                'time_documentation': session_state.get_output('procedure_coding')['time']
            }
        }
        
        return note
    
    async def export_to_ehr(self, clinical_note, format='fhir'):
        """Export to EHR system"""
        if format == 'fhir':
            return self.convert_to_fhir(clinical_note)
        elif format == 'ccd':
            return self.convert_to_ccd(clinical_note)
        else:
            return clinical_note
    
    def convert_to_fhir(self, note):
        """Convert to FHIR format"""
        bundle = {
            'resourceType': 'Bundle',
            'type': 'transaction',
            'entry': []
        }
        
        # Patient resource
        # Encounter resource
        # Condition resources (diagnoses)
        # Observation resources (MSE, assessments)
        # MedicationStatement resources
        # Procedure resources (CPT codes)
        # DocumentReference (clinical note)
        
        # ... implementation details
        
        return bundle
```

## 5. Security & Compliance

### 5.1 HIPAA Compliance Measures

```python
class SecurityManager:
    """Handles security and compliance"""
    
    def __init__(self):
        self.encryption_key = self.load_encryption_key()
        self.audit_logger = AuditLogger()
    
    async def encrypt_phi(self, data):
        """Encrypt Protected Health Information"""
        return await self.encrypt_aes256(data, self.encryption_key)
    
    async def log_access(self, user_id, resource_type, resource_id, action):
        """Log all access to PHI"""
        await self.audit_logger.log({
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'action': action,
            'timestamp': datetime.now(),
            'ip_address': request.remote_addr
        })
    
    def enforce_access_control(self, user_id, resource_id):
        """Enforce role-based access control"""
        user_role = self.get_user_role(user_id)
        resource_owner = self.get_resource_owner(resource_id)
        
        if user_role == 'psychiatrist' and resource_owner == user_id:
            return True
        
        return False
```

### 5.2 Audit Trail

Every action is logged:
- Agent executions and outputs
- Human reviews and modifications
- Data access
- Export/transmission events
- Configuration changes

## 6. Implementation Roadmap

### Phase 1: Core Infrastructure (Weeks 1-4)
- Set up backend architecture
- Implement agent execution framework
- Build orchestration engine
- Create database schemas

### Phase 2: Agent Development (Weeks 5-8)
- Implement all agent prompts
- Build agent containers
- Develop knowledge base integration
- Create validation logic

### Phase 3: UI Development (Weeks 9-12)
- Design and implement visual workflow editor
- Build agent status dashboard
- Create review/approval interfaces
- Implement real-time updates

### Phase 4: Integration (Weeks 13-14)
- EHR integration (FHIR)
- E-prescribing integration
- Billing system integration
- Export functionality

### Phase 5: Testing & Refinement (Weeks 15-16)
- Clinical validation with psychiatrists
- Security & compliance testing
- Performance optimization
- User acceptance testing

### Phase 6: Deployment (Weeks 17-18)
- Staged rollout
- Training and documentation
- Monitoring and support setup
- Feedback collection

## 7. Success Metrics

**Clinical Efficiency:**
- Documentation time: Target 50% reduction
- Session-to-note turnaround: <1 hour
- Coding accuracy: >95%

**User Satisfaction:**
- Psychiatrist satisfaction score: >4.5/5
- System usability scale (SUS): >80
- Time-to-proficiency: <2 hours

**Quality Metrics:**
- Clinical accuracy: >98%
- Safety alert sensitivity: 100%
- Billing denial rate: <2%

**System Performance:**
- Agent execution time: <30 seconds per agent
- End-to-end workflow: <5 minutes
- System uptime: >99.9%