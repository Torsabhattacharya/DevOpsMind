import streamlit as st
from datetime import datetime

st.set_page_config(page_title="DevOpsMind", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: #0b0b12;
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Gradient Title */
.gradient-text {
    font-size: 48px;
    font-weight: 700;
    background: linear-gradient(90deg,#6c63ff,#00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: #151522;
    padding: 25px;
    border-radius: 16px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.05);
    height: 120px;
    display: flex;
    align-items: center;
    font-size: 16px;
}
.card:hover {
    transform: translateY(-6px);
    border: 1px solid #6c63ff;
    box-shadow: 0px 10px 30px rgba(108,99,255,0.2);
}

/* Repo Card */
.repo-card {
    background: #151522;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Button */
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background: linear-gradient(135deg,#6c63ff,#8f44fd);
    color: white;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "repos" not in st.session_state:
    st.session_state.repos = {}
if "current_repo" not in st.session_state:
    st.session_state.current_repo = None

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🧠 DevOpsMind")
    st.caption("AI · CODE INTELLIGENCE")

    st.divider()

    repo_url = st.text_input("Add Repository", placeholder="https://github.com/user/repo")

    if st.button("⚡ Ingest Repo"):
        if repo_url:
            repo_name = repo_url.split("/")[-1]

            st.session_state.repos[repo_name] = {
                "url": repo_url,
                "time": datetime.now().strftime("%H:%M"),
                "chunks": 50
            }

            st.success("Repo added!")
            st.rerun()

    st.divider()
    st.markdown("### Indexed Repositories")

    for repo in st.session_state.repos:
        st.markdown(f"""
        <div class="repo-card">
        📦 <b>{repo}</b><br>
        <small>{st.session_state.repos[repo]['chunks']} chunks indexed</small>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Select {repo}"):
            st.session_state.current_repo = repo
            st.rerun()

# ---------------- MAIN ----------------
if not st.session_state.current_repo:

    # Center Title
    st.markdown("<div class='gradient-text'>🧠 Chat with any codebase</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Select or ingest a repository to get started</div>", unsafe_allow_html=True)

    st.markdown("")

    # Cards grid
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
        🧩 Understand project architecture and folder structure
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        🐞 Detect potential bugs and security issues
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        🔍 Find where specific functionality is implemented
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        📘 Generate documentation for any module
        </div>
        """, unsafe_allow_html=True)

else:
    repo = st.session_state.current_repo

    st.markdown(f"## 💬 Chatting with: {repo}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about your repo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        response = f"🤖 DevOpsMind analyzing **{repo}**..."

        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()