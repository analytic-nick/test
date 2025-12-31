from fastapi import APIRouter

router = APIRouter()

@router.get("/trending")
async def get_trending_questions(limit: int = 10):
    """Get trending questions"""
    
    # Mock trending questions for demo
    trending = [
        {
            "question": "Should I quit my 9-5 to start a business?",
            "category": "career",
            "run_count": 45,
            "trending_score": 892.5
        },
        {
            "question": "Is this product idea worth pursuing?",
            "category": "business",
            "run_count": 38,
            "trending_score": 756.2
        },
        {
            "question": "Should we add AI to our product?",
            "category": "tech",
            "run_count": 31,
            "trending_score": 623.8
        }
    ]
    
    return {"trending": trending[:limit]}

@router.get("/stats")
async def get_stats():
    """Get platform statistics"""
    
    return {
        "total_debates": 1247,
        "total_users": 523,
        "debates_today": 89,
        "most_popular_persona": "gen_z_teen"
    }
