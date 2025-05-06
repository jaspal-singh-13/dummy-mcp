# BMI Calculator Service

A natural language BMI calculator service using MCP (Message Communication Protocol) and OpenAI integration.

## Features

- Natural language query processing
- BMI calculation from height and weight
- BMI category determination
- Async server-client communication
- Error handling and retry logic

## Setup

1. **Environment Setup**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install mcp-core openai python-dotenv
   ```

2. **Configuration**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```

## Usage

1. **Start Server**
   ```bash
   python bmi_server.py
   ```

2. **Run Client**
   ```bash
   python bmi_client.py
   ```

3. **Example Queries**
   - "Calculate BMI for height 5ft 10inches and weight 80kg"
   - "What's the BMI category for BMI value 25.1"

## Project Structure

- `bmi_server.py`: MCP server implementing BMI calculations
- `bmi_client.py`: Client with OpenAI integration for natural language processing
- `.env`: Configuration file for API keys
- `.env.example`: Template for environment variables

## Error Handling

- Server connection retries
- Invalid input validation
- Process cleanup on exit
- Comprehensive error logging

## Development

- Uses async/await for efficient I/O
- Implements retry logic for reliability
- Includes detailed logging for debugging
- Follows PEP 8 style guidelines

## License

MIT License
