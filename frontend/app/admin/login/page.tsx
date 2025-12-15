"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";
import { Loader2, KeyRound } from "lucide-react";

export default function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const router = useRouter();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError("");

        try {
            await login(username, password);
            router.push("/admin");
        } catch (err: any) {
            console.error("Login error:", err);
            setError("Invalid credentials or server unavailable");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-background px-4">
            <div className="w-full max-w-md space-y-8">
                {/* Header */}
                <div className="text-center">
                    <div className="mx-auto w-16 h-16 rounded-full bg-primary/20 flex items-center justify-center mb-4">
                        <KeyRound className="w-8 h-8 text-primary" />
                    </div>
                    <h2 className="text-3xl font-bold tracking-tight text-foreground">
                        Admin Console
                    </h2>
                    <p className="mt-2 text-sm text-muted-foreground">
                        Sign in to access the dashboard
                    </p>
                </div>

                {/* Login Form */}
                <form className="mt-8 space-y-6" onSubmit={handleLogin}>
                    <div className="space-y-4">
                        <div>
                            <label htmlFor="username" className="block text-sm font-medium text-foreground mb-1">
                                Username
                            </label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                required
                                className="block w-full rounded-md bg-card border border-border py-2.5 px-3 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                                placeholder="Enter username"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                            />
                        </div>
                        <div>
                            <label htmlFor="password" className="block text-sm font-medium text-foreground mb-1">
                                Password
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                required
                                className="block w-full rounded-md bg-card border border-border py-2.5 px-3 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                                placeholder="Enter password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </div>
                    </div>

                    {error && (
                        <div className="text-red-400 text-sm text-center bg-red-500/10 py-2 rounded-md border border-red-500/30">
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full flex justify-center items-center rounded-md bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-70 transition-colors"
                    >
                        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                        Sign in
                    </button>
                </form>

                {/* Demo Credentials Hint */}
                <div className="rounded-lg border border-primary/30 bg-primary/5 backdrop-blur-sm p-4 text-center">
                    <p className="text-xs text-muted-foreground uppercase tracking-wider mb-2">Demo Credentials</p>
                    <div className="flex justify-center gap-8 text-sm">
                        <div>
                            <span className="text-muted-foreground">Username:</span>{" "}
                            <code className="font-mono font-bold text-primary bg-primary/10 px-1.5 py-0.5 rounded">admin</code>
                        </div>
                        <div>
                            <span className="text-muted-foreground">Password:</span>{" "}
                            <code className="font-mono font-bold text-primary bg-primary/10 px-1.5 py-0.5 rounded">admin</code>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
