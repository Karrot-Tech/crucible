"use client";
import * as React from "react";

import { TranscriptPanel } from "./TranscriptPanel";
import { AgentFlow } from "./AgentFlow";
import { SessionSetupDialog, SessionData } from "./SessionSetupDialog";
import { ClarificationDialog } from "./ClarificationDialog";
import { TeamChatPanel, ChatMessage } from "./TeamChatPanel";
import { FileText, Info, Power, Plus } from "lucide-react";
import { Button } from "@/components/ui/button";
import { OutputView } from "./OutputView";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useWebSocket } from "@/hooks/useWebSocket";
import { cn } from "@/lib/utils";
import {
    ResizableHandle,
    ResizablePanel,
    ResizablePanelGroup,
} from "@/components/ui/resizable";

export function Workspace() {
    const [sessionData, setSessionData] = React.useState<SessionData | null>(null);
    const [currentSessionId, setCurrentSessionId] = React.useState<string | null>(null);
    const [isSetupOpen, setIsSetupOpen] = React.useState(true);
    const [isOutputOpen, setIsOutputOpen] = React.useState(false);
    const [agentStatuses, setAgentStatuses] = React.useState<Record<string, string>>({});

    // HITL State
    const [clarificationReq, setClarificationReq] = React.useState<{
        question: string,
        agentId: string,
        sessionId: string,
        history: any[],
        suggestedAnswer?: string,
        peerSuggestions?: { agent_name: string, suggestion: string }[]
    } | null>(null);
    const [isSubmitting, setIsSubmitting] = React.useState(false);

    // Chat Log
    const [chatLog, setChatLog] = React.useState<ChatMessage[]>([]);

    // Connect to WebSocket
    const { isConnected, subscribe } = useWebSocket("ws://localhost:8000/ws");

    React.useEffect(() => {
        const unsubscribe = subscribe((message) => {
            console.log("WS Update:", message);
            if (message.type === "agent_update") {
                setAgentStatuses(prev => ({
                    ...prev,
                    [message.agent_id]: message.status
                }));
            }
            if (message.type === "workflow_pause") {
                setClarificationReq({
                    question: message.question,
                    agentId: message.agent_id,
                    sessionId: message.session_id,
                    history: message.history || [],
                    suggestedAnswer: message.data.suggested_answer || null,
                    peerSuggestions: message.peer_suggestions || []
                });
            }
            if (message.type === "chat_message") {
                setChatLog(prev => [...prev, message]);
                // Set agent to idle immediately when they post a message
                if (message.agent_id) {
                    setAgentStatuses(prev => ({
                        ...prev,
                        [message.agent_id]: 'idle'
                    }));
                }
            }
            if (message.type === "workflow_complete") {
                const outputData = message.data.output;
                if (outputData && outputData.soap_note) {
                    setSessionData(prev => prev ? {
                        ...prev,
                        soapNotes: outputData.soap_note
                    } : null);
                }
            }
        });
        return unsubscribe;
    }, [subscribe]);

    const handleSessionStart = async (data: SessionData) => {
        setSessionData(data);
        setIsSetupOpen(false);

        // Trigger Backend Analysis
        try {
            const response = await fetch("http://localhost:8000/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    patient_id: data.patientId,
                    session_date: data.sessionDate,
                    transcript: data.transcript,
                    soap_notes: data.soapNotes
                })
            });
            const result = await response.json();
            if (result.session_id) {
                setCurrentSessionId(result.session_id);
            }
        } catch (error) {
            console.error("Failed to start analysis:", error);
        }
    };

    const handleClarificationSubmit = async (answer: string) => {
        if (!clarificationReq) return;

        setIsSubmitting(true);
        try {
            await fetch("http://localhost:8000/api/clarify", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    session_id: clarificationReq.sessionId,
                    agent_id: clarificationReq.agentId,
                    answer: answer
                })
            });
            // Clear dialog
            setClarificationReq(null);
        } catch (error) {
            console.error("Failed to submit clarification:", error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleNewSession = () => {
        // Reset all states for a clean slate
        setSessionData(null);
        setCurrentSessionId(null);
        setAgentStatuses({});
        setChatLog([]);
        setIsSetupOpen(true);
        setIsOutputOpen(false);
    };

    const handleTerminate = async () => {
        if (currentSessionId) {
            try {
                await fetch(`http://localhost:8000/api/terminate/${currentSessionId}`, { method: 'POST' });
                // Manual UI reset for immediate feedback
                setSessionData(null);
                setCurrentSessionId(null);
                setAgentStatuses({});
                // forcing isConnected to false is handled by the hook usually, but we clear the session data which hides the "LIVE" badge context
            } catch (e) {
                console.error("Termination failed", e);
            }
        }
    };

    // Ensure network termination on browser refresh/close
    React.useEffect(() => {
        const handleUnload = () => {
            if (currentSessionId) {
                // Use keepalive: true to ensure the request survives page unload
                fetch(`http://localhost:8000/api/terminate/${currentSessionId}`, {
                    method: 'POST',
                    keepalive: true,
                }).catch(console.error);
            }
        };

        window.addEventListener('beforeunload', handleUnload);
        return () => window.removeEventListener('beforeunload', handleUnload);
    }, [currentSessionId]);

    return (
        <div className="h-screen w-full bg-background pt-2 px-3 pb-6 text-foreground flex flex-col overflow-hidden">
            <SessionSetupDialog open={isSetupOpen} onStart={handleSessionStart} />
            <OutputView
                isOpen={isOutputOpen}
                onOpenChange={setIsOutputOpen}
                soapNotes={sessionData?.soapNotes}
            />

            {clarificationReq && (
                <ClarificationDialog
                    isOpen={!!clarificationReq}
                    onOpenChange={(open) => !open && setClarificationReq(null)}
                    question={clarificationReq.question}
                    agentId={clarificationReq.agentId}
                    onSubmit={handleClarificationSubmit}
                    isSubmitting={isSubmitting}
                    history={clarificationReq.history}
                    suggestedAnswer={clarificationReq.suggestedAnswer}
                    peerSuggestions={clarificationReq.peerSuggestions}
                />
            )}

            <header className="mb-2 flex items-center justify-between border-b pb-2 shrink-0">
                <div className="flex items-center gap-4">
                    <div>
                        <h1 className="text-xl font-bold tracking-tight text-emerald-600 dark:text-emerald-400 leading-tight">Crucible</h1>
                        <p className="text-muted-foreground text-[10px] leading-tight flex items-center gap-2">
                            {sessionData ? (
                                <>
                                    <span className="bg-emerald-500/10 text-emerald-600 px-1.5 py-0.5 rounded font-bold">LIVE</span>
                                    <span>Patient: {sessionData.patientId} | Session: {sessionData.sessionDate}</span>
                                </>
                            ) : (
                                "System Ready. Waiting for session setup..."
                            )}
                        </p>
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    {/* Always show Terminate/New Session to allow recovery/reset */}
                    <Button
                        variant="outline"
                        size="sm"
                        className="h-8 gap-2 border-red-200 dark:border-red-900/50 bg-red-50/50 dark:bg-red-950/20 text-red-600 dark:text-red-400 hover:bg-red-100 hover:text-red-700 transition-all font-bold text-[11px] uppercase tracking-wider"
                        onClick={handleTerminate}
                        disabled={!isConnected || !currentSessionId}
                        title={!isConnected ? "Network offline" : (!currentSessionId ? "No active session" : "Terminate Network")}
                    >
                        <Power className="h-3.5 w-3.5" />
                        Terminate Network
                    </Button>

                    <Button
                        variant="outline"
                        size="sm"
                        className="h-8 gap-2 border-zinc-200 dark:border-zinc-800 hover:bg-zinc-50 dark:hover:bg-zinc-900 transition-all font-bold text-[11px] uppercase tracking-wider"
                        onClick={handleNewSession}
                        disabled={!!currentSessionId}
                        title={!!currentSessionId ? "Session in progress" : "Start New Session"}
                    >
                        <Plus className="h-3.5 w-3.5" />
                        New Session
                    </Button>

                    <div className="w-px h-6 bg-zinc-200 dark:bg-zinc-800 mx-1" />

                    <Button
                        variant="outline"
                        size="sm"
                        className="h-8 gap-2 border-emerald-200 dark:border-emerald-900 bg-emerald-50/30 dark:bg-emerald-950/20 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 transition-all font-bold text-[11px] uppercase tracking-wider shadow-sm"
                        onClick={() => setIsOutputOpen(true)}
                        disabled={!sessionData}
                    >
                        <FileText className="h-3.5 w-3.5" />
                        View Result
                    </Button>
                </div>
            </header>

            <ResizablePanelGroup orientation="horizontal" className="flex-1 w-full rounded-lg border bg-white dark:bg-zinc-950/50">
                {/* Left Panel: Transcript & Chat */}
                <ResizablePanel defaultSize={25} minSize={20}>
                    <div className="h-full p-1 flex flex-col">
                        <Tabs defaultValue="chat" className="h-full flex flex-col">
                            <TabsList className="w-full flex items-center justify-between mb-1 bg-transparent border-b rounded-none px-0 h-9">
                                <div className="flex bg-muted p-1 rounded-md">
                                    <TabsTrigger value="transcript" className="text-xs h-7">Transcript</TabsTrigger>
                                    <TabsTrigger value="chat" className="text-xs h-7">Team Chat</TabsTrigger>
                                </div>
                                <div className="flex items-center gap-2 pr-1">
                                    <div className={cn(
                                        "flex items-center gap-2 px-2 py-1 rounded-md border transition-colors shadow-sm",
                                        isConnected
                                            ? "bg-emerald-50 dark:bg-emerald-950/30 border-emerald-200 dark:border-emerald-800"
                                            : "bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-900/30"
                                    )}>
                                        {isConnected ? (
                                            <div className="relative flex h-2 w-2">
                                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                                                <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                                            </div>
                                        ) : (
                                            <Info className="h-3 w-3 text-red-500" />
                                        )}
                                        <span className={cn(
                                            "text-[10px] font-bold uppercase tracking-widest leading-none",
                                            isConnected ? "text-emerald-600 dark:text-emerald-400" : "text-red-600 dark:text-red-400"
                                        )}>
                                            {isConnected ? "LIVE" : "OFFLINE"}
                                        </span>
                                    </div>
                                </div>
                            </TabsList>
                            <TabsContent value="transcript" className="flex-1 overflow-hidden h-full mt-0">
                                <TranscriptPanel transcript={sessionData?.transcript} />
                            </TabsContent>
                            <TabsContent value="chat" className="flex-1 overflow-hidden h-full mt-0">
                                <TeamChatPanel messages={chatLog} />
                            </TabsContent>
                        </Tabs>
                    </div>
                </ResizablePanel>

                <ResizableHandle withHandle />

                {/* Center Panel: Agent Flow (Maximized) */}
                <ResizablePanel defaultSize={75} minSize={40}>
                    <div className="h-full p-2">
                        <AgentFlow agentStatuses={agentStatuses} />
                    </div>
                </ResizablePanel>
            </ResizablePanelGroup>
        </div>
    );
}
