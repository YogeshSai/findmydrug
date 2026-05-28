```python
# ============================================================
# AI + NLP POWERED MEDICINE BOT
# ============================================================

# ============================================================
# IMPORTS
# ============================================================

import re
import zipfile
import numpy as np
import pandas as pd
import streamlit as st

from groq import Groq

from rapidfuzz import process, fuzz

import spacy

from sentence_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# MEDICINE BOT CLASS
# ============================================================

class MedicineBot:

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self):

        print("\n🚀 Initializing MedicineBot...\n")

        # ----------------------------------------------------
        # LOAD DATASET
        # ----------------------------------------------------

        self.df = self.load_dataset()

        # ----------------------------------------------------
        # CLEAN SEARCH COLUMN
        # ----------------------------------------------------

        self.df["search_name"] = (
            self.df["name"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        # ----------------------------------------------------
        # CREATE NLP SEARCH TEXT
        # ----------------------------------------------------

        self.df["nlp_text"] = (
            self.df.astype(str)
            .apply(lambda x: " ".join(x), axis=1)
            .str.lower()
        )

        # ----------------------------------------------------
        # MEDICINE NAMES
        # ----------------------------------------------------

        self.medicine_names = (
            self.df["search_name"]
            .dropna()
            .tolist()
        )

        # ----------------------------------------------------
        # LOAD NLP MODELS
        # ----------------------------------------------------

        print("🧠 Loading NLP Models...")

        self.nlp = spacy.load("en_core_web_sm")

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        # ----------------------------------------------------
        # CREATE EMBEDDINGS
        # ----------------------------------------------------

        print("⚡ Creating Embeddings...")

        self.embeddings = (
            self.embedding_model.encode(
                self.df["nlp_text"].tolist(),
                show_progress_bar=True
            )
        )

        # ----------------------------------------------------
        # GROQ CLIENT
        # ----------------------------------------------------

        self.client = Groq(
            api_key=st.secrets["GROQ_API_KEY"]
        )

        print("\n✅ MedicineBot Ready\n")

    # ========================================================
    # LOAD DATASET
    # ========================================================

    def load_dataset(self):

        zip_path = "Data/medicine_dataset.zip"

        with zipfile.ZipFile(zip_path) as z:

            csv_file = z.namelist()[0]

            with z.open(csv_file) as f:

                df = pd.read_csv(
                    f,
                    low_memory=False
                )

        print("✅ Dataset Loaded")
        print(f"📦 Total Medicines: {len(df)}")

        return df

    # ========================================================
    # CLEAN TEXT
    # ========================================================

    def clean_text(self, text):

        if pd.isna(text):
            return ""

        text = str(text).lower().strip()

        remove_words = [
            "tablet",
            "tablets",
            "tab",
            "capsule",
            "capsules",
            "cap",
            "syrup",
            "oral suspension",
            "injection",
            "mg",
            "ml"
        ]

        for word in remove_words:
            text = text.replace(word, "")

        text = " ".join(text.split())

        return text

    # ========================================================
    # EXTRACT DOSAGE
    # ========================================================

    def extract_strength(self, text):

        text = str(text).lower()

        match = re.search(
            r'(\d+)\s?(mg|ml)',
            text
        )

        if match:
            return match.group(1)

        return None

    # ========================================================
    # NLP QUERY UNDERSTANDING
    # ========================================================

    def understand_query(self, query):

        doc = self.nlp(query)

        keywords = []

        for token in doc:

            if (
                not token.is_stop
                and not token.is_punct
            ):

                keywords.append(token.text)

        return " ".join(keywords)

    # ========================================================
    # SEMANTIC SEARCH
    # ========================================================

    def semantic_search(self, query):

        print("\n🧠 Semantic Search Running...")

        cleaned_query = (
            self.understand_query(query)
        )

        query_embedding = (
            self.embedding_model.encode(
                [cleaned_query]
            )
        )

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        best_index = np.argmax(similarities)

        best_score = similarities[best_index]

        print("Semantic Score:", best_score)

        if best_score > 0.35:

            return self.df.iloc[best_index]

        return None

    # ========================================================
    # FUZZY SEARCH
    # ========================================================

    def fuzzy_search(self, query):

        query_clean = self.clean_text(query)

        result = process.extractOne(
            query_clean,
            self.medicine_names,
            scorer=fuzz.token_sort_ratio
        )

        if result is None:
            return None

        best_match_name = result[0]
        score = result[1]

        print("\n🔍 Fuzzy Score:", score)

        if score < 60:
            return None

        matched_row = self.df[
            self.df["search_name"]
            == best_match_name
        ]

        if matched_row.empty:
            return None

        return matched_row.iloc[0]

    # ========================================================
    # SEARCH MEDICINE
    # ========================================================

    def search_medicine(self, query):

        query_clean = self.clean_text(query)

        print(f"\n🔍 Searching: {query_clean}")

        # ----------------------------------------------------
        # EXACT MATCH
        # ----------------------------------------------------

        exact_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            == query_clean
        ]

        if not exact_match.empty:

            print("✅ Exact Match Found")

            return exact_match.iloc[0]

        # ----------------------------------------------------
        # STARTS WITH MATCH
        # ----------------------------------------------------

        starts_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.startswith(query_clean)
        ]

        if not starts_match.empty:

            print("✅ Starts-With Match Found")

            return starts_match.iloc[0]

        # ----------------------------------------------------
        # CONTAINS MATCH
        # ----------------------------------------------------

        contains_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.contains(query_clean, na=False)
        ]

        if not contains_match.empty:

            print("✅ Contains Match Found")

            return contains_match.iloc[0]

        # ----------------------------------------------------
        # FUZZY SEARCH
        # ----------------------------------------------------

        fuzzy_result = self.fuzzy_search(query)

        if fuzzy_result is not None:

            print("✅ Fuzzy Match Found")

            return fuzzy_result

        # ----------------------------------------------------
        # SEMANTIC NLP SEARCH
        # ----------------------------------------------------

        semantic_result = self.semantic_search(query)

        if semantic_result is not None:

            print("✅ Semantic Match Found")

            return semantic_result

        print("❌ No Match Found")

        return None

    # ========================================================
    # GET COLUMN VALUES
    # ========================================================

    def get_values(self, row, keyword):

        values = []

        for col in row.index:

            if keyword.lower() in col.lower():

                value = row[col]

                if pd.notna(value):

                    value = str(value).strip()

                    invalid_values = [
                        "",
                        "nan",
                        "none",
                        "null"
                    ]

                    if value.lower() not in invalid_values:

                        values.append(value)

        values = list(dict.fromkeys(values))

        return values

    # ========================================================
    # AI SUMMARY
    # ========================================================

    def generate_ai_summary(
        self,
        medicine_name,
        salts,
        uses,
        side_effects
    ):

        try:

            prompt = f"""
You are a helpful medicine assistant.

Explain this medicine in simple,
beginner-friendly language.

Medicine:
{medicine_name}

Salts:
{salts}

Uses:
{uses}

Side Effects:
{side_effects}

Instructions:
- Explain simply
- Mention medicine purpose
- Mention common uses
- Mention side effects
- Avoid medical jargon
- Keep response short
"""

            completion = (
                self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=250
                )
            )

            return (
                completion
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            print("❌ AI Error:", e)

            return "AI Summary Unavailable."

    # ========================================================
    # FORMAT RESPONSE
    # ========================================================

    def format_response(self, row):

        if row is None:

            return """
# ❌ Medicine Not Found

Try:
- Dolo 650
- Crocin
- Calpol
- Azithromycin
"""

        medicine_name = row.get(
            "name",
            "Unknown Medicine"
        )

        salts = self.get_values(
            row,
            "salt"
        )

        if not salts:

            salts = self.get_values(
                row,
                "composition"
            )

        uses = self.get_values(
            row,
            "use"
        )

        side_effects = self.get_values(
            row,
            "side"
        )

        substitutes = self.get_values(
            row,
            "substitute"
        )

        # ----------------------------------------------------
        # AI SUMMARY
        # ----------------------------------------------------

        ai_summary = self.generate_ai_summary(
            medicine_name,
            salts,
            uses,
            side_effects
        )

        # ----------------------------------------------------
        # FORMAT TEXT
        # ----------------------------------------------------

        uses_text = (
            "\n".join(
                [f"- {u}" for u in uses[:10]]
            )
            if uses else
            "Not Available"
        )

        side_effects_text = (
            "\n".join(
                [f"- {s}" for s in side_effects[:10]]
            )
            if side_effects else
            "Not Available"
        )

        substitutes_text = (
            "\n".join(
                [f"- {s}" for s in substitutes[:10]]
            )
            if substitutes else
            "Not Available"
        )

        # ----------------------------------------------------
        # FINAL RESPONSE
        # ----------------------------------------------------

        response = f"""
# 💊 {medicine_name}

## 🧠 AI Summary
{ai_summary}

---

## ✅ Uses
{uses_text}

---

## ⚠️ Side Effects
{side_effects_text}

---

## 🔄 Substitutes
{substitutes_text}
"""

        return response


# ============================================================
# STREAMLIT UI
# ============================================================

st.set_page_config(
    page_title="AI MedicineBot",
    page_icon="💊",
    layout="centered"
)

st.title("💊 AI MedicineBot")

st.markdown(
    """
Search medicines using:

- Medicine names
- Symptoms
- Natural language
- AI semantic search
"""
)

# ============================================================
# INITIALIZE BOT
# ============================================================

@st.cache_resource
def load_bot():
    return MedicineBot()

bot = load_bot()

# ============================================================
# SEARCH INPUT
# ============================================================

query = st.text_input(
    "Enter medicine or symptoms:"
)

# ============================================================
# SEARCH BUTTON
# ============================================================

if st.button("Search"):

    if query.strip() == "":

        st.warning(
            "Please enter a medicine name."
        )

    else:

        with st.spinner(
            "Searching Medicine Database..."
        ):

            result = bot.search_medicine(query)

            response = (
                bot.format_response(result)
            )

            st.markdown(response)
```
