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
RepeatRatio=0.4
MinCharPerPage=100

OuputDir="Output"