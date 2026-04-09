import os
from pathlib import Path
import openai
from dotenv import load_dotenv
import re

load_dotenv()

class DevOpsAgent:
    """Creates Dockerfile and CI/CD pipeline configuration"""
    
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if self.openai_key:
            openai.api_key = self.openai_key
        self.project_type = "unknown"
        self.language = "unknown"
    
    def generate_dockerfile(self, repo_url, code_analysis):
        """Generate Dockerfile based on project type"""
        print("🐳 Generating Dockerfile...")
        
        # Detect project type from analysis
        self._detect_project_type(repo_url, code_analysis)
        
        # Generate Dockerfile based on language
        if self.language == "python":
            dockerfile = self._generate_python_dockerfile()
        elif self.language == "node":
            dockerfile = self._generate_node_dockerfile()
        else:
            # Generic Dockerfile using AI if available
            dockerfile = self._generate_generic_dockerfile()
        
        return {
            "filename": "Dockerfile",
            "content": dockerfile,
            "message": f"Generated Dockerfile for {self.language} project"
        }
    
    def _detect_project_type(self, repo_url, code_analysis):
        """Detect language and framework"""
        # Simple detection based on common files
        repo_lower = repo_url.lower()
        
        if "python" in repo_lower or "django" in repo_lower or "flask" in repo_lower:
            self.language = "python"
            self.project_type = "python"
        elif "node" in repo_lower or "javascript" in repo_lower or "react" in repo_lower:
            self.language = "node"
            self.project_type = "node"
        else:
            # Default to Python
            self.language = "python"
            self.project_type = "python"
    
    def _generate_python_dockerfile(self):
        """Generate Dockerfile for Python projects"""
        return '''# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (common for Flask/FastAPI)
EXPOSE 8000

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]'''
    
    def _generate_node_dockerfile(self):
        """Generate Dockerfile for Node.js projects"""
        return '''# Use Node.js 20 slim image
FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]'''
    
    def _generate_generic_dockerfile(self):
        """Generate generic Dockerfile"""
        return '''# Generic Dockerfile
FROM alpine:latest

WORKDIR /app

# Copy application files
COPY . .

# Install basic dependencies
RUN apk add --no-cache bash

# Default command
CMD ["echo", "Application ready"]'''
    
    def generate_ci_cd_config(self, repo_url, test_results):
        """Generate GitHub Actions CI/CD workflow"""
        print("⚙️ Generating CI/CD configuration...")
        
        if self.language == "python":
            workflow = self._generate_python_workflow()
        elif self.language == "node":
            workflow = self._generate_node_workflow()
        else:
            workflow = self._generate_generic_workflow()
        
        return {
            "filename": ".github/workflows/ci-cd.yml",
            "content": workflow,
            "message": "Generated GitHub Actions workflow"
        }
    
    def _generate_python_workflow(self):
        """Generate GitHub Actions workflow for Python"""
        return '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest'''
    
    def _generate_node_workflow(self):
        """Generate GitHub Actions workflow for Node.js"""
        return '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: npm test
    
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest'''
    
    def _generate_generic_workflow(self):
        """Generate generic GitHub Actions workflow"""
        return '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build
      run: |
        echo "Building application..."
        # Add your build commands here'''