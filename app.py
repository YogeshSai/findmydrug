import streamlit as st
from medicine_bot import MedicineBot
import random

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Medicine Assistant",
    page_icon="💊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================================
# FACTS
# =====================================================

facts = [
    "💡 Paracetamol is one of the most widely used painkillers.",
    "💡 Antibiotics do NOT work for viral infections.",
    "💡 Always complete antibiotic course.",
    "💡 Generic medicines = same effect as branded.",
    "💡 Expired medicines may lose potency.",
]

fact = random.choice(facts)

# =====================================================
# BOT
# =====================================================

@st.cache_resource
def load_bot():
    return MedicineBot()

bot = load_bot()

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# BLACK UI CSS (FIXED LAYOUT)
# =====================================================

st.markdown("""
<style>

/* BLACK BACKGROUND */
.stApp {
    background: #000;
    color: white;
}

/* HIDE STREAMLIT UI */
#MainMenu, footer, header {
    visibility: hidden;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 1rem;
    padding-bottom: 8rem;  /* IMPORTANT: space for chat input */
}

/* TITLE */
.title {
    text-align: center;
    font-size: 2.3rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}

/* SUBTITLE */
.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 1rem;
}

/* CENTER FACT AREA (TRUE CENTER FIX) */
.center-area {
    height: 65vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* FACT CARD */
.fact {
    background: #111;
    border: 1px solid #222;
    padding: 1.5rem;
    border-radius: 18px;
    max-width: 600px;
    text-align: center;
    color: #ddd;
    line-height: 1.8;
}

/* CHAT INPUT SPACING FIX */
div[data-testid="stChatInput"] {
    position: fixed;
    bottom: 2rem !important;
    width: min(850px, 92%);
    left: 50%;
    transform: translateX(-50%);
    background: #111;
    border: 1px solid #222;
    border-radius: 18px;
    z-index: 999;
}

/* CHAT BUBBLES */
div[data-testid="stChatMessage"] {
    background: #111;
    border: 1px solid #222;
    border-radius: 14px;
    padding: 1rem;
}

/* TEXT */
p, li {
    color: #ddd !important;
}

h1, h2, h3 {
    color: white !important;
}

/* MOBILE */
@media (max-width: 768px) {

    .title {
        font-size: 1.7rem;
    }

    .center-area {
        height: 60vh;
    }

    div[data-testid="stChatInput"] {
        bottom: 1.2rem !important;
        width: 94%;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown("<div class='title'>💊 AI Medicine Assistant</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Search medicines instantly</div>", unsafe_allow_html=True)

# =====================================================
# CENTER FACT (ONLY WHEN EMPTY)
# =====================================================

if len(st.session_state.messages) == 0:

    st.markdown("<div class='center-area'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fact">
        🧠 Did You Know?<br><br>
        {fact}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# CHAT HISTORY
# =====================================================

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# =====================================================
# INPUT
# =====================================================

q = st.chat_input("Search medicine...")

if q:

    st.session_state.messages.append({"role": "user", "content": q})

    with st.chat_message("user"):
        st.markdown(q)

    with st.chat_message("assistant"):

        with st.spinner("Searching..."):

            result = bot.search_medicine(q)
            response = bot.format_response(result)

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
