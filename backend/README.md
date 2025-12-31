# Focus Group AI - Backend

FastAPI backend for the Synthetic Focus Group platform.

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. **Run the development server:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### REST API
- `GET /` - API info
- `GET /health` - Health check
- `POST /api/focus-groups/create` - Create new focus group
- `GET /api/focus-groups/{id}` - Get focus group details
- `GET /api/personas` - List all personas
- `GET /api/personas/categories` - Get personas by category
- `GET /api/trending` - Get trending questions

### WebSocket
- `WS /ws/debate/{session_id}` - Stream debate in real-time

## WebSocket Protocol

**Connect:**
```
ws://localhost:8000/ws/debate/{session_id}
```

**Send:**
```json
{
  "action": "start",
  "question": "Should I quit my job?",
  "persona_ids": ["gen_z_teen", "startup_founder", "the_skeptic"],
  "mode": "hybrid"
}
```

**Receive:**
```json
{
  "type": "debate_response",
  "data": {
    "persona_id": "gen_z_teen",
    "persona_name": "Zoe",
    "text": "Response text...",
    "sentiment": "positive",
    "wave": 1
  }
}
```

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Settings
│   ├── api/                 # API routes
│   ├── core/                # Business logic
│   ├── models/              # Database models
│   └── services/            # Services
├── requirements.txt
└── .env.example
```

## Available Personas

- **Demographics:** gen_z_teen, soccer_mom, boomer_dad, college_student
- **Professionals:** startup_founder, corporate_vp
- **Personalities:** the_skeptic, the_optimist

## Development

**Run with auto-reload:**
```bash
uvicorn app.main:app --reload
```

**Test WebSocket:**
```bash
# Use wscat or any WebSocket client
wscat -c ws://localhost:8000/ws/debate/test-session-id
```
