import os
from dotenv import load_dotenv

GroqApiKey=os.getenv("GROQ_API_KEY")

SummariseModel="llama-3.3-70b-versatile"
ReviewerModel="llama-3.3-70b-versatile"

# we are thinking first to control the word  lenght per page
TotalWordPerPage=500
CompressionTarget=0.28 
CompressionMin=0.23
CompressionMax=0.33

ChunkingMaxTokens=3500

# Now ratelimit the model to review and check it default working
MaxRetries=3
TimeGap=2

EdgeLine=3
RepeatRatio=0.6
MinCharPerPage=100
WINDOW_PAGES = 10              # fallback: fixed page windows when no chapters are found
OuputDir="Output"