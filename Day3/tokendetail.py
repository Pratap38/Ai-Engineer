
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

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

SystemMessage={
    "role":"system",
    "content":"You are gamer that use to suggest nick name suggest only one"
}
prompt="what colour is the sky"
prop2="what is India describe in less than 10 word"
prop3="who is elon musk describe in more that 1000word"
promptlist=[prompt,prop2,prop3]
for i in promptlist:
    message = {
    "role": "user",
    "content": i
}
    messages=[message]
    response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=2,
    max_tokens=50,
)
    usage=response.usage
    print(f"prmpt :{i}-->your token:{usage.prompt_tokens} completion token:{usage.completion_tokens} total:{usage.total_tokens} finish reson:{response.choices[0].finish_reason}")
    # print(response.choices[0].message.content)
    # print(response.message.content)
    # print(respo)
    




# API requires a list of messages
# messages = [SystemMessage,message]

# Create the completion call
# response = client.chat.completions.create(
#     model=model_name,
#     messages=messages,
#     temperature=2,
# )

# Print the response content
# print(response.choices[0].message.content)