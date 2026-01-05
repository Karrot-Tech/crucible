import * as React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ReactFlow, Background, Controls, useNodesState, useEdgesState, ConnectionMode, Node } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { AgentCardNode } from './AgentCardNode';
import { AgentDetailView, AgentData } from './AgentDetailView';
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog";

interface AgentFlowProps {
    agentStatuses?: Record<string, string>;
}

// Node Types Registration
const nodeTypes = {
    agentCard: AgentCardNode,
};

// --- Configuration & Metadata ---
import { AGENT_PERSONAS, getAgentPersona } from "@/lib/utils";

// ... Configuration & Metadata ...
const CENTER = { x: 400, y: 300 }; // Adjusted center for better fit
const RADIUS = 220; // Reduced radius for tighter mesh with smaller tokens

const AGENT_ROSTER: AgentData[] = [
    {
        id: 'safety_triage',
        label: AGENT_PERSONAS['safety_triage'],
        role: 'SAFETY MONITOR',
        avatar: '/avatars/safety_guardian.png',
        description: 'Monitors transaction for self-harm, violence, or emergency risks.',
        promptSnippet: 'You are a Safety Triage Agent. PRIORITY 1. Constantly scan for: Suicidal ideation, Homicidal intent, Domestic Violence, Medical Emergencies. If found, trigger STOP protocol.'
    },
    {
        id: 'risk_assessment',
        label: AGENT_PERSONAS['risk_assessment'],
        role: 'CLINICAL PSYCHOLOGIST',
        avatar: '/avatars/risk_monitor.png',
        description: 'Performs C-SSRS assessment when risks are detected.',
        promptSnippet: 'Execute Columbia-Suicide Severity Rating Scale (C-SSRS). Assess severity, intensity, and lethality of intent. Classify risk level: Low, Moderate, High, Imminent.'
    },
    {
        id: 'clinical_entity',
        label: AGENT_PERSONAS['clinical_entity'],
        role: 'MEDICAL SCRIBE',
        avatar: '/avatars/clinical_analyst.png',
        description: 'Extracts symptoms, medications, and conditions from speech.',
        promptSnippet: 'Extract ALL clinical entities. Categories: Symptoms (Onset, Duration, Severity), Medications (Dose, Freq), Diagnoses (History), Mental Status Exams observations.'
    },
    {
        id: 'diagnosis_mapping',
        label: AGENT_PERSONAS['diagnosis_mapping'],
        role: 'PSYCHIATRIST',
        avatar: '/avatars/doctor_female.png',
        description: 'Maps extracted symptoms to ICD-10 and DSM-5 criteria.',
        promptSnippet: 'You are a Diagnostic Specialist. Map symptoms to DSM-5 criteria. Rule out differentials. Assign ICD-10-CM F-codes. DEBATE with Medication Agent if meds dont match dx.'
    },
    {
        id: 'medication_management',
        label: AGENT_PERSONAS['medication_management'],
        role: 'PSYCHIATRIST',
        avatar: '/avatars/pharmacologist.png',
        description: 'Tracks current medications, adherence, and changes.',
        promptSnippet: 'Identify all medications. Compare against diagnosis (Mismatches?). Track changes (Start/Stop/Adjust). Check for interactions and side effects. Suggest titrations.'
    },
    {
        id: 'treatment_planning',
        label: AGENT_PERSONAS['treatment_planning'],
        role: 'CLINICAL DIRECTOR',
        avatar: '/avatars/care_planner.png',
        description: 'Formulates treatment goals and interventions.',
        promptSnippet: 'Synthesize Clinical + Diagnosis + Meds into a Plan. Set SMART goals. Define interventions (Psychotherapy, Pharmacotherapy, Social). Estimate prognosis.'
    },
    {
        id: 'procedure_coding',
        label: AGENT_PERSONAS['procedure_coding'],
        role: 'BILLING SPECIALIST',
        avatar: '/avatars/medical_coder.png',
        description: 'Assigns CPT codes based on complexity and time.',
        promptSnippet: 'Analyze complexity of MDM (Medical Decision Making). Calculate time spent. Assign E/M CPT Codes (99213 vs 99214). Add psychotherapy add-on codes (90833).'
    },
    {
        id: 'output_generation',
        label: AGENT_PERSONAS['output_generation'],
        role: 'DOCUMENTATION SPECIALIST',
        avatar: '/avatars/scribe_architect.png',
        description: 'Synthesizes all analysis into final SOAP Note.',
        promptSnippet: 'Compile final SOAP Note. Ensure professional medical tone. removing redundancies. Format: Subjective, Objective, Assessment, Plan. Append Billing Codes.'
    },
    {
        id: 'user_assist',
        label: AGENT_PERSONAS['user_assist'],
        role: 'INTAKE COORDINATOR',
        avatar: '/avatars/intake_coordinator.png',
        description: 'Coordinates session intake and initial orientation.',
        promptSnippet: 'Validate incoming session data. Check for missing context. Orient other agents.'
    }
];

// --- Layout Calculation ---
const generateMeshNodes = () => {
    const nodes = [];

    // 1. Center Node (Orchestrator / Administrator)
    nodes.push({
        id: 'orchestrator',
        type: 'agentCard', // Using the same token view
        position: { x: CENTER.x, y: CENTER.y },
        data: {
            id: 'orchestrator',
            label: AGENT_PERSONAS['administrator'],
            role: 'SYSTEM ORCHESTRATOR',
            avatar: '/avatars/administrator.png',
            description: 'Manages the debate, resolves conflicts, and ensures safety.',
            promptSnippet: 'You are the Administrator. Manage the flow. If Safety Agent flags high risk, HALT others. If Diagnosis and Meds disagree, force a DEBATE round.',
            status: 'running'
        }
    });


    // 2. Circle Nodes
    const angleStep = (2 * Math.PI) / AGENT_ROSTER.length;

    AGENT_ROSTER.forEach((agent, index) => {
        const angle = index * angleStep - (Math.PI / 2); // Start from top
        const x = CENTER.x + RADIUS * Math.cos(angle);
        const y = CENTER.y + RADIUS * Math.sin(angle);

        nodes.push({
            id: agent.id,
            type: 'agentCard',
            position: { x, y },
            data: {
                ...agent,
                status: 'idle'
            }
        });
    });

    return nodes;
};

// Mesh Edges: Connect everyone to Center, and maybe ring connections
const generateMeshEdges = () => {
    const edges = [];
    AGENT_ROSTER.forEach((agent) => {
        // Star topology (Everyone talks to Orchestrator)
        edges.push({
            id: `e-orch-${agent.id}`,
            source: 'orchestrator',
            target: agent.id,
            type: 'default',
            animated: true,
            style: { stroke: '#94a3b8', strokeWidth: 1, opacity: 0.3 },
        });

        // Ring topology (optional, connects neighbors)
        // const nextIndex = (index + 1) % AGENT_ROSTER.length;
        // edges.push({
        //     id: `e-${agent.id}-${AGENT_ROSTER[nextIndex].id}`,
        //     source: agent.id,
        //     target: AGENT_ROSTER[nextIndex].id,
        //     style: { stroke: '#e2e8f0', strokeWidth: 1, strokeDasharray: '5,5' },
        // });
    });

    // Explicit Debate Links (e.g., Diagnosis <-> Meds)
    edges.push({
        id: 'e-debate-dx-meds',
        source: 'diagnosis_mapping',
        target: 'medication_management',
        animated: true,
        style: { stroke: '#f59e0b', strokeWidth: 2, strokeDasharray: '5,5', opacity: 0.6 }, // Orange for debate
        label: 'Debate Link'
    });

    return edges;
};

const initialMeshNodes = generateMeshNodes();
const initialMeshEdges = generateMeshEdges();

export function AgentFlow({ agentStatuses = {} }: AgentFlowProps) {
    const [nodes, setNodes, onNodesChange] = useNodesState(initialMeshNodes);
    const [edges, setEdges, onEdgesChange] = useEdgesState(initialMeshEdges);

    // Interaction State
    const [selectedAgent, setSelectedAgent] = React.useState<AgentData | null>(null);

    // Update nodes when agentStatuses prop changes
    React.useEffect(() => {
        setNodes((nds) =>
            nds.map((node) => {
                const defaultStatus = node.id === 'orchestrator' ? 'running' : 'idle';
                const status = agentStatuses[node.id] || defaultStatus;
                // Also update orchestrator if any child is running?
                // For now just direct mapping

                // Inject fake confidence for demo if status is completed
                const confidence = status === 'completed' ? 0.95 : undefined;

                if (node.id === 'orchestrator') {
                    // Administrator Logic:
                    // 1. If any agent is 'running', Admin is 'running' (Active thinking/decision making)
                    // 2. If any agent is 'completed' but none 'running', Admin is 'observing' (Passive monitoring)
                    // 3. Otherwise, Admin is 'idle'
                    const runningAgents = Object.values(agentStatuses).filter(s => s === 'running');
                    const completedAgents = Object.values(agentStatuses).filter(s => s === 'completed');

                    let adminStatus: 'idle' | 'running' | 'observing' = 'idle';
                    if (runningAgents.length > 0) adminStatus = 'running';
                    else if (completedAgents.length > 0) adminStatus = 'observing';

                    return {
                        ...node,
                        data: {
                            ...node.data,
                            status: adminStatus
                        }
                    };
                }

                return {
                    ...node,
                    data: {
                        ...node.data,
                        status: status as any,
                        confidence
                    }
                };
            })
        );

        // Dynamic Edge Animation based on active agents
        setEdges((eds) =>
            eds.map((edge) => {
                // Star topology logic: Highlight synapses between Admin and active children
                const isAdminEdge = edge.source === 'orchestrator' || edge.target === 'orchestrator';
                const childId = edge.source === 'orchestrator' ? edge.target : edge.source;
                const childStatus = agentStatuses[childId];

                if (isAdminEdge) {
                    if (childStatus === 'running') {
                        return {
                            ...edge,
                            animated: true,
                            style: { ...edge.style, stroke: '#22d3ee', strokeWidth: 3, opacity: 1, filter: 'drop-shadow(0 0 8px rgba(34,211,238,0.8))' }
                        };
                    }
                    if (childStatus === 'completed') {
                        return {
                            ...edge,
                            animated: false,
                            style: { ...edge.style, stroke: '#10b981', strokeWidth: 1.5, opacity: 0.6 }
                        };
                    }
                }

                // Default state
                return { ...edge, animated: false, style: { ...edge.style, stroke: '#94a3b8', strokeWidth: 1, opacity: 0.15 } };
            })
        );

    }, [agentStatuses, setNodes, setEdges]);

    const onNodeDoubleClick = (event: React.MouseEvent, node: Node) => {
        setSelectedAgent(node.data as unknown as AgentData);
    };

    return (
        <Card className="h-full flex flex-col border-none shadow-none bg-slate-50 dark:bg-zinc-950">
            <CardHeader className="px-4 py-3 border-b bg-white dark:bg-zinc-900 flex flex-row justify-between items-center">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    Agent Neural Mesh
                </CardTitle>
                <div className="flex items-center gap-2 bg-emerald-500/5 dark:bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20 shadow-sm animate-in fade-in slide-in-from-top-2">
                    <div className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </div>
                    <span className="text-[10px] font-bold text-emerald-700 dark:text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                        <span className="opacity-50">Neural Insights:</span>
                        Double-click agent
                    </span>
                </div>
            </CardHeader>
            <CardContent className="flex-1 p-0 relative min-h-[600px] bg-[url('/grid.svg')]">
                <div style={{ width: '100%', height: '100%' }}>
                    <ReactFlow
                        nodes={nodes}
                        edges={edges}
                        nodeTypes={nodeTypes}
                        onNodesChange={onNodesChange}
                        onEdgesChange={onEdgesChange}
                        onNodeDoubleClick={onNodeDoubleClick}
                        connectionMode={ConnectionMode.Loose}
                        proOptions={{ hideAttribution: true }}
                        fitView
                        minZoom={0.5}
                        maxZoom={1.5}
                    >
                        <Background color="#94a3b8" gap={20} size={1} className="opacity-20" />
                        <Controls />
                    </ReactFlow>
                </div>

                {/* Agent Detail Dialog */}
                <Dialog open={!!selectedAgent} onOpenChange={(open) => !open && setSelectedAgent(null)}>
                    <DialogContent showCloseButton={false} className="p-0 border-0 bg-transparent shadow-none max-w-md text-left">
                        <DialogTitle className="sr-only">Agent Details</DialogTitle>
                        {selectedAgent && <AgentDetailView agent={selectedAgent} onClose={() => setSelectedAgent(null)} />}
                    </DialogContent>
                </Dialog>

            </CardContent>
        </Card>
    );
}
