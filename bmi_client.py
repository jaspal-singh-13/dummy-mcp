"""
BMI Calculator Client
This script implements a client that connects to a BMI calculation service using MCP protocol.
It uses OpenAI's GPT model to process natural language queries and convert them to tool calls.
"""

import asyncio
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Configure server connection parameters
server_params = StdioServerParameters(command="python", args=["bmi_server.py"])

def llm_client(message: str):
    """
    Communicates with OpenAI's LLM to process user queries.
    
    Args:
        message (str): The prompt/query to send to the LLM
        
    Returns:
        str: The LLM's response stripped of whitespace
    """
    # Initialize the OpenAI client
    print("Initializing OpenAI client...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print(f"Sending message to LLM: {message}")
    # Send the message to the LLM
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system",
                    "content":"You are an intelligent assistant. You will execute tasks as prompted",
                    "role": "user", "content": message}],
        max_tokens=250,
        temperature=0.2
    )

    # Extract and return the response content
    return response.choices[0].message.content.strip()


def get_prompt_to_identify_tool_and_arguments(query, tools):
    """
    Generates a prompt for the LLM to identify which tool to use and its arguments.
    
    Args:
        query (str): User's natural language query
        tools (list): Available tools and their descriptions
        
    Returns:
        str: Formatted prompt for the LLM
    """
    tools_description = "\n".join([f"- {tool.name}, {tool.description}, {tool.inputSchema} " for tool in tools])
    return  ("You are a helpful assistant with access to these tools:\n\n"
                f"{tools_description}\n"
                "Choose the appropriate tool based on the user's question. \n"
                f"User's Question: {query}\n"                
                "If no tool is needed, reply directly.\n\n"
                "IMPORTANT: When you need to use a tool, you must ONLY respond with "                
                "the exact JSON object format below, nothing else:\n"
                "Keep the values in str "
                "{\n"
                '    "tool": "tool-name",\n'
                '    "arguments": {\n'
                '        "argument-name": "value"\n'
                "    }\n"
                "}\n\n")

async def run(query: str):
    """
    Main execution function that:
    1. Connects to the BMI server
    2. Initializes a client session
    3. Gets available tools
    4. Processes the query through LLM
    5. Executes the tool call
    
    Args:
        query (str): Natural language query from user
        
    Returns:
        str: Result of the BMI calculation
    """
    try:
        print("Connecting to BMI server...")
        async with stdio_client(server_params) as (read, write):
            print("Connected to server, initializing session...")
            async with ClientSession(read,write) as session:
                await session.initialize()
                print("Session initialized successfully")

                # Get the list of available tools
                tools = await session.list_tools()
                print(f"Available tools: {tools}")

                # Get prompt for LLM
                prompt = get_prompt_to_identify_tool_and_arguments(query, tools.tools)
                print(f"Prompt for LLM: {prompt}")
                
                # Get LLM response
                print("Getting LLM response...")
                llm_response = llm_client(prompt)
                print(f"LLM Response: {llm_response}")

                # Parse the LLM response
                tool_call = json.loads(llm_response)
                
                # Call the tool with the arguments
                result = await session.call_tool(tool_call["tool"], arguments=tool_call["arguments"])
                
                # Print the result
                print(f'Result: {result.content[0].text}')
                return result.content[0].text
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    # Example query demonstrating height and weight input
    query = "Calculate BMI for height 5ft 10inches and weight 80kg"
    # query = "Calculate BMI category 25.1 bmi"
    print(f"Sending query: {query}")
    asyncio.run(run(query))