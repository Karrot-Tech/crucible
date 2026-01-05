"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { TEST_SCENARIO_DEPRESSION } from "@/data/test_scenarios";

interface SessionSetupDialogProps {
    open: boolean;
    onStart: (data: SessionData) => void;
}

export interface SessionData {
    patientId: string;
    sessionDate: string;
    transcript: string;
    soapNotes: string | {
        subjective?: string;
        objective?: string;
        assessment?: string;
        plan?: string;
    };
}

export function SessionSetupDialog({ open, onStart }: SessionSetupDialogProps) {
    const [patientId, setPatientId] = useState("");
    const [sessionDate, setSessionDate] = useState(new Date().toISOString().split('T')[0]);
    const [transcript, setTranscript] = useState("");
    const [soapNotes, setSoapNotes] = useState("");

    const handleStart = () => {
        onStart({
            patientId,
            sessionDate,
            transcript,
            soapNotes
        });
    };

    const fillTestData = () => {
        setPatientId(TEST_SCENARIO_DEPRESSION.patientId);
        setSessionDate(TEST_SCENARIO_DEPRESSION.sessionDate);
        setTranscript(TEST_SCENARIO_DEPRESSION.transcript);
        setSoapNotes(TEST_SCENARIO_DEPRESSION.soapNotes);
    };

    const fillAndStart = () => {
        onStart({
            patientId: TEST_SCENARIO_DEPRESSION.patientId,
            sessionDate: TEST_SCENARIO_DEPRESSION.sessionDate,
            transcript: TEST_SCENARIO_DEPRESSION.transcript,
            soapNotes: TEST_SCENARIO_DEPRESSION.soapNotes
        });
    };

    return (
        <Dialog open={open}>
            <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Start New Session Analysis</DialogTitle>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    <div className="flex justify-end gap-2 mb-2">
                        <Button variant="outline" size="sm" onClick={fillTestData} className="text-xs">
                            Fill Form (Debug)
                        </Button>
                        <Button variant="secondary" size="sm" onClick={fillAndStart} className="text-xs bg-emerald-600 hover:bg-emerald-700 text-white border-none">
                            🚀 Fill & Start Analysis
                        </Button>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="patientId">Patient ID</Label>
                            <Input
                                id="patientId"
                                placeholder="e.g., PT-12345"
                                value={patientId}
                                onChange={(e) => setPatientId(e.target.value)}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="sessionDate">Session Date</Label>
                            <Input
                                id="sessionDate"
                                type="date"
                                value={sessionDate}
                                onChange={(e) => setSessionDate(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="transcript">Session Transcript</Label>
                        <Textarea
                            id="transcript"
                            placeholder="Paste the full session transcript here..."
                            className="min-h-[200px]"
                            value={transcript}
                            onChange={(e) => setTranscript(e.target.value)}
                        />
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="soap">Initial SOAP Notes (Optional)</Label>
                        <Textarea
                            id="soap"
                            placeholder="Paste any existing notes..."
                            className="min-h-[100px]"
                            value={soapNotes}
                            onChange={(e) => setSoapNotes(e.target.value)}
                        />
                    </div>
                </div>
                <DialogFooter>
                    <Button onClick={handleStart} disabled={!patientId || !transcript}>
                        Start Analysis
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
