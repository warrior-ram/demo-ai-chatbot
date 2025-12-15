"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Users, MessageSquare, Bot, FileText, ArrowUpRight } from "lucide-react";
import { getDashboardStats, DashboardStats } from "@/lib/api";

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats>({
        total_sessions: 0,
        total_leads: 0,
        active_bots: 0,
        total_documents: 0
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const data = await getDashboardStats();
                setStats(data);
            } catch (error: any) {
                console.error("Failed to fetch dashboard stats", error);
                if (error.message === "Unauthorized") {
                    window.location.href = "/admin/login";
                }
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, []);

    const statCards = [
        { title: "Total Sessions", value: stats.total_sessions.toString(), icon: MessageSquare, change: "+12%" },
        { title: "Leads Captured", value: stats.total_leads.toString(), icon: Users, change: "+5%" },
        { title: "Active Bots", value: stats.active_bots.toString(), icon: Bot, change: "0%" },
        { title: "Documents", value: stats.total_documents.toString(), icon: FileText, change: "+8%" },
    ];

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
                <p className="text-muted-foreground">Overview of your AI chatbot performance.</p>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
                {statCards.map((stat, i) => (
                    <Card key={i}>
                        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                            <CardTitle className="text-sm font-medium">{stat.title}</CardTitle>
                            <stat.icon className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{loading ? "..." : stat.value}</div>
                            <p className="text-xs text-muted-foreground flex items-center gap-1">
                                <span className="text-green-500 font-medium flex items-center">
                                    <ArrowUpRight className="h-3 w-3" /> {stat.change}
                                </span>
                                from last month
                            </p>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
                <Card className="col-span-4">
                    <CardHeader>
                        <CardTitle>Recent Activity</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            {[1, 2, 3].map((i) => (
                                <div key={i} className="flex items-center gap-4 border-b pb-4 last:border-0">
                                    <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center text-primary font-bold">
                                        U
                                    </div>
                                    <div className="flex-1 space-y-1">
                                        <p className="text-sm font-medium leading-none">New conversation started</p>
                                        <p className="text-sm text-muted-foreground">Bot #1 • 2 minutes ago</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>

                <Card className="col-span-3">
                    <CardHeader>
                        <CardTitle>System Status</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-4">
                            <div className="flex items-center justify-between">
                                <span className="text-sm">RAG Engine</span>
                                <span className="text-xs font-bold text-green-500 bg-green-500/10 px-2 py-1 rounded">Online</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm">DeepSeek API</span>
                                <span className="text-xs font-bold text-green-500 bg-green-500/10 px-2 py-1 rounded">Connected</span>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm">Database</span>
                                <span className="text-xs font-bold text-green-500 bg-green-500/10 px-2 py-1 rounded">Healthy</span>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
