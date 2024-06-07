import os
from pinecone import Pinecone, ServerlessSpec
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding, VertexEmbeddingMode
from dotenv import load_dotenv

from load_data import convert_df_to_documents

load_dotenv("../.env")
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


def create_index(dims: int, metric: str = "cosine"):
    """
    Create a serverless Pinecone index.
    :param dims: Number of dimensions of the vectors to be stored.
    :param metric: Distance metric used for similarity search.
    """
    pc.create_index(
        name=os.environ["PINECONE_INDEX_NAME"],
        dimension=dims,
        metric=metric,
        spec=ServerlessSpec(cloud="aws", region="eu-west-1"),
    )


def populate_pinecone_db(csv_path: str):
    """
    Populate a Pinecone index with TED talks data.

    :param csv_path: Path to local CSV file containing TED talks data.
    """
    if os.environ["PINECONE_INDEX_NAME"] not in pc.list_indexes().names():
        create_index(dims=768, metric="cosine")

    vector_store = PineconeVectorStore(
        api_key=os.environ["PINECONE_API_KEY"],
        index_name=os.environ["PINECONE_INDEX_NAME"],
    )
    pipeline = IngestionPipeline(
        transformations=[
            VertexTextEmbedding(
                project=os.environ.get("GCP_PROJECT_ID"),
                location=os.environ.get("GCP_LOCATION"),
                model_name="text-embedding-004",
                embed_mode=VertexEmbeddingMode.SEMANTIC_SIMILARITY_MODE,
            )
        ],
        vector_store=vector_store,
    )

    documents = convert_df_to_documents(csv_path)
    pipeline.run(documents=documents, show_progress=True)
