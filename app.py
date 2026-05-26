import streamlit as st
from medicine_bot import MedicineBot
import random

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Medicine Assistant",
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

@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* ---- ROOT ---- */

*, *::before, *::after {
    box-sizing: border-box;
}

/* ---- APP BACKGROUND ---- */

.stApp {
    background: #080c14;
    font-family: 'DM Sans', sans-serif;
    color: #e2e8f0;
}

/* ---- HIDE STREAMLIT DEFAULT UI ---- */

#MainMenu, footer, header {
    visibility: hidden;
}

/* ---- MAIN CONTAINER ---- */

.block-container {
    max-width: 820px !important;
    padding-top: 2rem !important;
    padding-bottom: 6rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}

/* ---- HEADER ---- */

.app-header {
    text-align: center;
    padding: 1.5rem 0 2rem;
}

.app-header .pill {
    display: inline-block;
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.25);
    color: #38bdf8;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}

.app-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.6rem !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    letter-spacing: -1.5px;
    line-height: 1.15;
    margin: 0 0 0.6rem !important;
}

.app-header h1 span {
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.app-header p {
    color: #64748b !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    margin: 0 !important;
    line-height: 1.5 !important;
}

/* ---- FACT CARD ---- */

.fact-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 45vh;
    padding: 1rem 0;
}

.fact-card {
    width: 100%;
    max-width: 600px;
    background: linear-gradient(135deg, rgba(56,189,248,0.06) 0%, rgba(129,140,248,0.06) 100%);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    text-align: center;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    position: relative;
    overflow: hidden;
}

.fact-card::before {
    content: '';
    position: absolute;
    top: -60px;
    right: -60px;
    width: 180px;
    height: 180px;
    background: radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}

.fact-card .fact-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
    display: block;
}

.fact-card .fact-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 0.8rem;
    display: block;
}

.fact-card .fact-text {
    color: #cbd5e1 !important;
    font-size: 1rem !important;
    line-height: 1.75 !important;
    font-weight: 300 !important;
    margin: 0 !important;
}

/* ---- CHAT MESSAGES ---- */

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.8rem !important;
    backdrop-filter: blur(10px);
}

/* ---- CHAT INPUT ---- */

[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 25vh !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    width: min(820px, 92%) !important;
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(56, 189, 248, 0.2) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
    z-index: 999 !important;
    padding: 0.4rem !important;
}

[data-testid="stChatInput"] textarea {
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    background: transparent !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #475569 !important;
}

/* ---- TYPOGRAPHY IN RESPONSES ---- */

h2 {
    font-family: 'Syne', sans-serif !important;
    color: #38bdf8 !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    margin-top: 1.4rem !important;
    margin-bottom: 0.4rem !important;
    letter-spacing: -0.3px;
}

h3 {
    font-family: 'Syne', sans-serif !important;
    color: #818cf8 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    margin-top: 1rem !important;
    margin-bottom: 0.3rem !important;
}

p, li {
    color: #cbd5e1 !important;
    font-size: 0.93rem !important;
    line-height: 1.85 !important;
    font-weight: 300 !important;
}

strong {
    color: #e2e8f0 !important;
    font-weight: 500 !important;
}

/* ---- SPINNER ---- */

.stSpinner > div {
    border-top-color: #38bdf8 !important;
}

/* ---- SCROLLBAR ---- */

::-webkit-scrollbar {
    width: 4px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: #1e293b;
    border-radius: 10px;
}

/* ---- MOBILE ---- */

@media (max-width: 768px) {

    .app-header h1 {
        font-size: 1.9rem !important;
        letter-spacing: -1px;
    }

    .app-header p {
        font-size: 0.85rem !important;
    }

    .fact-card {
        padding: 1.5rem 1.4rem;
        border-radius: 16px;
    }

    .fact-card .fact-text {
        font-size: 0.9rem !important;
    }

    [data-testid="stChatInput"] {
        width: 94% !important;
        bottom: 25vh !important;
    }

    .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
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
    <div class="pill">AI Powered</div>
    <h1>💊 Medicine <span>Assistant</span></h1>
    <p>Search medicines, uses, side effects and substitutes instantly</p>
</div>
""", unsafe_allow_html=True)

# =====================================================
# EMPTY SCREEN — FACT CARD
# =====================================================

if len(st.session_state.messages) == 0:
    fact_card_html = (
        '<div class="fact-wrapper">'
        '<div class="fact-card">'
        '<span class="fact-icon">🧠</span>'
        '<span class="fact-label">Did You Know?</span>'
        '<p class="fact-text">💡 ' + random_fact + '</p>'
        '</div>'
        '</div>'
    )
    st.markdown(fact_card_html, unsafe_allow_html=True)

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input("Search a medicine, symptom or drug name...")

# =====================================================
# HANDLE USER QUERY
# =====================================================

if query:

    # Save & show user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    # Generate & show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing medicine..."):
            try:
                result = bot.search_medicine(query)
                response = bot.format_response(result)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except Exception as e:
                error_msg = f"❌ Something went wrong: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
