import os
from typing import List
from fastapi.responses import JSONResponse
from fastapi import APIRouter, File, UploadFile, HTTPException

from utils.document_loaders import text_document_loader, pdf_document_loader

UPLOAD_FOLDER = "uploads"
api_router = APIRouter(prefix="/documents", tags=["Document"])


@api_router.post(
    "/upload_files",
    summary="Upload and Process Text & PDF Files",
    description="""
                 This endpoint allows users to upload text and pdf files. 
                 The service will read the content of each file, 
                 create chunks of text, generate embeddings for these chunks, 
                 and store the embeddings into a vector database.
                 """,
)
async def upload_documents(files: List[UploadFile] = File(...)) -> JSONResponse:
    try:
        file_names = []
        for file in files:
            file_names.append(file.filename)
            if file.content_type not in ["application/pdf", "text/plain"]:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' is a {file.content_type} file. Only text and files are allowed.",
                )
            file_path = (
                os.path.join(f"{UPLOAD_FOLDER}/pdf_docs", file.filename)
                if file.content_type == "application/pdf"
                else os.path.join(f"{UPLOAD_FOLDER}/text_docs", file.filename)
            )
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

        text_document_loader(directory_path=f"{UPLOAD_FOLDER}/text_docs")
        pdf_document_loader(directory_path=f"{UPLOAD_FOLDER}/pdf_docs")

        # Return success message
        return JSONResponse({"message": "Files uploaded and processed successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
