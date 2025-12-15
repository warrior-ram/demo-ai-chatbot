import { Button } from "@/components/ui/Button";
import { X, Minimize2, RefreshCw } from "lucide-react";

interface ChatHeaderProps {
    botName?: string;
    onClose: () => void;
    onReset?: () => void;
}

export function ChatHeader({ botName = "Support Bot", onClose, onReset }: ChatHeaderProps) {
    return (
        <div className="flex items-center justify-between rounded-t-lg bg-primary px-4 py-3 text-primary-foreground shadow-md">
            <div className="flex items-center gap-2">
                <div className="h-2 w-2 rounded-full bg-green-400" />
                <span className="font-semibold">{botName}</span>
            </div>
            <div className="flex gap-1">
                {onReset && (
                    <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-primary/80 text-primary-foreground" onClick={onReset} title="Reset Chat">
                        <RefreshCw className="h-4 w-4" />
                    </Button>
                )}
                <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-primary/80 text-primary-foreground" onClick={onClose} title="Close">
                    <X className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}
