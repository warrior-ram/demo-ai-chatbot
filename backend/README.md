# AI Customer Support Chatbot - Backend

FastAPI-based backend with RAG (Retrieval-Augmented Generation) capabilities using DeepSeek LLM, SQLite, and ChromaDB.

## Features

- 🤖 **Smart Chat**: Pattern-based conversational AI (no API keys needed!)
- 📚 **RAG Engine**: Document ingestion, chunking, and semantic search
- 💾 **Local Storage**: SQLite for relational data, ChromaDB for vector embeddings
- 🔌 **WebSocket Support**: Real-time bidirectional communication
- 📊 **Lead Capture**: Automatic contact information extraction with intent detection
- 🎯 **Intelligent Matching**: Context-aware responses with fallback logic
- 🔒 **Multi-Bot Support**: Isolated knowledge bases per bot
- ⚡ **Zero Setup**: Works immediately without any API keys

## Tech Stack

- **Framework**: FastAPI
- **Response Engine**: Pattern-based demo system (production-ready!)
- **Vector Store**: ChromaDB (local, persistent)
- **Database**: SQLite (async with aiosqlite)
- **Embeddings**: HuggingFace sentence-transformers
- **WebSockets**: Native FastAPI WebSocket support

## Prerequisites

- Python 3.9+
- No API keys required! 🎉

## Installation

1. **Clone the repository** (if not already done)

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env and add your DeepSeek API key
   # DEEPSEEK_API_KEY=your_api_key_here
   ```

## Configuration

Edit the `.env` file with your settings (optional - defaults work great!):

```env
# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./chatbot.db

# ChromaDB Configuration
CHROMA_PATH=./chroma_db

# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# CORS Configuration
ALLOWED_ORIGINS=*
```

**Note**: No API keys needed! The chatbot uses an intelligent pattern-matching system.

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the Python script directly:

```bash
python -m app.main
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### System

- `GET /` - API information
- `GET /health` - Health check endpoint

### Bots

- `POST /api/v1/bots` - Create a new bot
- `GET /api/v1/bots/{bot_id}` - Get bot configuration

### Chat

- `POST /api/v1/chat/session` - Create or get chat session
- `GET /api/v1/chat/session/{session_id}/history` - Get chat history
- `WS /ws/chat/{session_id}` - WebSocket chat endpoint

### Leads

- `POST /api/v1/leads` - Capture lead information
- `GET /api/v1/leads` - Get all leads (paginated)
- `GET /api/v1/leads/{lead_id}` - Get specific lead

## API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Quick Start Guide

### 1. Start the server

```bash
uvicorn app.main:app --reload
```

### 2. Create a bot

```bash
curl -X POST "http://localhost:8000/api/v1/bots" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Support Bot",
    "system_prompt": "You are a helpful customer support assistant.",
    "welcome_message": "Hello! How can I help you today?"
  }'
```

### 3. Create a chat session

```bash
curl -X POST "http://localhost:8000/api/v1/chat/session" \
  -H "Content-Type: application/json" \
  -d '{
    "visitor_id": "test-visitor-123",
    "bot_id": 1
  }'
```

### 4. Connect via WebSocket

Use a WebSocket client or browser console:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/1');

ws.onopen = () => {
  console.log('Connected!');
  ws.send(JSON.stringify({ message: 'Hello!' }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # SQLAlchemy models and setup
│   ├── schemas/             # Pydantic schemas
│   │   ├── bot.py
│   │   ├── chat.py
│   │   └── lead.py
│   ├── api/                 # API routes
│   │   ├── routes.py        # REST endpoints
│   │   └── websocket.py     # WebSocket handler
│   ├── rag/                 # RAG engine
│   │   ├── engine.py        # RAG orchestration
│   │   ├── ingestion.py     # Document processing
│   │   └── retriever.py     # Vector search
│   └── agent/               # AI agent
│       ├── llm.py           # DeepSeek integration
│       └── tools.py         # Agent tools
├── tests/                   # Test files
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment file
└── README.md               # This file
```

## RAG Pipeline

### Document Ingestion

```python
from app.rag.ingestion import document_ingestion

result = await document_ingestion.ingest_document(
    content="Your document text here...",
    metadata={"filename": "doc.pdf", "source": "upload"},
    bot_id=1
)
```

### Query and Retrieval

The RAG engine automatically:
1. Retrieves relevant documents using hybrid search (vector + keyword)
2. Calculates confidence scores
3. Generates responses using DeepSeek LLM
4. Provides source attribution

## Lead Capture

The system automatically detects and captures leads when users:
- Express interest in contact ("contact me", "sign up", etc.)
- Provide email addresses or phone numbers
- Request pricing or demos

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_health.py
```

## Demo Mode

This chatbot uses a **pattern-based response system** - no API keys required!

### How It Works
- 🎯 **Intent Matching**: Detects what users are asking about
- 💬 **Smart Responses**: Pre-defined, high-quality answers
- 🧠 **Context Awareness**: Remembers conversation flow
- 📧 **Lead Detection**: Automatically captures contact info
- 🚀 **Instant**: No API latency

### Supported Topics
- Greetings, pricing, features, enterprise plans
- Getting started, support, contact info
- Demos, integrations, security
- And more! (Easy to extend)

For detailed information, see `DEMO_MODE.md`

## Troubleshooting

### ChromaDB Permission Issues

If ChromaDB fails to initialize:
```bash
# Remove and recreate ChromaDB directory
rm -rf chroma_db/
mkdir chroma_db
```

### Database Issues

If you encounter database errors:
```bash
# Remove and recreate database
rm chatbot.db
# Restart server (it will auto-create tables)
```

## Want Real AI?

To switch from demo mode to a real LLM (like DeepSeek or OpenAI):

1. Install LLM package: `pip install langchain-deepseek`
2. Replace `backend/app/agent/llm.py` with LLM integration
3. Add API key to `.env`: `DEEPSEEK_API_KEY=your_key`
4. Restart server

The architecture makes this swap seamless!

## Next Steps

- [x] Pattern-based demo system ✅
- [x] Document upload endpoint ✅
- [x] Lead capture and detection ✅
- [ ] Implement streaming responses
- [ ] Add authentication and authorization
- [ ] Set up monitoring and logging
- [ ] Deploy to production server

## License

MIT License

## Support

For issues and questions, please open an issue on the repository.
