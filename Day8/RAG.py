from pydantic import BaseModel,Field
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import time
load_dotenv()

# Retrieve API key
my_api_key = os.getenv("GROQ_API_KEY")
knowledgeBase={
    "name":"$$$$$$$$$$$$$$",
    "about":"############### ",
    "aim":"%%%%%%%%%%%%%%%%%%%%%%%^",
    "age":$$,
    "intership":"he is intern an spacex as an astorloger"
}

if not my_api_key:
    raise ValueError("API key missing")

# Initialize the client
client = Groq(api_key=my_api_key)

# Define model and message
model_name = "llama-3.3-70b-versatile"

Systemprompt=f"""
answer in 1 line only
"""
def retrivee(userprompt):
    userprompt=userprompt.lower()
    context_pieces = []

    if "about" in userprompt or "university" in userprompt or "education" in userprompt:
        context_pieces.append(knowledgeBase["about"])

    if "aim" in userprompt or "goal" in userprompt:
        context_pieces.append(knowledgeBase["aim"])

    if "age" in userprompt or "old" in userprompt:
        context_pieces.append(f"Age: {knowledgeBase['age']}")

    if "intern" in userprompt or "internship" in userprompt:
        context_pieces.append(knowledgeBase["intership"])

    if not context_pieces:
        return "No information is present in the knowledge base."

    return " | ".join(context_pieces)


def askllm(prompt):
    context=retrivee(prompt)
    Systempromp=f"""answer based on context do not think anything or search anywhere else. Context: {context}"""
    systemmessage={
        "role":"system",
        "content":Systempromp
    }
    message={
        "role":"user",
        "content":prompt
    }
    messages=[systemmessage,message]
    response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0,
        )
    answer=response.choices[0].message.content
    return answer

prompt="^^^^^^^^^^^^^^^^^^^^^^^^^^"
print(askllm(prompt))




"""
Step to Implement and rag
1.make an knowledge base make in pdf,dictionary etc etc
2.retival frm the knowlege base 
"""
