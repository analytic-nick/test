from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import focus_groups, personas, replays, analytics
from app.api.websocket.debate_stream import router as websocket_router
from app.config import settings

app = FastAPI(
    title="Focus Group AI API",
    description="Synthetic Focus Group Debate Platform",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(focus_groups.router, prefix="/api/focus-groups", tags=["focus_groups"])
app.include_router(personas.router, prefix="/api/personas", tags=["personas"])
app.include_router(replays.router, prefix="/api/replays", tags=["replays"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(websocket_router, prefix="/ws", tags=["websocket"])

@app.get("/")
async def root():
    return {
        "message": "Focus Group AI API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
