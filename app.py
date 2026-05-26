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
# CUSTOM MOBILE CSS
# =====================================================

st.markdown("""
<style>

/* Main App */
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 900px;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 2rem;
    font-size: 0.95rem;
}

/* Search Box */
.stTextInput input {
    border-radius: 12px;
    padding: 14px;
    font-size: 16px;
}

/* Button */
.stButton button {
    width: 100%;
    border-radius: 12px;
    height: 3rem;
    font-size: 1rem;
    font-weight: bold;
}

/* Result Card */
.result-card {
    background-color: #111827;
    padding: 1.2rem;
    border-radius: 16px;
    margin-top: 1rem;
}

/* Mobile Optimization */
@media (max-width: 768px) {

    .main-title {
        font-size: 1.6rem;
    }

    .subtitle {
        font-size: 0.85rem;
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
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">Find my Drug</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Search medicines, uses, substitutes and side effects instantly</div>',
    unsafe_allow_html=True
)

# =====================================================
# SEARCH BOX
# =====================================================

query = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Dolo 650"
)

# =====================================================
# SEARCH BUTTON
# =====================================================

if st.button("Search Medicine"):

    if query.strip():

        with st.spinner("Searching medicine..."):

            result = bot.search_medicine(query)

            response = bot.format_response(result)

            st.markdown(
                f'<div class="result-card">{response}</div>',
                unsafe_allow_html=True
            )

    else:

        st.warning("Please enter a medicine name")

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "⚠️ This chatbot is for informational purposes only and not medical advice."
)
