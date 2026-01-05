import React, { memo } from 'react';
import { Handle, Position, NodeProps } from '@xyflow/react';
import { Activity, AlertCircle, CheckCircle2, Eye, Zap, Brain } from 'lucide-react';
import { AgentData } from './AgentDetailView';

// Reuse the AgentData interface for type consistency
export const AgentCardNode = memo(({ data, selected }: any) => {
    const { id, label, role, avatar, status = 'idle' } = data as AgentData;
    const isOrchestrator = id === 'orchestrator';

    const getStatusStyles = (s: string) => {
        if (isOrchestrator) {
            switch (s) {
                case 'running':
                    return 'ring-4 ring-cyan-400 ring-offset-2 animate-pulse shadow-[0_0_25px_rgba(34,211,238,0.6)] border-2 border-cyan-500 bg-cyan-50/10';
                case 'observing':
                    return 'ring-4 ring-blue-500/50 ring-offset-2 shadow-[0_0_20px_rgba(59,130,246,0.3)] animate-[pulse_3s_infinite]';
                default:
                    return 'ring-2 ring-blue-500/20 ring-offset-1 shadow-inner hover:ring-blue-400/50 transition-all duration-700';
            }
        }

        switch (s) {
            case 'running': return 'ring-4 ring-cyan-500 ring-offset-2 animate-pulse shadow-[0_0_15px_rgba(6,182,212,0.5)]';
            case 'completed': return 'ring-4 ring-green-500 ring-offset-1';
            case 'error': return 'ring-4 ring-red-500 ring-offset-1';
            case 'paused': return 'ring-4 ring-orange-400 ring-offset-1 border-dashed';
            default: return 'ring-1 ring-neutral-200 dark:ring-neutral-700 hover:ring-4 hover:ring-primary/20 transition-all';
        }
    };

    const getStatusIconOverlay = (s: string) => {
        if (isOrchestrator) {
            if (s === 'running') return <div className="absolute -top-1 -right-1 bg-cyan-500 text-white p-1 rounded-full animate-spin-slow z-10 shadow-lg"><Zap className="w-3 h-3" /></div>;
            if (s === 'observing') return <div className="absolute -top-1 -right-1 bg-blue-600 text-white p-1 rounded-full z-10 shadow-md animate-pulse"><Eye className="w-3 h-3" /></div>;
            return null;
        }

        if (s === 'running') return <div className="absolute -top-1 -right-1 bg-cyan-500 text-white p-1 rounded-full animate-bounce z-10 shadow-sm"><Activity className="w-3 h-3" /></div>;
        if (s === 'error') return <div className="absolute -top-1 -right-1 bg-red-500 text-white p-1 rounded-full z-10 shadow-sm"><AlertCircle className="w-3 h-3" /></div>;
        if (s === 'completed') return <div className="absolute -top-1 -right-1 bg-green-500 text-white p-1 rounded-full z-10 shadow-sm"><CheckCircle2 className="w-3 h-3" /></div>;
        return null;
    };

    return (
        <div className={`relative group flex flex-col items-center justify-center pointer-events-auto`}>
            {/* Thinking Halo for Administrator */}
            {isOrchestrator && (status === 'running' || status === 'observing') && (
                <div className="absolute inset-0 bg-cyan-400/20 rounded-full animate-[ping_4s_infinite] scale-150 -z-10" />
            )}

            {/* The Token */}
            <div className={`
                relative w-16 h-16 rounded-full bg-white dark:bg-neutral-900 
                ${getStatusStyles(status)}
                ${selected ? 'scale-110 shadow-2xl ring-offset-4 ring-primary' : ''}
                transition-all duration-500 cursor-pointer overflow-visible
            `}>
                {getStatusIconOverlay(status)}
                <div className={`w-full h-full rounded-full overflow-hidden ${isOrchestrator ? 'grayscale-0' : 'grayscale-[20%] group-hover:grayscale-0 transition-all'}`}>
                    <img src={avatar} alt={label} className="w-full h-full object-cover" />
                    {isOrchestrator && (status === 'running' || status === 'observing') && (
                        <div className="absolute inset-0 bg-blue-500/10 flex items-center justify-center">
                            <Brain className="w-8 h-8 text-blue-400 opacity-20 animate-pulse" />
                        </div>
                    )}
                </div>

                {/* Scanning sweep animation for Admin */}
                {isOrchestrator && status !== 'idle' && (
                    <div className="absolute inset-0 rounded-full border border-cyan-400/50 animate-[spin_10s_linear_infinite]" />
                )}

                {/* Invisible handles for edges */}
                <Handle type="target" position={Position.Top} className="opacity-0 w-1 h-1 absolute left-1/2 top-1/2" />
                <Handle type="source" position={Position.Bottom} className="opacity-0 w-1 h-1 absolute left-1/2 top-1/2" />
            </div>

            {/* Label Below */}
            <div className={`mt-3 text-center transition-all duration-300 ${isOrchestrator || selected || status === 'running' ? 'opacity-100 transform translate-y-0' : 'opacity-70 group-hover:opacity-100'}`}>
                <div className={`text-xs font-bold px-3 py-0.5 rounded-full shadow-sm border ${isOrchestrator
                    ? 'bg-blue-600 text-white border-blue-700'
                    : 'bg-white/90 dark:bg-black/80 text-neutral-900 dark:text-neutral-100 border-neutral-200 dark:border-neutral-800'
                    }`}>
                    {isOrchestrator && status === 'observing' ? 'Observing...' : label}
                </div>
            </div>

        </div>
    );
});

AgentCardNode.displayName = 'AgentCardNode';
