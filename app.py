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
# RANDOM FACTS
# =====================================================

medicine_facts = [

    "💡 Did you know? Paracetamol is one of the most commonly used medicines worldwide.",

    "💡 Antibiotics do not work against viral infections like flu or cold.",

    "💡 Generic medicines contain the same active ingredients as branded medicines.",

    "💡 Some medicines should always be taken after food to avoid stomach irritation.",

    "💡 Expired medicines may lose effectiveness and safety over time.",

    "💡 Overusing painkillers may damage liver or kidney health.",

    "💡 Certain medicines can interact with caffeine or alcohol.",

    "💡 Completing your antibiotic course helps prevent resistance.",

    "💡 Medicines should be stored away from sunlight and moisture.",

    "💡 Self-medication can sometimes worsen symptoms."
]

random_fact = random.choice(medicine_facts)

# =====================================================
# CUSTOM BLACK THEME UI
# =====================================================

st.markdown("""
<style>

/* -------------------------------------------------
GLOBAL
------------------------------------------------- */

html, body, [class*="css"] {

    font-family: 'Inter', sans-serif;
}

/* -------------------------------------------------
BLACK BACKGROUND
------------------------------------------------- */

.stApp {

    background: #000000;

    color: white;
}

/* -------------------------------------------------
HIDE STREAMLIT DEFAULT
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

    font-size: 2.6rem;

    font-weight: 800;

    color: white;

    margin-top: 1rem;

    margin-bottom: 0.3rem;

    letter-spacing: -1px;
}

/* -------------------------------------------------
SUBTITLE
------------------------------------------------- */

.subtitle {

    text-align: center;

    color: #A1A1AA;

    font-size: 1rem;

    margin-bottom: 0;
}

/* -------------------------------------------------
EMPTY SCREEN
------------------------------------------------- */

.empty-screen {

    height: 62vh;

    display: flex;

    justify-content: center;

    align-items: center;

    flex-direction: column;
}

/* -------------------------------------------------
FACT CARD
------------------------------------------------- */

.fact-card {

    width: 100%;

    max-width: 650px;

    background: #111111;

    border: 1px solid #1f1f1f;

    border-radius: 24px;

    padding: 1.6rem;

    text-align: center;

    color: #E4E4E7;

    line-height: 1.9;

    font-size: 1rem;

    box-shadow: 0 10px 40px rgba(255,255,255,0.03);
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

    bottom: 14vh;

    left: 50%;

    transform: translateX(-50%);

    width: min(850px, 92%);

    background: #111111;

    border: 1px solid #1f1f1f;

    border-radius: 22px;

    padding: 0.7rem;

    z-index: 999;
}

/* -------------------------------------------------
INPUT TEXT
------------------------------------------------- */

[data-testid="stChatInput"] textarea {

    color: white !important;

    font-size: 16px !important;
}

/* -------------------------------------------------
CHAT MESSAGE
------------------------------------------------- */

[data-testid="stChatMessage"] {

    background: #111111;

    border: 1px solid #1f1f1f;

    border-radius: 22px;

    padding: 1rem;

    margin-bottom: 1rem;
}

/* -------------------------------------------------
HEADINGS
------------------------------------------------- */

h1 {

    color: white !important;
}

h2 {

    color: #60A5FA !important;

    margin-top: 1.4rem !important;
}

/* -------------------------------------------------
TEXT
------------------------------------------------- */

p, li {

    color: #E5E7EB !important;

    line-height: 1.8;

    font-size: 0.96rem;
}

/* -------------------------------------------------
SCROLLBAR
------------------------------------------------- */

::-webkit-scrollbar {

    width: 6px;
}

::-webkit-scrollbar-thumb {

    background: #27272A;

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

        height: 56vh;
    }

    .fact-card {

        font-size: 0.92rem;

        padding: 1.2rem;

        border-radius: 18px;
    }

    [data-testid="stChatInput"] {

        width: 94%;

        bottom: 12vh;

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
        Search medicines, uses, substitutes and side effects instantly
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# EMPTY SCREEN FACT AREA
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="empty-screen">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="fact-card">

            <div class="fact-title">
                🧠 Did You Know?
            </div>

            <div>
                {random_fact}
            </div>

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

    # ASSISTANT RESPONSE

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
