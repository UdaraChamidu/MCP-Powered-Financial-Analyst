from crewai import Agent

# Agent 1: Query Parser
query_parser = Agent(
    role="Query Parser",
    goal="Understand the financial query and break it down into actionable tasks",
    backstory="You are skilled at interpreting financial analysis queries.",
    tools=[]
)

# Agent 2: Code Writer
code_writer = Agent(
    role="Code Writer",
    goal="Write Python code that answers the financial query using finance libraries",
    backstory="You are a Python and financial data expert.",
    tools=[]
)

# Agent 3: Code Executor
code_executor = Agent(
    role="Code Executor",
    goal="Execute Python code safely and return results (tables, plots)",
    backstory="You are responsible for running and validating generated code.",
    tools=[]
)
