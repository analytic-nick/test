from typing import List, AsyncGenerator
import asyncio
from datetime import datetime
from app.core.llm_client import ClaudeClient
from app.core.persona_engine import PersonaEngine
from app.models.schemas import DebateResponse, SentimentType

class PersonaResponseData:
    """Simple data class for persona responses"""
    def __init__(self, persona_id, persona_name, text, sentiment, confidence_score):
        self.persona_id = persona_id
        self.persona_name = persona_name
        self.text = text
        self.sentiment = sentiment
        self.confidence_score = confidence_score

class DebateOrchestrator:
    """Manages the flow of AI debate between personas"""
    
    def __init__(self):
        self.claude = ClaudeClient()
        self.persona_engine = PersonaEngine()
    
    async def run_debate(
        self,
        session_id: str,
        question: str,
        persona_ids: List[str],
        mode: str = "hybrid"
    ) -> AsyncGenerator[DebateResponse, None]:
        """
        Orchestrates the debate and streams responses
        
        Modes:
        - sequential: One at a time (safest)
        - parallel: All at once (fastest)
        - hybrid: Waves of responses (best UX)
        """
        
        personas = await self.persona_engine.get_personas(persona_ids)
        
        if mode == "hybrid":
            async for response in self._hybrid_debate(session_id, question, personas):
                yield response
        elif mode == "parallel":
            async for response in self._parallel_debate(session_id, question, personas):
                yield response
        else:
            async for response in self._sequential_debate(session_id, question, personas):
                yield response
    
    async def _hybrid_debate(self, session_id, question, personas):
        """Wave-based responses with reactions"""
        
        # Wave 1: First 3 personas
        wave1_personas = personas[:3]
        wave1_responses = []
        
        tasks = [
            self._get_persona_response(p, question, [])
            for p in wave1_personas
        ]
        
        for task in asyncio.as_completed(tasks):
            response = await task
            wave1_responses.append(response)
            
            yield DebateResponse(
                session_id=session_id,
                persona_id=response.persona_id,
                persona_name=response.persona_name,
                text=response.text,
                wave=1,
                sentiment=response.sentiment,
                confidence_score=response.confidence_score,
                is_complete=False,
                timestamp=datetime.utcnow()
            )
        
        # Wave 2: Remaining personas respond to wave 1
        if len(personas) > 3:
            wave2_personas = personas[3:]
            wave2_responses = []
            
            tasks = [
                self._get_persona_response(p, question, wave1_responses)
                for p in wave2_personas
            ]
            
            for task in asyncio.as_completed(tasks):
                response = await task
                wave2_responses.append(response)
                
                yield DebateResponse(
                    session_id=session_id,
                    persona_id=response.persona_id,
                    persona_name=response.persona_name,
                    text=response.text,
                    wave=2,
                    sentiment=response.sentiment,
                    confidence_score=response.confidence_score,
                    is_complete=False,
                    timestamp=datetime.utcnow()
                )
            
            # Wave 3: Quick rebuttals (first 2 personas)
            rebuttal_personas = personas[:2]
            all_responses = wave1_responses + wave2_responses
            
            for persona in rebuttal_personas:
                rebuttal = await self._get_rebuttal(persona, question, all_responses)
                
                yield DebateResponse(
                    session_id=session_id,
                    persona_id=rebuttal.persona_id,
                    persona_name=rebuttal.persona_name,
                    text=rebuttal.text,
                    wave=3,
                    sentiment=rebuttal.sentiment,
                    confidence_score=rebuttal.confidence_score,
                    is_complete=False,
                    is_rebuttal=True,
                    timestamp=datetime.utcnow()
                )
        
        # Final: Mark complete
        yield DebateResponse(
            session_id=session_id,
            persona_id="",
            persona_name="",
            text="",
            wave=0,
            is_complete=True,
            timestamp=datetime.utcnow()
        )
    
    async def _sequential_debate(self, session_id, question, personas):
        """One persona at a time"""
        previous_responses = []
        
        for idx, persona in enumerate(personas):
            response = await self._get_persona_response(persona, question, previous_responses)
            previous_responses.append(response)
            
            yield DebateResponse(
                session_id=session_id,
                persona_id=response.persona_id,
                persona_name=response.persona_name,
                text=response.text,
                wave=1,
                sentiment=response.sentiment,
                confidence_score=response.confidence_score,
                is_complete=False,
                timestamp=datetime.utcnow()
            )
        
        yield DebateResponse(
            session_id=session_id,
            persona_id="",
            persona_name="",
            text="",
            wave=0,
            is_complete=True,
            timestamp=datetime.utcnow()
        )
    
    async def _parallel_debate(self, session_id, question, personas):
        """All at once"""
        tasks = [
            self._get_persona_response(p, question, [])
            for p in personas
        ]
        
        for task in asyncio.as_completed(tasks):
            response = await task
            
            yield DebateResponse(
                session_id=session_id,
                persona_id=response.persona_id,
                persona_name=response.persona_name,
                text=response.text,
                wave=1,
                sentiment=response.sentiment,
                confidence_score=response.confidence_score,
                is_complete=False,
                timestamp=datetime.utcnow()
            )
        
        yield DebateResponse(
            session_id=session_id,
            persona_id="",
            persona_name="",
            text="",
            wave=0,
            is_complete=True,
            timestamp=datetime.utcnow()
        )
    
    async def _get_persona_response(self, persona, question: str, previous_responses: List) -> PersonaResponseData:
        """Get a single persona's response"""
        
        # Build context from previous responses
        context = self._build_context(previous_responses)
        
        # Generate system prompt
        system_prompt = self.persona_engine.build_prompt(
            persona=persona,
            question=question,
            context=context
        )
        
        # Get completion from Claude
        response_text = await self.claude.get_completion(
            system_prompt=system_prompt,
            user_message=question,
            max_tokens=300
        )
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(response_text)
        
        return PersonaResponseData(
            persona_id=persona.id,
            persona_name=persona.name,
            text=response_text,
            sentiment=sentiment,
            confidence_score=self._calculate_confidence(response_text)
        )
    
    async def _get_rebuttal(self, persona, question: str, all_responses: List) -> PersonaResponseData:
        """Get a rebuttal response"""
        
        context = self._build_context(all_responses)
        context += "\n\nNow provide a brief rebuttal or final thought (1-2 sentences)."
        
        system_prompt = self.persona_engine.build_prompt(
            persona=persona,
            question=question,
            context=context
        )
        
        response_text = await self.claude.get_completion(
            system_prompt=system_prompt,
            user_message="Provide your rebuttal",
            max_tokens=150
        )
        
        sentiment = self._analyze_sentiment(response_text)
        
        return PersonaResponseData(
            persona_id=persona.id,
            persona_name=persona.name,
            text=response_text,
            sentiment=sentiment,
            confidence_score=self._calculate_confidence(response_text)
        )
    
    def _build_context(self, previous_responses: List) -> str:
        """Format previous responses for context"""
        if not previous_responses:
            return ""
        
        context = "Other panel members have said:\n\n"
        for resp in previous_responses:
            context += f"{resp.persona_name}: {resp.text}\n\n"
        
        return context
    
    def _analyze_sentiment(self, text: str) -> SentimentType:
        """Determine sentiment of response"""
        positive_words = ['great', 'love', 'amazing', 'yes', 'definitely', 'excellent', 'perfect', 'good']
        negative_words = ['bad', 'hate', 'terrible', 'no', 'never', 'awful', 'wrong', 'problem']
        
        text_lower = text.lower()
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            return SentimentType.POSITIVE
        elif neg_count > pos_count:
            return SentimentType.NEGATIVE
        else:
            return SentimentType.NEUTRAL
    
    def _calculate_confidence(self, text: str) -> float:
        """Calculate how confident the response is"""
        hedging = ['maybe', 'perhaps', 'possibly', 'might', 'could', 'probably']
        hedge_count = sum(1 for w in hedging if w in text.lower())
        
        confidence = max(0.3, 1.0 - (hedge_count * 0.15))
        return round(confidence, 2)
