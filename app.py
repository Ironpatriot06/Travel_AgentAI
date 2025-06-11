# app.py

import streamlit as st
from agents.blog_agent import search_blog

st.title("🗺️ Travel Blog Search Assistant")
st.markdown("Ask questions about the ingested blog content!")

query = st.text_input("Enter your query:")

if st.button("Search"):
    if query.strip():
        with st.spinner("Searching the blog..."):
            result = search_blog(query)
        st.markdown("### 📖 Results:")
        if isinstance(result, str):
            st.warning(result)
        else:
            for i, res in enumerate(result, 1):
                st.markdown(f"**Result {i}:**\n{res[:800]}...")
    else:
        st.warning("Please enter a query.")

