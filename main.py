import os
import uvicorn
from fastapi import FastAPI
from routers import documents, chat


async def check_env_vars():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    connection = os.getenv("PG_CONNECTION_STRING")
    
    if not openai_api_key:
        raise RuntimeError("Environment variable OPENAI_API_KEY is not set.")
    if not connection:
        raise RuntimeError("Environment variable PG_CONNECTION_STRING is not set.")
    
    uploads_folder = "uploads"
    text_folder = f"{uploads_folder}/text_docs"
    pdf_folder = f"{uploads_folder}/pdf_docs"
    if not os.path.exists(uploads_folder): 
        os.makedirs(uploads_folder)
        print(f"Created folder: {uploads_folder}")
    else:
        print(f"Folder already exists: {uploads_folder}")

    if not os.path.exists(text_folder):
        os.makedirs(text_folder)

    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
        
app = FastAPI(
    on_startup=[check_env_vars]
)

app.include_router(router=documents.api_router)
app.include_router(router=chat.api_router)

if __name__ == '__main__':
    uvicorn.run(app="main:app", host="127.0.0.1", port=5000, reload=True)