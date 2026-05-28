import re
import zipfile

import pandas as pd
import streamlit as st
from groq import Groq
from rapidfuzz import fuzz, process


# =========================================================
# CONSTANTS
# =========================================================

REMOVE_WORDS = re.compile(
    r'\b(tablets?|tab|capsules?|cap|syrup|oral suspension|injection|mg|ml)\b',
    flags=re.IGNORECASE
)

STRENGTH_PATTERN = re.compile(r'(\d+)\s?(mg|ml)', re.IGNORECASE)

FUZZY_SCORE_CUTOFF  = 60
MAX_DISPLAY_ITEMS   = 10
AI_MAX_TOKENS       = 250
AI_TEMPERATURE      = 0.3
AI_MODEL            = "llama-3.1-8b-instant"

AI_PROMPT_TEMPLATE = """You are a helpful medicine assistant.

Explain this medicine in simple and beginner friendly language.

Medicine Name:
{medicine_name}

Salts / Composition:
{salts}

Uses:
{uses}

Instructions:
- Explain what the medicine is and mention common uses
- Mention what the salts do
- Keep it short under 75 words
- Avoid difficult medical jargon
- Make it easy to understand
"""


# =========================================================
# MEDICINE BOT
# =========================================================

class MedicineBot:

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(self):

        print("\n🚀 Initializing MedicineBot...\n")

        self.df     = self._load_dataset()
        self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])

        self._build_search_index()

        print("✅ MedicineBot Ready\n")

    # =====================================================
    # LOAD DATASET
    # =====================================================

    def _load_dataset(self) -> pd.DataFrame:

        zip_path = "Data/medicine_dataset.zip"

        with zipfile.ZipFile(zip_path) as z:
            csv_name = z.namelist()[0]
            with z.open(csv_name) as f:
                df = pd.read_csv(f, low_memory=False)

        print(f"✅ Dataset Loaded — {len(df):,} medicines")

        return df

    # =====================================================
    # BUILD SEARCH INDEX  (runs once at startup)
    # =====================================================

    def _build_search_index(self) -> None:
        """
        Pre-compute every derived column once so that
        search_medicine() never calls apply() at query time.
        """

        # Raw lowercase name (kept for display fallback)
        self.df["_raw_lower"] = (
            self.df["name"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        # Fully cleaned name — strip form-factor words & dosage
        self.df["_clean_name"] = self.df["_raw_lower"].map(self._clean_text)

        # Strength extracted once per row
        self.df["_strength"] = self.df["_raw_lower"].map(self._extract_strength)

        # The list rapidfuzz searches against
        self._clean_names: list[str] = self.df["_clean_name"].tolist()

        print("✅ Search Index Built")

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    @staticmethod
    def _clean_text(text: str) -> str:

        if not text or pd.isna(text):
            return ""

        text = REMOVE_WORDS.sub("", str(text).lower().strip())

        return " ".join(text.split())

    # =====================================================
    # EXTRACT STRENGTH
    # =====================================================

    @staticmethod
    def _extract_strength(text: str) -> str | None:

        m = STRENGTH_PATTERN.search(str(text))

        return m.group(1) if m else None

    # =====================================================
    # SEARCH MEDICINE
    # =====================================================

    def search_medicine(self, query: str) -> pd.Series | None:

        query_clean    = self._clean_text(query)
        query_strength = self._extract_strength(query)

        print(f"\n🔍 Searching: '{query_clean}'")

        # 1. Exact match
        mask = self.df["_clean_name"] == query_clean
        if mask.any():
            print("✅ Exact match")
            return self.df[mask].iloc[0]

        # 2. Starts-with match
        mask = self.df["_clean_name"].str.startswith(query_clean, na=False)
        if mask.any():
            print("✅ Starts-with match")
            return self.df[mask].iloc[0]

        # 3. Contains match
        mask = self.df["_clean_name"].str.contains(query_clean, na=False, regex=False)
        if mask.any():
            print("✅ Contains match")
            return self.df[mask].iloc[0]

        # 4. Fuzzy match  (vectorized — no Python loop)
        result = process.extractOne(
            query_clean,
            self._clean_names,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=FUZZY_SCORE_CUTOFF,
        )

        if result:
            matched_name, score, idx = result

            # Apply strength penalty / bonus without re-looping
            row = self.df.iloc[idx]
            if query_strength:
                if row["_strength"] == query_strength:
                    score += 10
                else:
                    score -= 20

            if score >= FUZZY_SCORE_CUTOFF:
                print(f"✅ Fuzzy match — '{matched_name}' (score: {score})")
                return row

        print("❌ No match found")

        return None

    # =====================================================
    # GET COLUMN VALUES  (keyword search across columns)
    # =====================================================

    @staticmethod
    def _get_values(row: pd.Series, keyword: str) -> list[str]:

        keyword_lower = keyword.lower()

        invalid = {"", "nan", "none", "null"}

        values = []

        for col in row.index:

            if keyword_lower not in col.lower():
                continue

            val = row[col]

            if pd.isna(val):
                continue

            val = str(val).strip()

            if val.lower() not in invalid:
                values.append(val)

        # Preserve order, remove duplicates
        return list(dict.fromkeys(values))

    # =====================================================
    # GENERATE AI SUMMARY
    # =====================================================

    def _generate_ai_summary(
        self,
        medicine_name: str,
        salts: list[str],
        uses: list[str],
    ) -> str:

        prompt = AI_PROMPT_TEMPLATE.format(
            medicine_name=medicine_name,
            salts=", ".join(salts) if salts else "Not available",
            uses=", ".join(uses[:5]) if uses else "Not available",
        )

        try:
            completion = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=AI_TEMPERATURE,
                max_tokens=AI_MAX_TOKENS,
            )

            return completion.choices[0].message.content

        except Exception as e:
            print(f"❌ Groq Error: {e}")
            return "AI Summary Unavailable."

    # =====================================================
    # FORMAT RESPONSE
    # =====================================================

    def format_response(self, row: pd.Series | None) -> str:

        if row is None:
            return (
                "# ❌ Medicine Not Found\n\n"
                "Oops! Please search with the medicine name only — e.g. **Dolo 650**"
            )

        medicine_name = row.get("name", "Unknown Medicine")

        # Collect fields
        salts       = self._get_values(row, "salt") or self._get_values(row, "composition")
        uses        = self._get_values(row, "use")
        side_effects = self._get_values(row, "side")
        substitutes  = self._get_values(row, "substitute")

        ai_summary = self._generate_ai_summary(medicine_name, salts, uses)

        def bullet_list(items: list[str], limit: int = MAX_DISPLAY_ITEMS) -> str:
            return (
                "\n".join(f"- {i}" for i in items[:limit])
                if items else "Not Available"
            )

        return (
            f"# {medicine_name}\n\n"
            f"## AI Summary\n{ai_summary}\n\n"
            "---\n\n"
            f"## Uses\n{bullet_list(uses)}\n\n"
            "---\n\n"
            f"## Side Effects\n{bullet_list(side_effects)}\n\n"
            "---\n\n"
            f"## 🔄 Substitutes\n{bullet_list(substitutes)}"
        )
