# AI Customer Support Chatbot - Usage & User Manual 📘

Welcome to the AI Customer Support Chatbot! This system is designed to provide intelligent, 24/7 customer support using a RAG (Retrieval-Augmented Generation) engine and a modern web interface.

## 🎯 What it Does

1.  **Answers Questions**: Users can ask natural language questions ("How much does it cost?", "How do I reset my password?").
2.  **Captures Leads**: The intelligent agent detects when a user is interested in services or provides contact info and saves it as a valid "Lead".
3.  **Manages Knowledge**: You can upload PDF or Text documents to the Admin Dashboard. The AI reads them and uses that knowledge to answer questions.
4.  **Admin Dashboard**: A centralized hub to view chat statistics, manage captured leads, view active bots, and control the knowledge base.

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.9+ installed
- Node.js 18+ installed

### Step 1: Start the Backend (Server)

1.  Open a terminal in the `backend` folder.
2.  Activate the virtual environment (if created):
    ```bash
    # Windows
    venv\Scripts\activate
    ```
3.  Install dependencies (first time only):
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    python -m app.main
    ```
5.  **Optional**: To seed the database with demo data (recommended for first run):
    ```bash
    python seed_data.py
    ```
    *The server runs at `http://localhost:8000`*

### Step 2: Start the Frontend (Client)

1.  Open a new terminal in the `frontend` folder.
2.  Install dependencies (first time only):
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    *The application runs at `http://localhost:3000`*

---

## 📱 Using the System

### 1. The Chat Widget (Visitor Mode)
- Go to `http://localhost:3000`.
- Click the **blue chat icon** in the bottom-right corner.
- Type a message like "Hello" or "Tell me about your pricing".
- **Try Lead Capture**: Type "My email is test@example.com". The bot will acknowledge it, and it will appear in the Admin Dashboard.

### 2. The Admin Dashboard (Manager Mode)
- Go to `http://localhost:3000/admin`.
- You will be redirected to the login page.
- **Login Credentials**:
    - **Username**: `admin`
    - **Password**: `admin`
- Once logged in, you can see:
    - **Dashboard**: Real-time stats (Total Sessions, Active Bots, etc.).
    - **Leads**: A table of all people who left their contact info.
    - **Documents**: Drag & drop PDF files here to "teach" the bot new things.

### 3. Embedding on Your Website
- Go to `http://localhost:3000/embed/1`.
- This page simulates an external customer website.
- It shows the exact script tag you can copy-paste into *any* website (WordPress, Shopify, custom HTML) to add this chatbot.

---

## 🧠 "Demo Mode" vs "Real AI"

By default, the system runs in **Portfolio Demo Mode**.
- **No API Keys Needed**: It uses a sophisticated pattern-matching engine to simulate AI responses instantly.
- **Zero Cost**: Great for testing and demos.

**To Enable Real AI (DeepSeek LLM):**
1.  Open `backend/.env`.
2.  Add `DEEPSEEK_API_KEY=your_key_here`.
3.  Update `backend/app/agent/llm.py` to switch from `DemoResponseEngine` to `DeepSeekLLM`.

---

## 📁 Project Structure (For Developers)

- **`backend/`**: fastAPI server
    - `app/api/`: REST endpoints
    - `app/rag/`: Logic for reading PDFs and vector search
    - `chatbot.db`: Local SQLite database
- **`frontend/`**: Next.js 14 App
    - `app/admin/`: Admin dashboard pages
    - `components/chat/`: The widget implementation
- **`core/`**: Documentation (you are here!)

---

## 🆘 Support

If you encounter issues (e.g., "Database locked"), simply delete the `backend/chatbot.db` file and restart the server/seed script to reset everything.
