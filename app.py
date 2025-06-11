import streamlit as st
from agents.blog_agent import search_blog

st.title("🗺️ Travel Blog Search Assistant")
st.markdown("Ask questions about the ingested blog content!")

# User input
query = st.text_input("Enter your query:")

# Search button
if st.button("Search"):
    if query.strip():
        with st.spinner("Searching the blog..."):
            result = search_blog(query)
        st.markdown("### 📖 Results:")
        st.write(result)
    else:
        st.warning("Please enter a query.")

