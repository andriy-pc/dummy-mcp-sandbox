# Dummy MCP server & client implementation

Minimal MCP server & client implementation using MCP SDK. 
Both are intended for local-only run using stdio for communication.


# Overwiew
## API
FastAPI API exposes only one endpoint: `api/v1/health` to check if the server is up and running.

## Server
MCP server that supports only one tool: `internal_api_health`. This tool pings the `API` to verify it's running

## Client
MCP client that uses OpenAI API.
Originally, the project was planned as vendor-agnostic (that's why this project has `lite-llm` dependency), but it requires more effort, which doesn't make sense for such a **dummy** project. 

# Local run

## Start API
`python .\api\main.py`

## Start MCP Client
1. Set OpenAI API key in `dummy_mcp\client\.env` file
2. Activate venv (to activate venv on Windows, run this command first: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`): `.\client\.venv\Scripts\activate`

3. Run client specifying path to server's `main.py`: `python .\client\main.py ./server/main.py`
4. Test tool integration:
```
Query: Is my API healthy?

[Calling tool 'internal_api_health' with args {}]
Yes. The API health check reports: healthy. No issues indicated.
```
