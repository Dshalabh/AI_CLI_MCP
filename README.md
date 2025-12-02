# MCP Agent Demo

An interactive CLI agent that uses the Model Context Protocol (MCP) with Groq's LLM and built-in conversation memory.

## Features

- Interactive CLI interface with conversation memory
- Powered by Groq's Llama 3.3 70B model
- MCP integration with Playwright, Airbnb, and DuckDuckGo search servers
- Memory management with commands to view and clear history

## Requirements

- Python 3.13+
- Groq API key

## Installation

1. Clone the repository and navigate to the project directory

2. Install dependencies using uv:
   ```bash
   uv sync
   ```

3. Set your Groq API key:
   ```powershell
   # Windows PowerShell
   $env:GROQ_API_KEY='your-api-key'
   ```
   ```cmd
   # Windows CMD
   set GROQ_API_KEY=your-api-key
   ```
   ```bash
   # Linux/Mac
   export GROQ_API_KEY='your-api-key'
   ```

## Usage

Run the agent:
```bash
python app.py
```

### CLI Commands

- Type your message and press Enter to chat
- `history` - View conversation history
- `clear` - Clear conversation memory
- `exit` - Quit the agent

## Configuration

The MCP server configuration is stored in `Browser_mcp.json`. The default configuration includes:

- **Playwright** - Browser automation
- **Airbnb** - Airbnb search integration
- **DuckDuckGo** - Web search capabilities

## Dependencies

- `langchain-groq` - Groq LLM integration
- `langchain-openai` - OpenAI LangChain support
- `mcp-use` - Model Context Protocol client
- `numpy` - Numerical computing
- `pandas` - Data manipulation

## License

MIT
