from crew import financial_crew

if __name__ == "__main__":
    query = "Plot YTD stock gain of Tesla"
    result = financial_crew.kickoff(inputs={"query": query})
    print("Final Output:", result)
