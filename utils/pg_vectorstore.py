import os
from typing import List
from langchain_core.documents import Document
from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings

from .helpers import get_openai_embeddings

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
CONNECTION_STRING = os.environ.get('PG_CONNECTION_STRING')
COLLECTION_NAME = 'general_collection'


def insert_documents(documents: List[Document], collection_name: str | None) -> None:
    embeddings = get_openai_embeddings()

    PGVector.from_documents(
        embedding=embeddings,
        documents=documents,
        connection=CONNECTION_STRING,
        collection_name=collection_name or COLLECTION_NAME,
        use_jsonb=True
    )

    print("Documents inserted successfully!")