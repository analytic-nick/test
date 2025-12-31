from fastapi import APIRouter
from app.core.persona_engine import PersonaEngine
from typing import List

router = APIRouter()
persona_engine = PersonaEngine()

@router.get("/")
async def get_all_personas():
    """Get all available personas"""
    
    personas = []
    for pid, template in persona_engine.PERSONA_TEMPLATES.items():
        personas.append({
            "id": pid,
            "name": template["name"],
            "category": template["category"],
            "description": template["description"],
            "speaking_style": template["speaking_style"],
            "avatar_url": f"/personas/{pid}.png",
            "is_premium": False
        })
    
    return {"personas": personas, "total": len(personas)}

@router.get("/categories")
async def get_persona_categories():
    """Get personas grouped by category"""
    
    categories = {
        "demographic": [],
        "professional": [],
        "personality": []
    }
    
    for pid, template in persona_engine.PERSONA_TEMPLATES.items():
        category = template["category"]
        if category in categories:
            categories[category].append({
                "id": pid,
                "name": template["name"],
                "description": template["description"],
                "avatar_url": f"/personas/{pid}.png"
            })
    
    return categories

@router.get("/{persona_id}")
async def get_persona(persona_id: str):
    """Get details for a specific persona"""
    
    template = persona_engine.PERSONA_TEMPLATES.get(persona_id)
    if not template:
        return {"error": "Persona not found"}, 404
    
    return {
        "id": persona_id,
        "name": template["name"],
        "category": template["category"],
        "description": template["description"],
        "speaking_style": template["speaking_style"],
        "avatar_url": f"/personas/{persona_id}.png",
        "system_prompt": template["system_prompt"]
    }
