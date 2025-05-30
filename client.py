# client.py

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langchain.callbacks import StdOutCallbackHandler  # Add this import
from pprint import pprint
import asyncio
import os

# Set your API key (replace with your actual key or use environment variables)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the LLM model

# model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

model = ChatOllama(model="llama3.2", temperature=0.5)  # Add this line

server_params = StdioServerParameters(

   command="python",      # Command to execute

   args=["mcp_server.py"] # Arguments for the command (our server script)

)

async def run_agent(user_prompt):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("MCP Session Initialized.")
            tools = await load_mcp_tools(session)
            print(f"Loaded Tools: {[tool.name for tool in tools]}")
            agent = create_react_agent(model, tools)
            print("ReAct Agent Created.")
            print(f"Invoking agent with query")
            # Add the callback handler to print tool usage
            response = await agent.ainvoke(
                {
                    "messages": [("user", f"{user_prompt}")]
                }
            )
            print("Agent invocation complete.")
            pprint(f"Agent Response: {response}")
            return response["messages"][-1].content

# Standard Python entry point check

async def main():
    print("Starting MCP Client...")
    while True:
        user_prompt = input("Enter your prompt (type exit() to quit): ")
        if user_prompt.strip() == "exit()":
            print("Exiting MCP Client.")
            break
        result = await run_agent(user_prompt)
        print("\nAgent Final Response:")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())