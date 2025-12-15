# AI Customer Support Chatbot 🤖

A state-of-the-art, business-ready AI customer support chatbot system.
Built with **FastAPI** (Backend) and **Next.js** (Frontend).

## 🚀 Quick Start

### 1. Start Backend
```bash
cd backend
venv\Scripts\activate   # Windows
python -m app.main
```
*Runs on http://localhost:8001*

### 2. Start Frontend
```bash
cd frontend
npm install
npm run dev
```
*Runs on http://localhost:3000*

### 3. (Optional) Seed Demo Data
```bash
cd backend
python seed_data.py
```

---

## 🔑 Demo Credentials

- **Username:** `admin`
- **Password:** `admin`

---

## 📂 Project Structure

```
demo/
├── backend/          # FastAPI server, RAG engine, Database
├── frontend/         # Next.js app, Admin UI, Chat Widget
├── core/            # Documentation & Screenshots
│   ├── USAGE.md         # How to use the system
│   ├── WALKTHROUGH.md   # Visual tour with screenshots
│   └── PROJECT_OVERVIEW.md  # Technical details
└── README.md         # This file
```

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [USAGE.md](core/USAGE.md) | Step-by-step user guide |
| [WALKTHROUGH.md](core/WALKTHROUGH.md) | Visual tour with screenshots |
| [PROJECT_OVERVIEW.md](core/PROJECT_OVERVIEW.md) | Architecture & development status |

---

## ✨ Key Features

- **Real-time Chat** - WebSocket-based messaging
- **RAG Engine** - Upload PDFs to train the bot
- **Lead Capture** - Automatic contact detection
- **Admin Dashboard** - Analytics & management
- **Demo Mode** - Works without API keys

---

## 📄 License

MIT License
