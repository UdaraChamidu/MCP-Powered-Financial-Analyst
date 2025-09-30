from crewai import Task, Crew
from agents import query_parser, code_writer, code_executor

# Task 1: Parse query
task1 = Task(
    description="Parse the user query into a structured request",
    agent=query_parser
)

# Task 2: Write code
task2 = Task(
    description="Generate Python code to fetch stock data and produce a plot",
    agent=code_writer
)

# Task 3: Execute code
task3 = Task(
    description="Run the generated Python code and return the final plot or data",
    agent=code_executor
)

# Orchestrate the workflow
financial_crew = Crew(
    agents=[query_parser, code_writer, code_executor],
    tasks=[task1, task2, task3]
)
