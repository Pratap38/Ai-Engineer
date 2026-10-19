Task is we are building an multi agent system 
before:
we want an single agent system that is responsible for using the tool like websearch along with using the calculator to analyse the price in emi and also the year require based on salary
this ai is responsible for searching the best available home rent  by asking the user first the buget and also the location in India only
after showcasng the home area and all when the user input the flat name our ai ask their salary monthly and then
the calculator agent is responsible for calculating all the emi and all to buy that flat
for it have an single askllm function 
max attempt of tool call is 4

after this building we will convert this into multiagent system without langgraph first

in multi agent divide in 3 -> 1. mangaer -> only job to decide the helper llm need
2 search llm-> access to search tool
3 calucator llm-> only access to calculation

the role will be for all given through system prompt as an expert prompt engineer
the manager llm must have an notes file in order to keep the notes by the llm ( mean keep an track)
also use to show in both the token consumption of both single and multi agent for the same in order to compare the token consumption for them 

if you have any doubt ask me
