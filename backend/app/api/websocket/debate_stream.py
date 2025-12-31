from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
import json
from app.core.debate_orchestrator import DebateOrchestrator
import uuid

router = APIRouter()

class DebateStreamManager:
    """Manages WebSocket connections for live debate streaming"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.orchestrator = DebateOrchestrator()
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        print(f"WebSocket connected: {session_id}")
    
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            print(f"WebSocket disconnected: {session_id}")
    
    async def stream_debate(
        self,
        session_id: str,
        question: str,
        persona_ids: list,
        mode: str = "hybrid"
    ):
        """Stream debate responses to connected client"""
        
        websocket = self.active_connections.get(session_id)
        if not websocket:
            print(f"No websocket found for session: {session_id}")
            return
        
        try:
            print(f"Starting debate for session: {session_id}")
            
            # Start debate
            async for response in self.orchestrator.run_debate(
                session_id=session_id,
                question=question,
                persona_ids=persona_ids,
                mode=mode
            ):
                # Send to client
                await websocket.send_json({
                    "type": "debate_response",
                    "data": {
                        "session_id": response.session_id,
                        "persona_id": response.persona_id,
                        "persona_name": response.persona_name,
                        "text": response.text,
                        "wave": response.wave,
                        "sentiment": response.sentiment.value if response.sentiment else None,
                        "confidence_score": response.confidence_score,
                        "is_rebuttal": response.is_rebuttal,
                        "is_complete": response.is_complete,
                        "timestamp": response.timestamp.isoformat()
                    }
                })
                
                # If complete, send summary
                if response.is_complete:
                    await websocket.send_json({
                        "type": "debate_complete",
                        "data": {
                            "summary": "Debate completed successfully",
                            "share_url": f"/replay/{session_id}"
                        }
                    })
            
            print(f"Debate completed for session: {session_id}")
            
        except WebSocketDisconnect:
            print(f"Client disconnected during debate: {session_id}")
            self.disconnect(session_id)
        except Exception as e:
            print(f"Error in debate stream: {e}")
            try:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
            except:
                pass
            self.disconnect(session_id)

# Global manager instance
manager = DebateStreamManager()

@router.websocket("/debate/{session_id}")
async def debate_websocket(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for debate streaming"""
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Wait for start command from client
            data = await websocket.receive_json()
            print(f"Received WebSocket message: {data}")
            
            if data.get("action") == "start":
                await manager.stream_debate(
                    session_id=session_id,
                    question=data["question"],
                    persona_ids=data["persona_ids"],
                    mode=data.get("mode", "hybrid")
                )
                
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(session_id)
