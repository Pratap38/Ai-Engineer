"""Runs the SAME scripted conversation through both systems and compares token usage."""
from single_agent import SingleAgent
from multi_agent import MultiAgent

SCRIPT = [
    "Hi, I want to buy a flat",
    "Budget 80 lakh, location Pune",
    "Tell me more about the first flat you listed",
    "My monthly salary is 1.5 lakh",
]

agents = [SingleAgent(), MultiAgent()]
for agent in agents:
    print(f"\n===== {agent.counter.name} =====")
    for line in SCRIPT:
        print(f"\nYou: {line}")
        print("Agent:", agent.turn(line))

print("\n===== TOKEN COMPARISON =====")
for agent in agents:
    print(agent.counter.report())
s, m = (a.counter.total for a in agents)
print(f"Multi agent used {m / s:.2f}x the tokens of single agent ({m - s:+d})")
