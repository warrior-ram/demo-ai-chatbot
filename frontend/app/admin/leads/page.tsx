"use client";

import { useState, useEffect } from "react";
import { Download, Search, Mail, Phone } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { getLeads, type Lead } from "@/lib/api";

export default function LeadsPage() {
    const [leads, setLeads] = useState<Lead[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [search, setSearch] = useState("");

    useEffect(() => {
        getLeads()
            .then(setLeads)
            .catch(console.error)
            .finally(() => setIsLoading(false));
    }, []);

    const filteredLeads = leads.filter(l =>
    (l.name?.toLowerCase().includes(search.toLowerCase()) ||
        l.email?.toLowerCase().includes(search.toLowerCase()))
    );

    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Leads</h2>
                    <p className="text-muted-foreground">Manage captured contact information.</p>
                </div>
                <Button variant="outline">
                    <Download className="mr-2 h-4 w-4" /> Export CSV
                </Button>
            </div>

            <div className="flex items-center space-x-2">
                <Input
                    placeholder="Search leads..."
                    className="max-w-sm"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                />
                <Button variant="secondary" size="icon"><Search className="h-4 w-4" /></Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>Recent Leads</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-muted text-muted-foreground">
                                <tr>
                                    <th className="p-4 font-medium">Name</th>
                                    <th className="p-4 font-medium">Contact</th>
                                    <th className="p-4 font-medium">Date captured</th>
                                    <th className="p-4 font-medium">Session ID</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y">
                                {isLoading ? (
                                    <tr><td colSpan={4} className="p-8 text-center">Loading...</td></tr>
                                ) : filteredLeads.length === 0 ? (
                                    <tr><td colSpan={4} className="p-8 text-center text-muted-foreground">No leads found</td></tr>
                                ) : (
                                    filteredLeads.map((lead) => (
                                        <tr key={lead.id} className="hover:bg-muted/50">
                                            <td className="p-4 font-medium">{lead.name || "Anonymous"}</td>
                                            <td className="p-4 space-y-1">
                                                {lead.email && <div className="flex items-center gap-1"><Mail className="h-3 w-3" /> {lead.email}</div>}
                                                {lead.phone && <div className="flex items-center gap-1"><Phone className="h-3 w-3" /> {lead.phone}</div>}
                                            </td>
                                            <td className="p-4 text-muted-foreground">{new Date(lead.created_at).toLocaleDateString()}</td>
                                            <td className="p-4 font-mono text-xs">{lead.session_id}</td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
