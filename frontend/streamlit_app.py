import streamlit as st
import sys
from pathlib import Path
import shutil
import os
from datetime import datetime
import subprocess
import time
import re
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(Path(__file__).parent.parent))

from app.llm.llm_engine import LLMEngine

st.set_page_config(
    page_title="DevOpsMind - AI Code Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with Professional UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0a0a0f, #050507);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0a0f 0%, #0d0d15 100%);
        border-right: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .sidebar-title {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff, #a78bfa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px;
        margin-bottom: 5px;
        padding-left: 20px;
    }
    
    .sidebar-badge {
        font-size: 10px;
        color: #8b5cf6;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 35px;
        padding-left: 20px;
    }
    
    .section-header {
        font-size: 11px;
        font-weight: 700;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin: 25px 0 12px 0;
        padding-left: 20px;
    }
    
    .repo-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 14px;
        margin: 0 15px 10px 15px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
    }
    
    .repo-card:hover {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.1);
        transform: translateX(5px);
    }
    
    .repo-card.active {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.15);
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);
    }
    
    .repo-name {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
    }
    
    .repo-stats {
        font-size: 10px;
        color: #6b7280;
    }
    
    .settings-card {
        background: rgba(30, 30, 45, 0.4);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 15px;
        margin: 0 15px 20px 15px;
    }
    
    /* Question Section in Sidebar */
    .questions-section {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(139, 92, 246, 0.03));
        border-radius: 12px;
        padding: 12px;
        margin: 15px;
        border: 1px solid rgba(139, 92, 246, 0.15);
    }
    
    .questions-title {
        font-size: 12px;
        font-weight: 600;
        color: #a78bfa;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .hero-section {
        text-align: center;
        padding: 80px 20px;
        max-width: 1000px;
        margin: 0 auto;
        animation: fadeInUp 0.8s ease-out;
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff, #c084fc, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        animation: gradientShift 3s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .hero-subtitle {
        color: #9ca3af;
        font-size: 18px;
        margin-bottom: 35px;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 28px;
        transition: all 0.4s ease;
        cursor: pointer;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        border-color: #8b5cf6;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.15);
    }
    
    .feature-icon { font-size: 36px; margin-bottom: 16px; }
    .feature-title { font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
    .feature-desc { font-size: 13px; color: #9ca3af; line-height: 1.5; }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #6d28d9);
        border: none;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        font-size: 13px;
        transition: all 0.3s ease;
        width: 100%;
        padding: 10px 12px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(139, 92, 246, 0.4);
    }
    
    [data-testid="stTextInput"] input {
        background: rgba(30, 30, 45, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 12px 16px;
        color: #ffffff;
        font-size: 14px;
    }
    
    [data-testid="stTextInput"] input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2);
        outline: none;
    }
    
    /* Professional Chat Messages */
    [data-testid="stChatMessage"] {
        background: linear-gradient(135deg, rgba(30, 30, 45, 0.6), rgba(30, 30, 45, 0.4));
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 20px;
        padding: 16px;
        margin: 12px 0;
        animation: slideInMessage 0.4s ease-out;
        font-size: 13px !important;
        line-height: 1.5 !important;
    }
    
    [data-testid="stChatMessage"]:hover {
        border-color: rgba(139, 92, 246, 0.4);
    }
    
    [data-testid="stChatMessage"] p {
        font-size: 13px !important;
        line-height: 1.5 !important;
    }
    
    [data-testid="stChatMessage"] pre {
        font-size: 11px !important;
        margin: 8px 0 !important;
    }
    
    [data-testid="stChatMessage"] code {
        font-size: 11px !important;
    }
    
    @keyframes slideInMessage {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Project Title */
    .project-title {
        background: linear-gradient(135deg, #a78bfa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 25px;
        letter-spacing: -0.5px;
    }
    
    /* Action Cards */
    .action-card {
        background: linear-gradient(135deg, rgba(30, 30, 45, 0.6), rgba(30, 30, 45, 0.4));
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .action-card:hover {
        transform: translateY(-5px);
        border-color: #8b5cf6;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.2);
    }
    
    .action-icon {
        font-size: 42px;
        margin-bottom: 12px;
    }
    
    .action-title {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
    }
    
    .action-desc {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 16px;
    }
    
    .action-btn {
        margin-top: 8px;
    }
    
    hr { border-color: rgba(139, 92, 246, 0.1); margin: 25px 0; }
    
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #1a1a2a; }
    ::-webkit-scrollbar-thumb { background: #8b5cf6; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repositories" not in st.session_state:
    st.session_state.repositories = {}
if "current_repo" not in st.session_state:
    st.session_state.current_repo = None
if "agentic_mode" not in st.session_state:
    st.session_state.agentic_mode = True
if "repo_contents" not in st.session_state:
    st.session_state.repo_contents = {}
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True
if "suggested_questions" not in st.session_state:
    st.session_state.suggested_questions = []

def delete_repo_folder(path):
    try:
        if os.path.exists(path):
            if os.name == 'nt':
                for root, dirs, files in os.walk(path):
                    for file in files:
                        try:
                            os.chmod(os.path.join(root, file), 0o666)
                        except:
                            pass
            shutil.rmtree(path)
        return True
    except:
        try:
            shutil.rmtree(path, ignore_errors=True)
        except:
            pass
        return False

def simple_ingest(repo_url):
    try:
        repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        repo_path = Path("repos") / repo_name
        
        if repo_path.exists():
            try:
                shutil.rmtree(repo_path)
            except:
                time.sleep(1)
                shutil.rmtree(repo_path, ignore_errors=True)
        
        repo_path.parent.mkdir(exist_ok=True)
        
        with st.spinner(f"Cloning {repo_name}..."):
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(repo_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                st.error(f"Git error: {result.stderr}")
                return False
        
        file_contents = {}
        file_count = 0
        code_count = 0
        found_files = []
        
        for file in repo_path.rglob("*"):
            if file.is_file():
                file_count += 1
                if file.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.html', '.css', '.json', '.md', '.txt']:
                    try:
                        content = file.read_text(encoding='utf-8', errors='ignore')
                        if len(content.strip()) > 30:
                            rel_path = str(file.relative_to(repo_path))
                            if len(content) < 10000:
                                file_contents[rel_path] = content
                            else:
                                file_contents[rel_path] = content[:8000]
                            code_count += 1
                            found_files.append(rel_path)
                    except:
                        pass
        
        if found_files:
            st.info(f"Found: {', '.join(found_files[:3])}...")
        
        st.session_state.suggested_questions = [
            f"What is the overall architecture of {repo_name}?",
            f"How does {repo_name} work?",
            f"What are the main entry points of {repo_name}?",
            f"Explain the folder structure of {repo_name}"
        ]
        
        st.session_state.repositories[repo_name] = {
            "name": repo_name, "url": repo_url, "path": str(repo_path),
            "chunks": max(code_count, 10), "files": file_count, "code_files": code_count,
            "indexed_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        st.session_state.repo_contents = file_contents
        st.session_state.current_repo = repo_name
        st.session_state.messages = []
        st.session_state.show_suggestions = True
        
        st.success(f"{repo_name}: {code_count} files indexed")
        return True
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def remove_emojis(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def search_code(query, repo_contents):
    results = []
    q = query.lower()
    
    arch_keywords = ['main', 'app', 'dashboard', 'class', 'def', 'import', 'from', 'api', 'route', 'server']
    
    for file_path, content in repo_contents.items():
        content_lower = content.lower()
        
        is_relevant = False
        
        if q in content_lower:
            is_relevant = True
        
        if 'architecture' in q or 'structure' in q:
            if any(kw in content_lower for kw in arch_keywords):
                is_relevant = True
        
        if is_relevant:
            lines = content.split('\n')
            relevant_lines = []
            
            for i, line in enumerate(lines):
                if q in line.lower() or ('architecture' in q and any(kw in line.lower() for kw in arch_keywords)):
                    start = max(0, i-3)
                    end = min(len(lines), i+4)
                    for j in range(start, end):
                        if lines[j].strip() and lines[j] not in relevant_lines:
                            relevant_lines.append(f"Line {j+1}: {lines[j]}")
            
            if relevant_lines:
                results.append({
                    "file": file_path,
                    "snippet": '\n'.join(relevant_lines[:20])
                })
    
    return results[:5]

def generate_readme(repo_name, repo_contents, repo_data):
    context = f"Repository: {repo_name}\n"
    context += f"Total Files: {repo_data.get('files', 0)}\n"
    context += f"Code Files: {repo_data.get('code_files', 0)}\n\n"
    
    context += "Main files in repository:\n"
    for file_path in list(repo_contents.keys())[:20]:
        context += f"- {file_path}\n"
    
    prompt = f"""Generate a professional README.md documentation for the repository '{repo_name}'.

Based on the following file structure:

{context}

Create a complete README.md with:
1. Project Title and Description
2. Features
3. Installation Instructions
4. Usage Guide
5. Project Structure
6. Technologies Used
7. Contributing Guidelines
8. License

Make it professional and well-formatted."""
    
    try:
        llm = LLMEngine()
        readme = llm.generate_response(prompt, context)
        readme = remove_emojis(readme)
        return readme
    except Exception as e:
        return f"# {repo_name}\n\n## Overview\n\nThis repository contains code for {repo_name}.\n\n## Files\n\n" + "\n".join([f"- {f}" for f in list(repo_contents.keys())[:15]])

def ask_question(question, repo_name, repo_data, repo_contents):
    search_results = search_code(question, repo_contents)
    
    context = f"Repository: {repo_name}\n"
    context += f"Total Files: {repo_data.get('files', 0)}\n"
    context += f"Code Files: {repo_data.get('code_files', 0)}\n\n"
    
    if search_results:
        context += "RELEVANT CODE FOUND\n\n"
        for r in search_results:
            context += f"File: {r['file']}\n"
            context += "```python\n"
            context += r['snippet'][:2000]
            context += "\n```\n\n"
    else:
        context += "ALL CODE FILES IN REPOSITORY\n\n"
        for file_path in list(repo_contents.keys())[:15]:
            context += f"- {file_path}\n"
        context += "\n"
    
    try:
        llm = LLMEngine()
        response = llm.generate_response(question, context)
        response = remove_emojis(response)
        return response
    except Exception as e:
        return f"DevOpsMind AI Assistant\n\nRepository: {repo_name}\n\nFiles Found: {len(repo_contents)} code files\n\nAnalysis for: {question}\n\nThe repository has been successfully indexed and is ready for detailed code analysis."

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title">DevOpsMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-badge">AI · CODE INTELLIGENCE</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">ADD REPOSITORY</div>', unsafe_allow_html=True)
    repo_url = st.text_input("", placeholder="https://github.com/user/repo", label_visibility="collapsed", key="repo_input")
    
    if st.button("Ingest Repo", use_container_width=True):
        if repo_url:
            if simple_ingest(repo_url):
                st.rerun()
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">INDEXED REPOSITORIES</div>', unsafe_allow_html=True)
    
    if st.session_state.repositories:
        for repo_name, repo_data in st.session_state.repositories.items():
            is_active = st.session_state.current_repo == repo_name
            st.markdown(f"""
            <div class="repo-card {'active' if is_active else ''}">
                <div class="repo-name">{repo_name}</div>
                <div class="repo-stats">{repo_data['chunks']} chunks indexed</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_active:
                if st.button(f"Select", key=f"select_{repo_name}", use_container_width=True):
                    st.session_state.current_repo = repo_name
                    st.session_state.messages = []
                    st.session_state.show_suggestions = True
                    st.rerun()
    else:
        st.caption("No repositories indexed yet")
    
    st.markdown("---")
    
    st.markdown('<div class="section-header">SETTINGS</div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<span style="color:#e0e0e0; font-size:13px;">Agentic Mode</span>', unsafe_allow_html=True)
    with col2:
        agentic_toggle = st.toggle("", value=st.session_state.agentic_mode, key="agentic_toggle")
        st.session_state.agentic_mode = agentic_toggle
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Suggested Questions Section in Sidebar
    if st.session_state.current_repo and st.session_state.suggested_questions:
        st.markdown("---")
        st.markdown('<div class="questions-section">', unsafe_allow_html=True)
        st.markdown('<div class="questions-title">SUGGESTED QUESTIONS</div>', unsafe_allow_html=True)
        
        for i, q in enumerate(st.session_state.suggested_questions):
            if st.button(f"{q}", key=f"sidebar_q_{i}", use_container_width=True):
                st.session_state.show_suggestions = False
                st.session_state.messages.append({"role": "user", "content": q})
                with st.chat_message("user"):
                    st.markdown(q)
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing codebase..."):
                        response = ask_question(q, st.session_state.current_repo, st.session_state.repositories[st.session_state.current_repo], st.session_state.repo_contents)
                        st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main content
if not st.session_state.current_repo:
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Chat with any codebase</div>
        <div class="hero-subtitle">Your AI-powered code intelligence platform</div>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🏗️</div>
                <div class="feature-title">Understand project architecture</div>
                <div class="feature-desc">Visualize folder structure, dependencies, and entry points</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Semantic code search</div>
                <div class="feature-desc">Find code by meaning, not just keywords</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🐛</div>
                <div class="feature-title">AI bug detection</div>
                <div class="feature-desc">LLM-powered static analysis for vulnerabilities</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📘</div>
                <div class="feature-title">Generate documentation</div>
                <div class="feature-desc">Auto-generate README, API docs, and comments</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    repo_name = st.session_state.current_repo
    repo_data = st.session_state.repositories[repo_name]
    repo_contents = st.session_state.repo_contents
    
    # Project Title
    st.markdown(f'<div class="project-title">{repo_name}</div>', unsafe_allow_html=True)
    
    # Quick Actions Section
    st.markdown("### Quick Actions")
    
    # Row 1 - Two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">🏗️</div>
            <div class="action-title">Architecture</div>
            <div class="action-desc">Understand project structure and components</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Architecture", key="arch_btn", use_container_width=True):
            q = f"What is the overall architecture of {repo_name}? Explain the folder structure and main components."
            st.session_state.show_suggestions = False
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"):
                st.markdown(q)
            with st.chat_message("assistant"):
                with st.spinner("Analyzing architecture..."):
                    response = ask_question(q, repo_name, repo_data, repo_contents)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">🔍</div>
            <div class="action-title">Code Search</div>
            <div class="action-desc">Find specific functionality in codebase</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Search Codebase", key="search_btn", use_container_width=True):
            q = f"Find the main entry points and key functionality in {repo_name}. What are the important files and what do they do?"
            st.session_state.show_suggestions = False
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"):
                st.markdown(q)
            with st.chat_message("assistant"):
                with st.spinner("Searching codebase..."):
                    response = ask_question(q, repo_name, repo_data, repo_contents)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # Row 2 - Two columns
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">🐛</div>
            <div class="action-title">Bug Detection</div>
            <div class="action-desc">Find security issues and vulnerabilities</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Scan for Bugs", key="bug_btn", use_container_width=True):
            q = f"Analyze {repo_name} for potential bugs, security vulnerabilities, and code quality issues. List any problems found."
            st.session_state.show_suggestions = False
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"):
                st.markdown(q)
            with st.chat_message("assistant"):
                with st.spinner("Scanning for bugs..."):
                    response = ask_question(q, repo_name, repo_data, repo_contents)
                    st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        st.markdown("""
        <div class="action-card">
            <div class="action-icon">📘</div>
            <div class="action-title">Documentation</div>
            <div class="action-desc">Generate README and API docs</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Generate Docs", key="docs_btn", use_container_width=True):
            with st.spinner("Generating documentation..."):
                readme_content = generate_readme(repo_name, repo_contents, repo_data)
                
                st.session_state.show_suggestions = False
                st.session_state.messages.append({"role": "user", "content": "Generate comprehensive documentation for this repository"})
                with st.chat_message("user"):
                    st.markdown("Generate comprehensive documentation for this repository")
                with st.chat_message("assistant"):
                    st.markdown("## Generated Documentation\n\n" + readme_content)
                    
                    st.download_button(
                        label="Download README.md",
                        data=readme_content,
                        file_name=f"{repo_name}_README.md",
                        mime="text/markdown",
                        key="download_readme"
                    )
                
                st.session_state.messages.append({"role": "assistant", "content": "## Generated Documentation\n\n" + readme_content})
                st.rerun()
    
    st.markdown("---")
    
    # Suggested Questions
    if st.session_state.show_suggestions and len(st.session_state.messages) == 0:
        st.markdown("### Suggested Questions")
        
        for i, q in enumerate(st.session_state.suggested_questions):
            if st.button(f"{q}", use_container_width=True, key=f"main_q_{i}"):
                st.session_state.show_suggestions = False
                st.session_state.messages.append({"role": "user", "content": q})
                with st.chat_message("user"):
                    st.markdown(q)
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing codebase..."):
                        response = ask_question(q, repo_name, repo_data, repo_contents)
                        st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input(f"Ask anything about {repo_name}..."):
        st.session_state.show_suggestions = False
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing codebase..."):
                response = ask_question(prompt, repo_name, repo_data, repo_contents)
                st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()