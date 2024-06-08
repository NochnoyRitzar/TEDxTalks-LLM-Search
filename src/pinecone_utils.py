import os
from pinecone import Pinecone, ServerlessSpec
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding, VertexEmbeddingMode
from src.load_data import convert_df_to_documents


def create_index(dims: int, metric: str = "cosine"):
    """
    Create a serverless Pinecone index.
    :param dims: Number of dimensions of the vectors to be stored.
    :param metric: Distance metric used for similarity search.
    """
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pc.create_index(
        name=os.environ["PINECONE_INDEX_NAME"],
        dimension=dims,
        metric=metric,
        spec=ServerlessSpec(cloud="aws", region="eu-west-1"),
    )
    print("Pinecone index is set up and ready.")


def populate_pinecone_db(json_path: str):
    """
    Populate a Pinecone index with TED talks data.

    :param json_path: Path to local JSON file containing TED talks data.
    """
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
        docstore=SimpleDocumentStore(),
    )

    documents = convert_df_to_documents(json_path)
    pipeline.run(documents=documents, show_progress=True, num_workers=4)

    # Persist the pipeline for future use, avoids duplicates when inserting new data
    pipeline.persist("../data/pipeline_storage")

    print("Data has been successfully populated into the Pinecone database.")
