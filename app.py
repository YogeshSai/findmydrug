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
# CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after {
    box-sizing: border-box;
}

/* ---- BACKGROUND ---- */

.stApp {
    background: #000000;
    font-family: 'Inter', sans-serif;
    color: #ffffff;
}

/* ---- HIDE STREAMLIT CHROME ---- */

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---- CONTAINER ---- */

.block-container {
    max-width: 760px !important;
    padding-top: 0 !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ---- HEADER ---- */

.app-header {
    text-align: center;
    padding: 3.5rem 0 1.5rem;
}

.app-header h1 {
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -1px !important;
    margin: 0 0 0.6rem !important;
    line-height: 1.2 !important;
}

.app-header p {
    color: #888888 !important;
    font-size: 1.05rem !important;
    font-weight: 400 !important;
    margin: 0 !important;
    line-height: 1.6 !important;
}

/* ---- FACT CARD ---- */

.fact-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 44vh;
    padding: 1rem 0;
}

.fact-card {
    width: 100%;
    max-width: 620px;
    background: #111111;
    border: 1px solid #222222;
    border-radius: 16px;
    padding: 2.4rem 2.8rem;
    text-align: center;
}

.fact-card .fact-label {
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #555555;
    margin-bottom: 1rem;
    display: block;
}

.fact-card .fact-text {
    color: #dddddd !important;
    font-size: 1.45rem !important;
    line-height: 1.9 !important;
    font-weight: 400 !important;
    margin: 0 !important;
}

/* ---- CHAT MESSAGES ---- */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 1.2rem 0 !important;
    margin-bottom: 0 !important;
    border-bottom: 1px solid #1a1a1a !important;
}

/* ---- CHAT INPUT ---- */

[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 10vh !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(760px, 92%) !important;
    background: #111111 !important;
    border-radius: 14px !important;
    border: 1px solid #2a2a2a !important;
    box-shadow: 0 8px 40px rgba(0,0,0,0.8) !important;
    z-index: 999 !important;
    padding: 0.4rem !important;
}

[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #444444 !important;
}

/* ---- RESPONSE TYPOGRAPHY ---- */

h1 {
    color: #ffffff !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}

h2 {
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    margin-top: 1.4rem !important;
    margin-bottom: 0.4rem !important;
    border-bottom: 1px solid #1e1e1e !important;
    padding-bottom: 0.3rem !important;
}

h3 {
    font-family: 'Inter', sans-serif !important;
    color: #bbbbbb !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.2rem !important;
}

p, li {
    color: #cccccc !important;
    font-size: 0.97rem !important;
    line-height: 1.85 !important;
    font-weight: 400 !important;
}

strong {
    color: #ffffff !important;
    font-weight: 600 !important;
}

code {
    background: #111111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 5px !important;
    padding: 0.15rem 0.45rem !important;
    font-size: 0.87rem !important;
    color: #aaaaaa !important;
}

/* ---- SCROLLBAR ---- */

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #222222; border-radius: 10px; }

/* ---- MOBILE ---- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    .app-header h1 {
        font-size: 2rem !important;
    }

    .app-header p {
        font-size: 0.92rem !important;
    }

    .fact-card {
        padding: 1.8rem 1.6rem;
    }

    .fact-card .fact-text {
        font-size: 1.2rem !important;
    }

    [data-testid="stChatInput"] {
        width: 94% !important;
        bottom: 10vh !important;
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
    <h1>Find my Drug</h1>
    <p>Search medicines, uses, side effects and substitutes</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# EMPTY SCREEN
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
