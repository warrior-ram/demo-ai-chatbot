"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    LayoutDashboard,
    Bot,
    Users,
    FileText,
    Settings,
    LogOut
} from "lucide-react";
import { Button } from "@/components/ui/Button";

const sidebarItems = [
    { icon: LayoutDashboard, label: "Overview", href: "/admin" },
    { icon: Bot, label: "My Bots", href: "/admin/bots" },
    { icon: Users, label: "Leads", href: "/admin/leads" },
    { icon: FileText, label: "Knowledge Base", href: "/admin/documents" },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex h-screen w-64 flex-col border-r bg-card text-card-foreground">
            <div className="flex h-16 items-center border-b px-6">
                <span className="text-xl font-bold text-primary">AI Chatbot Admin</span>
            </div>

            <div className="flex-1 overflow-y-auto py-4">
                <nav className="space-y-1 px-3">
                    {sidebarItems.map((item) => {
                        const isActive = pathname === item.href;
                        return (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
                                    isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground"
                                )}
                            >
                                <item.icon className="h-4 w-4" />
                                {item.label}
                            </Link>
                        );
                    })}
                </nav>
            </div>

            <div className="border-t p-4">
                <Button variant="ghost" className="w-full justify-start gap-3 text-red-500 hover:bg-red-500/10 hover:text-red-600">
                    <LogOut className="h-4 w-4" />
                    Logout
                </Button>
            </div>
        </div>
    );
}
