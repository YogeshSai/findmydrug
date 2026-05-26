import streamlit as st
from medicine_bot import MedicineBot

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
# MODERN MOBILE RESPONSIVE UI
# =====================================================

st.markdown("""
<style>

/* -------------------------------------------------
GLOBAL
------------------------------------------------- */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 100%
    );
    color: white;
}

/* Hide Streamlit Branding */
#MainMenu,
footer,
header {
    visibility: hidden;
}

/* Main Container */
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
    font-size: 2.3rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
    color: white;
    letter-spacing: -1px;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #CBD5E1;
    font-size: 1rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* -------------------------------------------------
CHAT MESSAGES
------------------------------------------------- */

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 0.8rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

/* User Message */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
    background: rgba(37,99,235,0.12);
    border: 1px solid rgba(59,130,246,0.25);
}

/* Assistant Message */
[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
    background: rgba(255,255,255,0.06);
}

/* -------------------------------------------------
CHAT INPUT
------------------------------------------------- */

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 0.8rem;
    left: 50%;
    transform: translateX(-50%);
    width: min(850px, 95%);
    background: rgba(17,24,39,0.92);
    backdrop-filter: blur(12px);
    padding: 0.6rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    z-index: 999;
}

/* Input Box */
[data-testid="stChatInput"] textarea {
    color: white !important;
    font-size: 16px !important;
}

/* -------------------------------------------------
HEADINGS INSIDE RESPONSE
------------------------------------------------- */

h1 {
    font-size: 1.7rem !important;
    color: white !important;
}

h2 {
    font-size: 1.1rem !important;
    color: #93C5FD !important;
    margin-top: 1.3rem !important;
}

/* Text */
p, li {
    color: #E5E7EB !important;
    line-height: 1.7 !important;
    font-size: 0.95rem !important;
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
MOBILE
------------------------------------------------- */

@media (max-width: 768px) {

    .main-title {
        font-size: 1.8rem;
        line-height: 1.3;
    }

    .subtitle {
        font-size: 0.88rem;
        margin-bottom: 1.4rem;
    }

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
        padding-bottom: 7rem;
    }

    [data-testid="stChatInput"] {
        width: 96%;
        bottom: 0.5rem;
        border-radius: 18px;
    }

    h1 {
        font-size: 1.4rem !important;
    }

    h2 {
        font-size: 1rem !important;
    }

    p, li {
        font-size: 0.9rem !important;
    }
}

</style>
""", unsafe_allow_html=True)

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
        Search medicines and get uses, side effects and substitutes instantly
    </div>
    """,
    unsafe_allow_html=True
)

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
# DISPLAY CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Enter medicine name..."
)

# =====================================================
# HANDLE USER INPUT
# =====================================================

if query:

    # Store User Message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Show User Message
    with st.chat_message("user"):
        st.markdown(query)

    # Assistant Response
    with st.chat_message("assistant"):

        with st.spinner("Searching medicine..."):

            try:

                result = bot.search_medicine(query)

                response = bot.format_response(result)

                st.markdown(response)

                # Store Assistant Response
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
