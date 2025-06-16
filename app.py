import os
import re
import streamlit as st
from flight_agent import agent as flight_agent
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma  # ✅ Updated import

# 🔐 API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"

# 📚 Load Vector DB
persist_directory = "vector_db/blogs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# 🧠 Prompt Template
custom_prompt = PromptTemplate(
    input_variables=["chat_history", "question", "context"],
    template="""
You are a helpful Dubai travel planning assistant.

Use the following travel blog content:
{context}

Conversation so far:
{chat_history}

User asked:
{question}

If the user hasn't mentioned how many days they're staying, politely ask them.
If days and child age are mentioned, generate a personalized itinerary with activities that suit their stay and the child’s age.
Be concise, realistic, and helpful.
"""
)

# 🤖 LLM Setup
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-002",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="question",  # if you're passing {"question": user_input}
    output_key="answer"    # match your output format
)


# 🧠 Memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",   # ✅ Only once
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
st.title("Dubai Travel Assistant ✈️🇦🇪")
st.markdown("Ask me anything about your Dubai trip — itinerary, activities, and now flights too!")

# ✅ State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "flight_requested" not in st.session_state:
    st.session_state.flight_requested = False

# 📝 User Input
user_input = st.chat_input("Ask something...")

# 🚦 Input Handling
if user_input:
    if "flight" in user_input.lower() and not st.session_state.flight_requested:
        st.session_state.flight_requested = True
        st.session_state.chat_history.append(("You", user_input))

    elif "flight" not in user_input.lower():
        st.session_state.chat_history.append(("You", user_input))
        with st.spinner("Thinking..."):
            response = qa_chain.run({"question": user_input})
            # response = qa_chain.run({"input": user_input})
            st.session_state.chat_history.append(("Assistant", response))

# ✈️ Flight Form
if st.session_state.flight_requested:
    with st.spinner("Checking flight options..."):
        origin = st.text_input("From (origin city):", key="origin")
        destination = st.text_input("To (destination city):", key="destination")
        dates = st.text_input("Travel dates (YYYY-MM-DD):", key="dates")
        budget = st.text_input("Budget (INR, optional):", key="budget")

        if st.button("Find Flights ✈️"):
            
            try:
                query = f"I want to find flights from {origin} to {destination} on {dates}."
                if budget:
                    query += f" My budget is ₹{budget}."

                flight_response = flight_agent.run(query)
                st.session_state.chat_history.append(("Assistant (Flight Agent)", flight_response))
                st.session_state.flight_requested = False
                st.session_state.flight_options = offers[:3] 
                if "book option" in user_input.lower():
                    option_number = int(user_input.strip().split("option")[-1]) - 1
                    selected_flight = st.session_state.get("flight_options", [])[option_number]
    


            except Exception as e:
                st.error(f"Error fetching flights: {e}")
                st.session_state.flight_requested = False

def book_flight(flight_offer):
    # In real scenario, you'd call Amadeus booking APIs
    airline = flight_offer["itineraries"][0]["segments"][0]["carrierCode"]
    departure = flight_offer["itineraries"][0]["segments"][0]["departure"]["at"]
    price = flight_offer["price"]["total"]
    return f"✅ Booking confirmed!\nAirline: {airline}, Departure: {departure}, Price: ₹{price}"

# 💬 Chat History Display
st.divider()
for role, message in st.session_state.chat_history:
    st.markdown(f"**{role}:**\n\n{message}")

