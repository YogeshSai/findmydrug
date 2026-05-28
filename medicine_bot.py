import pandas as pd
import streamlit as st
from rapidfuzz import fuzz
from groq import Groq
import zipfile
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
        # SEARCH COLUMN
        # -------------------------------------------------

        self.df["search_name"] = (
            self.df["name"]
            .astype(str)
            .str.lower()
            .str.strip()
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

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    def clean_text(self, text):

        if pd.isna(text):
            return ""

        text = str(text).lower().strip()

        # Remove symbols

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        # Remove extra spaces

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

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
    # AI MEDICINE EXTRACTION
    # =====================================================

    def extract_medicine_name(self, query):

        try:

            prompt = f"""
You are a medicine name extraction AI.

Your task:
Extract ONLY the medicine name from the user query.

IMPORTANT:
- User MUST mention a medicine name
- If user only mentions symptoms or disease,
  return NONE

Examples:

User: What is dolo 650 used for
Output: dolo 650

User: Tell me about azithromycin
Output: azithromycin

User: Can I use frisium tablet
Output: frisium

User: I have fever
Output: NONE

User: Medicine for headache
Output: NONE

User: What should I take for cough
Output: NONE

Return ONLY the medicine name.
No explanation.
No punctuation.

User Query:
{query}
"""

            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0,
                max_tokens=20
            )

            medicine = (
                completion
                .choices[0]
                .message
                .content
                .strip()
                .lower()
            )

            if medicine == "none":
                return None

            return medicine

        except Exception as e:

            print("❌ AI Extraction Error:", e)

            return None

    # =====================================================
    # SEARCH MEDICINE
    # =====================================================

    def search_medicine(self, query):

        # -------------------------------------------------
        # AI EXTRACTION
        # -------------------------------------------------

        extracted_name = self.extract_medicine_name(query)

        print("\n🤖 Extracted Medicine:", extracted_name)

        # Reject symptom-based queries

        if extracted_name is None:

            return "NO_MEDICINE"

        query = extracted_name

        # -------------------------------------------------
        # CLEAN QUERY
        # -------------------------------------------------

        cleaned_query = self.clean_text(query)

        query_strength = self.extract_strength(query)

        # -------------------------------------------------
        # EXACT MATCH
        # -------------------------------------------------

        exact_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            == cleaned_query
        ]

        if not exact_match.empty:

            print("✅ Exact Match")

            return exact_match.iloc[0]

        # -------------------------------------------------
        # STARTS WITH
        # -------------------------------------------------

        starts_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.startswith(cleaned_query)
        ]

        if not starts_match.empty:

            print("✅ Starts-With Match")

            return starts_match.iloc[0]

        # -------------------------------------------------
        # CONTAINS
        # -------------------------------------------------

        contains_match = self.df[
            self.df["search_name"]
            .apply(self.clean_text)
            .str.contains(cleaned_query, na=False)
        ]

        if not contains_match.empty:

            print("✅ Contains Match")

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
                cleaned_query,
                cleaned_name
            )

            # Strength bonus

            med_strength = self.extract_strength(
                medicine_name
            )

            if query_strength and med_strength:

                if query_strength == med_strength:
                    score += 10
                else:
                    score -= 20

            if score > best_score:

                best_score = score

                best_match = row

        if best_match is not None and best_score >= 60:

            print("✅ Fuzzy Match")

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

                    invalid = [
                        "",
                        "nan",
                        "none",
                        "null"
                    ]

                    if value.lower() not in invalid:

                        values.append(value)

        values = list(dict.fromkeys(values))

        return values

    # =====================================================
    # AI SUMMARY
    # =====================================================

    def generate_ai_summary(
        self,
        medicine_name,
        salts
    ):

        try:

            prompt = f"""
Explain this medicine simply.

Medicine:
{medicine_name}

Composition:
{salts}

Rules:
- Keep under 80 words
- Beginner friendly
- Mention what medicine is commonly used for
- Simple language
"""

            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=120
            )

            return (
                completion
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            print("❌ Summary Error:", e)

            return "AI Summary Unavailable."

    # =====================================================
    # FORMAT RESPONSE
    # =====================================================

    def format_response(self, row):

        # -------------------------------------------------
        # SYMPTOM QUERY BLOCK
        # -------------------------------------------------

        if row == "NO_MEDICINE":

            return """
# ❌ Medicine Name Required

Please enter a medicine name.

Examples:
- Dolo 650
- Crocin
- Frisium
- Azithromycin
"""

        # -------------------------------------------------
        # NOT FOUND
        # -------------------------------------------------

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
        # SALTS
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
        # VALUES
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
            salts
        )

        # -------------------------------------------------
        # FORMAT
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
# {medicine_name}

## AI Summary
{ai_summary}

---

## Uses
{uses_text}

---

## Side Effects
{side_effects_text}

---

## Substitutes
{substitutes_text}
"""

        return response
