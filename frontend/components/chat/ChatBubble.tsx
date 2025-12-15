import { cn } from "@/lib/utils";
import { User, Bot } from "lucide-react";

interface ChatBubbleProps {
    role: "user" | "assistant" | "system";
    content: string;
}

export function ChatBubble({ role, content }: ChatBubbleProps) {
    if (role === "system") return null; // Or show system messages differently

    const isUser = role === "user";

    return (
        <div className={cn("flex w-full gap-2", isUser ? "justify-end" : "justify-start")}>
            {!isUser && (
                <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-primary text-primary-foreground">
                    <Bot className="h-5 w-5" />
                </div>
            )}

            <div
                className={cn(
                    "max-w-[80%] rounded-lg px-4 py-2 text-sm shadow-sm",
                    isUser
                        ? "bg-primary text-primary-foreground rounded-br-none"
                        : "bg-muted text-foreground rounded-bl-none"
                )}
            >
                <div className="whitespace-pre-wrap">{content}</div>
            </div>

            {isUser && (
                <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-full bg-secondary text-secondary-foreground">
                    <User className="h-5 w-5" />
                </div>
            )}
        </div>
    );
}
