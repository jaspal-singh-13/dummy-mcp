# BMI Calculator Technical Documentation

## Architecture Overview
The BMI calculator consists of two main components:
- BMI Server (bmi_server.py)
- BMI Client (bmi_client.py)

## Server Implementation (bmi_server.py)

### Server Components
- Uses FastMCP framework for tool registration
- Exposes a single BMI calculation tool
- Implements stdio transport for communication

### Tool Specification
```python
@mcp.tool()
def calculate_bmi(weight: float, height: float) -> float
```
- **Input Parameters:**
  - weight: float (in kilograms)
  - height: float (in meters)
- **Return Value:** 
  - float (BMI value)
- **Error Handling:**
  - Validates height > 0
  - Throws ValueError for invalid inputs

## Client Implementation (bmi_client.py)

### Client Components
1. **OpenAI Integration**
   - Model: gpt-4o-mini
   - Temperature: 0.2
   - Max tokens: 250

2. **MCP Client**
   - Uses stdio transport
   - Implements async communication
   - Handles tool discovery and execution

### Main Functions

1. **llm_client(message: str)**
   - Handles OpenAI API communication
   - Processes natural language input
   - Returns structured tool commands

2. **get_prompt_to_identify_tool_and_arguments(query, tools)**
   - Generates LLM prompts
   - Formats available tools information
   - Structures tool execution requests

3. **run(query: str)**
   - Main execution function
   - Manages server connection
   - Coordinates LLM and tool execution

## Communication Flow
1. User inputs natural language query
2. Client processes query through OpenAI
3. LLM generates structured tool command
4. Client sends command to BMI server
5. Server executes calculation
6. Result returned to client

## Environment Setup
Required environment variables:
- OPENAI_API_KEY: OpenAI API authentication key

## Error Handling
1. Server-side:
   - Input validation for height and weight
   - Proper error messages for invalid inputs

2. Client-side:
   - Connection error handling
   - LLM response parsing
   - Tool execution error handling

## Example Usage
```python
query = "Calculate BMI for height 5ft 10inches and weight 80kg"
result = asyncio.run(run(query))
```

## Performance Considerations
- Async implementation for improved responsiveness
- Minimal data transfer between components
- Efficient error handling and validation
