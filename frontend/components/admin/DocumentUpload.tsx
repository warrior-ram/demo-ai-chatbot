"use client";

import { useState } from "react";
import { Upload, File, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";
import { uploadDocument } from "@/lib/api";

interface DocumentUploadProps {
    botId: number;
    onUploadComplete: () => void;
}

export function DocumentUpload({ botId, onUploadComplete }: DocumentUploadProps) {
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setIsDragging(true);
        } else if (e.type === "dragleave") {
            setIsDragging(false);
        }
    };

    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            await handleUpload(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            await handleUpload(e.target.files[0]);
        }
    };

    const handleUpload = async (file: File) => {
        setIsUploading(true);
        setError(null);
        try {
            await uploadDocument(botId, file);
            onUploadComplete();
        } catch (e: any) {
            setError(e.message || "Upload failed");
        } finally {
            setIsUploading(false);
        }
    };

    return (
        <div className="space-y-4">
            <div
                className={cn(
                    "relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-colors",
                    isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25",
                    isUploading && "opacity-50 pointer-events-none"
                )}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <div className="flex flex-col items-center justify-center space-y-4 text-center">
                    <div className="rounded-full bg-primary/10 p-4 text-primary">
                        {isUploading ? <Loader2 className="h-8 w-8 animate-spin" /> : <Upload className="h-8 w-8" />}
                    </div>
                    <div className="space-y-1">
                        <p className="text-sm font-medium">
                            Drag & drop or Click to upload
                        </p>
                        <p className="text-xs text-muted-foreground">
                            PDF or TXT files (max 10MB)
                        </p>
                    </div>
                    <input
                        type="file"
                        className="absolute inset-0 cursor-pointer opacity-0"
                        accept=".pdf,.txt"
                        onChange={handleFileChange}
                        disabled={isUploading}
                    />
                </div>
            </div>
            {error && <p className="text-sm text-red-500">{error}</p>}
        </div>
    );
}
