import os
import json
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL = "openai/gpt-oss-20b"


def web_search(query: str) -> str:
    """Runs a live web search via Tavily and returns the top results as text."""
    results = tavily_client.search(query=query, max_results=3)
    return json.dumps(results["results"])


def text_sumariser(text: str) -> str:
   
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Summarise the given text always stricly in hinglish clearly and concisely ."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content


# This is the "menu" the LLM reads to decide if/when it needs a tool.
tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the live web for current or unknown information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "text_sumariser",
            "description": "Summarise a given piece of text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "The text to summarise"}
                },
                "required": ["text"],
            },
        },
    },
]

available_functions = {"web_search": web_search, "text_sumariser": text_sumariser}


def run_agent(user_question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Use the web_search tool whenever you need current or unknown information, and the text_sumariser tool when asked to summarise text. If a tool already returns a complete, final answer (such as a summary), pass it back to the user exactly as given - do not translate, rewrite, or paraphrase it into a different language or style.",
        },
        {"role": "user", "content": user_question},
    ]

    # Round 1: let the model decide whether it needs a tool
    response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if not tool_calls:
        return response_message.content

    # The model asked for a tool: run it and feed the result back
    messages.append(response_message)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_response = available_functions[function_name](**function_args)
        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            }
        )

    # Round 2: model writes the final answer using the tool results
    second_response = groq_client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return second_response.choices[0].message.content


if __name__ == "__main__":
    question = input("Ask your agent something: ")
    print(run_agent(question))
