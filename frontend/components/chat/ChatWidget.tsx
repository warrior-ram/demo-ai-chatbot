"use client";

import { useState, useEffect, useRef } from "react";
import { MessageSquare, X } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { ChatHeader } from "./ChatHeader";
import { ChatBubble } from "./ChatBubble";
import { ChatInput } from "./ChatInput";
import { TypingIndicator } from "./TypingIndicator";
import { createSession, getChatHistory } from "@/lib/api";
import { WebSocketClient } from "@/lib/websocket";
import { v4 as uuidv4 } from "uuid";

interface Message {
    role: "user" | "assistant" | "system";
    content: string;
}

interface ChatWidgetProps {
    botId?: number;
}

export default function ChatWidget({ botId = 1 }: ChatWidgetProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [isTyping, setIsTyping] = useState(false);
    const [sessionId, setSessionId] = useState<number | null>(null);
    const wsClient = useRef<WebSocketClient | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Load session or create new one
    useEffect(() => {
        const initSession = async () => {
            let storedSessionId = localStorage.getItem("chat_session_id");
            let storedVisitorId = localStorage.getItem("chat_visitor_id");

            if (!storedVisitorId) {
                storedVisitorId = uuidv4();
                localStorage.setItem("chat_visitor_id", storedVisitorId);
            }

            if (storedSessionId) {
                setSessionId(parseInt(storedSessionId));
                // Load history
                try {
                    const history = await getChatHistory(parseInt(storedSessionId));
                    setMessages(history.messages || []);
                } catch (e) {
                    console.error("Failed to load history", e);
                }
            } else {
                // Create new session
                try {
                    const session = await createSession(botId, storedVisitorId);
                    setSessionId(session.id);
                    localStorage.setItem("chat_session_id", session.id.toString());
                } catch (e) {
                    console.error("Failed to create session", e);
                }
            }
        };

        if (isOpen && !sessionId) {
            initSession();
        }
    }, [isOpen, sessionId, botId]);

    // Connect WebSocket when session is ready
    useEffect(() => {
        if (sessionId && !wsClient.current) {
            const client = new WebSocketClient(sessionId);
            client.connect();

            client.onMessage((data) => {
                if (data.role === "system" && data.content === "typing") {
                    setIsTyping(true);
                    // Auto-hide typing after 3s if no message comes
                    setTimeout(() => setIsTyping(false), 3000);
                } else {
                    setIsTyping(false);
                    setMessages((prev) => [...prev, { role: data.role, content: data.content }]);
                }
            });

            wsClient.current = client;

            return () => {
                client.disconnect();
                wsClient.current = null;
            };
        }
    }, [sessionId]);

    // Scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping, isOpen]);

    const handleSend = (content: string) => {
        if (!wsClient.current) return;

        //Optimistic update
        // setMessages((prev) => [...prev, { role: "user", content }]);
        // Actually the backend echoes the message, so we wait for that? 
        // Wait, backend logic: "Echo user message back".
        // So we don't need optimistic update if backend echoes fast.

        wsClient.current.sendMessage(content);
    };

    return (
        <div className="fixed bottom-4 right-4 z-50 flex flex-col items-end gap-2">
            {/* Chat Window */}
            {isOpen && (
                <Card className="flex h-[500px] w-[350px] flex-col overflow-hidden shadow-xl animate-scale-in origin-bottom-right sm:w-[380px]">
                    <ChatHeader
                        onClose={() => setIsOpen(false)}
                        onReset={() => {
                            localStorage.removeItem("chat_session_id");
                            localStorage.removeItem("chat_visitor_id"); // Clear visitor ID to force new session on backend
                            setSessionId(null);
                            setMessages([]);
                            wsClient.current?.disconnect();
                            wsClient.current = null;
                        }}
                    />

                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-background/50">
                        {messages.map((msg, i) => (
                            <div key={i} className="animate-slide-up">
                                <ChatBubble role={msg.role} content={msg.content} />
                            </div>
                        ))}
                        {isTyping && (
                            <div className="flex justify-start">
                                <div className="bg-muted rounded-lg rounded-bl-none p-2"><TypingIndicator /></div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <ChatInput onSend={handleSend} disabled={!sessionId} />
                </Card>
            )}

            {/* Toggle Button */}
            {!isOpen && (
                <Button
                    size="icon"
                    className="h-14 w-14 rounded-full shadow-lg hover:scale-105 transition-transform"
                    onClick={() => setIsOpen(true)}
                >
                    <MessageSquare className="h-6 w-6" />
                </Button>
            )}
        </div>
    );
}
