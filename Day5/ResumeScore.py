from pydantic import BaseModel,Field
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

# Retrieve API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key missing")

# Initialize the client
client = Groq(api_key=my_api_key)

# Define model and message
model_name = "llama-3.3-70b-versatile"
jobDescription="""
Project Role : Custom Software Engineer
Project Role Description : Develop custom software solutions to design, code, and enhance components across systems or applications. Use modern frameworks and agile practices to deliver scalable, high-performing solutions tailored to specific business needs.
Must have skills : API Management
Good to have skills : Java (Programming Language)
Minimum 0-2 year(s) of experience is required
Educational Qualification : 15 years full time education

Summary:
This position is responsible for providing support to customers using new and emerging technologies. This is a customer-facing role during pre and post implementation launches and must have a solid understanding of all Vertex offerings to act as an escalation point for complex issues. An adept understanding and intermediate expertise in the areas of network issues, API, MSSQL, Oracle, Java, Linux, Postgres and Hana/DB2 is needed.

Roles & Responsibilities:
-Perform as a final escalation point for highly complex, visible, and sensitive client issues.
-Drive positive results in Customer Experience through timely response, and positive interaction.
-Communicate customers needs and requirements to other Vertex employees and teams.
-Provide technology expertise, work leadership, and assistance to less senior staff.
-Demonstrate self-direction in meeting targets for performance metrics to achieve daily work goals.
-Act as a Customer Support liaison during implementation of customer programs to understand product, usage and technology for post-implementation support.
-Provide ongoing support and troubleshooting for installed technical solutions by analyzing a chain of events and applying technical knowledge, following established procedures and standards.
-Ability to work within the direction and expectations of the Customer Support Work Center.
-Work closely with Vertex emerging products and emerging technologies to understand and implement support processes.
-Work highly technical and sensitive issues through to a mutually acceptable resolution by accurately assessing the issue/situation and using critical and creative thinking.
-Build and leverage strong relationships with both internal and external customers.
-Receive highly complex escalations from Tier 2 analysts.
-Provide support as dictated by business drivers.
-Create, edit and maintain knowledge entries including best practices entries.
-Help drive positive results in Customer Experience through timely response, and positive interaction.
-Maintain all support shared systems (virtual environments, databases, and shared instances).
-Participate in other projects or duties.

Professional & Technical Skills:

Professional experience in troubleshooting, maintaining, or developing data-driven applications connected to relational databases, XML sources, and high volume web services.
Subject Matter Expert in one or more of the following areas: Database technology (Oracle, SQL Server, Postgres, DB2, Hana), Java, XML, web services, ERP's, network architecture, database or application performance issues.
Experience with troubleshooting, maintaining, or developing data-driven applications connected to relational databases, XML sources, and high-volume web services.
Expert knowledge in supported transmission types (XML, REST, JSON) and record types within each transmission (examples - Address Validation, Quotation Requests, Invoice Request, Accruals, and Purchases,) and processing tools such as SoapUI and Postman.
Experience with Data Security & Operations.
Experience with LINUX and Web Programming, including HTTP programming, ICF, Framework, Web Services in ABAP (SOAP, WSDLs) JAVA programming.
Experience with SAP NetWeaver Architecture and Integration technology and SAP Mobility Technology is preferred
Understand VM's, NAS, Unix, Shell programming and mainframe systems.
Understand FTP scripting, ECG, TWS, etc.
Understand Java and functional programming concepts.
Deep understanding of and debugging experience with networking protocols.
Excellent debugging skills in a wide variety of technologies and programming languages.
Ability to network with key contacts outside own area of expertise.
Ability to listen and understand information and communicate the same.
Must possess strong interpersonal, organizational, presentation and facilitation skills.
Must be results oriented and customer focused.
Understanding of Vertex customers use of the Vertex products is highly desired.
Strong desire to research and study new emerging technologies for consideration in future and ongoing development efforts.
Understand internal proprietary information and distribute information appropriately.
Experience in handling customer escalations, and calmly working in stressful situations.
Excellent analytical and creative problem-solving skills.
Ability to apply professional concepts, experience and company objectives in order to perform an in-depth analysis of situations or data to resolve complex issues in creative ways.
Exercise a professional approach with others using all appropriate tools of communication ability to adjust communication style and delivery to the audience.
Must possess good organizational skills.
Must be results oriented, customer focused, and exhibit good interpersonal skills.
Proficiency in Microsoft office packages.
Sufficient knowledge of business communications, including telephone, voicemail, and e-mail and operations of office machines, such as photocopier, scanner, and fax.
This role covers the Vertex on-call duties on a rotational basis.


Additional Information:

Bachelor's/Master s degree in Management Information Systems or Computer Information Technology or related field required.
Six (6) plus years of relevant industry experience.
Professional experience in troubleshooting, maintaining, or developing data-driven applications connected to relational databases, XML sources, web services, big data driven backend systems.
Experience with building and maintaining Big Data and Fast Data applications.
Experience with Data Governance, Security & Operations.
Experience with Web Programming, including HTTP programming, ICF Framework, Web Services in ABAP (SOAP, WSDLs) JAVA programming SAP NetWeaver Architecture and Integration technology and SAP Mobility Technology
Experience in handling customer escalations, and calmly working in stressful situations.
Or equivalent combination of education and/or experience.
"""

class JobDesc(BaseModel):
    role:str
    requiredSkill:list[str]
    preferSkill:list[str]
    minExperience:float|None
    educationRequirement:list[str]
    responsibility:list[str]

jobSchema=JobDesc.model_json_schema()

system_prompt=f"""
You are an expert HR assistant 

your main goal is to analyse this resume and extract the structure information from it

Return only the valid json Schema that matches this {jobSchema}
Important:
Donot return the schema itself
Donot return any useless info like the title summary etc.

if any experiecne is not then return null
if any requred info is missing then just simply return an empty list for that field
donot add anything else by own just need as per the resume and schema.
"""

userPrompt=f"""
Analyse the following  job description
{jobDescription}
"""
messageSystem={
    "role":"system",
    "content":system_prompt
}
messageUser={
    "role":"user",
    "content":userPrompt
}
responseformat={
    "type":"json_object"
}
messages=[messageSystem,messageUser]
response = client.chat.completions.create(
    model=model_name,
    messages=messages,

)
answer=response.choices[0].message.content

rawJson=answer

import json

jsonData=json.load(rawJson)

job=jobDescription(**jsonData)


class MatchResult(BaseModel):
    score:float
    details:dict

class ExperienceResume(BaseModel):
    company:str|None=None
    role:str|None=None
    duration:str|None=None
    skillUsed:list[str]=[]

class Resume(BaseModel):
    name:str|None=None
    email:str|None=None
    phone:str|None=None
    totalExperienceinYears:float|None=None
    skills:list[str]=[]
    experience:list[ExperienceResume]=[]
    project:list[str]=[]
    certification:list[str]=[]

resumeSchema=Resume.model_json_schema()

def finalScore(job,resume):
    matchschema=MatchResult.model_json_schema()
    prompt=f"""
you are an expert Hr recruiter
Compare this candidate  resume with the jd

"""






##resume read method
from pydf import PdfReader
from docx import Document

def Readpdf(filePath):
    reader=PdfReader(filePath)
    text=""
    for page in reader.pages:
        pagetext=page.extract_text()
        if pagetext:
            text+=pagetext+"\n"
    return text

def Readdoc(filePath):
    reader=Document(filePath)
    text=""
    for para in reader.paragraph:
        if para.text.strip():
            text+=para.text+"\n"
    for table in reader.tables:
        for row in table.rows:
            for cell in row.cells:        ##for coloum jo ki resume me present and upar wala row mean kch resume me table bane rehte
                if cell.text.strip():
                    text+=cell.text+"\n"
    return text

def readResume(filePath):
    if filePath.suffix.lower()==".pdf":
        return Readpdf(filePath)
    elif filePath.suffix.lower()==".docx":
        return Readdoc(filePath)
    else :
        return None


resumeFolder=Path("resume")
allResult=[]
for filepath in  resumeFolder.iterdir():
    if (filepath.suffix.lower() not in [".pdf",".docx"]):
        continue


