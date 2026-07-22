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

message = {
    "role": "user",
    "content": "Do you know  Pratap38 as he is in github?"
}

# API requires a list of messages
messages = [message]

# Create the completion call
response = client.chat.completions.create(
    model=model_name,
    messages=messages
)

# Print the response content
print(response.choices[0].message.content)