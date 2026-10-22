"""Bug-fixing coding agent (no LangGraph).

Flow: ask the user for the bug -> LLM investigates with tools (search_files, search_in_file,
replace_line) -> run a verify command -> if it still fails, retry with the error (max 2 attempts).
The tools only touch files inside WORKSPACE, so the agent can never edit the rest of the project.
"""
import os
import json
import subprocess
import sys
from pathlib import Path
from groq import Groq, BadRequestError, APIError
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"), max_retries=4)

MODEL = "openai/gpt-oss-20b"
WORKSPACE = Path(__file__).parent / "workspace"
DEFAULT_VERIFY = f'"{sys.executable}" shop.py'
MAX_FIX_ATTEMPTS = 2
MAX_TOOL_CALLS_PER_ATTEMPT = 12
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv"}


def step(text: str):
    print(f"\n>>> {text}")


# ---------------- tools ----------------

def _resolve(path: str) -> Path:
    """Workspace-relative path -> absolute path; refuses anything outside WORKSPACE."""
    full = (WORKSPACE / path).resolve()
    if WORKSPACE.resolve() not in full.parents and full != WORKSPACE.resolve():
        raise ValueError(f"Path '{path}' is outside the workspace")
    return full


def search_files(keyword: str) -> str:
    """Paths (relative to workspace) whose name or content contains the keyword."""
    keyword_lower = keyword.lower()
    matches = []
    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            full = Path(root) / name
            rel = full.relative_to(WORKSPACE).as_posix()
            try:
                content = full.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                content = ""
            if not keyword or keyword_lower in name.lower() or keyword_lower in content.lower():
                matches.append(rel)
    return json.dumps(matches[:20]) if matches else "No files found."


def search_in_file(path: str, keyword: str = "") -> str:
    """Matching lines with line numbers (+/-2 lines of context). Empty keyword = whole file."""
    lines = _resolve(path).read_text(encoding="utf-8").splitlines()
    if not keyword:
        return "\n".join(f"{i}: {line}" for i, line in enumerate(lines[:300], 1))
    hits = [i for i, line in enumerate(lines) if keyword.lower() in line.lower()]
    if not hits:
        return f"'{keyword}' not found in {path}."
    shown = sorted({j for i in hits for j in range(max(0, i - 2), min(len(lines), i + 3))})
    return "\n".join(f"{j + 1}: {lines[j]}" for j in shown)


def replace_line(path: str, line_number: int, old_line: str, new_line: str) -> str:
    """Replace one line (1-indexed). old_line must match the current line, so a wrong
    line number can never overwrite unrelated code. new_line must include its indentation."""
    full = _resolve(path)
    with full.open(encoding="utf-8", newline="") as f:  # newline="" keeps \r\n vs \n as-is
        lines = f.read().splitlines(keepends=True)
    if not 1 <= line_number <= len(lines):
        return f"Invalid line number {line_number}; {path} has {len(lines)} lines."
    current = lines[line_number - 1]
    content = current.rstrip("\r\n")
    if content.strip() != old_line.strip():
        nearby = range(max(0, line_number - 3), min(len(lines), line_number + 2))
        context = "\n".join(f"{i + 1}: {lines[i].rstrip()}" for i in nearby)
        return (f"REFUSED: line {line_number} is not the line you expected.\n"
                f"Expected: {old_line.strip()}\nActual:   {content.strip()}\nNearby lines:\n{context}")
    lines[line_number - 1] = new_line.rstrip("\r\n") + current[len(content):]
    with full.open("w", encoding="utf-8", newline="") as f:
        f.write("".join(lines))
    print(f"    {path}:{line_number}\n    - {content}\n    + {new_line}")
    return f"Replaced line {line_number}.\nOLD: {content}\nNEW: {new_line}"


TOOLS = [
    {"type": "function", "function": {
        "name": "search_files",
        "description": "List workspace file paths whose name or content contains a keyword "
                       "(function name, class, error text...). Empty keyword lists all files.",
        "parameters": {"type": "object", "properties": {"keyword": {"type": "string"}},
                       "required": ["keyword"]}}},
    {"type": "function", "function": {
        "name": "search_in_file",
        "description": "Show lines of a file containing a keyword, with line numbers and context. "
                       "Empty keyword shows the whole file with line numbers.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string", "description": "Path relative to the workspace"},
            "keyword": {"type": "string"}}, "required": ["path", "keyword"]}}},
    {"type": "function", "function": {
        "name": "replace_line",
        "description": "Replace a single line in a file with a new line. You must pass the current text "
                       "of that line as old_line; the edit is refused if it does not match.",
        "parameters": {"type": "object", "properties": {
            "path": {"type": "string"},
            "line_number": {"type": "integer", "description": "1-indexed line number"},
            "old_line": {"type": "string", "description": "Current text of that line, copied exactly"},
            "new_line": {"type": "string", "description": "Full replacement line, with indentation"}},
            "required": ["path", "line_number", "old_line", "new_line"]}}},
]
FUNCTIONS = {"search_files": search_files, "search_in_file": search_in_file, "replace_line": replace_line}

SYSTEM_PROMPT = """You are an expert software engineer and debugger. You fix bugs in code written in ANY
programming language (Python, JavaScript, Java, C++, Go, ...), working only through your tools.

Tools:
- search_files(keyword): find which files are related to the bug.
- search_in_file(path, keyword): get exact line numbers and surrounding code. Use an empty keyword to read a whole file.
- replace_line(path, line_number, old_line, new_line): replace ONE line. old_line must be the exact current
  text of that line (copy it from search_in_file output); keep the original indentation in new_line.
  If an edit is REFUSED, read the "Actual" line and nearby lines it shows, then retry with the right line number.
Do not re-read the same file over and over; read it once, then act.

Method:
1. Understand the bug report / error output (stack traces name the file and line).
2. Locate the related files, then read the relevant code.
3. Find the ROOT CAUSE; do not hide the error (no try/except swallowing, no deleting checks or asserts).
4. Make the smallest correct change with replace_line.
5. When done, reply in plain text: the root cause, the file:line you changed, and why the fix works.
If you cannot find the bug, say so plainly instead of guessing."""


# ---------------- agent loop ----------------

def ask_llm(messages, tools=None):
    kwargs = {"model": MODEL, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"
    return groq_client.chat.completions.create(**kwargs).choices[0].message


def final_answer(messages) -> str:
    """Plain-text reply. gpt-oss sometimes still emits a tool call (Groq 400) - don't crash on it."""
    try:
        return ask_llm(messages).content
    except BadRequestError:
        return "(The model did not produce a summary.)"


def run_fix_attempt(messages) -> str:
    """One attempt: let the LLM use tools until it answers in plain text."""
    used = 0
    while True:
        if used >= MAX_TOOL_CALLS_PER_ATTEMPT:
            step("Tool-call limit reached, asking the model to summarise")
            messages.append({"role": "user", "content": "Tool limit reached. Summarise what you changed."})
            return final_answer(messages)
        step("Thinking (LLM deciding next action)")
        try:
            msg = ask_llm(messages, TOOLS)
        except BadRequestError as e:
            if "tool_use_failed" not in str(e):
                raise
            step("Model made an invalid tool call, asking it to try again")
            messages.append({"role": "user", "content": "Your last tool call was invalid (wrong or missing "
                             "arguments). Check the tool schema and try again."})
            used += 1
            continue
        if not msg.tool_calls:
            return msg.content
        messages.append(msg)
        for call in msg.tool_calls:
            used += 1
            args = json.loads(call.function.arguments or "{}")
            step(f"Tool {used}/{MAX_TOOL_CALLS_PER_ATTEMPT}: {call.function.name}({json.dumps(args)[:150]})")
            try:
                result = FUNCTIONS[call.function.name](**args)
            except Exception as e:
                result = f"Tool error: {e}"
            messages.append({"role": "tool", "tool_call_id": call.id, "name": call.function.name,
                             "content": result})


def verify(command: str):
    """Run the user's check command in the workspace. Returns (passed, output)."""
    step(f"Verifying fix: {command}")
    try:
        proc = subprocess.run(command, shell=True, cwd=WORKSPACE, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, "Command timed out after 60s."
    output = (proc.stdout + proc.stderr).strip()
    print("    " + (output[-1500:].replace("\n", "\n    ") or "(no output)"))
    return proc.returncode == 0, output[-3000:]


def fix_bug(bug: str, verify_command: str) -> bool:
    step("Step 1: Running the program to reproduce the bug")
    passed, output = verify(verify_command)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Bug report from the user:\n{bug}\n\n"
                                    f"Output of `{verify_command}` right now (exit "
                                    f"{'OK' if passed else 'FAILED'}):\n{output or '(no output)'}"},
    ]
    for attempt in range(1, MAX_FIX_ATTEMPTS + 1):
        step(f"Step 2: Fix attempt {attempt}/{MAX_FIX_ATTEMPTS}")
        summary = run_fix_attempt(messages)
        messages.append({"role": "assistant", "content": summary or ""})
        print(f"\n[Agent] {summary}")

        step("Step 3: Checking the fix")
        passed, output = verify(verify_command)
        if passed:
            step(f"Bug fixed on attempt {attempt}")
            return True
        if attempt < MAX_FIX_ATTEMPTS:
            step("Still failing, retrying with the new error output")
            messages.append({"role": "user", "content": f"The check still fails. New output:\n{output}\n"
                                                        "Find what is still wrong and fix it."})
    step(f"Could not fix the bug in {MAX_FIX_ATTEMPTS} attempts")
    return False


if __name__ == "__main__":
    print("=== Coding agent ===")
    print(f"Workspace: {WORKSPACE}")
    while True:
        bug = input("\nAgent: What bug are you facing? Describe it or paste the error ('exit' to quit):\n> ")
        if bug.strip().lower() == "exit":
            break
        command = input(f"Agent: Command to check the code (Enter for default: {DEFAULT_VERIFY}):\n> ").strip()
        try:
            fix_bug(bug, command or DEFAULT_VERIFY)
        except APIError as e:
            print(f"[API error: {getattr(e, 'message', e)}] Wait a moment and try again.")
