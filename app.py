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
# CUSTOM MODERN UI
# =====================================================

st.markdown("""
<style>

/* ---------------------------------------------------
BACKGROUND
--------------------------------------------------- */

.stApp {
    background: linear-gradient(
        180deg,
        #0f172a 0%,
        #111827 45%,
        #0b1120 100%
    );
    color: white;
}

/* ---------------------------------------------------
HIDE STREAMLIT DEFAULT
--------------------------------------------------- */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* ---------------------------------------------------
MAIN CONTAINER
--------------------------------------------------- */

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 850px;
}

/* ---------------------------------------------------
LOGO ICON
--------------------------------------------------- */

.logo-box {
    width: 80px;
    height: 80px;
    margin: auto;
    border-radius: 22px;
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    box-shadow: 0 10px 35px rgba(37,99,235,0.35);
    margin-bottom: 1rem;
}

/* ---------------------------------------------------
TITLE
--------------------------------------------------- */

.main-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.3rem;
    letter-spacing: -1px;
}

/* ---------------------------------------------------
SUBTITLE
--------------------------------------------------- */

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 1rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

/* ---------------------------------------------------
SEARCH BOX
--------------------------------------------------- */

.stTextInput > div > div > input {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    color: white;
    border-radius: 18px;
    padding: 16px;
    font-size: 16px;
    backdrop-filter: blur(10px);
}

.stTextInput > div > div > input:focus {
    border: 1px solid #3b82f6;
    box-shadow: 0 0 0 1px #3b82f6;
}

/* ---------------------------------------------------
BUTTON
--------------------------------------------------- */

.stButton button {
    width: 100%;
    height: 3.2rem;
    border-radius: 18px;
    border: none;
    background: linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    font-size: 1rem;
    font-weight: 700;
    transition: 0.3s ease;
    box-shadow: 0 10px 25px rgba(37,99,235,0.25);
}

.stButton button:hover {
    transform: translateY(-2px);
}

/* ---------------------------------------------------
RESULT CARD
--------------------------------------------------- */

.result-card {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1.5rem;
    border-radius: 24px;
    margin-top: 1.5rem;
    color: white;
    box-shadow: 0 10px 35px rgba(0,0,0,0.25);
    overflow-wrap: break-word;
}

/* ---------------------------------------------------
HEADINGS
--------------------------------------------------- */

.result-card h1 {
    font-size: 1.8rem;
    margin-bottom: 1rem;
}

.result-card h2 {
    margin-top: 1.4rem;
    font-size: 1.2rem;
    color: #93c5fd;
}

/* ---------------------------------------------------
TEXT
--------------------------------------------------- */

.result-card p,
.result-card li {
    color: #e5e7eb;
    line-height: 1.7;
    font-size: 0.96rem;
}

/* ---------------------------------------------------
FOOTER
--------------------------------------------------- */

.footer {
    text-align: center;
    color: #94a3b8;
    margin-top: 2rem;
    font-size: 0.8rem;
}

/* ---------------------------------------------------
MOBILE
--------------------------------------------------- */

@media (max-width: 768px) {

    .main-title {
        font-size: 2rem;
    }

    .subtitle {
        font-size: 0.9rem;
        margin-bottom: 1.4rem;
    }

    .logo-box {
        width: 68px;
        height: 68px;
        font-size: 2rem;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .result-card {
        padding: 1rem;
        border-radius: 18px;
    }

    .stButton button {
        height: 3rem;
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
# HERO SECTION
# =====================================================

st.markdown(
    """
    <div class="logo-box">
        💊
    </div>
    """,
    unsafe_allow_html=True
)

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
        AI-powered medicine assistant for uses, side effects, substitutes and composition insights
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SEARCH INPUT
# =====================================================

query = st.text_input(
    label="Medicine Search",
    placeholder="Search medicine... Example: Dolo 650",
    label_visibility="collapsed"
)

# =====================================================
# SEARCH BUTTON
# =====================================================

search_clicked = st.button(
    "🔍 Search Medicine"
)

# =====================================================
# SEARCH LOGIC
# =====================================================

if search_clicked:

    if query.strip():

        with st.spinner("Analyzing medicine..."):

            try:

                # SEARCH
                result = bot.search_medicine(query)

                # FORMAT RESPONSE
                response = bot.format_response(result)

                # SHOW RESULT
                st.markdown(
                    f"""
                    <div class="result-card">
                    {response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            except Exception as e:

                st.error(
                    f"Error: {str(e)}"
                )

    else:

        st.warning(
            "Please enter a medicine name"
        )

# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        ⚠️ Informational purposes only. Always consult a healthcare professional.
    </div>
    """,
    unsafe_allow_html=True
)
