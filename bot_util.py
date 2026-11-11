from groq import Groq

client = Groq()

def llm(messages):
  completion = client.chat.completions.create(
      model="qwen/qwen3.8-27b",
      messages=messages,
      temperature=0.1,
      max_completion_tokens=4096,
      top_p=0.95,
      reasoning_effort="none",
      stream=False,
      stop=None
  )
  result = completion.choices[0].message.content
  messages.append({
      "role": "assistant",
      "content": result
  })
  return result


def ask(messages, question):
    messages.append({
      "role": "user",
      "content": question
    })
    return llm(messages)

if __name__ == "__main__":
   print(ask([], "What is the capital of France?"))