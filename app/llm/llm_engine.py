import groq
from typing import List, Dict
from app.config import Config
import os

class LLMEngine:
    """Handle LLM operations using Groq"""
    
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = groq.Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using RAG context"""
        
        system_prompt = """You are DevOpsMind AI, an expert code assistant. Help users understand their codebase.

Guidelines:
1. Answer based ONLY on the provided code context
2. Cite specific files and code snippets
3. Explain technical concepts clearly
4. If information is missing, say so honestly
5. Be helpful, precise, and concise

When analyzing code:
- Identify main entry points
- Explain the architecture
- Point out key components
- Mention dependencies and interactions"""

        user_prompt = f"""Context from codebase:
{context}

Question: {query}

Answer based on the code context above. Include file references when possible."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"