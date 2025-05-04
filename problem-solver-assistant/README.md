# Problem Solver Assistant API

## Overview
This is a FastAPI-based REST API that provides an interface to interact with OpenAI's GPT-4 model. The API is designed to process user prompts and return AI-generated responses, specifically configured to provide step-by-step problem-solving assistance.

## Features
- RESTful API endpoint for AI-powered problem solving
- Integration with OpenAI's GPT-4 model
- Environment-based configuration
- Structured request/response handling using Pydantic models

## Dependencies
- FastAPI: Web framework for building APIs
- OpenAI: Official OpenAI Python client
- python-dotenv: Environment variable management
- Pydantic: Data validation and settings management

## Configuration
The API requires the following configuration:

1. Create a `.env` file in the same directory as `agent_api.py` with the following content:
```
OPENAI_API_KEY=your_openai_api_key_here
```

2. Ensure the `.env` file is in the same directory as the script for proper loading.

## API Endpoints

### POST /ask
Processes a user prompt and returns an AI-generated response.

#### Request Body
```json
{
    "prompt": "string"
}
```

#### Response
```json
{
    "response": "string"
}
```

#### Example Usage
```bash
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "How do I solve this math problem?"}'
```

## Error Handling
The API includes the following error handling mechanisms:
- Validation of required environment variables
- Input validation through Pydantic models
- Proper error responses for invalid requests

## Security Considerations
1. **API Key Protection**
   - The OpenAI API key is stored in environment variables
   - Never commit the `.env` file to version control
   - Use secure methods to distribute API keys

2. **Input Validation**
   - All inputs are validated using Pydantic models
   - Prevents injection attacks and malformed requests

3. **Rate Limiting**
   - Consider implementing rate limiting for production use
   - Monitor API usage to prevent abuse

## Running the API
1. Install dependencies:
```bash
pip install fastapi uvicorn openai python-dotenv pydantic
```

2. Start the server:
```bash
uvicorn agent_api:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation
Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Model Configuration
The API uses GPT-4 with the following settings:
- Temperature: 0.2 (for consistent, focused responses)
- System prompt: Configured for step-by-step problem solving

## Best Practices
1. Always validate the API key is present before starting the server
2. Use environment variables for sensitive configuration
3. Implement proper error handling in production
4. Consider adding logging for monitoring and debugging
5. Add appropriate CORS settings if needed
6. Implement rate limiting for production use

## Contributing
When contributing to this project:
1. Follow the existing code style
2. Add appropriate documentation for new features
3. Include error handling for new functionality
4. Update the README with any new configuration options

## License
[Add appropriate license information here]
