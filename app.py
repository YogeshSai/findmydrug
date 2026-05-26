import streamlit as st
from medicine_bot import MedicineBot
import random

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Find my Drug",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# MEDICINE FACTS
# =====================================================

medicine_facts = [
    "Paracetamol is one of the most commonly used medicines worldwide.",
    "Antibiotics do not work against viral infections like cold and flu.",
    "Generic medicines contain the same active ingredients as branded medicines.",
    "Some medicines work better when taken after food.",
    "Painkillers should not be overused without medical advice.",
    "Always complete your antibiotic course even if you feel better.",
    "Medicines should be stored away from sunlight and moisture.",
    "Expired medicines may lose effectiveness over time.",
    "Certain medicines can interact with caffeine or alcohol.",
    "Self-medication can sometimes worsen symptoms.",
]

random_fact = random.choice(medicine_facts)

# =====================================================
# CSS — Clean Claude-style UI
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
}

/* ---- BACKGROUND ---- */

.stApp {
    background: #0d1117;
    font-family: 'Inter', sans-serif;
    color: #e6edf3;
}

/* ---- HIDE STREAMLIT CHROME ---- */

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---- CONTAINER ---- */

.block-container {
    max-width: 720px !important;
    padding-top: 3rem !important;
    padding-bottom: 2rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* ---- HEADER ---- */

.app-header {
    text-align: center;
    padding: 2rem 0 2.5rem;
}

.app-header .icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.75rem;
}

.app-header h1 {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: #e6edf3 !important;
    letter-spacing: -0.4px !important;
    margin: 0 0 0.5rem !important;
    line-height: 1.3 !important;
}

.app-header p {
    color: #7d8590 !important;
    font-size: 0.88rem !important;
    font-weight: 400 !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}

/* ---- FACT CARD ---- */

.fact-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 40vh;
    padding: 1rem 0;
}

.fact-card {
    width: 100%;
    max-width: 560px;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    text-align: center;
}

.fact-card .fact-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #7d8590;
    margin-bottom: 0.75rem;
    display: block;
}

.fact-card .fact-text {
    color: #c9d1d9 !important;
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* ---- CHAT MESSAGES ---- */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.6rem 0 !important;
    margin-bottom: 0 !important;
    border-bottom: 1px solid #21262d !important;
}

/* ---- CHAT INPUT ---- */

[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 14vh !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(720px, 92%) !important;
    background: #161b22 !important;
    backdrop-filter: blur(12px) !important;
    border-radius: 12px !important;
    border: 1px solid #30363d !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.5) !important;
    z-index: 999 !important;
    padding: 0.3rem !important;
}

[data-testid="stChatInput"] textarea {
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.93rem !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #484f58 !important;
}

/* ---- RESPONSE TYPOGRAPHY ---- */

h2 {
    font-family: 'Inter', sans-serif !important;
    color: #e6edf3 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    margin-top: 1.2rem !important;
    margin-bottom: 0.3rem !important;
}

h3 {
    font-family: 'Inter', sans-serif !important;
    color: #8b949e !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    margin-top: 0.8rem !important;
    margin-bottom: 0.2rem !important;
}

p, li {
    color: #c9d1d9 !important;
    font-size: 0.91rem !important;
    line-height: 1.8 !important;
    font-weight: 400 !important;
}

strong {
    color: #e6edf3 !important;
    font-weight: 500 !important;
}

code {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 4px !important;
    padding: 0.1rem 0.4rem !important;
    font-size: 0.85rem !important;
    color: #79c0ff !important;
}

/* ---- SCROLLBAR ---- */

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #21262d; border-radius: 10px; }

/* ---- MOBILE ---- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .app-header h1 {
        font-size: 1.35rem !important;
    }

    .fact-card {
        padding: 1.3rem 1.4rem;
    }

    [data-testid="stChatInput"] {
        width: 94% !important;
        bottom: 14vh !important;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD BOT
# =====================================================

@st.cache_resource
def load_bot():
    return MedicineBot()

bot = load_bot()

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="app-header">
    <span class="icon"></span>
    <h1>Find my Drug</h1>
    <p>Search medicines, uses, side effects and substitutes</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# EMPTY SCREEN — FACT CARD
# =====================================================

if len(st.session_state.messages) == 0:
    fact_card_html = (
        '<div class="fact-wrapper">'
        '<div class="fact-card">'
        '<span class="fact-label">💡 Did you know</span>'
        '<p class="fact-text">' + random_fact + '</p>'
        '</div>'
        '</div>'
    )
    st.markdown(fact_card_html, unsafe_allow_html=True)

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input("Ask about a medicine")

# =====================================================
# HANDLE QUERY
# =====================================================

if query:

    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Looking up..."):
            try:
                result = bot.search_medicine(query)
                response = bot.format_response(result)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"❌ Something went wrong: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
