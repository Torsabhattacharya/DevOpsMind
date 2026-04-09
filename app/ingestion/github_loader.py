import os
import git
import shutil
from pathlib import Path
from app.config import Config

class GitHubLoader:
    """Clone and manage GitHub repositories"""
    
    def __init__(self):
        self.clone_dir = Path(Config.CLONE_DIR)
        self.clone_dir.mkdir(exist_ok=True)
    
    def clone_repository(self, repo_url):
        """Clone a GitHub repository"""
        try:
            # Extract repo name from URL
            repo_name = repo_url.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            
            repo_path = self.clone_dir / repo_name
            
            # Remove if already exists
            if repo_path.exists():
                shutil.rmtree(repo_path)
            
            print(f"📦 Cloning {repo_name}...")
            repo = git.Repo.clone_from(repo_url, repo_path)
            
            return {
                "success": True,
                "repo_name": repo_name,
                "repo_path": str(repo_path),
                "branch": repo.active_branch.name
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def delete_repository(self, repo_path):
        """Delete cloned repository"""
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            return True
        return False
    
    def get_repo_info(self, repo_path):
        """Get repository information"""
        repo_path = Path(repo_path)
        
        # Count files by language
        files_by_lang = {}
        total_files = 0
        total_size = 0
        
        for file_path in repo_path.rglob("*"):
            if file_path.is_file():
                total_files += 1
                total_size += file_path.stat().st_size
                ext = file_path.suffix
                if ext in Config.SUPPORTED_EXTENSIONS:
                    lang = Config.SUPPORTED_EXTENSIONS[ext]
                    files_by_lang[lang] = files_by_lang.get(lang, 0) + 1
        
        return {
            "total_files": total_files,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "languages": files_by_lang
        }