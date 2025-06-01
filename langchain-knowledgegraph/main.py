import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_neo4j import Neo4jGraph
from langchain_openai import ChatOpenAI

# Clear terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

# Get Neo4j connection information
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

if not all([neo4j_uri, neo4j_username, neo4j_password]):
    raise ValueError("Neo4j connection information not found in .env file")

# Check Neo4j connection
try:
    # Try to execute a simple query to verify connection
    print("\n✅ Successfully connected to Neo4j!")
    print(f"Connection details:")
    print(f"URI: {neo4j_uri}")
    print(f"Username: {neo4j_username}")
except Exception as e:
    print("\n❌ Failed to connect to Neo4j!")
    print(f"Error: {str(e)}")
    raise


# Initialize Neo4j graph connection with schema caching enabled
graph = Neo4jGraph(refresh_schema=False)

# Initialize the OpenAI language model
# Temperature set to 0 for deterministic outputs
llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")

# Create a graph transformer that uses the LLM to transform text into graph structures
llm_transformer = LLMGraphTransformer(llm=llm)

async def transform_to_graph(text: str, transformer: LLMGraphTransformer) -> tuple:
    documents = [Document(page_content=text)]
    graph_documents = await transformer.aconvert_to_graph_documents(documents)
    return graph_documents[0].nodes, graph_documents[0].relationships

async def main():
    # Define allowed relationships as tuples
    allowed_relationships = [
        ("Person", "SPOUSE", "Person"),
        ("Person", "NATIONALITY", "Country"),
        ("Person", "WORKED_AT", "Organization"),
    ]

    # Create a filtered graph transformer that only allows specific node and relationship types
    llm_transformer_filtered = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=["Person", "Country", "Organization"],
        allowed_relationships=allowed_relationships,
    )

    # Create a transformer with node properties
    llm_transformer_props = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=["Person", "Country", "Organization"],
        allowed_relationships=["NATIONALITY", "LOCATED_IN", "WORKED_AT", "SPOUSE"],
        node_properties=["born_year"],
    )

    text = """
    Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
    She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
    Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
    She was, in 1906, the first woman to become a professor at the University of Paris.
    """
    
    # Get filtered results with tuple-based relationships
    nodes_filtered, relationships_filtered = await transform_to_graph(text, llm_transformer_filtered)
    print("\nFiltered Results (with tuple-based relationships):")
    print(f"Nodes: {nodes_filtered}")
    print(f"Relationships: {relationships_filtered}")

    # Get results with node properties
    nodes_props, relationships_props = await transform_to_graph(text, llm_transformer_props)
    print("\nResults with Node Properties:")
    print(f"Nodes: {nodes_props}")
    print(f"Relationships: {relationships_props}")

    # Add the graph documents to Neo4j
    graph_documents_props = await llm_transformer_props.aconvert_to_graph_documents([Document(page_content=text)])
    graph.add_graph_documents(graph_documents_props)
    print("\n✅ Graph documents added to Neo4j successfully!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())