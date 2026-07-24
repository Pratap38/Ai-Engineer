import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

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
text="hello myself suresh Rain i buyed chenai super kinges and they are not working .My email id is sureshRaina@gmal.com"
prompt=f"""
This is an customer an extract the personal information and the complain from this {text}
"""
class StructureDetail(BaseModel):
    name:str
    email:str
    issue:str

schema=StructureDetail.model_json_schema()
responseFormat={
    "type":"json_object"
}
SystemPrompt=f"""
extract the personal info and the output is based  on this {schema}and provide in json format
"""
message = {
    "role": "user",
    "content": prompt
}
messageSystem = {
    "role": "system",
    "content": SystemPrompt
}

# API requires a list of messages
messages = [messageSystem,message]

# Create the completion call
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=2
)

# Print the response content
print(response.choices[0].message.content)



# this is the output of an unstructure when pydantic is not been applied before
#Here's the extracted personal information and complaint:
# **Personal Information:**
# - Name: Suresh Rain
# - Email ID: sureshRaina@gmal.com (Note: there seems to be a typo in the email provider, it likely should be "gmail" instead of "gmal")

# **Complaint:**
# - The customer, Suresh Rain, purchased "Chennai Super Kings" products/items (the context suggests these could be related to a sports team or specific merchandise, as Chennai Super Kings is a cricket team) and reports that they are not working as expected.

#After Structure output here is the answer 
#  StructureDetail =
# {
#     "name": "Suresh Rain",
#     "email": "sureshRaina@gmal.com",
#     "issue": " Chenai Super kings product is not working"
# }