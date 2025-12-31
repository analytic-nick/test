from fastapi import APIRouter, HTTPException
from app.models.schemas import FocusGroupCreate, FocusGroupSession
from app.core.persona_engine import PersonaEngine
import uuid
from datetime import datetime

router = APIRouter()
persona_engine = PersonaEngine()

# In-memory storage for demo (replace with database in production)
sessions_db = {}

@router.post("/create", response_model=FocusGroupSession)
async def create_focus_group(data: FocusGroupCreate):
    """Create a new focus group session"""
    
    # Generate session ID and key
    session_id = str(uuid.uuid4())
    session_key = str(uuid.uuid4())[:12]
    
    # Validate personas exist
    available_personas = persona_engine.get_all_template_ids()
    for pid in data.persona_ids:
        if pid not in available_personas:
            raise HTTPException(status_code=400, detail=f"Invalid persona ID: {pid}")
    
    # Create session
    session = FocusGroupSession(
        id=session_id,
        session_key=session_key,
        question=data.question,
        selected_persona_ids=data.persona_ids,
        status="pending",
        created_at=datetime.utcnow()
    )
    
    # Store session
    sessions_db[session_id] = session
    
    return session

@router.get("/{session_id}", response_model=FocusGroupSession)
async def get_focus_group(session_id: str):
    """Get focus group session details"""
    
    session = sessions_db.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.get("/")
async def list_focus_groups(limit: int = 10, offset: int = 0):
    """List recent focus group sessions"""
    
    all_sessions = list(sessions_db.values())
    # Sort by created_at descending
    sorted_sessions = sorted(all_sessions, key=lambda x: x.created_at, reverse=True)
    
    return {
        "sessions": sorted_sessions[offset:offset+limit],
        "total": len(sorted_sessions)
    }
