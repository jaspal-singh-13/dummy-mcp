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
from subprocess import Popen, PIPE
import sys
import logging
import subprocess

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configure server connection parameters with subprocess management
def get_server_process():
    """Helper function to start and manage server process"""
    try:
        server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "bmi_server.py"))
        logger.debug(f"Starting server from: {server_path}")
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        return process
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

server_params = StdioServerParameters(
    command=sys.executable,
    args=[os.path.join(os.path.dirname(__file__), "bmi_server.py")]
)

def llm_client(message: str):
    """
    Communicates with OpenAI's LLM to process user queries.
    
    Args:
        message (str): The prompt/query to send to the LLM
        
    Returns:
        str: The LLM's response stripped of whitespace
    """
    # Initialize the OpenAI client
    logger.debug("Initializing OpenAI client...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logger.debug(f"Sending message to LLM: {message}")
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
    Main execution function with improved server process handling
    """
    server_process = None
    try:
        # Start server process
        server_process = get_server_process()
        logger.debug("Server process started")
        
        # Wait for server to initialize
        await asyncio.sleep(1)
        
        if server_process.poll() is not None:
            raise RuntimeError("Server process terminated unexpectedly")
        
        async with stdio_client(server_params) as (read, write):
            logger.debug("Connected to server, initializing session...")
            async with ClientSession(read, write) as session:
                await session.initialize()
                logger.debug("Session initialized successfully")

                # Get the list of available tools
                tools = await session.list_tools()
                logger.debug(f"Available tools: {tools}")

                # Get prompt for LLM
                prompt = get_prompt_to_identify_tool_and_arguments(query, tools.tools)
                logger.debug(f"Prompt for LLM: {prompt}")
                
                # Get LLM response
                logger.debug("Getting LLM response...")
                llm_response = llm_client(prompt)
                logger.debug(f"LLM Response: {llm_response}")

                # Parse the LLM response
                tool_call = json.loads(llm_response)
                
                # Call the tool with the arguments
                result = await session.call_tool(tool_call["tool"], arguments=tool_call["arguments"])
                
                # Print the result
                logger.debug(f'Result: {result.content[0].text}')
                return result.content[0].text
    except Exception as e:
        logger.error(f"Error in run: {e}")
        raise
    finally:
        if server_process:
            logger.debug("Cleaning up server process")
            try:
                server_process.terminate()
                await asyncio.sleep(0.5)
                server_process.kill()  # Force kill if still running
                server_process.wait(timeout=1)
            except Exception as e:
                logger.error(f"Error cleaning up server: {e}")


if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        query = "Calculate BMI for height 5ft 10inches and weight 80kg"
        # query = "calulate bmi category for 25 bmi"
        logger.info(f"Processing query: {query}")
        result = loop.run_until_complete(run(query))
        print(f"Final Result: {result}")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        loop.close()