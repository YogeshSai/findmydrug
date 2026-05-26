import streamlit as st
from medicine_bot import MedicineBot

st.set_page_config(
    page_title="Find my drug",
    page_icon="💊"
)

st.title("Find my drug")

st.write(
    """
Search medicines and get:

- Uses
- Side Effects
- Substitutes
"""
)

@st.cache_resource
def load_bot():
    return MedicineBot()

bot = load_bot()

query = st.chat_input(
    "Enter medicine name..."
)

if query:

    with st.chat_message("user"):
        st.write(query)

    with st.spinner("Searching medicine..."):

        result = bot.search_medicine(query)

        response = bot.format_response(result)

    with st.chat_message("assistant"):
        st.markdown(response)
