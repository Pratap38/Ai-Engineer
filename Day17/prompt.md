we want to make an coding agent which is responsible for solving the bug that user will be providing
for this we are using the grok llm. As u can see in the project

the llm will have some tol which help to solve the bugs
one tool can be search file which list path of files  which are realted to the bug.
we need search in file tol which can give line number that is related to bug.
we need relace hwich allows the replacing a line with another line

i want to test this using an simple .py file and write an boiler plate code in it. and for now keep it bug free

i will provide the bug that i get through the cli to the llm to fix the bug.
make this without using langgraph.
Max retry of fixing this bugis allowed is 2
also showcase using print statement which step is currently going
as i introduce the bug the llm should as me the bug and start working on it
also this llm is reponsible to fix the bug at any language but the coding is done in python
if any doubt ask me .