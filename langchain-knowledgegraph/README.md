# LangChain Knowledge Graph with Neo4j

This project demonstrates the integration of LangChain with Neo4j to create and manage knowledge graphs.

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- OpenAI API key

## Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd langchain-knowledgegraph
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory with the following content:
```
OPENAI_API_KEY=your-openai-api-key
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=neo4j_admin_2025
```

5. **Start Neo4j using Docker Compose**
```bash
# Create necessary directories
mkdir -p neo4j/{data,logs,import,plugins}

# Start Neo4j container
docker-compose up -d
```

The Neo4j container will be available at:
- Neo4j Browser: http://localhost:7474
- Bolt connection: bolt://localhost:7687

## Usage

1. **Access Neo4j Browser**
   - Open http://localhost:7474 in your web browser
   - Login credentials:
     - Username: neo4j
     - Password: neo4j_admin_2025

2. **Run the application**
```bash
python main.py
```

## Testing

To verify your Neo4j setup and connection:

1. **Run the test script**
```bash
python test_neo4j.py
```

The test script will:
- Test direct Neo4j connection
- Test LangChain Neo4j integration
- Create a test node
- Query the test node
- Clean up test data

2. **Manual Testing in Neo4j Browser**
   - Open http://localhost:7474
   - Try this Cypher query:
   ```cypher
   MATCH (n) RETURN n LIMIT 25
   ```

## Docker Compose Configuration

The `docker-compose.yml` file includes the following configuration:

- Neo4j version: 5.14.1
- Ports:
  - 7474: HTTP interface (Neo4j Browser)
  - 7687: Bolt protocol
- Environment variables:
  - NEO4J_AUTH: Authentication settings
  - Memory settings for optimal performance
- Volumes:
  - ./neo4j/data: Database storage
  - ./neo4j/logs: Log files
  - ./neo4j/import: Import directory
  - ./neo4j/plugins: Plugins directory

## Useful Docker Commands

```bash
# Start the container
docker-compose up -d

# Stop the container
docker-compose down

# View logs
docker-compose logs -f

# Restart the container
docker-compose restart
```

## Project Structure

```
.
├── docker-compose.yml
├── requirements.txt
├── main.py
├── test_neo4j.py
├── .env
└── neo4j/
    ├── data/
    ├── logs/
    ├── import/
    └── plugins/
```

## Troubleshooting

1. **Container won't start**
   - Check if ports 7474 and 7687 are available
   - Ensure you have sufficient disk space
   - Check Docker logs: `docker-compose logs`

2. **Connection issues**
   - Verify Neo4j is running: `docker-compose ps`
   - Check if the ports are correctly mapped
   - Verify your .env file has the correct credentials
   - Run the test script to verify connection: `python test_neo4j.py`

## License

[Your License Here] 