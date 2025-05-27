# Model Content Protocol Server

A FastAPI-based server implementing the Model Content Protocol (MCP) for code analysis.

## Features

- MCP-compliant request/response handling
- Built-in model support through MCP package
- RESTful API endpoints
- Configurable settings
- Health monitoring
- CORS support
- API key authentication (optional)

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (optional):
```env
HOST=0.0.0.0
PORT=8000
DEBUG=false
API_KEY=your_api_key_here
```

## Running the Server

Start the server:
```bash
python server/mcp_server.py
```

The server will be available at `http://localhost:8000`

## API Endpoints

### Analyze Code
```http
POST /mcp/analyze
Content-Type: application/json

{
    "model": "ast_parser",
    "content": {
        "code": "...",
        "options": {}
    },
    "parameters": {
        "key": "value"
    }
}
```

### List Available Models
```http
GET /mcp/models
```

### Health Check
```http
GET /health
```

## API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

The server can be configured through:
1. Environment variables
2. `.env` file
3. Default settings in `config.py`

## Development

1. Enable debug mode in `.env`:
```env
DEBUG=true
```

2. The server will automatically reload on code changes

## MCP Integration

This server uses the MCP package for:
- Request/response handling
- Model type definitions
- Protocol compliance
- Built-in model capabilities

## License

MIT