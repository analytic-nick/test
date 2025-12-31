# Quick Start Guide

Get Focus Group AI running in 5 minutes!

## Option 1: Manual Setup (Recommended for Development)

### Step 1: Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

**Edit `.env` and add your Anthropic API key:**
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Start the backend:**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend should be running on http://localhost:8000

### Step 2: Frontend Setup

**In a new terminal:**
```bash
cd frontend
npm install
cp .env.example .env.local
```

**Start the frontend:**
```bash
npm run dev
```

✅ Frontend should be running on http://localhost:3000

### Step 3: Try It Out!

1. Open http://localhost:3000
2. Enter a question: "Should I quit my job to start a business?"
3. Select 3-4 personas (try Gen Z, Startup Founder, and The Skeptic)
4. Click "Start Focus Group"
5. Watch the debate unfold!

---

## Option 2: Docker (One Command)

**Prerequisites:** Docker and Docker Compose installed

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Start everything
docker-compose up
```

Access the app at http://localhost:3000

---

## Troubleshooting

### Backend won't start
- ❌ "ModuleNotFoundError" → Run `pip install -r requirements.txt`
- ❌ "API key not set" → Check `.env` file has ANTHROPIC_API_KEY
- ❌ "Port 8000 in use" → Stop other apps on port 8000 or change port

### Frontend won't start
- ❌ "Cannot find module" → Run `npm install`
- ❌ "Port 3000 in use" → Stop other apps or edit package.json to use different port

### WebSocket not connecting
- ❌ Check backend is running on http://localhost:8000
- ❌ Verify `NEXT_PUBLIC_WS_URL=ws://localhost:8000` in frontend/.env.local
- ❌ Check browser console for connection errors

### Debate not starting
- ❌ Select at least 2 personas
- ❌ Enter a question (min 10 characters)
- ❌ Check backend logs for Anthropic API errors

---

## First Time Using?

**Try these questions:**
- "Should I switch careers to AI development?"
- "Is this business idea worth pursuing?"
- "What do people think about working remote vs. in-office?"
- "Should we add AI features to our product?"

**Recommended persona combinations:**
- **Career advice:** Gen Z, Corporate VP, Startup Founder
- **Product validation:** The Skeptic, The Optimist, Soccer Mom
- **Business strategy:** Startup Founder, Corporate VP, The Skeptic
- **Marketing ideas:** Gen Z, Soccer Mom, Boomer Dad

---

## What's Next?

- Read the full README.md
- Explore the code in `backend/app/core/`
- Customize personas in `persona_engine.py`
- Add your own personas!

---

**Need help?** Open an issue on GitHub or check the troubleshooting section in README.md
