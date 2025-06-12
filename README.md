# 🏝️ Dubai Travel Assistant Chatbot

This project is an interactive **travel planning assistant** built with **LangChain**, **Google Gemini**, and **Streamlit**. It allows users to chat with a bot that can answer queries based on **scraped travel blogs** and even **generate a personalized itinerary** for a family trip to Dubai.

---

## ✨ Features

- 🔍 **Semantic search** over scraped travel blogs using a vector database (Chroma).
- 💬 **Conversational chatbot** using Google Gemini Pro (via LangChain).
- 🗺️ **Personalized itinerary generation** based on user preferences.
- 🧠 Context memory so the assistant remembers previous messages.
- 🧾 Built with modular, clean Python for extensibility.

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Ironpatriot06/Travel_AgentAI.git
cd Travel_AgentAI
```

FOR MacOS
```bash
python3 -m venv venv
source venv/bin/activate
```

FOR Windows
```bash
python -m venv venv
venv\Scripts\activate
```
The required installations are
```bash
pip install streamlit langchain google-generativeai langchain-google-genai chromadb tiktoken
```

Put your Gemini API key in app.py 
```bash
GOOGLE_API_KEY=your_gemini_api_key
```

To run the Streamlit 
```bash
streamlit run app.py
```
