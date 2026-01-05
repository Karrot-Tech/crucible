import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Activity, AlertCircle, CheckCircle2, Cpu, Globe, Info, Terminal, Zap, X, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
export interface AgentData {
    id: string;
    label: string;
    role: string;
    description: string;
    avatar: string;
    promptSnippet: string;
    status?: 'idle' | 'running' | 'completed' | 'error' | 'paused' | 'waiting' | 'observing';
    confidence?: number;
}
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";

interface AgentDetailViewProps {
    agent: AgentData;
    onClose: () => void;
}

export function AgentDetailView({ agent, onClose }: AgentDetailViewProps) {
    const { label, role, description, avatar, promptSnippet, status = 'idle', confidence, id } = agent;

    const getStatusColor = (s: string) => {
        switch (s) {
            case 'running': return 'text-sky-600 dark:text-sky-400 border-sky-200 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/30';
            case 'completed': return 'text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/30';
            case 'error': return 'text-red-600 dark:text-red-400 border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-950/30';
            default: return 'text-zinc-500 border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900';
        }
    };

    return (
        <Dialog open={true} onOpenChange={(open) => !open && onClose()}>
            <DialogContent className="max-w-4xl p-0 gap-0 bg-background border-border shadow-2xl overflow-hidden sm:rounded-xl">
                {/* Header */}
                <div className="relative h-32 overflow-hidden border-b border-border bg-muted/20">
                    {/* Explicit Close Button */}
                    <div className="absolute top-2 right-2 z-50">
                        <Button variant="ghost" size="icon" className="hover:bg-muted" onClick={onClose}>
                            <X className="w-5 h-5 text-muted-foreground" />
                        </Button>
                    </div>

                    <div className="relative z-10 flex items-end h-full p-6 pb-4 gap-6">
                        <div className="relative group">
                            <div className={cn(
                                "w-24 h-24 rounded-full border-4 relative overflow-hidden transition-all duration-500 bg-background",
                                status === 'running' ? "border-sky-400 shadow-lg shadow-sky-100 dark:shadow-sky-900/20" : "border-background shadow-sm"
                            )}>
                                <img src={avatar} alt={label} className="w-full h-full object-cover" />
                                {/* Status Beacon */}
                                <div className={cn(
                                    "absolute bottom-0 right-0 w-6 h-6 rounded-full border-[3px] border-background flex items-center justify-center z-20 shadow-sm",
                                    getStatusColor(status)
                                )}>
                                    {status === 'running' && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                                    {status === 'completed' && <CheckCircle2 className="w-3.5 h-3.5" />}
                                    {status === 'error' && <AlertCircle className="w-3.5 h-3.5" />}
                                    {status === 'idle' && <div className="w-2 h-2 rounded-full bg-current" />}
                                </div>
                            </div>
                        </div>

                        <div className="flex-1 pb-1">
                            <div className="flex items-center gap-2 mb-1">
                                <h2 className="text-2xl font-bold tracking-tight text-foreground uppercase">
                                    {label}
                                </h2>
                                <Badge variant="outline" className="font-mono text-[10px] tracking-widest uppercase text-muted-foreground">
                                    {id}
                                </Badge>
                            </div>
                            <div className="flex items-center gap-4 text-sm font-medium text-muted-foreground font-mono tracking-wide">
                                <span className="flex items-center gap-1.5">
                                    <Cpu className="w-4 h-4" />
                                    {role.toUpperCase()}
                                </span>
                                <span className="w-1 h-1 rounded-full bg-border" />
                                <span className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-500">
                                    <Zap className="w-4 h-4" />
                                    CONFIDENCE: {(confidence ?? 0 * 100).toFixed(1)}%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-12 h-[500px]">
                    {/* Left Panel: Stats & Context */}
                    <div className="col-span-4 border-r border-border bg-muted/5 p-6 flex flex-col gap-6">
                        <div className="space-y-3">
                            <div className="flex items-center gap-2 text-muted-foreground text-xs font-bold font-mono tracking-wider uppercase">
                                <Info className="w-3.5 h-3.5" />
                                Operational Profile
                            </div>
                            <p className="text-sm text-foreground/80 leading-relaxed font-light border-l-2 border-primary/20 pl-3">
                                {description}
                            </p>
                        </div>

                        <div className="mt-auto pt-6 border-t border-border">
                            <div className="flex items-center gap-2 text-emerald-600/80 dark:text-emerald-500/80">
                                <Globe className="w-3.5 h-3.5" />
                                <span className="text-[10px] font-mono tracking-widest uppercase">Network Active</span>
                            </div>
                        </div>
                    </div>

                    {/* Right Panel: Logic View */}
                    <div className="col-span-8 bg-zinc-950 flex flex-col relative overflow-hidden">
                        <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800 bg-zinc-900/50 text-[10px] font-mono text-zinc-500">
                            <div className="flex gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 border border-red-500/50" />
                                <div className="w-2.5 h-2.5 rounded-full bg-amber-500/20 border border-amber-500/50" />
                                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/20 border border-emerald-500/50" />
                            </div>
                            <div className="opacity-30">
                                LIVE FEED
                            </div>
                        </div>

                        <ScrollArea className="flex-1 p-6 font-mono text-sm relative z-10 text-emerald-400">
                            <div className="flex gap-2 opacity-30 mb-4 select-none">
                                <span>$ agent_manifest.json</span>
                            </div>

                            {promptSnippet.split('\n').map((line: string, i: number) => (
                                <div key={i} className="flex gap-4 group hover:bg-white/5 px-1 rounded transition-colors">
                                    <span className="text-zinc-600 w-6 text-right shrink-0 select-none">{(i + 1).toString().padStart(2, '0')}</span>
                                    <span
                                        className="break-all whitespace-pre-wrap"
                                        dangerouslySetInnerHTML={{
                                            __html: line
                                                .replace(/([A-Z_]+)(?=:)/g, '<span class="text-amber-400 font-bold">$1</span>')
                                                .replace(/(".*?")/g, '<span class="text-sky-300">$1</span>')
                                                .replace(/(\/\/.*)/g, '<span class="text-zinc-500 italic">$1</span>')
                                        }}
                                    />
                                </div>
                            ))}
                            <div className="animate-pulse text-sky-500 mt-2">_</div>
                        </ScrollArea>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    );
}

// Helpers

