"use client";

import { useState, useEffect } from "react";
import { ArrowLeft, Save, Copy } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import Link from "next/link";
import { getBot, type Bot } from "@/lib/api";

export default function BotConfigPage({ params }: { params: { id: string } }) {
    const [bot, setBot] = useState<Bot | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        getBot(parseInt(params.id))
            .then(setBot)
            .catch((e) => {
                // Fallback
                setBot({
                    id: parseInt(params.id),
                    name: "Demo Bot",
                    system_prompt: "You are a helpful AI customer support agent.",
                    welcome_message: "Hi! How can I help you today?",
                    created_at: ""
                });
            })
            .finally(() => setIsLoading(false));
    }, [params.id]);

    if (isLoading) return <div>Loading...</div>;
    if (!bot) return <div>Bot not found</div>;

    return (
        <div className="space-y-8 max-w-4xl mx-auto">
            <div className="flex items-center gap-4">
                <Link href="/admin/bots">
                    <Button variant="ghost" size="icon">
                        <ArrowLeft className="h-4 w-4" />
                    </Button>
                </Link>
                <div>
                    <h2 className="text-2xl font-bold tracking-tight">{bot.name}</h2>
                    <p className="text-muted-foreground">Configuration & Settings</p>
                </div>
                <div className="ml-auto flex gap-2">
                    <Button>
                        <Save className="mr-2 h-4 w-4" /> Save
                    </Button>
                </div>
            </div>

            <div className="grid gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>General Settings</CardTitle>
                        <CardDescription>Basic information about your bot.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Bot Name</label>
                            <Input defaultValue={bot.name} />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Welcome Message</label>
                            <Input defaultValue={bot.welcome_message} />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>AI Personality</CardTitle>
                        <CardDescription>Define how the AI should behave.</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">System Prompt</label>
                            <textarea
                                className="flex min-h-[150px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                defaultValue={bot.system_prompt}
                            />
                            <p className="text-xs text-muted-foreground">
                                Instructions for the AI model on how to answer questions and interact with users.
                            </p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>Installation</CardTitle>
                        <CardDescription>Add this bot to your website.</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="bg-muted p-4 rounded-md font-mono text-xs relative group">
                            {`<script src="https://demo-chat.com/embed.js" data-bot-id="${bot.id}"></script>`}
                            <Button variant="ghost" size="icon" className="absolute top-2 right-2 h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity">
                                <Copy className="h-3 w-3" />
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
