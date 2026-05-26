<div align="center">

<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
<img src="https://img.shields.io/badge/Grok_AI-000000?style=for-the-badge&logo=x&logoColor=white" />
<img src="https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />

# 💊 FindMyDrug

### An AI-powered Indian Medicinal Chatbot

> Query over **2,00,000+ Indian drugs** in plain language — get instant, intelligent answers powered by Grok AI and Hugging Face.

**[🚀 Live Demo →](https://findmydrug.streamlit.app/)**

</div>

---

## 🌿 About

**FindMyDrug** is an AI-powered chatbot built specifically for the Indian pharmaceutical landscape. It lets users search, query, and learn about medicines using natural language — backed by a massive dataset of 2 lakh+ drugs and augmented by large language model intelligence.

Whether you're a patient, caregiver, pharmacist, or healthcare professional, FindMyDrug bridges the gap between complex drug data and accessible, conversational answers.

---

## ✨ Features

- 🔍 **Natural Language Drug Search** — Ask questions like *"What is Paracetamol used for?"* or *"Side effects of Metformin?"*
- 🧠 **AI-Powered Responses** — Grok AI at the backend delivers accurate, context-aware answers
- 📦 **2,00,000+ Drug Database** — Comprehensive Indian pharmaceutical dataset covering generics, branded drugs, compositions, and more
- 🤗 **Hugging Face Integration** — LLM data enhancement for richer, more nuanced responses
- ⚡ **Streamlit Frontend** — Clean, fast, and interactive UI accessible directly in the browser
- 🇮🇳 **India-Focused** — Tailored specifically to the Indian drug market and nomenclature

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) |
| **AI Backend** | [Grok AI](https://x.ai/) |
| **LLM Enhancement** | [Hugging Face](https://huggingface.co/) |
| **Dataset** | 2,00,000+ Indian Drug Records |
| **Language** | Python |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YogeshSai/findmydrug.git
cd findmydrug

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the root directory and add your API keys:

```env
GROK_API_KEY=your_grok_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

### Run Locally

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

## 💬 Example Queries

```
"What are the uses of Azithromycin?"
"Is Pantoprazole safe during pregnancy?"
"What is the composition of Dolo 650?"
"Alternatives to Crocin?"
"Side effects of long-term Omeprazole use?"
```

---

## 📊 Dataset

The underlying dataset contains **2,00,000+ Indian pharmaceutical records**, including:

- Drug names (generic & branded)
- Compositions & salt combinations
- Therapeutic uses & indications
- Dosage information
- Manufacturer details
- Side effects & contraindications

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the dataset, enhance the AI pipeline, or improve the UI:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## ⚠️ Disclaimer

> FindMyDrug is intended for **informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before making any medical decisions.

---

## 📄 License

This project is open source. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ for India's healthcare ecosystem

**[Try it live →](https://findmydrug.streamlit.app/)**

</div>
