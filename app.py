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

os.environ["GOOGLE_API_KEY"] = "your_api_key"
os.environ["GOOGLE_API_KEY"] = "AIzaSyCfbPlEBg4QQF4CwuROqvyn_ZCpKos3Frc"

# 📚 Load Vector DB
persist_directory = "vector_db/blogs"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)
retriever = vectordb.as_retriever(search_kwargs={"k": 8})

# 🧠 Prompt Template
custom_prompt = PromptTemplate(
    input_variables=["chat_history", "question", "context", "num_days", "child_age", "budget", "num_people"],
    template="""
You are a helpful Dubai travel planning assistant.

Use the following travel blog content:
{context}

User Info:
- Days staying: {num_days}
- Child age: {child_age}
- Budget: {budget}
- Number of travelers: {num_people}

Conversation so far:
{chat_history}

User asked:
{question}

Instructions:
- If any of the fields above are "None", politely ask ONLY for the missing ones.
- Otherwise, answer the question or generate the itinerary.
- Do NOT ask again for values already provided.
- Do NOT infer from chat_history — trust the passed fields instead.

Be helpful, concise, and avoid repetition.
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

if "num_days" not in st.session_state:
    st.session_state.num_days = None

if "child_age" not in st.session_state:
    st.session_state.child_age = None

if "budget" not in st.session_state:
    st.session_state.budget = None

if "flight_requested" not in st.session_state:
    st.session_state.flight_requested = False

if "num_people" not in st.session_state:
    st.session_state.num_people = None


# 📝 User Input
user_input = st.chat_input("Ask something...")




if user_input:
    # Check for days
    days_match = re.search(r"\b(\d+)\s*(days|day)\b", user_input.lower())
    if days_match:
        st.session_state.num_days = int(days_match.group(1))
        st.session_state.chat_history.append(("Assistant", f"Got it — planning for {st.session_state.num_days} days!"))


    # Check for child age
    age_match = re.search(r"\b(\d+)\s*(years|year)\s*old\b", user_input.lower())
    if age_match:
        st.session_state.child_age = int(age_match.group(1))

    # Check for people
    people_match = re.search(r"\b(\d+)\s*(adults|people|persons|travelers|members)\b", user_input.lower())
    if people_match:
        st.session_state.num_people = int(people_match.group(1))
        st.session_state.chat_history.append(("Assistant", f"Noted — {st.session_state.num_people} people traveling."))

    # Check for budget
    budget_match = re.search(r"(\d{1,3}(?:,\d{3})+|\d+)\s*(inr|rs|rupees)?", user_input.lower())
    if budget_match:
        budget_clean = budget_match.group(1).replace(",", "")
        st.session_state.budget = int(budget_clean)
        st.session_state.chat_history.append(("Assistant", f"Great! Budget is ₹{st.session_state.budget}."))


# 🚦 Input Handling
if user_input:
    # extract days, age, budget...
    ...
    
    if "flight" in user_input.lower() and not st.session_state.flight_requested:
        st.session_state.flight_requested = True
        st.session_state.chat_history.append(("You", user_input))

    elif "flight" not in user_input.lower():
        st.session_state.chat_history.append(("You", user_input))
        with st.spinner("Thinking..."):
            response = qa_chain.run({
                "question": user_input,
                "num_days": str(st.session_state.num_days) if st.session_state.num_days is not None else "None",
                "child_age": str(st.session_state.child_age) if st.session_state.child_age is not None else "None",
                "budget": str(st.session_state.budget) if st.session_state.budget is not None else "None",
                "num_people": str(st.session_state.num_people) if st.session_state.num_people is not None else "None"
            })
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

                # st.markdown("### Raw Flight Response")
                # st.code(flight_response)

                # ✅ Parse response only if it looks like JSON
                import json
                if flight_response.strip().startswith("["):
                    offers = json.loads(flight_response)
                    if offers:
                        st.session_state.flight_options = offers[:3]

                        for idx, offer in enumerate(offers[:3], start=1):
                            st.markdown(
                                f"""
                                **Option {idx}**  
                                ✈️ **Airline:** {offer['airline']}  
                                🕓 **Departure:** {offer['departure']}  
                                🛬 **Arrival:** {offer['arrival']}  
                                💰 **Price:** {offer['price']}
                                """
                            )

            except Exception as e:
                st.error(f"Error fetching flights: {e}")




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

