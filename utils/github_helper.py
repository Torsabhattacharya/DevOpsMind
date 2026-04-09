import os
import re
from github import Github, GithubException
from dotenv import load_dotenv

load_dotenv()

class GitHubHelper:
    """Helper class for GitHub operations"""
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        if self.token:
            self.github = Github(self.token)
        else:
            self.github = Github()  # Unauthenticated (rate limited)
    
    def get_repo_info(self, repo_url):
        """Get repository information"""
        repo_name = self._extract_repo_name(repo_url)
        
        try:
            repo = self.github.get_repo(repo_name)
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "default_branch": repo.default_branch,
                "is_private": repo.private
            }
        except GithubException as e:
            return {"error": f"Failed to get repo: {e}"}
    
    def _extract_repo_name(self, repo_url):
        """Extract owner/repo from GitHub URL"""
        # Handle different GitHub URL formats
        patterns = [
            r'github\.com[:/]([^/]+/[^/\.]+)',
            r'github\.com/([^/]+/[^/]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, repo_url)
            if match:
                return match.group(1)
        
        return repo_url
    
    def create_commit(self, repo_url, file_path, content, commit_message):
        """Create a new file in the repository"""
        repo_name = self._extract_repo_name(repo_url)
        
        try:
            repo = self.github.get_repo(repo_name)
            
            # Check if file already exists
            try:
                existing_file = repo.get_contents(file_path)
                repo.update_file(
                    file_path,
                    commit_message,
                    content,
                    existing_file.sha
                )
                return {"status": "updated", "path": file_path}
            except:
                repo.create_file(
                    file_path,
                    commit_message,
                    content
                )
                return {"status": "created", "path": file_path}
                
        except GithubException as e:
            return {"error": str(e)}
    
    def get_file_content(self, repo_url, file_path):
        """Get content of a file from repository"""
        repo_name = self._extract_repo_name(repo_url)
        
        try:
            repo = self.github.get_repo(repo_name)
            file_content = repo.get_contents(file_path)
            return file_content.decoded_content.decode('utf-8')
        except:
            return None