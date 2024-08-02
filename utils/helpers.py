import os
import re
from typing import List
from langchain_core.documents import Document
from langchain_postgres.vectorstores import PGVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

CONNECTION_STRING = os.environ.get('PG_CONNECTION_STRING')
COLLECTION_NAME = "general_collection"

def delete_files(folder_name: str) -> None:
    # Check if the folder exists
    if not os.path.exists(folder_name):
        print(f"The folder '{folder_name}' does not exist.")
        return

    # Iterate over the list of file names and delete each file
    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        
        # Check if the file exists
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file '{file_path}': {e}")
        else:
            print(f"File '{file_path}' does not exist.")

def get_openai_embeddings():
    embeddings = OpenAIEmbeddings()
    return embeddings

def get_openai_llm(model: str="gpt-3.5-turbo", temperature: int = 0):
    return ChatOpenAI(
        model=model,
        temperature=temperature
    )

def search_from_vector_db(query: str, collection_name: str, top_k: int=3) -> List[Document]:
    embeddings = get_openai_embeddings()
    

    index = PGVector.from_existing_index(
        embedding=embeddings,
        collection_name=collection_name or COLLECTION_NAME,
        connection=CONNECTION_STRING,
    )

    results = index.similarity_search(query, top_k)
    
    return results

def get_pg_vector_retriever(collection_name: str, top_k: int = 3):
    embeddings = get_openai_embeddings()
    

    index = PGVector.from_existing_index(
        embedding=embeddings,
        collection_name=collection_name or COLLECTION_NAME,
        connection=CONNECTION_STRING,
    )

    return index.as_retriever(search_kwargs={'k': top_k})
    

def get_db_config_from_connection_string(connection_string) -> dict[str, str] | None:
    pattern = re.compile(
        r"postgresql\+psycopg:\/\/(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)\/(?P<dbname>[^\/]+)"
    )

    match = pattern.match(connection_string)

    if match:
        db_info = match.groupdict()
        return db_info
    
    return None
        