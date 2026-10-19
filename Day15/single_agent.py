from common import safe_turn, TokenCounter, run_tool_loop, SEARCH_TOOL, EMI_TOOL, YEARS_TOOL

SYSTEM_PROMPT = """You are an expert Indian real-estate advisor and prompt-following assistant.
Tools: web_search (find homes/flats), calculate_emi, calculate_years_required.

Workflow, follow strictly:
1. First ask the user for their BUDGET and the LOCATION (India only). Do not search before you have both.
   Refuse locations outside India.
2. Use web_search to find the best available homes at that budget/location. Show a short list with
   name, area, price and key details.
3. When the user picks a flat by name, ask for their MONTHLY SALARY (if not yet known).
4. Then use the calculator tools to give: monthly EMI, total interest, and the loan years required
   based on their salary (assume 20% down payment, 8.5% rate unless the user says otherwise; state assumptions).
Call a calculator tool ONLY when you know the flat's real price (from search results) AND the
user's monthly salary. If either is missing, ask the user instead. If the user answers with just a number
like '1', it means the Nth flat in your last list.
Never invent prices: use search results. Never do EMI maths yourself: use the calculator tools.
Use at most 2 web searches per user message (make them broad, not many near-duplicates).
At most 4 tool calls per user message. Be concise."""


class SingleAgent:
    def __init__(self):
        self.counter = TokenCounter("SINGLE AGENT")
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def turn(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})
        reply = run_tool_loop(self.messages, self.counter, [SEARCH_TOOL, EMI_TOOL, YEARS_TOOL])
        self.messages.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    agent = SingleAgent()
    print("Home advisor (single agent). Type 'exit' to quit.")
    while True:
        text = input("\nYou: ")
        if text.strip().lower() == "exit":
            break
        print("\nAgent:", safe_turn(agent, text))
    print("\n" + agent.counter.report())
