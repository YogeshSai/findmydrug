```python
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
    "Self-medication can sometimes worsen symptoms."
]

random_fact = random.choice(medicine_facts)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* =====================================================
APP
===================================================== */

.stApp {
    background: #000000;
    color: white;
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
    IMPORTANT
    Prevents content from hiding behind searchbox
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

    color: #808080;

    font-size: 1rem;

    line-height: 1.6;
}

/* =====================================================
FACT CARD
===================================================== */

.fact-wrapper {

    min-height: 45vh;

    display: flex;

    align-items: center;

    justify-content: center;
}

.fact-card {

    width: 100%;

    background: #111111;

    border: 1px solid #1f1f1f;

    border-radius: 20px;

    padding: 2rem;
}

.fact-label {

    color: #666666;

    font-size: 0.78rem;

    font-weight: 700;

    letter-spacing: 2px;

    text-transform: uppercase;

    margin-bottom: 1rem;
}

.fact-text {

    color: #e2e2e2;

    font-size: 1.35rem;

    line-height: 1.9;
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

    bottom: 1cm !important;

    left: 50% !important;

    transform: translateX(-50%) !important;

    width: min(760px, calc(100% - 20px)) !important;

    background: #111111 !important;

    border: 1px solid #262626 !important;

    border-radius: 18px !important;

    padding: 0.45rem !important;

    z-index: 999999 !important;

    box-shadow: 0px -5px 25px rgba(0,0,0,0.65) !important;
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
}

p, li {

    color: #d4d4d4 !important;

    line-height: 1.85 !important;

    font-size: 0.98rem !important;
}

strong {
    color: white !important;
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

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">FindMyDrug</div>
        <div class="app-subtitle">
            Search medicines, uses, side effects and substitutes
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# EMPTY SCREEN
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True
    )

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

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):

        st.markdown(query)

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
```
