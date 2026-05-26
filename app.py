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

    "💡 Did you know? Paracetamol is one of the most commonly used medicines worldwide.",

    "💡 Antibiotics do not work against viral infections like the common cold.",

    "💡 Always complete your prescribed antibiotic course even if you feel better.",

    "💡 Taking medicines with food can reduce stomach irritation for some drugs.",

    "💡 Overusing painkillers may affect liver or kidney health.",

    "💡 Store medicines away from direct sunlight and moisture.",

    "💡 Generic medicines contain the same active ingredients as branded medicines.",

    "💡 Some medicines can interact with caffeine or alcohol.",

    "💡 Never self-medicate antibiotics without medical advice.",

    "💡 Expired medicines may lose effectiveness over time."
]

random_fact = random.choice(medicine_facts)

# =====================================================
# CUSTOM UI
# =====================================================

st.markdown("""
<style>

/* -------------------------------------------------
BACKGROUND
------------------------------------------------- */

.stApp {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 100%
    );
    color: white;
}

/* Hide Streamlit */
#MainMenu,
footer,
header {
    visibility: hidden;
}

/* Main Container */
.block-container {
    max-width: 850px;
    padding-top: 1rem;
    padding-bottom: 3rem;
}

/* -------------------------------------------------
TITLE
------------------------------------------------- */

.main-title {
    text-align: center;
    font-size: 2.4rem;
    font-weight: 800;
    color: white;
    margin-top: 1rem;
    margin-bottom: 0.4rem;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #CBD5E1;
    font-size: 1rem;
    margin-bottom: 2rem;
}

/* -------------------------------------------------
CENTER CONTENT
------------------------------------------------- */

.center-container {
    min-height: 58vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* -------------------------------------------------
FACT CARD
------------------------------------------------- */

.fact-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1rem;
    border-radius: 18px;
    margin-top: 1rem;
    margin-bottom: 1rem;
    text-align: center;
    color: #E2E8F0;
    line-height: 1.7;
    backdrop-filter: blur(10px);
    font-size: 0.95rem;
}

/* -------------------------------------------------
CHAT INPUT
------------------------------------------------- */

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 1.2rem;
    left: 50%;
    transform: translateX(-50%);
    width: min(850px, 92%);
    background: rgba(17,24,39,0.92);
    backdrop-filter: blur(12px);
    padding: 0.6rem;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    z-index: 999;
}

/* Chat Input Text */
[data-testid="stChatInput"] textarea {
    color: white !important;
    font-size: 16px !important;
}

/* -------------------------------------------------
CHAT MESSAGE
------------------------------------------------- */

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.08);
}

/* -------------------------------------------------
HEADINGS
------------------------------------------------- */

h1 {
    color: white !important;
}

h2 {
    color: #93C5FD !important;
}

/* -------------------------------------------------
TEXT
------------------------------------------------- */

p, li {
    color: #E5E7EB !important;
    line-height: 1.7;
}

/* -------------------------------------------------
MOBILE
------------------------------------------------- */

@media (max-width: 768px) {

    .main-title {
        font-size: 1.8rem;
        line-height: 1.3;
    }

    .subtitle {
        font-size: 0.88rem;
    }

    .center-container {
        min-height: 52vh;
    }

    .fact-card {
        font-size: 0.88rem;
        padding: 0.9rem;
        border-radius: 16px;
    }

    [data-testid="stChatInput"] {
        width: 94%;
        bottom: 1rem;
        border-radius: 18px;
    }

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
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
    <div class="main-title">
        Find my Drug
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Search medicines, uses, side effects and substitutes instantly
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# EMPTY SCREEN CENTER LAYOUT
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="center-container">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="fact-card">
            {random_fact}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Search medicine..."
)

# =====================================================
# HANDLE INPUT
# =====================================================

if query:

    # User Message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    # Assistant Message
    with st.chat_message("assistant"):

        with st.spinner("Analyzing medicine..."):

            try:

                result = bot.search_medicine(query)

                response = bot.format_response(result)

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:

                error_message = f"❌ Error: {str(e)}"

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
