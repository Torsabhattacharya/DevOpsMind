import os
import re
from pathlib import Path
from github import Github, GithubException
import openai
from dotenv import load_dotenv

load_dotenv()

class CodeAnalyzer:
    """Analyzes repository code and finds issues"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.openai_key = os.getenv('OPENAI_API_KEY')
        
        if self.github_token:
            self.github = Github(self.github_token)
        
        if self.openai_key:
            openai.api_key = self.openai_key
    
    def analyze_repo(self, repo_url):
        """Main method to analyze a GitHub repository"""
        print(f"🔍 Analyzing repository: {repo_url}")
        
        # Extract repo name from URL
        repo_name = self._extract_repo_name(repo_url)
        
        # Get repository content
        try:
            repo = self.github.get_repo(repo_name)
            print(f"✅ Connected to repository: {repo.full_name}")
        except GithubException as e:
            return {"error": f"Failed to access repo: {e}"}
        
        # Find issues
        issues = {
            "missing_dockerfile": self._check_dockerfile(repo),
            "missing_requirements": self._check_requirements(repo),
            "no_tests": self._check_tests(repo),
            "code_smells": self._analyze_code_quality(repo)
        }
        
        print(f"📊 Analysis complete. Found issues: {issues}")
        return issues
    
    def _extract_repo_name(self, repo_url):
        """Extract owner/repo from GitHub URL"""
        # Handle formats like:
        # https://github.com/owner/repo
        # git@github.com:owner/repo.git
        match = re.search(r'github\.com[:/](.+?)(\.git)?$', repo_url)
        if match:
            return match.group(1)
        return repo_url
    
    def _check_dockerfile(self, repo):
        """Check if Dockerfile exists"""
        try:
            repo.get_contents("Dockerfile")
            return False  # Dockerfile exists, no issue
        except:
            return True   # Missing Dockerfile
    
    def _check_requirements(self, repo):
        """Check for requirements.txt or package.json"""
        try:
            repo.get_contents("requirements.txt")
            return False  # Python requirements exist
        except:
            try:
                repo.get_contents("package.json")
                return False  # Node.js package exists
            except:
                return True   # Missing dependency file
    
    def _check_tests(self, repo):
        """Check for test files"""
        try:
            contents = repo.get_contents("")
            for content in contents:
                if 'test' in content.name.lower() or content.name == 'tests':
                    return False  # Tests exist
            return True  # No tests found
        except:
            return True
    
    def _analyze_code_quality(self, repo):
        """Analyze code quality (basic checks)"""
        issues = []
        
        # Check for common issues
        try:
            readme = repo.get_readme()
            if not readme:
                issues.append("No README.md found")
        except:
            issues.append("No README.md found")
        
        # Check for .gitignore
        try:
            repo.get_contents(".gitignore")
        except:
            issues.append("Missing .gitignore")
        
        return issues