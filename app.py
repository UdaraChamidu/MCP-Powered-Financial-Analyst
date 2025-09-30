import streamlit as st
from crew import financial_crew

st.title("📊 MCP-Powered Financial Analyst")

query = st.text_input("Enter your financial query", "Plot YTD stock gain of Tesla")

if st.button("Run Analysis"):
    result = financial_crew.kickoff(inputs={"query": query})
    st.write(result)
    st.image("plot.png")


