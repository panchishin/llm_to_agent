from bot_util import llm
from rag_util import search_document

chat = []

while True:
    question = input("? ")
    
    top_passages = search_document(question)

    print("\n=== Passages being sent to the LLM along with the question ===\n" + "\n===\n".join(top_passages) + "\n")

    context = """You are a helpful assistant.
The user is asking questions about a book.
Answer the users question based on the following context found by searching the book:
===
""" + "\n===\n".join(top_passages) + "\n==="

    messages = [
        {"role": "system", "content": context},
        *chat,
        {"role": "user", "content": question}
    ]

    # CALL THE LLM !
    response = llm(messages)
    
    chat.append({"role": "user", "content": question})
    chat.append({"role": "assistant", "content": response})

    print("\n=== LLM Response ===\n", response, "\n")
