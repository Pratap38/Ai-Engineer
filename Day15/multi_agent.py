import json
from pathlib import Path
from common import safe_turn, TokenCounter, ask_llm, run_tool_loop, SEARCH_TOOL, EMI_TOOL, YEARS_TOOL

NOTES_FILE = Path(__file__).parent / "manager_notes.md"
MAX_MANAGER_STEPS = 4

MANAGER_PROMPT = """You are an expert prompt engineer acting as the MANAGER of a home-buying assistant for India.
Your ONLY job is to decide which helper is needed next. You never search or calculate yourself.

Helpers:
- "search": has the web search tool. Use it to find homes/flats once budget AND location (India only) are known.
- "calculator": has EMI / loan-years tools. Use it only once a flat is chosen (name + price known) AND monthly salary is known.
- "user": nobody else is needed; talk to the user (ask for missing budget/location/salary, refuse non-India
  locations, or present the final results).

If the user answers with just a number like '1', it means the Nth flat in the last list from the notes.
Flow: ask budget+location -> search -> show homes -> user picks a flat -> ask monthly salary -> calculator -> present.
You get the NOTES file (your running memory) and the conversation. Reply with JSON only:
{"next": "search"|"calculator"|"user",
 "task": "precise instruction for the helper (for user: the exact message to send, using helper results from the notes)",
 "note": "one short line to append to the notes (facts learned, decisions made)"}"""

SEARCH_PROMPT = """You are an expert prompt engineer-trained SEARCH specialist for Indian real estate.
Use web_search to carry out the task. Return a concise list of the best options: name, area, price, key details.
Never invent data. Max 4 tool calls."""

CALC_PROMPT = """You are an expert prompt engineer-trained CALCULATION specialist for home loans.
If the price or salary is missing from the task, reply asking for it instead of calling a tool.
Use calculate_emi and calculate_years_required only; never do the maths yourself. Assume 20% down payment and
8.5% rate unless told otherwise, and state assumptions. Return a concise result. Max 4 tool calls."""


def append_note(text: str):
    with NOTES_FILE.open("a", encoding="utf-8") as f:
        f.write(f"- {text}\n")


class MultiAgent:
    def __init__(self):
        self.counter = TokenCounter("MULTI AGENT")
        self.history = []  # only user/assistant turns, for the manager
        NOTES_FILE.write_text("# Manager notes\n", encoding="utf-8")

    def _worker(self, system_prompt, tools, task):
        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": task}]
        return run_tool_loop(messages, self.counter, tools)

    def turn(self, user_text: str) -> str:
        self.history.append({"role": "user", "content": user_text})
        append_note(f"USER: {user_text}")
        for _ in range(MAX_MANAGER_STEPS):
            notes = NOTES_FILE.read_text(encoding="utf-8")
            messages = [{"role": "system", "content": MANAGER_PROMPT + "\n\nNOTES FILE:\n" + notes}] + self.history
            decision = json.loads(ask_llm(messages, self.counter, json_mode=True).content)
            nxt, task = decision.get("next"), decision.get("task", "")
            if decision.get("note"):
                append_note(f"MANAGER: {decision['note']}")
            print(f"   [manager -> {nxt}]")
            if nxt == "search":
                result = self._worker(SEARCH_PROMPT, [SEARCH_TOOL], task)
                append_note(f"SEARCH RESULT: {result}")
            elif nxt == "calculator":
                result = self._worker(CALC_PROMPT, [EMI_TOOL, YEARS_TOOL], task)
                append_note(f"CALC RESULT: {result}")
            else:
                self.history.append({"role": "assistant", "content": task})
                return task
        fallback = "Sorry, I could not finish that. Please rephrase."
        self.history.append({"role": "assistant", "content": fallback})
        return fallback


if __name__ == "__main__":
    agent = MultiAgent()
    print("Home advisor (multi agent). Type 'exit' to quit.")
    while True:
        text = input("\nYou: ")
        if text.strip().lower() == "exit":
            break
        print("\nAgent:", safe_turn(agent, text))
    print("\n" + agent.counter.report())
