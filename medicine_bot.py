```python
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
# MEDICINE BOT
# ============================================================

class MedicineBot:

    # ========================================================
    # INITIALIZE
    # ========================================================

    def __init__(self):

        print("\n🚀 Initializing MedicineBot...\n")

        # ----------------------------------------------------
        # LOAD DATASET
        # ----------------------------------------------------

        self.df = self.load_dataset()

        # ----------------------------------------------------
        # SEARCH NAME
        # ----------------------------------------------------

        self.df["search_name"] = (
            self.df["name"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        # ----------------------------------------------------
        # NLP SEARCH TEXT
        # ----------------------------------------------------

        self.df["nlp_text"] = (
            self.df.astype(str)
            .apply(
                lambda row: " ".join(row),
                axis=1
            )
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

        self.nlp = spacy.load(
            "en_core_web_sm"
        )

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

        text = str(text).lower()

        remove_words = [
            "tablet",
            "tablets",
            "tab",
            "capsule",
            "capsules",
            "cap",
            "syrup",
            "medicine",
            "drug",
            "mg",
            "ml"
        ]

        for word in remove_words:

            text = text.replace(
                word,
                ""
            )

        text = re.sub(
            r'[^a-zA-Z0-9\s]',
            '',
            text
        )

        return " ".join(text.split())

    # ========================================================
    # CLEAN NLP QUERY
    # ========================================================

    def clean_query(self, query):

        query = query.lower()

        remove_patterns = [
            r'what is',
            r'what are',
            r'tell me about',
            r'uses of',
            r'side effects of',
            r'substitute for',
            r'substitutes for',
            r'medicine for',
            r'tablet for',
            r'capsule for',
            r'i have',
            r'suffering from',
            r'give me medicine for'
        ]

        for pattern in remove_patterns:

            query = re.sub(
                pattern,
                '',
                query
            )

        query = re.sub(
            r'[^a-zA-Z0-9\s]',
            '',
            query
        )

        return query.strip()

    # ========================================================
    # DETECT QUERY TYPE
    # ========================================================

    def detect_intent(self, query):

        query = query.lower()

        symptom_keywords = [
            "medicine for",
            "tablet for",
            "capsule for",
            "i have",
            "suffering from",
            "fever",
            "cold",
            "headache",
            "pain",
            "infection",
            "cough",
            "vomiting",
            "allergy"
        ]

        for word in symptom_keywords:

            if word in query:
                return "symptom"

        return "medicine"

    # ========================================================
    # NLP KEYWORDS
    # ========================================================

    def understand_query(self, query):

        doc = self.nlp(query)

        keywords = []

        for token in doc:

            if (
                not token.is_stop
                and not token.is_punct
            ):

                keywords.append(
                    token.text
                )

        return " ".join(keywords)

    # ========================================================
    # FUZZY SEARCH
    # ========================================================

    def fuzzy_search(self, query):

        query_clean = self.clean_text(
            query
        )

        result = process.extractOne(
            query_clean,
            self.medicine_names,
            scorer=fuzz.token_sort_ratio
        )

        if result is None:
            return None

        best_match_name = result[0]
        score = result[1]

        print("🔍 Fuzzy Score:", score)

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

        best_index = np.argmax(
            similarities
        )

        best_score = similarities[
            best_index
        ]

        print(
            "Semantic Score:",
            best_score
        )

        if best_score > 0.35:

            return self.df.iloc[
                best_index
            ]

        return None

    # ========================================================
    # SYMPTOM SEARCH
    # ========================================================

    def symptom_search(self, query):

        print("\n🧠 Running Symptom Search...")

        cleaned_query = self.clean_query(
            query
        )

        cleaned_query = (
            self.understand_query(
                cleaned_query
            )
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

        top_indices = (
            similarities.argsort()[-5:][::-1]
        )

        medicines = []

        for idx in top_indices:

            score = similarities[idx]

            if score > 0.30:

                medicines.append(
                    self.df.iloc[idx]
                )

        return medicines

    # ========================================================
    # SEARCH MEDICINE
    # ========================================================

    def search_medicine(self, query):

        intent = self.detect_intent(
            query
        )

        # ----------------------------------------------------
        # SYMPTOM SEARCH
        # ----------------------------------------------------

        if intent == "symptom":

            medicines = self.symptom_search(
                query
            )

            if not medicines:
                return None

            return medicines

        # ----------------------------------------------------
        # MEDICINE LOOKUP
        # ----------------------------------------------------

        query = self.clean_query(
            query
        )

        query_clean = self.clean_text(
            query
        )

        print(
            f"\n🔍 Searching: {query_clean}"
        )

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
        # STARTS WITH
        # ----------------------------------------------------

        starts_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.startswith(query_clean)
        ]

        if not starts_match.empty:

            print(
                "✅ Starts-With Match Found"
            )

            return starts_match.iloc[0]

        # ----------------------------------------------------
        # CONTAINS
        # ----------------------------------------------------

        contains_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.contains(
                query_clean,
                na=False
            )
        ]

        if not contains_match.empty:

            print("✅ Contains Match Found")

            return contains_match.iloc[0]

        # ----------------------------------------------------
        # FUZZY SEARCH
        # ----------------------------------------------------

        fuzzy_result = self.fuzzy_search(
            query_clean
        )

        if fuzzy_result is not None:

            print("✅ Fuzzy Match Found")

            return fuzzy_result

        # ----------------------------------------------------
        # SEMANTIC SEARCH
        # ----------------------------------------------------

        semantic_result = self.semantic_search(
            query
        )

        if semantic_result is not None:

            print("✅ Semantic Match Found")

            return semantic_result

        print("❌ No Match Found")

        return None

    # ========================================================
    # GET VALUES
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

                    if (
                        value.lower()
                        not in invalid_values
                    ):

                        values.append(value)

        values = list(
            dict.fromkeys(values)
        )

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

Explain this medicine simply.

Medicine:
{medicine_name}

Salts:
{salts}

Uses:
{uses}

Side Effects:
{side_effects}

Instructions:
- Beginner friendly
- Short response
- Avoid medical jargon
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

            return (
                "AI Summary Unavailable."
            )

    # ========================================================
    # FORMAT RESPONSE
    # ========================================================

    def format_response(self, row):

        # ----------------------------------------------------
        # MULTIPLE MEDICINES
        # ----------------------------------------------------

        if isinstance(row, list):

            response = (
                "# 💊 Recommended Medicines\n\n"
            )

            for medicine in row:

                medicine_name = medicine.get(
                    "name",
                    "Unknown Medicine"
                )

                uses = self.get_values(
                    medicine,
                    "use"
                )

                response += (
                    f"## {medicine_name}\n\n"
                )

                if uses:

                    response += "### Uses\n"

                    for use in uses[:3]:

                        response += (
                            f"- {use}\n"
                        )

                response += "\n---\n"

            return response

        # ----------------------------------------------------
        # NO RESULT
        # ----------------------------------------------------

        if row is None:

            return """
# ❌ Medicine Not Found

Try:
- Dolo 650
- Crocin
- Calpol
- Medicine for fever
- I have headache
"""

        # ----------------------------------------------------
        # SINGLE MEDICINE
        # ----------------------------------------------------

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
```
