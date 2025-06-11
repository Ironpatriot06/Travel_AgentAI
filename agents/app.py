# streamlit_app.py
import streamlit as st
from .blog_agent import search_blog

st.title("🧳 Travel Blog Q&A")
query = st.text_input("Ask a question about your travel destination:")
submit = st.button("Search")

if submit and query:
    with st.spinner("Searching..."):
        response = search_blog(query)
    st.write("### Answer")
    st.write(response)

