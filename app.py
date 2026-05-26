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

    "💡 Did you know? Paracetamol is one of the most commonly used medicines worldwide.",

    "💡 Antibiotics do not work against viral infections like cold and flu.",

    "💡 Generic medicines contain the same active ingredients as branded medicines.",

    "💡 Some medicines work better when taken after food.",

    "💡 Painkillers should not be overused without medical advice.",

    "💡 Always complete your antibiotic course even if you feel better.",

    "💡 Medicines should be stored away from sunlight and moisture.",

    "💡 Expired medicines may lose effectiveness over time.",

    "💡 Certain medicines can interact with caffeine or alcohol.",

    "💡 Self-medication can sometimes worsen symptoms."
]

random_fact = random.choice(medicine_facts)

# =====================================================
# MODERN UI CSS
# =====================================================

st.markdown("""
<style>

/* -------------------------------------------------
APP BACKGROUND
------------------------------------------------- */

.stApp {

    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 100%
    );

    color: white;
}

/* -------------------------------------------------
HIDE STREAMLIT DEFAULT UI
------------------------------------------------- */

#MainMenu,
footer,
header {

    visibility: hidden;
}

/* -------------------------------------------------
MAIN CONTAINER
------------------------------------------------- */

.block-container {

    max-width: 850px;

    padding-top: 1rem;

    padding-bottom: 2rem;
}

/* -------------------------------------------------
TITLE
------------------------------------------------- */

.main-title {

    text-align: center;

    font-size: 2.5rem;

    font-weight: 800;

    color: white;

    margin-top: 1rem;

    margin-bottom: 0.4rem;

    letter-spacing: -1px;
}

/* -------------------------------------------------
SUBTITLE
------------------------------------------------- */

.subtitle {

    text-align: center;

    color: #CBD5E1;

    font-size: 1rem;

    margin-bottom: 0;
}

/* -------------------------------------------------
EMPTY SCREEN AREA
------------------------------------------------- */

.empty-screen {

    height: 62vh;

    display: flex;

    flex-direction: column;

    justify-content: center;

    align-items: center;
}

/* -------------------------------------------------
FACT CARD
------------------------------------------------- */

.fact-card {

    width: 100%;

    max-width: 650px;

    background: rgba(255,255,255,0.06);

    border: 1px solid rgba(255,255,255,0.08);

    padding: 1.5rem;

    border-radius: 24px;

    text-align: center;

    color: #E2E8F0;

    line-height: 1.9;

    font-size: 1rem;

    backdrop-filter: blur(14px);

    box-shadow: 0 10px 35px rgba(0,0,0,0.25);
}

/* -------------------------------------------------
FACT TITLE
------------------------------------------------- */

.fact-title {

    color: white;

    font-size: 1.2rem;

    font-weight: 700;

    margin-bottom: 1rem;
}

/* -------------------------------------------------
CHAT INPUT
------------------------------------------------- */

[data-testid="stChatInput"] {

    position: fixed;

    bottom: 16vh;

    left: 50%;

    transform: translateX(-50%);

    width: min(850px, 92%);

    background: rgba(17,24,39,0.94);

    backdrop-filter: blur(12px);

    padding: 0.7rem;

    border-radius: 22px;

    border: 1px solid rgba(255,255,255,0.08);

    z-index: 999;
}

/* -------------------------------------------------
CHAT INPUT TEXT
------------------------------------------------- */

[data-testid="stChatInput"] textarea {

    color: white !important;

    font-size: 16px !important;
}

/* -------------------------------------------------
CHAT MESSAGE
------------------------------------------------- */

[data-testid="stChatMessage"] {

    background: rgba(255,255,255,0.05);

    border-radius: 20px;

    padding: 1rem;

    margin-bottom: 1rem;

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(10px);
}

/* -------------------------------------------------
HEADINGS
------------------------------------------------- */

h1 {

    color: white !important;
}

h2 {

    color: #93C5FD !important;

    margin-top: 1.4rem !important;
}

/* -------------------------------------------------
TEXT
------------------------------------------------- */

p, li {

    color: #E5E7EB !important;

    line-height: 1.8;

    font-size: 0.95rem;
}

/* -------------------------------------------------
SCROLLBAR
------------------------------------------------- */

::-webkit-scrollbar {

    width: 6px;
}

::-webkit-scrollbar-thumb {

    background: #374151;

    border-radius: 10px;
}

/* -------------------------------------------------
MOBILE RESPONSIVE
------------------------------------------------- */

@media (max-width: 768px) {

    .main-title {

        font-size: 1.9rem;

        line-height: 1.3;
    }

    .subtitle {

        font-size: 0.9rem;
    }

    .empty-screen {

        height: 55vh;
    }

    .fact-card {

        font-size: 0.92rem;

        padding: 1.2rem;

        border-radius: 18px;
    }

    [data-testid="stChatInput"] {

        width: 94%;

        bottom: 13vh;

        border-radius: 18px;
    }

    .block-container {

        padding-left: 0.7rem;

        padding-right: 0.7rem;
    }

    p, li {

        font-size: 0.9rem;
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
        💊 AI Medicine Assistant
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
# EMPTY SCREEN
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        f"""
        <div class="empty-screen">

            <div class="fact-card">

                <div class="fact-title">
                    🧠 Did You Know?
                </div>

                {random_fact}

            </div>

        </div>
        """,
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
# HANDLE USER QUERY
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

        with st.spinner("Analyzing medicine..."):

            try:

                # SEARCH

                result = bot.search_medicine(query)

                # FORMAT RESPONSE

                response = bot.format_response(result)

                # SHOW RESPONSE

                st.markdown(response)

                # SAVE RESPONSE

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
