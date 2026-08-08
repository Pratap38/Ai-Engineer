import os
from pathlib import Path
from time import sleep
from dotenv import load_dotenv
from groq import Groq
import re

# Load environment variables
load_dotenv()

# Retrieve API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key missing")

# Initialize the client
client = Groq(api_key=my_api_key)

# Define model and message
model_name = "llama-3.3-70b-versatile"

def getperson(person1):
    person1 = person1.strip().lower()

    if person1 in [
        "mahatma gandhi",
        "gandhi",
        "mohandas karamchand gandhi"
    ]:
        return {
            "name": "Mahatma Gandhi",
            "full_name": "Mohandas Karamchand Gandhi",
            "born": "2 October 1869",
            "birthplace": "Porbandar, Gujarat, India",
            "died": "30 January 1948",
            "known_for": "Leading India's freedom movement",
            "principles": "Truth, non-violence and peaceful protest",
            "role": "Leader of the Indian independence movement",
            "important_work": "He encouraged Indians to fight for independence through non-violent civil disobedience.",
            "famous_for": "The Salt March and the Quit India Movement"
        }

    elif person1 in [
        "b. r. ambedkar",
        "b.r. ambedkar",
        "br ambedkar",
        "bhimrao ramji ambedkar",
        "ambedkar"
    ]:
        return {
            "name": "B. R. Ambedkar",
            "full_name": "Bhimrao Ramji Ambedkar",
            "born": "14 April 1891",
            "birthplace": "Mhow, Madhya Pradesh, India",
            "died": "6 December 1956",
            "known_for": "Social reform and fighting for equality",
            "role": "Chairman of the Drafting Committee of the Indian Constitution",
            "principles": "Equality, justice and education",
            "important_work": "He worked to improve the rights and opportunities of disadvantaged communities."
        }

    else:
        return {
            "error": "I don't have information about this person."
        }

def getQuality(quality):
    if quality == "non-violence":
        return "Mahatma Gandhi"

    elif quality == "social reform":
        return "B. R. Ambedkar"

    elif quality == "equality":
        return "B. R. Ambedkar"

    elif quality == "independence movement":
        return "Mahatma Gandhi"

    elif quality == "peaceful protest":
        return "Mahatma Gandhi"

    elif quality == "constitution":
        return "B. R. Ambedkar"

    else:
        return "I don't have an answer for that field."

tool={
        "getperson":getperson,
        "quality":getQuality
    }
systemPrompt ="""
You are an social activist.

you have 2 tool:
getperson(person)
quality(quality)
Important:
Call tool exactly as shown in the example:
Action: getperson("mahatma Gandhi")
Action: quality("equality")
Never write:
getperson(person="gandhi")
and same for the quality
Follow these rules:

1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7.If the user ask for information of any  person provde the information
8. If the user asks for BOTH person information and a comparison, include BOTH:
   - the person's information from getperson()
   - the comparison result from quality()
9. When the task is complete, give the Final Answer.
Format:

Thought: what you need to do
Action: tool_name(argument)

When finished:

Final Answer: your answer

"""

def Agent(query):
    message=[
        {"role":"system",
        "content":systemPrompt
        },
        {
            "role":"user",
            "content":query
        }
    ]
    for i in range(5):
        print("the step number is:",i+1)

        response=client.chat.completions.create(
            model=model_name,
            messages=message
        )
        answer=response.choices[0].message.content
        print(answer)
        if "Final Answer:" in answer:
            break

        match = re.search(
            r"Action:\s*(\w+)\((.*?)\)",
            answer
        )
        if match:
            toolName=match.group(1)
            tool_input = match.group(2)

            tool_input = tool_input.strip()

            tool_input = tool_input.strip('"')

            if toolName in tool:
                tools=tool[toolName]
                Observation=tools(tool_input)
            else:
                Observation="required tool doesnot exit"

            message.append({
                "role":"assistant",
                "content":answer

            })
            message.append({
                "role": "user",
                "content":
                    "Observation: "
                    + str(Observation)
            })
            sleep(5)

prompt="""
hey i want to know about mahatma Gandhi who is he mean about him all tell me 
and some what i want to know the quality between him and br amedhkar who is the best
"""

Agent(prompt)
