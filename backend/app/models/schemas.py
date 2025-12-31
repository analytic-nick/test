from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class SentimentType(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"

class DebateMode(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"

class SessionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# Persona Schemas
class PersonaBase(BaseModel):
    name: str
    slug: str
    category: str
    description: str
    avatar_url: Optional[str] = None
    speaking_style: str
    is_premium: bool = False

class PersonaCreate(PersonaBase):
    system_prompt_template: str

class PersonaResponse(PersonaBase):
    id: str
    usage_count: int
    created_at: datetime

# Focus Group Schemas
class FocusGroupCreate(BaseModel):
    question: str = Field(..., min_length=10, max_length=500)
    persona_ids: List[str] = Field(..., min_items=2, max_items=6)
    mode: DebateMode = DebateMode.HYBRID
    is_public: bool = True

class FocusGroupSession(BaseModel):
    id: str
    session_key: str
    question: str
    selected_persona_ids: List[str]
    status: SessionStatus
    created_at: datetime

# Debate Response Schemas
class DebateResponse(BaseModel):
    session_id: str
    persona_id: str
    persona_name: str
    text: str
    wave: int = 1
    sentiment: Optional[SentimentType] = None
    confidence_score: Optional[float] = None
    is_rebuttal: bool = False
    is_complete: bool = False
    timestamp: datetime

class PersonaResponseCreate(BaseModel):
    persona_id: str
    persona_name: str
    text: str
    sentiment: SentimentType
    confidence_score: float

# Summary Schemas
class SentimentBreakdown(BaseModel):
    positive: int
    negative: int
    neutral: int
    mixed: int

class DebateSummary(BaseModel):
    session_id: str
    summary_text: str
    sentiment_breakdown: SentimentBreakdown
    key_insights: List[str]
    consensus_points: List[str]
    most_controversial_take: str
    share_url: str

# Analytics Schemas
class TrendingQuestion(BaseModel):
    question: str
    category: Optional[str]
    run_count: int
    trending_score: float
    last_run: datetime

# WebSocket Message Schemas
class WSMessage(BaseModel):
    type: str
    data: Optional[Dict] = None
    message: Optional[str] = None

class WSDebateStart(BaseModel):
    action: str = "start"
    question: str
    persona_ids: List[str]
    mode: str = "hybrid"
