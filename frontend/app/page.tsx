import ChatWidget from "@/components/chat/ChatWidget";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-background text-foreground">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <h1 className="text-4xl font-bold mb-8">AI Support Chatbot Demo</h1>
        <div className="bg-card p-6 rounded-lg border border-border max-w-lg">
          <p className="mb-4">
            This is a demo page for the AI Customer Support Chatbot.
            Click the button in the bottom right to start chatting!
          </p>
          <ul className="list-disc list-inside space-y-2 text-muted-foreground mb-6">
            <li>Real-time RAG responses</li>
            <li>DeepSeek LLM integration</li>
            <li>Lead capture capability</li>
            <li>History persistence</li>
          </ul>

          <div className="pt-4 border-t border-border">
            <a
              href="/admin"
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              Go to Admin Dashboard
            </a>
          </div>
        </div>
      </div>

      <ChatWidget botId={1} />
    </main>
  );
}
