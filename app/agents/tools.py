from typing import List, Dict
from app.retrieval.retriever import SemanticRetriever
from app.ingestion.file_extractor import FileExtractor
from app.llm.llm_engine import LLMEngine

class AgentTools:
    """Tools for LangGraph agent to interact with codebase"""
    
    def __init__(self, retriever: SemanticRetriever, extractor: FileExtractor, llm: LLMEngine):
        self.retriever = retriever
        self.extractor = extractor
        self.llm = llm
        self.repo_path = None
    
    def set_repo_path(self, repo_path: str):
        self.repo_path = repo_path
    
    def search_codebase(self, query: str, k: int = 5) -> str:
        """Search for relevant code chunks"""
        results = self.retriever.retrieve(query, k)
        
        if not results:
            return "No relevant code found."
        
        output = []
        for i, r in enumerate(results, 1):
            output.append(f"[{i}] File: {r['metadata'].get('file', 'unknown')}")
            output.append(f"    Relevance: {r['similarity']:.2f}")
            output.append(f"    Code: {r['chunk'][:300]}...")
        
        return "\n".join(output)
    
    def read_file(self, file_path: str) -> str:
        """Read a specific file from repository"""
        if not self.repo_path:
            return "No repository loaded."
        
        file_data = self.extractor.extract_file_by_path(self.repo_path, file_path)
        
        if file_data:
            return f"File: {file_path}\nLanguage: {file_data['language']}\n\n```{file_data['language']}\n{file_data['content']}\n```"
        
        return f"File {file_path} not found."
    
    def get_repo_structure(self) -> str:
        """Get repository folder structure"""
        if not self.repo_path:
            return "No repository loaded."
        
        structure = self.extractor.get_file_structure(self.repo_path)
        return f"Repository Structure:\n{structure}"
    
    def search_by_language(self, language: str, limit: int = 10) -> str:
        """Search files by programming language"""
        if not self.repo_path:
            return "No repository loaded."
        
        files = self.extractor.extract_files(self.repo_path)
        filtered = [f for f in files if f['language'] == language]
        
        if not filtered:
            return f"No files found for language: {language}"
        
        output = [f"Found {len(filtered)} {language} files:"]
        for f in filtered[:limit]:
            output.append(f"  - {f['relative_path']}")
        
        return "\n".join(output)
    
    def analyze_bugs(self, file_path: str = None) -> str:
        """Analyze code for bugs"""
        if not self.repo_path:
            return "No repository loaded."
        
        if file_path:
            file_data = self.extractor.extract_file_by_path(self.repo_path, file_path)
            if file_data:
                result = self.llm.analyze_code(file_data['content'], file_data['language'])
                return result.get('analysis', 'Analysis failed')
        
        # Analyze all Python files
        all_files = self.extractor.extract_files(self.repo_path)
        python_files = [f for f in all_files if f['language'] == 'python'][:3]
        
        analyses = []
        for f in python_files:
            result = self.llm.analyze_code(f['content'], 'python')
            analyses.append(f"### {f['relative_path']}\n{result.get('analysis', 'Analysis failed')}")
        
        return "\n\n".join(analyses) if analyses else "No files to analyze"