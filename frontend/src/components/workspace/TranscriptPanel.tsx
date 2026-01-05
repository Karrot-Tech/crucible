"use client";

import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Badge } from "@/components/ui/badge";

interface TranscriptPanelProps {
    transcript?: string;
}

export function TranscriptPanel({ transcript }: TranscriptPanelProps) {
    const parsedTranscript = React.useMemo(() => {
        if (!transcript) return [];

        // Simple parsing logic: split by newlines, try to identify speaker
        return transcript.split('\n').filter(line => line.trim()).map((line, index) => {
            const isProvider = line.toUpperCase().trim().startsWith('PROVIDER:') || line.toUpperCase().trim().startsWith('DOCTOR:');
            const isPatient = line.toUpperCase().trim().startsWith('PATIENT:');
            let text = line;
            let speaker = 'UNKNOWN';

            if (isProvider) {
                speaker = 'PROVIDER';
                text = line.replace(/^(PROVIDER:|DOCTOR:)\s*/i, '');
            } else if (isPatient) {
                speaker = 'PATIENT';
                text = line.replace(/^PATIENT:\s*/i, '');
            }

            return {
                speaker,
                text,
                time: "00:00" // Placeholder
            };
        });
    }, [transcript]);

    return (
        <Card className="h-full flex flex-col border-none shadow-none">
            <CardHeader className="px-4 py-3 border-b">
                <CardTitle className="text-sm font-medium flex justify-between items-center">
                    Transcript
                    <Badge variant="outline" className="text-xs">{transcript ? 'Loaded' : 'Waiting'}</Badge>
                </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 p-0 overflow-hidden">
                <ScrollArea className="h-full px-4 py-4">
                    <div className="space-y-4">
                        {parsedTranscript.length > 0 ? parsedTranscript.map((entry, index) => (
                            <div key={index} className="flex flex-col gap-1">
                                <div className="flex items-center gap-2">
                                    <span className={`text-xs font-bold ${entry.speaker === 'PROVIDER' ? 'text-blue-500' : entry.speaker === 'PATIENT' ? 'text-green-600' : 'text-gray-500'}`}>
                                        {entry.speaker}
                                    </span>
                                    <span className="text-[10px] text-muted-foreground">{entry.time}</span>
                                </div>
                                <p className="text-sm leading-relaxed">{entry.text}</p>
                            </div>
                        )) : (
                            <div className="text-center text-muted-foreground text-sm mt-10">
                                No transcript available. Start a session to view.
                            </div>
                        )}
                    </div>
                </ScrollArea>
            </CardContent>
        </Card>
    );
}
