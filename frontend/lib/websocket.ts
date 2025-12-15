type MessageHandler = (message: any) => void;

export class WebSocketClient {
    private ws: WebSocket | null = null;
    private url: string;
    private messageHandlers: MessageHandler[] = [];
    private reconnectInterval = 3000;
    private shouldReconnect = true;

    constructor(sessionId: number) {
        this.url = `ws://localhost:8001/ws/chat/${sessionId}`;
    }

    connect() {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = () => {
            console.log("WebSocket connected");
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.messageHandlers.forEach((handler) => handler(data));
        };

        this.ws.onclose = () => {
            console.log("WebSocket disconnected");
            if (this.shouldReconnect) {
                setTimeout(() => this.connect(), this.reconnectInterval);
            }
        };

        this.ws.onerror = (error) => {
            console.error("WebSocket error:", error);
        };
    }

    sendMessage(message: string) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({ message }));
        } else {
            console.warn("WebSocket is not open");
        }
    }

    onMessage(handler: MessageHandler) {
        this.messageHandlers.push(handler);
    }

    disconnect() {
        this.shouldReconnect = false;
        this.ws?.close();
    }
}
