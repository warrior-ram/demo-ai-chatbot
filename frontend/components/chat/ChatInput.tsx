import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { SendHorizontal } from "lucide-react";
import { useState, FormEvent } from "react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
    const [message, setMessage] = useState("");

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();
        if (message.trim()) {
            onSend(message);
            setMessage("");
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex w-full items-center gap-2 p-4 border-t border-border">
            <Input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
                disabled={disabled}
                className="flex-1"
            />
            <Button type="submit" size="icon" disabled={!message.trim() || disabled}>
                <SendHorizontal className="h-4 w-4" />
            </Button>
        </form>
    );
}
