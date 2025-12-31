from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ARRAY, JSON, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Persona(Base):
    __tablename__ = "personas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    category = Column(String(50))
    description = Column(Text)
    avatar_url = Column(Text)
    speaking_style = Column(Text)
    system_prompt_template = Column(Text)
    is_premium = Column(Boolean, default=False)
    is_custom = Column(Boolean, default=False)
    created_by = Column(UUID(as_uuid=True))
    unlock_requirement = Column(JSON)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class FocusGroupSession(Base):
    __tablename__ = "focus_group_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_key = Column(String(12), unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True))
    question = Column(Text, nullable=False)
    selected_persona_ids = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    status = Column(String(20))
    debate_mode = Column(String(20))
    
    # Results
    transcript = Column(JSON)
    summary = Column(Text)
    sentiment_breakdown = Column(JSON)
    key_insights = Column(ARRAY(Text))
    consensus_points = Column(ARRAY(Text))
    most_controversial_take = Column(Text)
    
    # Metadata
    duration_seconds = Column(Integer)
    token_usage = Column(Integer)
    share_count = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_public = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime)

class PersonaResponse(Base):
    __tablename__ = "persona_responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey('focus_group_sessions.id', ondelete='CASCADE'))
    persona_id = Column(UUID(as_uuid=True), ForeignKey('personas.id'))
    response_text = Column(Text, nullable=False)
    response_order = Column(Integer)
    responding_to = Column(UUID(as_uuid=True))
    sentiment = Column(String(20))
    confidence_score = Column(Float)
    reaction_emojis = Column(ARRAY(Text))
    created_at = Column(DateTime, server_default=func.now())

class TrendingQuestion(Base):
    __tablename__ = "trending_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    category = Column(String(50))
    run_count = Column(Integer, default=1)
    last_run_at = Column(DateTime, server_default=func.now())
    trending_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())
