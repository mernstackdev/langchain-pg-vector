import os
import uuid
import psycopg
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_postgres.chat_message_histories import PostgresChatMessageHistory

from utils.helpers import get_openai_llm, get_db_config_from_connection_string
from utils.prompts import JUST_CHAT_PROMPT

db_conn = get_db_config_from_connection_string(os.environ.get('PG_CONNECTION_STRING'))

db_name = db_conn['dbname']
user = db_conn['user']
password = db_conn['password']
host = db_conn['host']
port = db_conn['port']


class HistoryChain():
    def __init__(self, session_id: uuid.UUID) -> None:
        self._table_name = "chat_messages_history"
        self._session_id = session_id
        self._db_connection_string = f"dbname={db_name} user={user} password={password} host={host} port={port}"
        self._sync_conn = psycopg.connect(self._db_connection_string)

        self._llm = get_openai_llm()
        self._prompt = JUST_CHAT_PROMPT

    def _get_chat_history(self, session_id: uuid.UUID):
        PostgresChatMessageHistory.create_tables(self._sync_conn, self._table_name)
        return PostgresChatMessageHistory(
            self._table_name,
            session_id,
            sync_connection=self._sync_conn
        )
    
    def chat(self, message: str) -> str:
        chain = self._prompt | self._llm | StrOutputParser()

        history_chain = RunnableWithMessageHistory(
            chain,
            lambda session_id: self._get_chat_history(session_id),
            input_messages_key="message",
            history_messages_key="chat_history",
        )

        result = history_chain.invoke(
            {"message": message},
            config={"configurable": {"session_id": str(self._session_id)}},
        )

        return result
    
