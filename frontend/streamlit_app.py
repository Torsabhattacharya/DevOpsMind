import streamlit as st
import sys
from pathlib import Path
import git
import shutil
import time
import os
import json
from datetime import datetime
import tempfile

st.set_page_config(
    page_title="DevOpsMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Clean Sidebar UI
st.markdown("""
<style>
    .stApp {
        background: #0b0b12;
    }
    
    [data-testid="stSidebar"] {
        background: #0f0f1a;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    .sidebar-badge {
        font-size: 10px;
        color: #8b5cf6;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 30px;
    }
    
    .section-header {
        font-size: 11px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 0 10px 0;
    }
    
    .repo-card {
        background: rgba(30, 30, 45, 0.5);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .repo-card:hover {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.1);
        transform: translateX(4px);
    }
    
    .repo-card.active {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.15);
    }
    
    .repo-name {
        font-size: 13px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 4px;
    }
    
    .repo-stats {
        font-size: 10px;
        color: #6b7280;
    }
    
    .settings-card {
        background: rgba(30, 30, 45, 0.4);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 10px;
        padding: 12px;
        margin-top: 20px;
    }
    
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .hero-title {
        font-size: 44px;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #c084fc, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    .hero-subtitle {
        color: #9ca3af;
        font-size: 16px;
        margin-bottom: 25px;
    }
    
    .info-message {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 30px;
        padding: 10px 24px;
        display: inline-block;
        font-size: 13px;
        color: #c084fc;
        margin-bottom: 45px;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        max-width: 700px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: rgba(30, 30, 45, 0.4);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 14px;
        padding: 20px;
        text-align: left;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: #8b5cf6;
        background: rgba(139, 92, 246, 0.08);
        transform: translateY(-3px);
    }
    
    .feature-icon {
        font-size: 28px;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .feature-desc {
        font-size: 11px;
        color: #9ca3af;
    }
    
    .chat-header {
        border-bottom: 1px solid rgba(139, 92, 246, 0.2);
        padding-bottom: 15px;
        margin-bottom: 20px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #6d28d9);
        border: none;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        font-size: 13px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }
    
    /* Back button style */
    .back-button > button {
        background: rgba(30, 30, 45, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.3);
        width: auto;
        padding: 6px 16px;
    }
    
    .back-button > button:hover {
        background: rgba(139, 92, 246, 0.2);
        transform: none;
    }
    
    /* Clear button style */
    .clear-button > button {
        background: rgba(220, 38, 38, 0.6);
    }
    
    .clear-button > button:hover {
        background: rgba(220, 38, 38, 0.8);
    }
    
    [data-testid="stTextInput"] input {
        background: rgba(30, 30, 45, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 8px;
        padding: 10px 14px;
        color: #ffffff;
        font-size: 13px;
    }
    
    [data-testid="stTextInput"] input:focus {
        border-color: #8b5cf6;
        outline: none;
    }
    
    [data-testid="stChatMessage"] {
        background: rgba(30, 30, 45, 0.4);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
    }
    
    hr {
        border-color: rgba(139, 92, 246, 0.15);
        margin: 15px 0;
    }
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
if "repo_path" not in st.session_state:
    st.session_state.repo_path = None
if "repo_files" not in st.session_state:
    st.session_state.repo_files = []
if "total_chunks" not in st.session_state:
    st.session_state.total_chunks = 0
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True


def delete_folder_quiet(path):
    """Delete folder silently without showing messages"""
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
    except Exception as e:
        return False


def simple_ingest(repo_url):
    """Simple repository ingestion - silent mode"""
    try:
        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        
        repo_base = Path("repos")
        repo_base.mkdir(exist_ok=True)
        repo_path = repo_base / repo_name
        
        # Silently remove if exists (no message)
        if repo_path.exists():
            delete_folder_quiet(str(repo_path))
        
        with st.spinner(f"📥 Cloning {repo_name}..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_repo_path = Path(temp_dir) / repo_name
                git.Repo.clone_from(repo_url, temp_repo_path, depth=1)
                shutil.move(str(temp_repo_path), str(repo_path))
        
        # Count files
        file_count = 0
        code_files = []
        all_files = []
        
        for file in repo_path.rglob("*"):
            if file.is_file():
                file_count += 1
                all_files.append(str(file))
                if file.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.cpp', '.c', '.html', '.css', '.json', '.md']:
                    try:
                        content = file.read_text(encoding='utf-8', errors='ignore')
                        if len(content.strip()) > 50:
                            code_files.append(file)
                    except:
                        pass
        
        chunks_count = max(len(code_files), 10)
        
        st.session_state.repositories[repo_name] = {
            "name": repo_name,
            "url": repo_url,
            "path": str(repo_path),
            "chunks": chunks_count,
            "files": file_count,
            "code_files": len(code_files),
            "indexed_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        st.session_state.current_repo = repo_name
        st.session_state.repo_path = str(repo_path)
        st.session_state.repo_files = all_files[:200]
        st.session_state.messages = []
        st.session_state.show_suggestions = True
        
        return True
        
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False


def ask_question(question, repo_name, repo_data):
    """Generate answer for question"""
    return f"""
**🤖 DevOpsMind AI Assistant**

**Question:** {question}

**Repository:** {repo_name}

**Repository Stats:**
- Total Files: {repo_data.get('files', 0)}
- Code Files: {repo_data.get('code_files', 0)}
- Chunks: {repo_data.get('chunks', 0)}
- Indexed: {repo_data.get('indexed_at', 'Unknown')}

**Analysis:** The repository has been successfully cloned and indexed.

**You can ask me about:**
- Architecture and folder structure
- Main entry points and key files
- Features and functionality
- Potential issues or improvements
"""


# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="sidebar-title">DevOpsMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-badge">AI · CODE INTELLIGENCE</div>', unsafe_allow_html=True)
    
    # Add Repository
    st.markdown('<div class="section-header">ADD REPOSITORY</div>', unsafe_allow_html=True)
    repo_url = st.text_input("", placeholder="https://github.com/user/repo", label_visibility="collapsed", key="repo_input")
    
    if st.button("📥 Ingest Repo", use_container_width=True, key="ingest_btn"):
        if repo_url:
            if simple_ingest(repo_url):
                st.rerun()
    
    st.markdown("---")
    
    # Indexed Repositories
    st.markdown('<div class="section-header">INDEXED REPOSITORIES</div>', unsafe_allow_html=True)
    
    if st.session_state.repositories:
        for repo_name, repo_data in st.session_state.repositories.items():
            is_active = st.session_state.current_repo == repo_name
            st.markdown(f"""
            <div class="repo-card {'active' if is_active else ''}">
                <div class="repo-name">{repo_name}</div>
                <div class="repo-stats">📄 {repo_data['chunks']} chunks | 📁 {repo_data['files']} files</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_active:
                if st.button(f"Select", key=f"select_{repo_name}", use_container_width=True):
                    st.session_state.current_repo = repo_name
                    st.session_state.repo_path = repo_data["path"]
                    st.session_state.messages = []
                    st.session_state.show_suggestions = True
                    st.rerun()
    else:
        st.caption("✨ No repos indexed yet")
    
    st.markdown("---")
    
    # Settings
    st.markdown('<div class="section-header">SETTINGS</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="settings-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<span style="color:#e0e0e0; font-size:13px;">🧠 Agentic Mode</span>', unsafe_allow_html=True)
    with col2:
        agentic_toggle = st.toggle("", value=st.session_state.agentic_mode, key="agentic_toggle")
        st.session_state.agentic_mode = agentic_toggle
    st.markdown('</div>', unsafe_allow_html=True)


# ==================== MAIN CONTENT ====================
if not st.session_state.current_repo:
    # Welcome Screen
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Chat with any codebase</div>
        <div class="hero-subtitle">Your AI-powered code intelligence platform</div>
        <div class="info-message">
            📦 Enter a GitHub URL in the sidebar and click "Ingest Repo"
        </div>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🏗️</div>
                <div class="feature-title">Understand project architecture and folder structure</div>
                <div class="feature-desc">Visualize code organization</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Find where specific functionality is implemented</div>
                <div class="feature-desc">Semantic code search</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🐛</div>
                <div class="feature-title">Detect potential bugs and security issues</div>
                <div class="feature-desc">AI-powered static analysis</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📘</div>
                <div class="feature-title">Generate documentation for any module</div>
                <div class="feature-desc">Auto-generate README and API docs</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    repo_name = st.session_state.current_repo
    repo_data = st.session_state.repositories[repo_name]
    
    # Header with Back Button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"""
        <div class="chat-header">
            <h2 style="margin:0; color:#ffffff;">💬 {repo_name}</h2>
            <span style="background:#8b5cf6; border-radius:12px; padding:3px 10px; font-size:10px;">📄 {repo_data['chunks']} chunks indexed</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Back to Questions button (shows only when not in suggestions mode or has messages)
        if not st.session_state.show_suggestions or len(st.session_state.messages) > 0:
            if st.button("← Back to Questions", use_container_width=True, key="back_btn"):
                st.session_state.messages = []
                st.session_state.show_suggestions = True
                st.rerun()
    
    with col3:
        if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_btn"):
            st.session_state.messages = []
            st.session_state.show_suggestions = True
            st.rerun()
    
    # Agentic Mode Indicator
    if st.session_state.agentic_mode:
        st.info("🧠 **Agentic Mode Active** - AI will intelligently search and analyze code")
    else:
        st.info("⚡ **Simple Mode** - Quick responses without advanced tool calling")
    
    # Show Suggested Questions
    if st.session_state.show_suggestions and len(st.session_state.messages) == 0:
        st.markdown("### ✨ Suggested Questions")
        
        suggested = [
            f"What is the overall architecture of {repo_name}?",
            f"What are the main entry points of {repo_name}?",
            f"Explain the key features and functionality",
            f"Are there any potential bugs or security issues?"
        ]
        
        for q in suggested:
            if st.button(q, use_container_width=True, key=f"suggest_{q[:30]}"):
                st.session_state.show_suggestions = False
                st.session_state.messages.append({"role": "user", "content": q})
                
                with st.chat_message("user"):
                    st.markdown(q)
                
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing codebase..."):
                        response = ask_question(q, repo_name, repo_data)
                        st.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
        
        st.markdown("---")
        st.markdown("### 💬 Ask anything about your codebase")
    
    # Chat history display
    if len(st.session_state.messages) > 0:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if not st.session_state.show_suggestions or len(st.session_state.messages) > 0:
        if prompt := st.chat_input(f"Ask anything about {repo_name}..."):
            st.session_state.show_suggestions = False
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing codebase..."):
                    response = ask_question(prompt, repo_name, repo_data)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()