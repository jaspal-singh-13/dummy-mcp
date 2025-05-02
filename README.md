# BMI Calculator MCP Service

A simple Body Mass Index (BMI) calculator service using Message Communication Protocol (MCP) with OpenAI integration for natural language processing.

## Overview
This service allows users to calculate BMI using natural language queries. It leverages OpenAI's API to interpret user input and communicate with a BMI calculation service.

## Prerequisites
- Python 3.8+
- OpenAI API key
- MCP Core library
- Python dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/jaspal-singh-13/dummy-mcp.git
cd dummy-mcp
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install mcp-core openai python-dotenv
```

4. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

## Running the Service

1. Start the BMI server:
```bash
python bmi_server.py
```

2. In a new terminal, run the client(NOTE: Kill the BMI Server script first.):
```bash
python bmi_client.py
```

## Project Components

### BMI Server (`bmi_server.py`)
- MCP server implementation
- Provides BMI calculation functionality
- Accepts weight (kg) and height (m) parameters

### BMI Client (`bmi_client.py`)
- Handles natural language processing via OpenAI
- Connects to BMI server using stdio transport
- Translates user queries into tool calls

## Example Usage

```bash
# The client accepts natural language queries like:
"Calculate BMI for height 5ft 10inches and weight 80kg"
```

## Security Notes
- Never commit `.env` file containing API keys
- Use `.env.example` for configuration templates
- Keep your OpenAI API key secure and rotate regularly

## Error Handling
The service includes error handling for:
- Invalid input values
- Server connection issues
- OpenAI API failures
