import streamlit as st
from openai import OpenAI

# ── Groq API via OpenAI-compatible client (free!) ──────────────────────────────
GROQ_API_KEY = "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"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Customer Support",
    page_icon="💬",
    layout="centered"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; padding: 8px; }
    .header-box {
        background: linear-gradient(135deg, #1B2B4B, #2D7D7D);
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 24px;
        color: white;
    }
    .header-box h2 { margin: 0; font-size: 22px; }
    .header-box p  { margin: 6px 0 0; font-size: 13px; opacity: 0.85; }
    .status-dot {
        display: inline-block;
        width: 9px; height: 9px;
        background: #4ade80;
        border-radius: 50%;
        margin-right: 7px;
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.4; }
    }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h2>💬 AI Customer Support</h2>
    <p><span class="status-dot"></span>Online — powered by Groq · LLaMA 3</p>
</div>
""", unsafe_allow_html=True)

# ── Client ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_client():
    return OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )

client = get_client()

# ── System prompt ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a helpful, friendly, and professional AI customer support agent.

Your responsibilities:
- Answer customer questions clearly and concisely
- Help with order tracking, returns, refunds, account issues, and product queries
- Escalate complex issues by saying: "I'll connect you with a human agent for this."
- Always stay polite, empathetic, and solution-focused
- If you don't know something, say so honestly and offer alternatives

Keep responses short and to the point — 2 to 4 sentences max unless a detailed explanation is needed.
"""

# ── Session state ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    model = st.selectbox(
        "Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama3-groq-70b-8192-tool-use-preview",
            "gemma2-9b-it",
        ],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.6, 0.1,
                            help="Higher = more creative, Lower = more precise")
    max_tokens = st.slider("Max response length", 100, 1024, 400, 50)

    st.divider()
    st.markdown("### 💡 Quick prompts")
    quick_prompts = [
        "Where is my order?",
        "How do I return a product?",
        "I want a refund",
        "Reset my password",
        "Talk to a human agent",
    ]
    for qp in quick_prompts:
        if st.button(qp, use_container_width=True):
            st.session_state.quick_input = qp

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

    st.markdown("---")
    st.caption("Built with Streamlit · Groq · LLaMA 3")

# ── Display existing messages ──────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Welcome message ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "👋 Hi there! I'm your AI support assistant. How can I help you today?\n\n"
            "You can ask me about **orders, returns, refunds, account issues**, or anything else!"
        )

# ── Handle quick prompt ────────────────────────────────────────────────────────
user_input = None
if "quick_input" in st.session_state and st.session_state.quick_input:
    user_input = st.session_state.quick_input
    st.session_state.quick_input = None

# ── Chat input ─────────────────────────────────────────────────────────────────
chat_input = st.chat_input("Type your message here...")
if chat_input:
    user_input = chat_input

# ── Process message ────────────────────────────────────────────────────────────
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.chat_history,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

            except Exception as e:
                st.error(f"⚠️ Error: {str(e)}")
