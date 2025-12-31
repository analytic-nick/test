# Focus Group AI - Frontend

Next.js 14 frontend for the Synthetic Focus Group platform.

## Setup

1. **Install dependencies:**
```bash
npm install
```

2. **Set up environment variables:**
```bash
cp .env.example .env.local
# Edit .env.local with your backend URLs
```

3. **Run the development server:**
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app router
│   │   ├── page.tsx      # Landing page
│   │   ├── debate/       # Main debate interface
│   │   └── layout.tsx    # Root layout
│   ├── components/       # React components
│   ├── hooks/            # Custom hooks
│   ├── store/            # Zustand state management
│   ├── types/            # TypeScript types
│   └── lib/              # Utilities
├── public/               # Static assets
└── package.json
```

## Key Features

- **Real-time WebSocket streaming** - Watch debates unfold live
- **Zustand state management** - Clean, reactive state
- **Framer Motion animations** - Smooth UI transitions
- **Tailwind CSS** - Beautiful, responsive design
- **TypeScript** - Type-safe code

## Available Pages

- `/` - Landing page
- `/debate` - Main debate interface
- `/trending` - Trending questions (coming soon)
- `/replay/[id]` - Replay past debates (coming soon)

## Development

**Run dev server:**
```bash
npm run dev
```

**Build for production:**
```bash
npm run build
npm start
```

**Lint code:**
```bash
npm run lint
```

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)
- `NEXT_PUBLIC_WS_URL` - WebSocket URL (default: ws://localhost:8000)

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion
- Zustand
- WebSockets
