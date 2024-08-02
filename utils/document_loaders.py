import os
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, PyPDFLoader, DirectoryLoader

from .helpers import delete_files
from .pg_vectorstore import insert_documents

def text_document_loader(directory_path: str) -> None:
    try:
        if len(os.listdir(directory_path)) == 0:
            return None
        
        loader = DirectoryLoader(
            path=directory_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            use_multithreading=True
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=200,
            length_function=len,
        )

        documents = loader.load_and_split(text_splitter=text_splitter)

        insert_documents(documents, None)
        delete_files(folder_name=directory_path)

    except Exception as e:
        delete_files(folder_name=directory_path)
        print(f"Error loading text files: {e}")

def pdf_document_loader(directory_path: str) -> None:
    try:
        if len(os.listdir(directory_path)) == 0:
            return None
        
        loader = DirectoryLoader(
            path=directory_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            use_multithreading=True,
            show_progress=True
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=200,
            length_function=len,
        )

        documents = loader.load_and_split(text_splitter=text_splitter)

        insert_documents(documents, None)
        delete_files(folder_name=directory_path)
    
    except Exception as e:
        delete_files(folder_name=directory_path)
        print(f"Error loading PDF files: {e}")