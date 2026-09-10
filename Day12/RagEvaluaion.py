import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance ,VectorParams,PointStruct


load_dotenv()


client=QdrantClient(url=Quadrant_Cluster,api_key=QuadrantAPI)
print("Quadrant connected !")


# creating quadrant collection/Table

CollectionName="knowledge"
EmbeddingSize=384


if client.collection_exists(CollectionName):
    print(f"Deleting existing collection :{CollectionName}")
    client.delete_collection(CollectionName)

    # creating an table

client.create_collection(
    collection_name=CollectionName,
    vectors_config=VectorParams(
        size=EmbeddingSize,
        distance=Distance.COSINE
    )
)

print(f"Table is been created:{CollectionName}")
print(f"Arraysize done{EmbeddingSize}")

with open("/content/knowledge.txt","r",encoding="utf-8")as f:
    lines=[
        line.strip()
        for line in f
        if line.strip()
    ]
CHUNK=5
OVERLAP=2
documents=[
    " ".join(lines[i:i+CHUNK])
    for i in range(0, len(lines), CHUNK-OVERLAP)
]

print(f"loaded {len(lines)} lines -> {len(documents)} chunks")


# now loading embedding profgram


model = SentenceTransformer('all-MiniLM-L6-v2')
model_name = "openai/gpt-oss-20b"

embedding=model.encode(documents)

points=[]        ## as we rember an point is that which store arrays id ,array and payload

for i,embed in enumerate(embedding):
    point=PointStruct(
        id=i+1,
        vector=embed.tolist(),
        payload={
            "text":documents[i]
        }
    )
    points.append(point)

# upload in quadrant

client.upsert(       ##upsert means upload+insert
    collection_name=CollectionName,
    points=points
)
print("file success upload")

def search(query,k=3):
    queryArray=model.encode(query).tolist()

    response = client.query_points(
        collection_name=CollectionName,
        query=queryArray,
        limit=k,
        with_payload=True,
    )
    return response.points


groqClient=Groq(
    api_key=GroqApi
)

goldenDataset = [
    {
        "id": 1,
        "question": "What is the standard internship stipend at Nexora Technologies?",
        "expected_information": [
            "Standard stipend is ₹15,000 per month",
            "Actual stipend may vary depending on role, experience, and offer letter",
            "The offer letter is the final authority"
        ],
        "answer": "The standard internship stipend is ₹15,000 per month. The final stipend amount is determined by the individual intern's offer letter."
    },
    {
        "id": 2,
        "question": "What are the normal working hours for interns?",
        "expected_information": [
            "Monday to Friday",
            "Working hours are 9:30 AM to 6:30 PM",
            "Lunch break is from 1:00 PM to 2:00 PM",
            "Approximately 8 working hours per day excluding lunch"
        ],
        "answer": "Interns normally work Monday to Friday from 9:30 AM to 6:30 PM, with a one-hour lunch break from 1:00 PM to 2:00 PM."
    },
    {
        "id": 3,
        "question": "How many paid leave days does an intern receive?",
        "expected_information": [
            "Interns receive 1 paid leave day per month",
            "3-month internship provides up to 3 paid leave days",
            "6-month internship provides up to 6 paid leave days",
            "Unused leave does not automatically carry forward"
        ],
        "answer": "Interns receive 1 paid leave day per month. Unused monthly leave does not automatically carry forward to the next month."
    },
    {
        "id": 4,
        "question": "Can interns take leave for university examinations?",
        "expected_information": [
            "Academic leave is allowed for university examinations",
            "Academic leave can also cover mandatory academic activities and university projects",
            "Leave should be requested in advance whenever possible",
            "Approval from mentor or manager is required"
        ],
        "answer": "Yes. Interns can request academic leave for university examinations and other important academic requirements, subject to approval from their mentor or manager."
    },
    {
        "id": 5,
        "question": "Can interns work from home?",
        "expected_information": [
            "WFH is permitted with approval",
            "Mentor or manager must approve WFH",
            "WFH is not an automatic right",
            "WFH may be approved for illness, emergencies, university requirements, or transportation problems",
            "Interns must remain available during working hours"
        ],
        "answer": "Yes, but work from home requires approval from the mentor or manager. Interns must remain available during normal working hours and attend scheduled meetings."
    },
    {
        "id": 6,
        "question": "Who should an intern contact for technical questions?",
        "expected_information": [
            "Assigned mentor is the first point of contact",
            "Mentor helps with technical requirements",
            "Mentor helps with projects, tools, processes, and deadlines",
            "Escalation path is Mentor → Team Lead → Engineering Manager"
        ],
        "answer": "The assigned mentor is normally the first point of contact for technical or daily work-related questions."
    },
    {
        "id": 7,
        "question": "Who should an intern contact about stipend-related questions?",
        "expected_information": [
            "HR handles stipend-related questions",
            "Offer letter determines the applicable stipend amount",
            "Stipend is normally paid during the first week of the following month"
        ],
        "answer": "Interns should contact HR for stipend-related questions."
    },
    {
        "id": 8,
        "question": "What is the minimum attendance requirement?",
        "expected_information": [
            "Minimum attendance requirement is 90%",
            "Attendance is recorded through the company attendance system",
            "Repeated late arrival or unexplained absence can affect performance evaluation"
        ],
        "answer": "Interns should maintain at least 90% attendance during their internship."
    },
    {
        "id": 9,
        "question": "Are Saturday and Sunday working days?",
        "expected_information": [
            "Saturday is normally a non-working day",
            "Sunday is normally a non-working day",
            "Normal working days are Monday to Friday"
        ],
        "answer": "Normally, no. Saturday and Sunday are non-working days."
    },
    {
        "id": 10,
        "question": "What should an intern do if they are sick?",
        "expected_information": [
            "Inform mentor or manager as soon as possible",
            "Short-term illness requires a basic explanation",
            "Extended illness may require documentation",
            "Sick leave is subject to company leave policy and approval"
        ],
        "answer": "The intern should inform their mentor or manager as soon as possible. Extended illness may require appropriate documentation from HR."
    },
    {
        "id": 11,
        "question": "Can unused monthly leave be carried forward?",
        "expected_information": [
            "Unused monthly leave does not automatically carry forward",
            "Carry-forward requires specific approval"
        ],
        "answer": "No. Unused monthly leave does not automatically carry forward to the next month unless specifically approved."
    },
    {
        "id": 12,
        "question": "Does completing an internship guarantee a full-time job?",
        "expected_information": [
            "Internship completion does not guarantee full-time employment",
            "Outstanding interns may be considered",
            "Consideration depends on performance",
            "Technical skills, team requirements, available positions, and business requirements are relevant"
        ],
        "answer": "No. Successfully completing an internship does not guarantee full-time employment. Outstanding interns may be considered based on performance, skills, team requirements, and available positions."
    },
    {
        "id": 13,
        "question": "Will interns receive an internship completion certificate?",
        "expected_information": [
            "Successful interns may receive an Internship Completion Certificate",
            "Certificate contains intern name",
            "Certificate contains internship role",
            "Certificate contains internship duration",
            "Certificate contains company name and completion date",
            "Certificate contains authorized company representative",
            "HR handles certificate-related questions"
        ],
        "answer": "Interns who successfully complete their internship may receive an Internship Completion Certificate."
    },
    {
        "id": 14,
        "question": "How long can the internship last?",
        "expected_information": [
            "Internship duration can be between 3 and 6 months",
            "Exact duration depends on the offer letter"
        ],
        "answer": "The internship duration can generally be between 3 and 6 months, depending on the offer letter."
    },
    {
        "id": 15,
        "question": "What is the normal reporting structure for interns?",
        "expected_information": [
            "Intern reports to Mentor",
            "Mentor reports to Team Lead",
            "Team Lead reports to Engineering Manager",
            "Technical and project questions should normally go to the mentor first",
            "HR handles administrative questions"
        ],
        "answer": "The normal reporting structure is Intern → Mentor → Team Lead → Engineering Manager."
    },
    {
        "id": 16,
        "question": "What happens if an intern is repeatedly late?",
        "expected_information": [
            "Repeated lateness negatively affects attendance records",
            "Repeated lateness may affect performance evaluation",
            "Interns are expected to arrive on time"
        ],
        "answer": "Repeated late arrival may negatively affect the intern's attendance records and performance evaluation."
    },
    {
        "id": 17,
        "question": "When is the monthly stipend normally paid?",
        "expected_information": [
            "Stipend is normally paid during the first week of the following month",
            "January stipend is normally paid during the first week of February",
            "Payment terms may depend on the offer letter"
        ],
        "answer": "The stipend is normally paid during the first week of the following month. For example, January's stipend is normally paid during the first week of February."
    },
    {
        "id": 18,
        "question": "Can interns use personal cloud storage for company data?",
        "expected_information": [
            "Company data must not be uploaded to personal cloud storage",
            "Unauthorized AI tools must not be used for company data",
            "Approval is required before using unauthorized services",
            "Interns must protect confidential company information"
        ],
        "answer": "No. Company data should not be uploaded to personal cloud storage or unauthorized AI tools without approval."
    },
    {
        "id": 19,
        "question": "What should an intern do if they cannot finish a task on time?",
        "expected_information": [
            "Inform the mentor early",
            "Communicate before the expected deadline",
            "Explain that the task cannot be completed on time",
            "Interns are expected to communicate regularly with their mentor"
        ],
        "answer": "The intern should inform their mentor early if they are unable to complete the task by the expected deadline."
    },
    {
        "id": 20,
        "question": "What are interns evaluated on?",
        "expected_information": [
            "Technical ability",
            "Quality of work",
            "Problem-solving ability",
            "Learning ability",
            "Communication",
            "Teamwork",
            "Attendance",
            "Punctuality",
            "Meeting deadlines",
            "Professional behavior",
            "Initiative"
        ],
        "answer": "Interns may be evaluated on technical ability, quality of work, problem-solving, learning ability, communication, teamwork, attendance, punctuality, meeting deadlines, professional behavior, and initiative."
    }
]
# expected information we have added in order to have relevance

def precisioncal(question,retriveDoc):
    relevatChunk=0

    for i,doc in enumerate(retriveDoc):
        CHUNK=doc.payload["text"]


        prompt = f"""
        You are evaluating the retrieval quality
        of a RAG system.

        Question:
        {question}

        Retrieved chunk:
        {CHUNK}

        Is this chunk relevant to answering
        the question?

        Return ONLY JSON:

        {{
            "relevant": true,
            "reason": "short explanation"
        }}

        Return true if the chunk contains information
        that is useful for answering the question.

        Return false if it is unrelated.
        """

        result=llmJudge(prompt)

        if result["relevant"]:
            relevatChunk+=1
    if len(retriveDoc)==0:
        return 0.0
    return(relevatChunk/len(retriveDoc))

def Recall(question,context,groundTruth):
    prompt = f"""
    You are evaluating the retrieval quality
    of a RAG system.

    Question:
    {question}

    Ground Truth Answer:
    {groundTruth}

    Retrieved Context:
    {context}

    Does the retrieved context contain enough
    information to produce the ground truth answer?

    Return ONLY JSON:

    {{
        "score": 0.0,
        "reason": "short explanation"
    }}

    Scoring:

    1.0 = All important information needed for
        the answer is present.

    0.7 = Most important information is present,
        but some details are missing.

    0.5 = Some important information is present.

    0.0 = The required information is absent.
"""


    result = llJjudge(
        prompt
    )


    return result
    
