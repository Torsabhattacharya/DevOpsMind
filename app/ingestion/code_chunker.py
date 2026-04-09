import re
from pathlib import Path
from app.config import Config

class CodeChunker:
    """Split code into semantic chunks"""
    
    def __init__(self, chunk_size=1000, overlap=200):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_code(self, code, file_path, language):
        """Chunk code into smaller pieces"""
        chunks = []
        metadata_list = []
        
        # Try to split by functions/classes first
        semantic_chunks = self._split_by_semantics(code, language)
        
        if semantic_chunks:
            for i, chunk in enumerate(semantic_chunks):
                if len(chunk.strip()) > 50:
                    chunks.append(chunk)
                    metadata_list.append({
                        "file": file_path,
                        "language": language,
                        "chunk_type": "semantic",
                        "chunk_index": i,
                        "size": len(chunk)
                    })
        else:
            # Fallback to character-based chunking
            chunks_by_size = self._split_by_size(code)
            for i, chunk in enumerate(chunks_by_size):
                chunks.append(chunk)
                metadata_list.append({
                    "file": file_path,
                    "language": language,
                    "chunk_type": "size_based",
                    "chunk_index": i,
                    "size": len(chunk)
                })
        
        return chunks, metadata_list
    
    def _split_by_semantics(self, code, language):
        """Split code by functions, classes, or logical blocks"""
        chunks = []
        
        if language == "python":
            # Split Python code by functions/classes
            pattern = r'(def\s+\w+\([^)]*\):[\s\S]+?(?=\n\S|\Z))|(class\s+\w+:[\s\S]+?(?=\nclass|\ndef|\Z))'
            matches = re.finditer(pattern, code)
            
            for match in matches:
                chunk = match.group(0).strip()
                if len(chunk) <= self.chunk_size * 2:
                    chunks.append(chunk)
                else:
                    # Split large functions further
                    sub_chunks = self._split_by_size(chunk)
                    chunks.extend(sub_chunks)
        
        elif language in ["javascript", "typescript", "react"]:
            # Split JS/TS by functions
            pattern = r'(function\s+\w+\([^)]*\)[\s\S]+?(?=\nfunction|\nconst|\nlet|\Z))|(const\s+\w+\s*=\s*\([^)]*\)\s*=>[\s\S]+?(?=\nconst|\nfunction|\Z))'
            matches = re.finditer(pattern, code)
            
            for match in matches:
                chunk = match.group(0).strip()
                if len(chunk) <= self.chunk_size * 2:
                    chunks.append(chunk)
                else:
                    sub_chunks = self._split_by_size(chunk)
                    chunks.extend(sub_chunks)
        
        return chunks
    
    def _split_by_size(self, text):
        """Split text by character size"""
        chunks = []
        
        for i in range(0, len(text), self.chunk_size - self.overlap):
            chunk = text[i:i + self.chunk_size]
            if chunk.strip():
                chunks.append(chunk.strip())
        
        return chunks
    
    def chunk_repository(self, files_data):
        """Chunk entire repository"""
        all_chunks = []
        all_metadata = []
        
        for file_data in files_data:
            chunks, metadata = self.chunk_code(
                file_data["content"],
                file_data["relative_path"],
                file_data["language"]
            )
            
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)
        
        return all_chunks, all_metadata