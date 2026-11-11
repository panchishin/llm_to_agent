print("Starting up...")

import datetime # keep for the REPL tool
from rag_util import search_document
from bot_util import llm


tools = {
    "REVERSE": {
        "description": "Reverses the following text.  For example REVERSE hello world would return 'dlrow olleh'",
        "do": lambda x: x[::-1]
    },
    "LENGTH": {
        "description": "Returns the length of the following text.  For example LENGTH hello world would return '11'",
        "do": lambda x: f"{len(x)}"
    },
    "MAIL": {
        "description": "Sends an email to an address with just a subject.  For example MAIL jane@example.com Hello Jane would send 'Hello Jane' to jane@example.com",
        "do": lambda x: f"Sent email to '{x.split()[0]}' with subject '{' '.join(x.split()[1:])}'"
    },
    "REPL": {
        "description": "Executes the following python code and returns the output.  For example REPL 2 + 2 would return '4'.  Example REPL datetime.datetime.now().isoformat() would return the current date and time.  This tool only accepts 1 line of code.  The following imports are available: datetime and numpy (as np).  Do not import libraries.",
        "do": lambda x: str(eval(x))
    },
    "SEARCH": {
        "description": "Searches a book for relevant passages.  The search term becomes a vector cosine similarity query.  Because of this, state the search so that it matches concepts.  For example SEARCH falling or thoughts.  This would match passages about falling or thoughts." ,
        "do": lambda x: "\n".join(search_document(x))
    }
}


def tool_descriptions():
    return "\n".join([f"{name} = {tool['description']}" for name, tool in tools.items()])




system_message = f"""You are a helpful assistant.

You have access to the following tools:
{tool_descriptions()}

Attempt to use the tools to answer the users questions.  Be creative.  REPL can do a lot.
Only respond with facts from the tools.
NEVER use your own knowledge to answer questions.
If the answer is not in the tool output, say "I cannot find the answer and have been programmed to not make up answers"

To use a tool, first describe your intention, then state the tool and the arguments as the last line of your response.

Example 1 - reversing text:
User: Can you reverse the text 'hello world'?
Assistant: The user wants to reverse text.  This is something LLMs are not great at, so I'll use the REVERSE tool to do it.
REVERSE hello world

The output of the tool will be returned to you and you will have an opportunity to use the output in your quest to help the user.
After you receive the output of a tool, feel free to call another tool if needed.

If you do not specify a tool as the last line of your response then your entire response will be sent to the user.
"""



print("start")
message = [
    {"role": "system", "content": system_message},
]

while True:
    question = input("? ")

    message.append({"role": "user", "content": question})


    while True:

        # CALL THE LLM !
        response = llm(message)

        print("\nLLM RESPONSE: ", response, "\n---")
        message.append({"role": "assistant", "content": response})

        # get the last line and the tool name
        last_line = response.strip().split("\n")[-1]
        tool_name = last_line.split()[0]
        tool_args = " ".join(last_line.split()[1:])

        if tool_name not in tools:
            # assume the response is the final answer
            break

        try:
            tool = tools[tool_name]
            tool_result = tool["do"](tool_args)
        except Exception as e:
            tool_result = f"Error executing tool: {e}"

        tool_result = f"RESULT OF {last_line} = {tool_result}"

        print(f"\n{tool_result}")
        message.append({"role": "assistant", "content": f"{tool_result}"})

    print()

