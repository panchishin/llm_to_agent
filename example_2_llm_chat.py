from bot_util import llm


chat = []

while True:
    question = input("? ")
    chat.append({"role": "user", "content": question})          # append to chat
    response = llm(chat)
    print(response)
