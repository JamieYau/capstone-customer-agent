import streamlit as st
from app.agent.workflow_graph import build_graph

st.title("🛒 Customer Service Agent")

graph = build_graph()

user_input = st.text_input("Ask something:")

if user_input:
    result = graph.invoke({"user_input": user_input})
    st.write(result["result"])
