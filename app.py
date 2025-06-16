import os
import re

import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_chroma import Chroma
from flight_agent import agent as flight_agent


# 🔐 API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"
# 📚 Load Vector DB
persist_directory = "vector_db/blogs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# 🎯 Custom Prompt Template
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

# 🤖 LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash-002",
    temperature=0.3,
    google_api_key="AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"
)
# 🧠 Memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key="question",
        output_key="answer"
   )

memory = st.session_state.memory

# 🔗 QA Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": custom_prompt},
    output_key="answer"
)

# 🌐 Streamlit UI
st.set_page_config(page_title="Dubai Travel Assistant 🌴", page_icon="✈️")
st.title("Dubai Travel Assistant ✈️🇦🇪")

st.markdown("Ask me anything about your Dubai trip — itinerary, activities, and now flights too!")

# ✏️ User Input
user_input = st.text_input("Type your travel query here (e.g. plan trip for 4 days with 6-year-old):", key="input")

# 🗺️ Show chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📤 On Submit
if user_input:
    st.session_state.chat_history.append(("You", user_input))

    # ✈️ Flight keyword detection
    if "flight" in user_input.lower():
        with st.spinner("Checking flight options..."):
            # Example: extract pseudo slots
            origin = st.text_input("From (origin city):", key="origin")
            destination = st.text_input("To (destination city):", key="destination")
            dates = st.text_input("Travel dates:", key="dates")
            budget = st.text_input("Budget:", key="budget")

            if st.button("Find Flights ✈️"):
                try:
                    flight_response = flight_agent.run({
                        "origin": origin,
                        "destination": destination,
                        "dates": dates,
                        "budget": budget
                    })
                    st.session_state.chat_history.append(("Assistant (Flight Agent)", flight_response))
                except Exception as e:
                    st.error(f"Error fetching flights: {e}")
    else:
        with st.spinner("Thinking..."):
            response = qa_chain.run(user_input)
            st.session_state.chat_history.append(("Assistant", response))

# 💬 Display chat history
st.divider()
for role, message in st.session_state.chat_history:
    st.markdown(f"**{role}:** {message}")
