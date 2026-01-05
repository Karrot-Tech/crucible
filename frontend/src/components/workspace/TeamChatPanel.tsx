import React, { useRef, useEffect } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Info, User, Bot, ShieldAlert, FlaskConical, Power } from "lucide-react";
import { cn, getAgentPersona, AGENT_PERSONAS, replaceAgentNames } from "@/lib/utils";
import { Button } from "@/components/ui/button";

export interface ChatMessage {
    type: "chat_message";
    text: string;
    sender: string;
    variant: "system" | "agent" | "user" | "consultant";
    timestamp?: string;
}

const FormattedContent = ({ text }: { text: string }) => {
    // Regex to match **bold** or *highlight*
    // **text** -> Bold chip
    // *text* -> Highlight span
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*)/g);

    return (
        <p className="leading-relaxed">
            {parts.map((part, i) => {
                if (part.startsWith('**') && part.endsWith('**')) {
                    const content = part.slice(2, -2);
                    return (
                        <span key={i} className="inline-flex items-center px-1.5 py-0.5 rounded-md bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 text-xs font-bold text-zinc-900 dark:text-zinc-100 mx-0.5 shadow-sm">
                            {content}
                        </span>
                    );
                }
                if (part.startsWith('*') && part.endsWith('*')) {
                    const content = part.slice(1, -1);
                    return (
                        <span key={i} className="bg-amber-100 dark:bg-amber-900/40 text-amber-900 dark:text-amber-200 px-1 rounded-sm border-b-2 border-amber-400/50 font-medium">
                            {content}
                        </span>
                    );
                }
                return <span key={i}>{part}</span>;
            })}
        </p>
    );
};

interface TeamChatPanelProps {
    messages: ChatMessage[];
    onTerminate?: () => void;
}

export function TeamChatPanel({ messages, onTerminate }: TeamChatPanelProps) {
    const scrollRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    const getAgentIcon = (sender: string) => {
        const s = sender.toLowerCase();
        if (s.includes('safety')) return <ShieldAlert className="h-3 w-3" />;
        if (s.includes('admin')) return <FlaskConical className="h-3 w-3" />;
        return <Bot className="h-3 w-3" />;
    };

    return (
        <Card className="h-full border-none shadow-none flex flex-col bg-slate-50/50 dark:bg-zinc-950/20">
            <CardContent className="flex-1 p-0 overflow-hidden relative">
                <div
                    ref={scrollRef}
                    className="h-full w-full overflow-y-auto p-3 pb-6 space-y-4 text-sm"
                >
                    {messages.length === 0 && (
                        <div className="h-40 flex flex-col items-center justify-center text-center space-y-3 opacity-40">
                            <Info className="h-8 w-8" />
                            <div className="text-xs max-w-[180px] font-medium italic">
                                Orchestrating agent network... Waiting for initial stream.
                            </div>
                        </div>
                    )}

                    {messages.map((msg, idx) => {
                        if (msg.variant === 'system') {
                            return (
                                <div key={idx} className="flex justify-center my-4">
                                    <div className="flex items-center gap-2 text-[10px] text-zinc-400 font-mono uppercase tracking-tighter bg-zinc-100 dark:bg-zinc-800/50 px-3 py-1 rounded-full border border-zinc-200 dark:border-zinc-700">
                                        <div className="w-1 h-1 rounded-full bg-zinc-300 animate-pulse" />
                                        {replaceAgentNames(msg.text)}
                                    </div>
                                </div>
                            );
                        }

                        if (msg.variant === 'user') {
                            return (
                                <div key={idx} className="flex flex-col items-end gap-1.5 animate-in fade-in slide-in-from-right-3">
                                    <div className="flex items-center gap-1.5 mr-1 text-[10px] font-bold text-blue-600 uppercase tracking-wider">
                                        Physician <User className="h-3 w-3" />
                                    </div>
                                    <div className="max-w-[90%] bg-blue-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-sm shadow-md text-sm">
                                        {msg.text}
                                    </div>
                                </div>
                            );
                        }

                        // Agent & Consultant
                        const isConsultant = msg.variant === 'consultant';
                        return (
                            <div key={idx} className="flex flex-col gap-1.5 animate-in fade-in slide-in-from-left-3">
                                <div className={cn(
                                    "flex items-center gap-1.5 ml-1 text-[10px] font-bold uppercase tracking-wider",
                                    isConsultant ? "text-emerald-600" : "text-amber-600"
                                )}>
                                    {isConsultant ? <User className="h-3 w-3" /> : getAgentIcon(msg.sender)}
                                    {/* Direct Persona Lookup or Fallback */}
                                    {AGENT_PERSONAS[msg.sender] || getAgentPersona(msg.sender)}
                                    {isConsultant && " (CONSULTANT)"}
                                </div>
                                <div className={cn(
                                    "max-w-[95%] px-4 py-3 rounded-2xl rounded-tl-sm shadow-sm border border-zinc-200 dark:border-zinc-800",
                                    isConsultant
                                        ? "bg-emerald-50 text-emerald-900 dark:bg-emerald-900/10 dark:text-emerald-100 border-emerald-100 dark:border-emerald-900/30"
                                        : "bg-white dark:bg-zinc-900 text-zinc-800 dark:text-zinc-200"
                                )}>
                                    <FormattedContent text={msg.text} />
                                </div>
                            </div>
                        );
                    })}
                </div>
            </CardContent>
        </Card>
    );
}
