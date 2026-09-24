from typing import TypedDict
from langgraph.graph import END,StateGraph


# langgraph phase1 creating an state 1
class State(TypedDict):
  number:int
def double(state:State)->dict:
  board=state["number"]
  newnum=board*2
  print("in double")
  print(newnum)
  return{"number":newnum}
def finish(state:State)->dict:
  board=state["number"]
  
  print("finish")
  
  return{"number":board}
def decision(state:State)->str:
  if(state["number"]<100):
    return "double"
  else:
    return "finish"

    # creating an graph
  
builder=StateGraph(State)
builder.add_node("double",double)
builder.add_node("finish",finish)
# graph starting point source node
builder.set_entry_point("double")
builder.add_conditional_edges(
    "double",      ##this is the starting point means from wehre the edge is been starting 
    decision,      # decision function
    {"double":"double","finish":"finish"},  ##this is the condition on teh basic of descision output we decise if double then conect the double else finish one

)
builder.add_edge("finish",END)

#compile the graph that created
graph=builder.compile()

if __name__=="__main__":
  result=graph.invoke({"number":5})