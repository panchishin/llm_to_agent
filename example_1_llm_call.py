from bot_util import llm

while True:
    question = input("? ")
    message = [{"role": "user", "content": question}]
    response = llm(message)
    print(response)
