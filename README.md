# Focus Group AI - Synthetic Focus Group Platform

An AI-powered platform that generates instant focus group debates between diverse personas to help validate ideas, products, and strategies.

## 🎯 What It Does

Ask a question → Select 2-6 AI personas → Watch them debate in real-time → Get insights

**Example Use Cases:**
- "Should I quit my job to start a business?"
- "Will this product idea work?"
- "Is this ad effective?"
- "What do people think about this feature?"

## 🏗️ Architecture

### Backend (FastAPI + Python)
- Real-time WebSocket streaming
- Anthropic Claude API integration
- PostgreSQL database
- Redis caching
- REST API + WebSocket endpoints

### Frontend (Next.js 14 + TypeScript)
- Server-side rendering
- Real-time WebSocket client
- Zustand state management
- Framer Motion animations
- Tailwind CSS styling

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL (optional for MVP)
- Redis (optional for MVP)
- Anthropic API key

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Anthropic API key
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local if needed
npm run dev
```

Frontend runs on `http://localhost:3000`

### 3. Access the App

Open `http://localhost:3000` in your browser!

## 📁 Project Structure

```
focus-group-ai/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py       # FastAPI app
│   │   ├── config.py     # Settings
│   │   ├── api/          # API routes
│   │   ├── core/         # Business logic
│   │   │   ├── debate_orchestrator.py
│   │   │   ├── persona_engine.py
│   │   │   └── llm_client.py
│   │   └── models/       # Database models
│   └── requirements.txt
│
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/          # Pages
│   │   ├── components/   # React components
│   │   ├── hooks/        # Custom hooks
│   │   ├── store/        # Zustand stores
│   │   └── types/        # TypeScript types
│   └── package.json
│
└── README.md
```

## 🎭 Available Personas

### Demographics
- **Zoe (Gen Z)** - 18-year-old, extremely online, values authenticity
- **Jennifer (Soccer Mom)** - 42-year-old, practical, family-first
- **Bob (Boomer Dad)** - 62-year-old, traditional values, skeptical of tech
- **Alex (College Student)** - 20-year-old, idealistic, eager to learn

### Professionals
- **Marcus (Startup Founder)** - 34-year-old, growth-obsessed entrepreneur
- **David (Corporate VP)** - 51-year-old, risk-averse, process-oriented

### Personalities
- **Richard (The Skeptic)** - Questions everything, devil's advocate
- **Sarah (The Optimist)** - Sees opportunities, encouraging

## 🔌 API Endpoints

### REST API
- `GET /` - API info
- `GET /health` - Health check
- `POST /api/focus-groups/create` - Create focus group
- `GET /api/personas` - List personas
- `GET /api/trending` - Trending questions

### WebSocket
- `WS /ws/debate/{session_id}` - Live debate streaming

## 🎨 Key Features

### Current (MVP)
- ✅ Real-time AI debates
- ✅ 8 diverse personas
- ✅ WebSocket streaming
- ✅ Sentiment analysis
- ✅ Tension meter
- ✅ Wave-based debate flow

### Coming Soon
- 🔜 Debate replays
- 🔜 Share cards
- 🔜 Trending questions feed
- 🔜 Custom persona builder
- 🔜 User accounts
- 🔜 Analytics dashboard

## 🛠️ Tech Stack

**Backend:**
- FastAPI
- Anthropic Claude API
- SQLAlchemy
- PostgreSQL
- Redis
- WebSockets

**Frontend:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion
- Zustand
- WebSockets

## 📝 Environment Variables

### Backend (.env)
```
ANTHROPIC_API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost:5432/focusgroup
REDIS_URL=redis://localhost:6379
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

## 🐛 Troubleshooting

**WebSocket not connecting:**
- Check backend is running on port 8000
- Verify NEXT_PUBLIC_WS_URL in frontend .env.local
- Check browser console for errors

**Personas not loading:**
- Ensure backend API is accessible
- Check NEXT_PUBLIC_API_URL is correct
- Verify backend /api/personas endpoint works

**Debate not starting:**
- Ensure Anthropic API key is set in backend .env
- Check backend logs for errors
- Verify at least 2 personas are selected

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For issues or questions, open a GitHub issue.

---

**Built with ❤️ using Anthropic Claude**
