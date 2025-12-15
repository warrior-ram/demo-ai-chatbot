"use client";

import { useState, useEffect } from "react";
import { FileText, Trash2, Database } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { DocumentUpload } from "@/components/admin/DocumentUpload";
import { getDocuments, deleteDocument, type Document } from "@/lib/api";

export default function DocumentsPage() {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [botId] = useState(1); // Default to bot 1 for demo

    const loadDocuments = () => {
        getDocuments(botId).then(data => {
            setDocuments(data.documents);
            setStats(data.collection_stats);
        });
    };

    useEffect(() => {
        loadDocuments();
    }, [botId]);

    const handleDelete = async (id: number) => {
        if (confirm("Delete this document?")) {
            await deleteDocument(id);
            loadDocuments();
        }
    };

    return (
        <div className="space-y-8">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">Knowledge Base</h2>
                <p className="text-muted-foreground">Manage documents for Bot #{botId}.</p>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
                {/* Stats */}
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">Total Documents</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{documents.length}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">Indexed Chunks</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats?.count || 0}</div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
                {/* Upload Column */}
                <div className="md:col-span-1">
                    <Card>
                        <CardHeader>
                            <CardTitle>Upload Document</CardTitle>
                            <CardDescription>Add new knowledge source</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <DocumentUpload botId={botId} onUploadComplete={loadDocuments} />
                        </CardContent>
                    </Card>
                </div>

                {/* List Column */}
                <div className="md:col-span-2">
                    <Card>
                        <CardHeader>
                            <CardTitle>Documents</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                {documents.length === 0 ? (
                                    <div className="text-center py-8 text-muted-foreground">No documents uploaded yet.</div>
                                ) : (
                                    documents.map(doc => (
                                        <div key={doc.id} className="flex items-center justify-between p-4 border rounded-lg bg-card">
                                            <div className="flex items-center gap-3">
                                                <div className="h-10 w-10 rounded bg-primary/10 flex items-center justify-center text-primary">
                                                    <FileText className="h-5 w-5" />
                                                </div>
                                                <div>
                                                    <p className="font-medium">{doc.filename}</p>
                                                    <div className="flex gap-2 text-xs text-muted-foreground">
                                                        <span>{doc.chunk_count} chunks</span>
                                                        <span>•</span>
                                                        <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                                                    </div>
                                                </div>
                                            </div>
                                            <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-600 hover:bg-red-500/10" onClick={() => handleDelete(doc.id)}>
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    ))
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}
