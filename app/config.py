import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    
    # Model Settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384-dimension embeddings
    LLM_MODEL = "llama-3.1-8b-instant"   # Groq LLaMA 3.1
    
    # Vector Store
    FAISS_INDEX_PATH = "faiss_index"
    
    # Code Chunking
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # Repository
    CLONE_DIR = "cloned_repos"
    
    # Supported Languages
    SUPPORTED_EXTENSIONS = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'react',
        '.tsx': 'react',
        '.go': 'go',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.rb': 'ruby',
        '.php': 'php',
        '.html': 'html',
        '.css': 'css',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.md': 'markdown'
    }