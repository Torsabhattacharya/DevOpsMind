import subprocess
import os
import tempfile
from pathlib import Path
import requests
import re

class TestAgent:
    """Runs tests on the repository"""
    
    def __init__(self):
        self.test_results = {}
    
    def run_tests(self, repo_url):
        """Clone and run tests on the repository"""
        print(f"🧪 Running tests on: {repo_url}")
        
        # Create temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"📁 Cloning to: {temp_dir}")
            
            # Clone the repository
            try:
                repo_path = self._clone_repo(repo_url, temp_dir)
            except Exception as e:
                return {"error": f"Failed to clone: {e}"}
            
            # Detect project type and run appropriate tests
            project_type = self._detect_project_type(repo_path)
            print(f"📋 Detected project type: {project_type}")
            
            if project_type == "python":
                results = self._run_python_tests(repo_path)
            elif project_type == "node":
                results = self._run_node_tests(repo_path)
            else:
                results = {"status": "unknown", "message": "Could not detect project type"}
            
            self.test_results = results
            return results
    
    def _clone_repo(self, repo_url, target_dir):
        """Clone repository using git"""
        # Convert GitHub URL to git clone URL
        if repo_url.startswith("https://"):
            # For public repos, use HTTPS
            cmd = f"git clone {repo_url} {target_dir}/repo"
        else:
            # For SSH or other formats
            cmd = f"git clone {repo_url} {target_dir}/repo"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"Git clone failed: {result.stderr}")
        
        return f"{target_dir}/repo"
    
    def _detect_project_type(self, repo_path):
        """Detect if it's Python or Node.js project"""
        repo_path = Path(repo_path)
        
        # Check for Python files
        if (repo_path / "requirements.txt").exists() or \
           (repo_path / "setup.py").exists() or \
           (repo_path / "pyproject.toml").exists():
            return "python"
        
        # Check for Node.js files
        if (repo_path / "package.json").exists():
            return "node"
        
        return "unknown"
    
    def _run_python_tests(self, repo_path):
        """Run Python tests using pytest"""
        print("🐍 Running Python tests...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "details": []
        }
        
        # Check if pytest is available
        try:
            # Install dependencies
            subprocess.run(f"pip install -r {repo_path}/requirements.txt", 
                          shell=True, capture_output=True, timeout=60)
            
            # Run pytest
            result = subprocess.run(f"cd {repo_path} && python -m pytest --tb=short",
                                   shell=True, capture_output=True, text=True, timeout=60)
            
            # Parse results
            output = result.stdout + result.stderr
            
            # Simple parsing of pytest output
            if "passed" in output.lower() and "failed" in output.lower():
                # Extract numbers
                import re
                passed_match = re.search(r'(\d+) passed', output)
                failed_match = re.search(r'(\d+) failed', output)
                
                results["passed"] = int(passed_match.group(1)) if passed_match else 0
                results["failed"] = int(failed_match.group(1)) if failed_match else 0
                results["total"] = results["passed"] + results["failed"]
                
            elif result.returncode == 0:
                results["passed"] = 1
                results["total"] = 1
            
            results["details"] = output[-500:]  # Last 500 chars
            
        except subprocess.TimeoutExpired:
            results["error"] = "Tests timed out"
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def _run_node_tests(self, repo_path):
        """Run Node.js tests using npm"""
        print("📦 Running Node.js tests...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "details": []
        }
        
        try:
            # Install dependencies
            subprocess.run(f"cd {repo_path} && npm install",
                          shell=True, capture_output=True, timeout=120)
            
            # Run npm test
            result = subprocess.run(f"cd {repo_path} && npm test -- --watchAll=false",
                                   shell=True, capture_output=True, text=True, timeout=120)
            
            # Simple success/failure check
            if result.returncode == 0:
                results["passed"] = 1
                results["total"] = 1
            else:
                results["failed"] = 1
                results["total"] = 1
            
            results["details"] = result.stdout[-500:] + result.stderr[-500:]
            
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def get_summary(self):
        """Get test summary"""
        return {
            "status": "✅ All tests passed" if self.test_results.get("failed", 0) == 0 else "❌ Some tests failed",
            "passed": self.test_results.get("passed", 0),
            "failed": self.test_results.get("failed", 0),
            "total": self.test_results.get("total", 0)
        }