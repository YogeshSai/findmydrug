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
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Hide Streamlit Branding */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main Container */
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 850px;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 700;
    margin-top: 0rem;
    margin-bottom: 0.3rem;
    line-height: 1.2;
    word-wrap: break-word;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 0.95rem;
    margin-bottom: 1.8rem;
    line-height: 1.5;
}

/* Search Input */
.stTextInput input {
    border-radius: 14px;
    padding: 14px;
    font-size: 16px;
    border: 1px solid #374151;
}

/* Button */
.stButton button {
    width: 100%;
    border-radius: 14px;
    height: 3rem;
    font-size: 1rem;
    font-weight: 600;
    border: none;
}

/* Result Card */
.result-card {
    background-color: #111827;
    padding: 1.2rem;
    border-radius: 18px;
    margin-top: 1rem;
    border: 1px solid #1F2937;
    overflow-wrap: break-word;
}

/* Scroll Fix */
html, body, [class*="css"] {
    overflow-x: hidden;
}

/* Mobile Responsive */
@media (max-width: 768px) {

    .main-title {
        font-size: 1.6rem;
        margin-top: 0rem;
        padding-top: 0rem;
    }

    .subtitle {
        font-size: 0.82rem;
        margin-bottom: 1rem;
    }

    .block-container {
        padding-top: 0.2rem;
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .stButton button {
        height: 2.8rem;
        font-size: 0.95rem;
    }

    .result-card {
        padding: 0.9rem;
        border-radius: 14px;
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
# HEADER
# =====================================================

st.markdown(
    """
    <div class="main-title">
        Find my Drug💊
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Search medicines, substitutes, side effects and composition instantly
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SEARCH INPUT
# =====================================================

query = st.text_input(
    label="Medicine Name",
    placeholder="Example: Dolo 650",
    label_visibility="collapsed"
)

# =====================================================
# SEARCH BUTTON
# =====================================================

search_clicked = st.button(
    "Search Medicine"
)

# =====================================================
# SEARCH ACTION
# =====================================================

if search_clicked:

    if query.strip():

        with st.spinner("Searching medicine..."):

            try:

                # -----------------------------------------
                # SEARCH MEDICINE
                # -----------------------------------------

                result = bot.search_medicine(query)

                # -----------------------------------------
                # FORMAT RESPONSE
                # -----------------------------------------

                response = bot.format_response(result)

                # -----------------------------------------
                # DISPLAY RESULT
                # -----------------------------------------

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

st.markdown("---")

st.caption(
    "⚠️ This chatbot is for informational purposes only and should not replace professional medical advice."
)
