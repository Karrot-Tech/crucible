"use client";

import { useEffect, useRef, useState } from "react";

type MessageHandler = (data: any) => void;

export function useWebSocket(url: string) {
    const [isConnected, setIsConnected] = useState(false);
    const wsRef = useRef<WebSocket | null>(null);
    const handlersRef = useRef<MessageHandler[]>([]);

    useEffect(() => {
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("WebSocket connected");
            setIsConnected(true);
        };

        ws.onclose = () => {
            console.log("WebSocket disconnected");
            setIsConnected(false);
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handlersRef.current.forEach(handler => handler(data));
            } catch (e) {
                console.error("Failed to parse WebSocket message:", e);
            }
        };

        return () => {
            ws.close();
        };
    }, [url]);

    const subscribe = (handler: MessageHandler) => {
        handlersRef.current.push(handler);
        return () => {
            handlersRef.current = handlersRef.current.filter(h => h !== handler);
        };
    };

    return { isConnected, subscribe };
}
