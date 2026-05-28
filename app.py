import streamlit as st
from medicine_bot import MedicineBot
import random

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="FindMyDrug",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# FACTS
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

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #000000;
    color: white;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 760px !important;
    padding-top: 1rem !important;
    padding-left: 1.2rem !important;
    padding-right: 1.2rem !important;

    /* IMPORTANT */
    padding-bottom: 160px !important;
}

/* =====================================================
HEADER
===================================================== */

.app-header {
    text-align: center;
    padding-top: 2rem;
    padding-bottom: 1rem;
}

.app-title {
    font-size: 2.7rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
}

.app-subtitle {
    color: #8a8a8a;
    font-size: 1rem;
}

/* =====================================================
FACT CARD
===================================================== */

.fact-container {
    min-height: 45vh;

    display: flex;
    align-items: center;
    justify-content: center;
}

.fact-card {
    width: 100%;
    background: #111111;
    border: 1px solid #1f1f1f;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
}

.fact-title {
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.75rem;
    margin-bottom: 1rem;
    font-weight: 600;
}

.fact-text {
    color: #e0e0e0;
    font-size: 1.35rem;
    line-height: 1.8;
    font-weight: 400;
}

/* =====================================================
CHAT MESSAGES
===================================================== */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    border-bottom: 1px solid #141414 !important;
}

/* =====================================================
FIXED INPUT BOX
===================================================== */

[data-testid="stChatInput"] {
    position: fixed !important;
    bottom: 18px !important;
    left: 50% !important;
    transform: translateX(-50%) !important;

    width: min(760px, calc(100% - 24px)) !important;

    background: #111111 !important;
    border: 1px solid #262626 !important;
    border-radius: 16px !important;

    padding: 0.45rem !important;

    z-index: 999999 !important;

    box-shadow: 0 -4px 25px rgba(0,0,0,0.6) !important;
}

/* Input area */

[data-testid="stChatInput"] textarea {
    color: white !important;
    background: transparent !important;
    font-size: 1rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #5f5f5f !important;
}

/* =====================================================
MARKDOWN STYLING
===================================================== */

h1, h2, h3 {
    color: white !important;
}

h2 {
    border-bottom: 1px solid #1c1c1c;
    padding-bottom: 0.35rem;
}

p, li {
    color: #d0d0d0 !important;
    line-height: 1.8 !important;
    font-size: 0.98rem !important;
}

strong {
    color: white !important;
}

code {
    background: #111111 !important;
    border: 1px solid #222222 !important;
    padding: 0.15rem 0.4rem !important;
    border-radius: 6px !important;
}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar {
    width: 4px;
}

::-webkit-scrollbar-thumb {
    background: #222222;
    border-radius: 10px;
}

/* =====================================================
MOBILE
===================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 0.9rem !important;
        padding-right: 0.9rem !important;

        /* VERY IMPORTANT FOR MOBILE */
        padding-bottom: 180px !important;
    }

    .app-title {
        font-size: 2rem;
    }

    .app-subtitle {
        font-size: 0.9rem;
    }

    .fact-card {
        padding: 1.5rem;
    }

    .fact-text {
        font-size: 1.15rem;
        line-height: 1.7;
    }

    [data-testid="stChatInput"] {
        bottom: 14px !important;
        width: calc(100% - 16px) !important;
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
    <div class="app-title">Find My Drug</div>
    <div class="app-subtitle">
        Search medicines, uses, side effects and substitutes
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# EMPTY SCREEN
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(f"""
    <div class="fact-container">
        <div class="fact-card">
            <div class="fact-title">💡 Did You Know</div>
            <div class="fact-text">{random_fact}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input("Ask about a medicine...")

# =====================================================
# HANDLE QUERY
# =====================================================

if query:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    # ASSISTANT MESSAGE
    with st.chat_message("assistant"):

        with st.spinner("Looking up medicine..."):

            try:

                result = bot.search_medicine(query)

                response = bot.format_response(result)

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                error_msg = f"❌ Something went wrong: {str(e)}"

                st.error(error_msg)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
