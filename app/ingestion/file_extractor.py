import os
from pathlib import Path
from app.config import Config

class FileExtractor:
    """Extract code files from repository"""
    
    def __init__(self):
        self.supported_extensions = Config.SUPPORTED_EXTENSIONS
    
    def extract_files(self, repo_path):
        """Extract all code files from repository"""
        files_data = []
        
        for file_path in Path(repo_path).rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix
                
                # Check if file is supported
                if ext in self.supported_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Skip empty files or very small files
                        if len(content.strip()) > 10:
                            files_data.append({
                                "path": str(file_path),
                                "relative_path": str(file_path.relative_to(repo_path)),
                                "language": self.supported_extensions[ext],
                                "extension": ext,
                                "content": content,
                                "size": len(content)
                            })
                    except (UnicodeDecodeError, PermissionError):
                        # Skip binary files or files we can't read
                        pass
        
        return files_data
    
    def extract_file_by_path(self, repo_path, file_relative_path):
        """Extract a single file by its relative path"""
        full_path = Path(repo_path) / file_relative_path
        
        if full_path.exists() and full_path.is_file():
            ext = full_path.suffix
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return {
                    "path": str(full_path),
                    "relative_path": file_relative_path,
                    "language": self.supported_extensions.get(ext, "unknown"),
                    "extension": ext,
                    "content": content,
                    "size": len(content)
                }
            except:
                return None
        
        return None
    
    def get_file_structure(self, repo_path):
        """Get folder structure as tree"""
        structure = []
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden folders and venv
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv' and d != '__pycache__']
            
            level = root.replace(str(repo_path), '').count(os.sep)
            indent = '│   ' * level
            folder_name = os.path.basename(root)
            
            if level > 0:
                structure.append(f"{indent}├── 📁 {folder_name}/")
            
            sub_indent = '│   ' * (level + 1)
            for file in files:
                if not file.startswith('.'):
                    structure.append(f"{sub_indent}├── 📄 {file}")
        
        return '\n'.join(structure[:100])  # Limit to 100 lines