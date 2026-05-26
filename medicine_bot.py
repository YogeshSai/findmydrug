import pandas as pd
import streamlit as st
from rapidfuzz import process, fuzz
from groq import Groq
import re


class MedicineBot:

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(self):

        print("\n🚀 Initializing MedicineBot...\n")

        # -------------------------------------------------
        # LOAD DATASET
        # -------------------------------------------------

        self.df = self.load_dataset()

        # -------------------------------------------------
        # CREATE SEARCH COLUMN
        # -------------------------------------------------

        self.df["search_name"] = (
            self.df["name"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        # -------------------------------------------------
        # MEDICINE NAMES
        # -------------------------------------------------

        self.medicine_names = (
            self.df["search_name"]
            .dropna()
            .tolist()
        )

        # -------------------------------------------------
        # GROQ CLIENT
        # -------------------------------------------------

        self.client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
        )

        print("✅ MedicineBot Ready\n")

    # =====================================================
    # LOAD DATASET
    # =====================================================

    def load_dataset(self):

        path = "Data/medicine_dataset.csv"

        df = pd.read_csv(
            path,
            low_memory=False
        )

        print("✅ Dataset Loaded")
        print(f"📦 Total Medicines: {len(df)}")

        print("\n📋 Dataset Columns:")
        print(df.columns.tolist())

        return df

    # =====================================================
    # CLEAN TEXT
    # =====================================================

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

    # =====================================================
    # EXTRACT STRENGTH
    # =====================================================

    def extract_strength(self, text):

        text = str(text).lower()

        match = re.search(
            r'(\d+)\s?(mg|ml)',
            text
        )

        if match:
            return match.group(1)

        return None

    # =====================================================
    # SEARCH MEDICINE
    # =====================================================

    def search_medicine(self, query):

        query_clean = self.clean_text(query)

        print(f"\n🔍 Searching for: {query_clean}")

        query_strength = (
            self.extract_strength(query)
        )

        # -------------------------------------------------
        # EXACT MATCH
        # -------------------------------------------------

        exact_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text) == query_clean
        ]

        if not exact_match.empty:

            print("✅ Exact Match Found")

            return exact_match.iloc[0]

        # -------------------------------------------------
        # STARTS WITH MATCH
        # -------------------------------------------------

        starts_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.startswith(query_clean)
        ]

        if not starts_match.empty:

            print("✅ Starts-With Match Found")

            return starts_match.iloc[0]

        # -------------------------------------------------
        # CONTAINS MATCH
        # -------------------------------------------------

        contains_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.contains(query_clean, na=False)
        ]

        if not contains_match.empty:

            print("✅ Contains Match Found")

            return contains_match.iloc[0]

        # -------------------------------------------------
        # FUZZY MATCH
        # -------------------------------------------------

        best_match = None
        best_score = 0

        for _, row in self.df.iterrows():

            medicine_name = row["search_name"]

            cleaned_name = self.clean_text(
                medicine_name
            )

            score = fuzz.token_sort_ratio(
                query_clean,
                cleaned_name
            )

            # ---------------------------------------------
            # DOSAGE MATCH BONUS
            # ---------------------------------------------

            med_strength = (
                self.extract_strength(
                    medicine_name
                )
            )

            if (
                query_strength
                and med_strength
            ):

                if query_strength == med_strength:
                    score += 10

                else:
                    score -= 20

            # ---------------------------------------------
            # SAVE BEST MATCH
            # ---------------------------------------------

            if score > best_score:

                best_score = score
                best_match = row

        # -------------------------------------------------
        # FINAL RESULT
        # -------------------------------------------------

        if best_match is not None:

            print("\n🔍 Closest Match Found")
            print("Medicine:", best_match["name"])
            print("Score:", best_score)

            if best_score >= 60:
                return best_match

        print("❌ No Match Found")

        return None

    # =====================================================
    # GET VALUES
    # =====================================================

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

        # Remove duplicates
        values = list(dict.fromkeys(values))

        return values

    # =====================================================
    # GENERATE AI SUMMARY
    # =====================================================

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

Explain this medicine in simple and beginner friendly language.

Medicine Name:
{medicine_name}

Salts / Composition:
{salts}

Uses:
{uses}

Side Effects:
{side_effects}

Instructions:
- Explain what the medicine is
- Mention what the salts do
- Mention common uses
- Mention important side effects
- Keep it short
- Avoid difficult medical jargon
- Make it easy to understand
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

            print("❌ Groq Error:", e)

            return "AI Summary Unavailable."

    # =====================================================
    # FORMAT RESPONSE
    # =====================================================

    def format_response(self, row):

        if row is None:

            return """
# ❌ Medicine Not Found

Try searching:
- Dolo 650
- Crocin
- Calpol
- Azithromycin
"""

        # -------------------------------------------------
        # BASIC DETAILS
        # -------------------------------------------------

        medicine_name = row.get(
            "name",
            "Unknown Medicine"
        )

        # -------------------------------------------------
        # SALTS / COMPOSITION
        # -------------------------------------------------

        salts = self.get_values(
            row,
            "salt"
        )

        if not salts:

            salts = self.get_values(
                row,
                "composition"
            )

        # -------------------------------------------------
        # EXTRACT VALUES
        # -------------------------------------------------

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

        # -------------------------------------------------
        # AI SUMMARY
        # -------------------------------------------------

        ai_summary = self.generate_ai_summary(
            medicine_name,
            salts,
            uses,
            side_effects
        )

        # -------------------------------------------------
        # FORMAT TEXT
        # -------------------------------------------------

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

        # -------------------------------------------------
        # FINAL RESPONSE
        # -------------------------------------------------

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
