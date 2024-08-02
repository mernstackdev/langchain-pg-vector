from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

qa_template_prompt = """You are a helpful Assistant AI who has been equipped with your own special knowledge base. In response to the user's query you have retrieved the most relevant parts of your knowledge base you could find:

{context}

END OF RETRIEVED PARTS OF YOUR KNOWLEDGE BASE.

USER'S QUERY: {question}

YOUR TASK: present the retrieved parts in a digestible way:
1. Start with the TLDR section heading (use Markdown) followed by a quick summary of only the retrieved parts directly relevant to the user's query, if there are any.
2. Continue the rest of your report in Markdown, with section headings. For this part, completely ignore user's query.

YOUR RESPONSE: """
QA_PROMPT_TEMPLATE = ChatPromptTemplate.from_template(qa_template_prompt)

just_chat_system_template = """You are a friendly Assistant AI who has been equipped with your own special knowledge base and the ability to do Internet research. For this part of the conversation you won't be retrieving any information from your knowledge base or the Internet. Instead, you will just chat with the user, keeping in mind that you may have used your knowledge base and/or the Internet earlier in the conversation. Use Markdown syntax for your reply."""
JUST_CHAT_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", just_chat_system_template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{message}"),
    ]
)