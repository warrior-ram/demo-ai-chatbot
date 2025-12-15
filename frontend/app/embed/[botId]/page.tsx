"use client";

import ChatWidget from "@/components/chat/ChatWidget";
import { useParams } from "next/navigation";

export default function EmbedPreviewPage() {
    const params = useParams();
    const botId = parseInt(params.botId as string);

    return (
        <div className="min-h-screen bg-neutral-100 flex flex-col items-center justify-center text-neutral-800">
            <div className="max-w-2xl text-center space-y-6">
                <h1 className="text-4xl font-bold">Client Website Demo</h1>
                <p className="text-lg">
                    This page represents a client's website where the chatbot is embedded.
                    The widget should appear in the bottom right corner.
                </p>
                <div className="p-6 bg-white rounded-lg shadow-md text-left space-y-4">
                    <h2 className="text-2xl font-semibold">How to Embed</h2>
                    <code className="block bg-neutral-900 text-neutral-100 p-4 rounded text-sm overflow-x-auto">
                        {`<script src="https://demo-chat.com/embed.js" data-bot-id="${botId}"></script>`}
                    </code>
                </div>
            </div>

            {/* The Widget */}
            <ChatWidget botId={botId} />
        </div>
    );
}
