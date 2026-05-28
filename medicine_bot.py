import pandas as pd
import streamlit as st
from rapidfuzz import process, fuzz
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

        # -------------------------------------------------
        # REMOVE QUESTION PHRASES
        # -------------------------------------------------

        question_patterns = [
            "what is",
            "used for",
            "tell me about",
            "about",
            "can i use",
            "how to use",
            "side effects of",
            "uses of",
            "benefits of",
            "for what",
            "why use",
            "medicine for",
        ]

        for pattern in question_patterns:

            text = re.sub(
                rf"\b{pattern}\b",
                "",
                text,
                flags=re.IGNORECASE
            )

        # -------------------------------------------------
        # REMOVE SYMBOLS
        # -------------------------------------------------

        text = re.sub(
            r"[^a-zA-Z0-9\s]",
            " ",
            text
        )

        # -------------------------------------------------
        # REMOVE COMMON MEDICINE WORDS
        # -------------------------------------------------

        remove_words = [
            "tablet",
            "tablets",
            "tab",
            "capsule",
            "capsules",
            "cap",
            "syrup",
            "oral",
            "suspension",
            "injection",
            "mg",
            "ml"
        ]

        for word in remove_words:

            text = re.sub(
                rf"\b{word}\b",
                "",
                text
            )

        # -------------------------------------------------
        # REMOVE EXTRA SPACES
        # -------------------------------------------------

        text = re.sub(r"\s+", " ", text)

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
    # SEARCH MEDICINE (UPDATED TO WORD-BY-WORD BREAKDOWN)
    # =====================================================

    def search_medicine(self, query):

        # Extract strength from the overall query to use for dosage matching bonus
        query_strength = self.extract_strength(query)
        
        # Clean the sentence and break it down into independent words
        cleaned_query = self.clean_text(query)
        words = [w for w in cleaned_query.split(" ") if w.strip()]

        print(f"\n📝 Parsed search terms from sentence: {words}")

        # Check each word sequentially until a valid medicine match is found
        for query_clean in words:
            
            # Skip short words or single letters that pass through the filter (e.g. "a", "i")
            if len(query_clean) <= 1:
                continue

            print(f"🔍 Testing word: '{query_clean}'")

            # 1. EXACT MATCH
            exact_match = self.df[
                self.df["search_name"].apply(self.clean_text) == query_clean
            ]
            if not exact_match.empty:
                print(f"✅ Exact Match Found for '{query_clean}'")
                return exact_match.iloc[0]

            # 2. STARTS WITH MATCH
            starts_match = self.df[
                self.df["search_name"]
                .apply(self.clean_text)
                .str.startswith(query_clean)
            ]
            if not starts_match.empty:
                print(f"✅ Starts-With Match Found for '{query_clean}'")
                return starts_match.iloc[0]

            # 3. CONTAINS MATCH
            contains_match = self.df[
                self.df["search_name"]
                .apply(self.clean_text)
                .str.contains(query_clean, na=False)
            ]
            if not contains_match.empty:
                print(f"✅ Contains Match Found for '{query_clean}'")
                return contains_match.iloc[0]

            # 4. FUZZY MATCH
            best_match = None
            best_score = 0

            for _, row in self.df.iterrows():
                medicine_name = row["search_name"]
                cleaned_name = self.clean_text(medicine_name)

                score = fuzz.token_sort_ratio(query_clean, cleaned_name)

                # Dosage match bonus
                med_strength = self.extract_strength(medicine_name)
                if query_strength and med_strength:
                    if query_strength == med_strength:
                        score += 10
                    else:
                        score -= 20

                if score > best_score:
                    best_score = score
                    best_match = row

            if best_match is not None and best_score >= 60:
                print(f"\n🔍 Closest Fuzzy Match Found for '{query_clean}'")
                print("Medicine:", best_match["name"])
                print("Score:", best_score)
                return best_match

        print("❌ No Match Found for any word in the sentence.")
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
        salts
    ):

        try:

            prompt = f"""
You are a helpful medicine assistant.

Explain this medicine in simple and beginner friendly language.

Medicine Name:
{medicine_name}

Salts / Composition:
{salts}

Instructions:
- Explain what the medicine is and mention common uses
- Mention what the salts do
- Keep it very short less than 100 words
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
            salts
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
# {medicine_name}

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
