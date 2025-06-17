
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
git clone https://github.com/yourusername/dubai-travel-agent.git
cd dubai-travel-agent
```


2. Create and activate a virtual environment
macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows
```bash
python -m venv venv
venv\Scripts\activate
```


3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set environment variables
 ```bash
GOOGLE_API_KEY=your_gemini_api_key
```

5. The required installations are
```bash
pip install streamlit langchain google-generativeai langchain-google-genai chromadb tiktoken
```

6. Run the Streamlit
```bash
streamlit run app.py
```


travel_agent/
├── app.py                  # Streamlit frontend
├── ingest.py               # Script to load travel blogs into Chroma DB
├── vectorstore/ # Local vector DB folder
    └── vectordb
├── tester.py               # Test Gemini model + list available models
├── requirements.txt        # Dependencies
├── agents/        # Dependencies
    └── blog_agent.py


