import os
import json
from groq import Groq, BadRequestError, APIError
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=4)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL = "openai/gpt-oss-20b"
MAX_TOOL_CALLS = 4


class TokenCounter:
    """Accumulates token usage from every LLM call of one system."""

    def __init__(self, name: str):
        self.name = name
        self.prompt = 0
        self.completion = 0
        self.calls = 0

    def add(self, usage):
        self.prompt += usage.prompt_tokens
        self.completion += usage.completion_tokens
        self.calls += 1

    @property
    def total(self) -> int:
        return self.prompt + self.completion

    def report(self) -> str:
        return (f"[{self.name}] LLM calls: {self.calls} | prompt: {self.prompt} | "
                f"completion: {self.completion} | total: {self.total}")


def ask_llm(messages, counter: TokenCounter, tools=None, json_mode=False):
    """The single LLM entry point: every model call in both systems goes through here."""
    kwargs = {"model": MODEL, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = groq_client.chat.completions.create(**kwargs)
    counter.add(response.usage)
    return response.choices[0].message


# ---------------- tools ----------------

def web_search(query: str) -> str:
    """Live web search via Tavily; trimmed to keep token usage low."""
    results = tavily_client.search(query=query, max_results=3)["results"]
    return json.dumps([{"title": r["title"], "url": r["url"], "content": r["content"][:250]} for r in results])


def calculate_emi(price: float, down_payment_percent: float = 20, annual_rate_percent: float = 8.5,
                  tenure_years: float = 20) -> str:
    """EMI for a home loan of price minus down payment."""
    loan = price * (1 - down_payment_percent / 100)
    r = annual_rate_percent / 12 / 100
    n = int(tenure_years * 12)
    emi = loan * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return json.dumps({"loan_amount": round(loan), "down_payment": round(price - loan),
                       "emi_per_month": round(emi), "total_payable": round(emi * n),
                       "total_interest": round(emi * n - loan)})


def calculate_years_required(price: float, monthly_salary: float, down_payment_percent: float = 20,
                             annual_rate_percent: float = 8.5, max_emi_percent_of_salary: float = 40) -> str:
    """Shortest tenure (years) at which EMI stays within the given share of salary."""
    loan = price * (1 - down_payment_percent / 100)
    r = annual_rate_percent / 12 / 100
    budget = monthly_salary * max_emi_percent_of_salary / 100
    for months in range(12, 30 * 12 + 1):
        emi = loan * r * (1 + r) ** months / ((1 + r) ** months - 1)
        if emi <= budget:
            return json.dumps({"years_required": round(months / 12, 1), "emi_per_month": round(emi),
                               "emi_budget_from_salary": round(budget)})
    return json.dumps({"error": "Not affordable even over 30 years", "emi_budget_from_salary": round(budget)})


SEARCH_TOOL = {"type": "function", "function": {
    "name": "web_search", "description": "Search the live web for homes/flats for rent or sale in India.",
    "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}}

EMI_TOOL = {"type": "function", "function": {
    "name": "calculate_emi", "description": "Monthly EMI, total interest and total payable for buying a flat.",
    "parameters": {"type": "object", "properties": {
        "price": {"type": "number", "description": "Flat price in INR"},
        "down_payment_percent": {"type": "number"},
        "annual_rate_percent": {"type": "number"},
        "tenure_years": {"type": "number"}}, "required": ["price"]}}}

YEARS_TOOL = {"type": "function", "function": {
    "name": "calculate_years_required",
    "description": "Years of loan tenure needed so that EMI fits within the user's monthly salary.",
    "parameters": {"type": "object", "properties": {
        "price": {"type": "number", "description": "Flat price in INR"},
        "monthly_salary": {"type": "number", "description": "Monthly salary in INR"},
        "down_payment_percent": {"type": "number"},
        "annual_rate_percent": {"type": "number"},
        "max_emi_percent_of_salary": {"type": "number"}}, "required": ["price", "monthly_salary"]}}}

FUNCTIONS = {"web_search": web_search, "calculate_emi": calculate_emi,
             "calculate_years_required": calculate_years_required}


def final_answer(messages, counter: TokenCounter) -> str:
    """Force a plain-text reply. gpt-oss sometimes still emits a tool call with no tools offered,
    which Groq rejects with 400 - in that case return a safe fallback instead of crashing."""
    try:
        return ask_llm(messages, counter).content
    except BadRequestError:
        return "I could not finish that with the information I have. Could you rephrase or give more details?"


def run_tool_loop(messages, counter: TokenCounter, tools):
    """Let the model call tools (max MAX_TOOL_CALLS in total), then return its final text.
    Mutates `messages`."""
    used = 0
    while True:
        if used >= MAX_TOOL_CALLS:
            messages.append({"role": "user", "content": "SYSTEM: tool limit reached. Reply in plain text now "
                             "using what you have, or ask the user for what is missing."})
            return final_answer(messages, counter)
        try:
            msg = ask_llm(messages, counter, tools=tools)
        except BadRequestError as e:
            # The model produced an invalid tool call (e.g. null/missing argument). Don't crash:
            # tell it, and let it answer without tools (usually by asking the user for the missing info).
            if "tool_use_failed" not in str(e):
                raise
            print("   [invalid tool call, asking model to recover]")
            messages.append({"role": "user", "content": "SYSTEM: your last tool call had missing or null "
                             "arguments. Do not call tools now; ask the user for the missing information."})
            return final_answer(messages, counter)
        if not msg.tool_calls:
            return msg.content
        messages.append(msg)
        for call in msg.tool_calls:
            if used >= MAX_TOOL_CALLS:
                result = "Tool call limit reached. Answer with what you have."
            else:
                used += 1
                try:
                    result = FUNCTIONS[call.function.name](**json.loads(call.function.arguments))
                except Exception as e:
                    result = f"Tool error: {e}"
                print(f"   [tool {used}/{MAX_TOOL_CALLS}] {call.function.name}")
            messages.append({"role": "tool", "tool_call_id": call.id, "name": call.function.name,
                             "content": result})


def safe_turn(agent, text: str) -> str:
    """CLI helper: API errors (rate limit etc.) become a message instead of a crash."""
    try:
        return agent.turn(text)
    except APIError as e:
        return f"[API error: {getattr(e, 'message', e)}] Wait a moment and try again."
