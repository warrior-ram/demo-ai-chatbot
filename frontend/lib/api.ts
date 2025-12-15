const API_BASE_URL = "http://localhost:8001/api/v1";

// --- Auth ---
function getAuthHeader() {
    return {
        "Content-Type": "application/json",
        "X-Token": localStorage.getItem("admin_token") || ""
    };
}

export async function login(username: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        throw new Error("Login failed");
    }

    const data = await response.json();
    localStorage.setItem("admin_token", data.access_token);
    return data;
}

// --- Sessions & Chat ---
export interface Session {
    id: number;
    bot_id: number;
    visitor_id: string;
    created_at: string;
}

export async function createSession(botId: number, visitorId: string): Promise<Session> {
    const response = await fetch(`${API_BASE_URL}/chat/session`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bot_id: botId, visitor_id: visitorId }),
    });

    if (!response.ok) {
        throw new Error("Failed to create session");
    }

    return response.json();
}

export async function getChatHistory(sessionId: number) {
    const response = await fetch(`${API_BASE_URL}/chat/session/${sessionId}/history`);
    if (!response.ok) return { messages: [] };
    return response.json();
}

// --- Bots ---
export interface Bot {
    id: number;
    name: string;
    system_prompt: string;
    welcome_message: string;
    created_at: string;
}

export async function getBots(): Promise<Bot[]> {
    const response = await fetch(`${API_BASE_URL}/bots`);
    if (!response.ok) return [];
    return response.json();
}

export async function getBot(id: number): Promise<Bot> {
    const response = await fetch(`${API_BASE_URL}/bots/${id}`);
    if (!response.ok) throw new Error("Bot not found");
    return response.json();
}

export async function createBot(data: Partial<Bot>) {
    const response = await fetch(`${API_BASE_URL}/bots`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to create bot");
    return response.json();
}

// --- Leads ---
export interface Lead {
    id: number;
    name?: string;
    email?: string;
    phone?: string;
    session_id: number;
    created_at: string;
}

export async function getLeads(): Promise<Lead[]> {
    const response = await fetch(`${API_BASE_URL}/leads`);
    if (!response.ok) return [];
    return response.json();
}

// --- Documents ---
export interface Document {
    id: number;
    filename: string;
    chunk_count: number;
    created_at: string;
    collection_stats?: any;
}

export async function getDocuments(botId: number): Promise<{ documents: Document[], collection_stats: any }> {
    const response = await fetch(`${API_BASE_URL}/documents/bot/${botId}`);
    if (!response.ok) return { documents: [], collection_stats: {} };
    return response.json();
}

export async function uploadDocument(botId: number, file: File) {
    const formData = new FormData();
    formData.append("bot_id", botId.toString());
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Upload failed");
    }
    return response.json();
}

export async function deleteDocument(docId: number) {
    const response = await fetch(`${API_BASE_URL}/documents/${docId}`, {
        method: "DELETE"
    });
    if (!response.ok) throw new Error("Delete failed");
    return response.json();
}

// --- Dashboard ---
export interface DashboardStats {
    total_sessions: number;
    total_leads: number;
    active_bots: number;
    total_documents: number;
}

export async function getDashboardStats(): Promise<DashboardStats> {
    const response = await fetch(`${API_BASE_URL}/admin/stats`, {
        headers: {
            "X-Token": localStorage.getItem("admin_token") || ""
        }
    });
    if (!response.ok) {
        if (response.status === 401) {
            throw new Error("Unauthorized");
        }
        // Fallback for demo if endpoint fails
        return {
            total_sessions: 0,
            total_leads: 0,
            active_bots: 0,
            total_documents: 0
        };
    }
    return response.json();
}
