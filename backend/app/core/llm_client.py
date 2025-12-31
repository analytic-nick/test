import anthropic
from typing import AsyncGenerator
from app.config import settings

class ClaudeClient:
    """Wrapper for Anthropic Claude API"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    async def stream_completion(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 300
    ) -> AsyncGenerator[str, None]:
        """Stream a completion from Claude"""
        
        try:
            with self.client.messages.stream(
                model=settings.DEFAULT_MODEL,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text
                    
        except Exception as e:
            print(f"Error streaming from Claude: {e}")
            raise
    
    async def get_completion(
        self,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 300
    ) -> str:
        """Get a complete response from Claude"""
        
        try:
            message = self.client.messages.create(
                model=settings.DEFAULT_MODEL,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"Error getting completion from Claude: {e}")
            raise
