import os
import uuid
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from models.langchain_pg_collection import Collection
from utils.database import get_db
from utils.prompts import JUST_CHAT_PROMPT, QA_PROMPT_TEMPLATE
from utils.helpers import get_openai_llm, get_pg_vector_retriever
from utils.llm_chains.history_chain import HistoryChain

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

llm = get_openai_llm()

class ChatModel(BaseModel):
    text: str
    session_id: uuid.UUID | None
    collection_name: str

api_router = APIRouter(prefix="/chat", tags=["Chat"])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

@api_router.post("",summary="Chat with OpenAI API", description="This endpoint accepts a text query and returns a response from the OpenAI API.")
async def chat(query: ChatModel):
    chain = JUST_CHAT_PROMPT | llm | StrOutputParser()
    response = await chain.ainvoke({"message": query})
    
    return JSONResponse({"answer": response})

@api_router.post("/docs",summary="Chat with your internal docs", description="This endpoint accepts a text query, searches it within your documents, and returns a crafted response from the OpenAI API.")
async def chat(body: ChatModel, db: Session = Depends(get_db)):
    if not body.collection_name:
        raise HTTPException(status_code=400, detail="You must provide a collection name")
    
    if not body.session_id:
        raise HTTPException(status_code=404, detail="Session id is required")
    
    collection = db.query(Collection).filter(Collection.name == body.collection_name).first()
    print("COLLECTION: ", collection)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    # chain = (
    #     {
    #         "context": get_pg_vector_retriever(collection_name=body.collection_name) | format_docs,
    #         "question": RunnablePassthrough()
    #     }
    #     | QA_PROMPT_TEMPLATE | llm | StrOutputParser()
    # )
    # response = chain.invoke(body.text)

    chain = HistoryChain(session_id=body.session_id)
    response = chain.chat(body.text)

    return JSONResponse({"answer": response})