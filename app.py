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
    "Self-medication can sometimes worsen symptoms."
]

random_fact = random.choice(medicine_facts)

# =====================================================
# CUSTOM CSS
# =====================================================

custom_css = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =====================================================
APP
===================================================== */

.stApp {
    background-color: #000000;
    color: #ffffff;
}

#MainMenu,
header,
footer {
    visibility: hidden;
}

/* =====================================================
MAIN CONTAINER
===================================================== */

.block-container {

    max-width: 760px !important;

    padding-top: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;

    /*
    Prevent content hiding behind searchbox
    */
    padding-bottom: 220px !important;
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

    font-size: 2.8rem;

    font-weight: 800;

    color: white;

    letter-spacing: -1px;

    margin-bottom: 0.5rem;
}

.app-subtitle {

    color: #7d7d7d;

    font-size: 1rem;

    line-height: 1.6;
}

/* =====================================================
FACT CARD
===================================================== */

.fact-wrapper {

    min-height: 45vh;

    display: flex;

    justify-content: center;

    align-items: center;
}

.fact-card {

    width: 100%;

    background: #111111;

    border: 1px solid #1e1e1e;

    border-radius: 20px;

    padding: 2rem;
}

.fact-label {

    color: #5d5d5d;

    font-size: 0.78rem;

    font-weight: 700;

    letter-spacing: 2px;

    text-transform: uppercase;

    margin-bottom: 1rem;
}

.fact-text {

    color: #e0e0e0;

    font-size: 1.35rem;

    line-height: 1.9;

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

    border-bottom: 1px solid #151515 !important;
}

/* =====================================================
SEARCH BOX
===================================================== */

[data-testid="stChatInput"] {

    position: fixed !important;

    /*
    1 cm above bottom
    */
    bottom: 1cm !important;

    left: 50% !important;

    transform: translateX(-50%) !important;

    width: min(760px, calc(100% - 20px)) !important;

    background: #111111 !important;

    border: 1px solid #252525 !important;

    border-radius: 18px !important;

    padding: 0.45rem !important;

    z-index: 999999 !important;

    box-shadow: 0px -5px 30px rgba(0,0,0,0.65) !important;
}

/* INPUT */

[data-testid="stChatInput"] textarea {

    color: white !important;

    background: transparent !important;

    font-size: 1rem !important;
}

[data-testid="stChatInput"] textarea::placeholder {

    color: #666666 !important;
}

/* =====================================================
TYPOGRAPHY
===================================================== */

h1, h2, h3 {
    color: white !important;
}

h2 {

    border-bottom: 1px solid #1d1d1d;

    padding-bottom: 0.4rem;

    margin-top: 1.4rem !important;
}

p, li {

    color: #d4d4d4 !important;

    line-height: 1.85 !important;

    font-size: 0.98rem !important;
}

strong {
    color: white !important;
}

code {

    background: #111111 !important;

    border: 1px solid #222222 !important;

    border-radius: 6px !important;

    padding: 0.15rem 0.4rem !important;
}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar {
    width: 4px;
}

::-webkit-scrollbar-thumb {
    background: #222222;
    border-radius: 20px;
}

/* =====================================================
MOBILE
===================================================== */

@media (max-width: 768px) {

    .block-container {

        padding-left: 0.8rem !important;

        padding-right: 0.8rem !important;

        padding-bottom: 240px !important;
    }

    .app-title {

        font-size: 2rem;
    }

    .app-subtitle {

        font-size: 0.92rem;
    }

    .fact-card {

        padding: 1.5rem;
    }

    .fact-text {

        font-size: 1.15rem;

        line-height: 1.75;
    }

    [data-testid="stChatInput"] {

        width: calc(100% - 14px) !important;

        bottom: 1cm !important;
    }
}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

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

header_html = """
<div class="app-header">

    <div class="app-title">
        FindMyDrug
    </div>

    <div class="app-subtitle">
        Search medicines, uses, side effects and substitutes
    </div>

</div>
"""

st.markdown(header_html, unsafe_allow_html=True)

# =====================================================
# EMPTY SCREEN
# =====================================================

if len(st.session_state.messages) == 0:

    fact_html = f"""
    <div class="fact-wrapper">

        <div class="fact-card">

            <div class="fact-label">
                💡 DID YOU KNOW
            </div>

            <div class="fact-text">
                {random_fact}
            </div>

        </div>

    </div>
    """

    st.markdown(fact_html, unsafe_allow_html=True)

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

                error_message = f"❌ Something went wrong: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
