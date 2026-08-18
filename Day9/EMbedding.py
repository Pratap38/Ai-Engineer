import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('all-MiniLM-L6-v2')
#
def consineSimilar(a,b):
  return np.dot(a,b)/( np.linalg.norm(a)*np.linalg.norm(b))
text="hello machine learning "
res=model.encode(text)
print(res[:10])
a="there is an sunny day"
b="today is an hot winter day "
a1=model.encode(a)
b1=model.encode(b)
print(consineSimilar(a1,b1))
