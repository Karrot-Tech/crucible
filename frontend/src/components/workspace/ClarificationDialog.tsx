import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';

interface HistoryItem {
    agent_id: string;
    question: string;
    answer: string;
}

interface ClarificationDialogProps {
    isOpen: boolean;
    onOpenChange: (open: boolean) => void;
    question: string;
    agentId: string;
    onSubmit: (answer: string) => void;
    isSubmitting?: boolean;
    history?: HistoryItem[];
    suggestedAnswer?: string | null;
    peerSuggestions?: { agent_name: string, suggestion: string }[];
}

export function ClarificationDialog({
    isOpen,
    onOpenChange,
    question,
    agentId,
    onSubmit,
    isSubmitting = false,
    history = [],
    suggestedAnswer,
    peerSuggestions = []
}: ClarificationDialogProps) {
    const [answer, setAnswer] = useState('');

    const handleSubmit = () => {
        if (!answer.trim()) return;
        onSubmit(answer);
        setAnswer('');
    };

    return (
        <Dialog open={isOpen} onOpenChange={onOpenChange}>
            <DialogContent className="sm:max-w-[600px] h-[80vh] flex flex-col">
                <DialogHeader>
                    <DialogTitle className="text-amber-600 flex items-center gap-2">
                        ⚠️ Assessment Team Chat
                    </DialogTitle>
                    <DialogDescription>
                        Collaborate with the AI agents to refine the clinical documentation.
                    </DialogDescription>
                </DialogHeader>

                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50 rounded-md border">
                    {/* History */}
                    {history.map((item, idx) => (
                        <div key={idx} className="space-y-2">
                            {/* Agent Bubble */}
                            <div className="flex justify-start">
                                <div className="max-w-[80%] bg-white border border-slate-200 p-3 rounded-2xl rounded-tl-sm shadow-sm text-sm">
                                    <div className="font-semibold text-xs text-slate-500 mb-1">
                                        {item.agent_id.replace('_', ' ').toUpperCase()}
                                    </div>
                                    {item.question}
                                </div>
                            </div>
                            {/* User Bubble */}
                            <div className="flex justify-end">
                                <div className="max-w-[80%] bg-blue-100 p-3 rounded-2xl rounded-tr-sm shadow-sm text-sm text-blue-900">
                                    {item.answer}
                                </div>
                            </div>
                        </div>
                    ))}

                    {/* Current Active Question */}
                    <div className="flex justify-start">
                        <div className="max-w-[90%] space-y-2">
                            <div className="bg-amber-50 border border-amber-200 p-3 rounded-2xl rounded-tl-sm shadow-sm text-sm animate-in fade-in slide-in-from-bottom-2">
                                <div className="font-semibold text-xs text-amber-700 mb-1 flex items-center gap-2">
                                    {(agentId || 'Unknown Agent').replace('_', ' ').toUpperCase()}
                                    <span className="inline-block w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
                                </div>
                                <span className="font-medium text-slate-800">{question}</span>
                            </div>

                            {/* Peer Suggestions */}
                            {peerSuggestions.length > 0 && (
                                <div className="flex flex-col gap-1 mt-1">
                                    {peerSuggestions.map((peer, idx) => (
                                        <button
                                            key={idx}
                                            onClick={() => setAnswer(peer.suggestion)}
                                            className="text-xs w-fit bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1.5 rounded-full hover:bg-emerald-100 transition-colors flex items-center gap-1.5 shadow-sm"
                                        >
                                            <span>👥 {peer.agent_name}:</span>
                                            <span className="font-medium">{peer.suggestion}</span>
                                        </button>
                                    ))}
                                </div>
                            )}

                            {/* Suggestion Chip */}
                            {suggestedAnswer && (
                                <button
                                    onClick={() => setAnswer(suggestedAnswer)}
                                    className="text-xs bg-indigo-50 text-indigo-700 border border-indigo-200 px-3 py-1.5 rounded-full hover:bg-indigo-100 transition-colors flex items-center gap-1.5 shadow-sm"
                                >
                                    <span>💡 Suggested:</span>
                                    <span className="font-medium">{suggestedAnswer}</span>
                                </button>
                            )}
                        </div>
                    </div>
                </div>

                <div className="mt-4 space-y-2">
                    <Label htmlFor="answer" className="sr-only">Your Answer</Label>
                    <div className="relative">
                        <Textarea
                            id="answer"
                            placeholder="Type your clarification here..."
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            className="min-h-[80px] w-full pr-12 resize-none"
                            onKeyDown={(e) => {
                                if (e.key === 'Enter' && !e.shiftKey) {
                                    e.preventDefault();
                                    handleSubmit();
                                }
                            }}
                        />
                    </div>
                </div>

                <DialogFooter>
                    <Button variant="outline" onClick={() => onOpenChange(false)} disabled={isSubmitting}>
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} disabled={!answer.trim() || isSubmitting}>
                        {isSubmitting ? 'Resuming...' : 'Submit & Resume'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
