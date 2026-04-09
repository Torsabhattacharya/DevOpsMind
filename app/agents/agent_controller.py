from typing import TypedDict, List, Dict, Any, Literal
from langgraph.graph import StateGraph, END
import json

class AgentState(TypedDict):
    """State for the LangGraph agent"""
    question: str
    context: str
    action: str
    tool_results: List[Dict]
    answer: str
    iterations: int

class LangGraphAgent:
    """Agent that uses tools to answer questions about codebase"""
    
    def __init__(self, tools):
        self.tools = tools
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        
        def should_continue(state: AgentState) -> Literal["use_tool", "generate_answer", "end"]:
            """Decide whether to use another tool or generate answer"""
            if state.get("iterations", 0) >= 3:
                return "generate_answer"
            if state.get("action") == "done":
                return "generate_answer"
            return "use_tool"
        
        def use_tool(state: AgentState) -> AgentState:
            """Execute a tool based on the question"""
            question = state["question"].lower()
            result = ""
            
            # Determine which tool to use
            if "structure" in question or "folder" in question or "organization" in question:
                result = self.tools.get_repo_structure()
                action = "structure_analyzed"
            
            elif "bug" in question or "issue" in question or "problem" in question or "vulnerab" in question:
                result = self.tools.analyze_bugs()
                action = "bugs_analyzed"
            
            elif "search" in question or "find" in question or "where" in question:
                # Extract search query
                search_query = question.replace("search", "").replace("find", "").strip()
                if len(search_query) < 10:
                    search_query = question
                result = self.tools.search_codebase(search_query, k=5)
                action = "searched"
            
            elif "read" in question or "show" in question and "file" in question:
                # Try to extract file path
                result = self.tools.get_repo_structure()
                action = "files_listed"
            
            elif "language" in question or "python" in question or "javascript" in question:
                lang = "python" if "python" in question else "javascript" if "javascript" in question else None
                if lang:
                    result = self.tools.search_by_language(lang)
                    action = "language_searched"
                else:
                    result = "Please specify a programming language (python, javascript, etc.)"
                    action = "error"
            
            else:
                # Default: search the codebase
                result = self.tools.search_codebase(question, k=3)
                action = "searched"
            
            # Update state
            new_tool_results = state.get("tool_results", []) + [{
                "action": action,
                "result": result[:1000]  # Limit result size
            }]
            
            return {
                **state,
                "tool_results": new_tool_results,
                "action": action,
                "context": result,
                "iterations": state.get("iterations", 0) + 1
            }
        
        def generate_answer(state: AgentState) -> AgentState:
            """Generate final answer using LLM"""
            # Combine all tool results as context
            context_parts = []
            for tr in state.get("tool_results", []):
                context_parts.append(f"--- {tr['action']} ---\n{tr['result']}")
            
            full_context = "\n\n".join(context_parts) if context_parts else state.get("context", "No context found")
            
            # Use LLM to generate answer
            from app.llm.llm_engine import LLMEngine
            llm = LLMEngine()
            
            system_prompt = """You are DevOpsMind AI, an expert code assistant. Answer questions based on the codebase context provided.

Instructions:
- Be precise and cite specific files
- Use code snippets when helpful
- If you don't know something, say so honestly
- Provide actionable insights"""
            
            user_prompt = f"""Context from codebase:
{full_context}

Question: {state["question"]}

Answer based on the context above:"""
            
            try:
                response = llm.client.chat.completions.create(
                    model=llm.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"Error generating answer: {str(e)}\n\nBased on tool results:\n{full_context[:500]}"
            
            return {**state, "answer": answer}
        
        # Build the graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("use_tool", use_tool)
        workflow.add_node("generate_answer", generate_answer)
        
        # Add edges
        workflow.set_entry_point("use_tool")
        workflow.add_conditional_edges(
            "use_tool",
            should_continue,
            {
                "use_tool": "use_tool",
                "generate_answer": "generate_answer",
                "end": END
            }
        )
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    def ask(self, question: str) -> str:
        """Ask a question about the codebase"""
        initial_state: AgentState = {
            "question": question,
            "context": "",
            "action": "",
            "tool_results": [],
            "answer": "",
            "iterations": 0
        }
        
        result = self.graph.invoke(initial_state)
        return result.get("answer", "I couldn't generate an answer.")