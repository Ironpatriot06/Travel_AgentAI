import os
import re
import json
import streamlit as st
from flight_agent import agent as flight_agent
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma

# 🔐 API Key
os.environ["GOOGLE_API_KEY"] = "your_api_key"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"

# 📚 Load Vector DB
persist_directory = "vector_db/blogs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# 🧠 Prompt Template
custom_prompt = PromptTemplate(
    input_variables=["chat_history", "question", "context", "num_days", "child_age"],
    template="""
You are a helpful Dubai travel planning assistant.

Use the following travel blog content:
{context}

Conversation so far:
{chat_history}

Trip info:
- Days staying: {num_days}
- Child age: {child_age}

User asked:
{question}

Instructions:
- If any of the above fields are \"None\", politely ask for them.
- Once you know all three (days, child age, budget), generate a personalized Dubai itinerary.
- Do NOT ask again if already known.

Be concise, realistic, and helpful.
"""
)

# 🤖 LLM Setup
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-002",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# 🧠 Memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="output"
    )

memory = st.session_state.memory

# 🔗 QA Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": custom_prompt},
    output_key="output"
)

# 🌐 Streamlit UI
st.set_page_config(page_title="Dubai Travel Assistant 🌴", page_icon="✈️")
st.markdown("""
    <h1 style='text-align: center;'>Dubai Travel Assistant ✈️🇦🇪</h1>
    <p style='text-align: center;'>Ask about itineraries, activities, and flights — we’ve got you covered!</p>
""", unsafe_allow_html=True)

if "num_days" not in st.session_state:
    st.session_state.num_days = 3  # or None if you prefer

if "child_age" not in st.session_state:
    st.session_state.child_age = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Trip Preferences
with st.sidebar:
    st.header("🧳 Trip Preferences")
    st.session_state.num_days = st.number_input("Days Staying", min_value=1, max_value=30, step=1,
                                                value=st.session_state.num_days or 3)
    st.session_state.child_age = st.number_input("Child Age (if any)", min_value=0, max_value=18,
                                                 value=st.session_state.child_age or 0)
    if st.button("🔄 Reset Conversation"):
        st.session_state.chat_history = []
        st.session_state.flight_requested = False

# ✅ State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "flight_requested" not in st.session_state:
    st.session_state.flight_requested = False

# 📝 User Input
user_input = st.chat_input("Ask something about your Dubai trip...")

if user_input:
    days_match = re.search(r"\b(\d+)\s*(days|day)\b", user_input.lower())
    if days_match:
        st.session_state.num_days = int(days_match.group(1))

    age_match = re.search(r"\b(\d+)\s*(years|year)\s*old\b", user_input.lower())
    if age_match:
        st.session_state.child_age = int(age_match.group(1))

    if "flight" in user_input.lower() and not st.session_state.flight_requested:
        st.session_state.flight_requested = True
        st.session_state.chat_history.append(("You", user_input))

    elif "flight" not in user_input.lower():
        st.session_state.chat_history.append(("You", user_input))
        with st.spinner("🧠 Thinking..."):
            response = qa_chain.run({
                "question": user_input,
                "num_days": st.session_state.num_days or "None",
                "child_age": st.session_state.child_age or "None"
            })
            st.session_state.chat_history.append(("Assistant", response))

# ✈️ Flight Form
if st.session_state.flight_requested:
    st.markdown("### ✈️ Flight Search")
    with st.spinner("Fetching flight options..."):
        origin = st.text_input("From (Origin City):", key="origin")
        destination = st.text_input("To (Destination City):", key="destination")
        dates = st.text_input("Travel Dates (YYYY-MM-DD):", key="dates")
        budget = st.text_input("Budget (INR, optional):", key="budget")

        if st.button("🔍 Find Flights"):
            try:
                query = f"I want to find flights from {origin} to {destination} on {dates}."
                if budget:
                    query += f" My budget is ₹{budget}."
                flight_response = flight_agent.run(query)
                st.session_state.chat_history.append(("Assistant (Flight Agent)", flight_response))
                st.session_state.flight_requested = False

                if flight_response.strip().startswith("["):
                    offers = json.loads(flight_response)
                    if offers:
                        st.session_state.flight_options = offers[:3]
                        for idx, offer in enumerate(offers[:3], start=1):
                            st.markdown(f"""
                                <div style='border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;'>
                                    <b>Option {idx}</b><br>
                                    ✈️ <strong>Airline:</strong> {offer['airline']}<br>
                                    🕓 <strong>Departure:</strong> {offer['departure']}<br>
                                    🛬 <strong>Arrival:</strong> {offer['arrival']}<br>
                                    💰 <strong>Price:</strong> {offer['price']}
                                </div>
                            """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error fetching flights: {e}")

# 💬 Chat History
st.markdown("---")
st.markdown("### 💬 Conversation")
for role, message in st.session_state.chat_history:
    
    st.markdown(f"""
        <div style='padding:10px; border-radius:10px; margin-bottom:10px;'>
            <b>{role}:</b><br>{message}
        </div>
    """, unsafe_allow_html=True)

def book_flight(flight_offer):
    airline = flight_offer["itineraries"][0]["segments"][0]["carrierCode"]
    departure = flight_offer["itineraries"][0]["segments"][0]["departure"]["at"]
    price = flight_offer["price"]["total"]
    return f"✅ Booking confirmed!\nAirline: {airline}, Departure: {departure}, Price: ₹{price}"
