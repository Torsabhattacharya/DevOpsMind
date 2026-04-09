import groq
from typing import List, Dict
from app.config import Config

class LLMEngine:
    """Handle LLM operations using Groq"""
    
    def __init__(self):
        self.client = groq.Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.LLM_MODEL
    
    def generate_response(self, query: str, context: str, chat_history: List = None) -> str:
        """Generate response using RAG context"""
        
        system_prompt = """You are DevOpsMind AI, an expert code assistant. Help users understand their codebase.

Guidelines:
1. Answer based on the provided code context
2. Cite specific files and code snippets
3. Explain technical concepts clearly
4. If information is missing, say so honestly
5. Provide actionable insights

Be helpful, precise, and concise."""

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
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def analyze_code(self, code: str, language: str) -> Dict:
        """Analyze code for bugs and improvements"""
        
        prompt = f"""Analyze this {language} code and identify:
1. Potential bugs or issues
2. Security vulnerabilities
3. Performance improvements
4. Best practice violations

Code:
```{language}
{code[:1500]}
```

Provide a structured analysis."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            return {
                "success": True,
                "analysis": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def generate_documentation(self, code: str, language: str) -> str:
        """Generate documentation for code"""
        
        prompt = f"""Generate comprehensive documentation for this {language} code:
```{language}
{code[:1500]}
```

Include:
* Purpose/description
* Key functions/classes
* Parameters and return values
* Usage examples"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=1000
            )
            return response.choices[0].message.content
        
        except Exception as e:
            return f"Error generating documentation: {str(e)}"