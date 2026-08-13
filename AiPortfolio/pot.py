from pydantic import BaseModel, Field
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

# Retrieve API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key missing")

# Initialize the client
client = Groq(api_key=my_api_key)

# Define model and message
model_name = "llama-3.1-8b-instant"
# Hrprompt=f"""
# hey okiee so i want to know about this guy tell me
# """

Hrprompt=f"""
tell me  about his project what he has done
"""


summary=f"""
Hi! Before Start This is mine Summary 
"""

projectdetail="""
1. Train Network & Route Optimization Engine

Problem Statement

India's railway network is one of the largest and most complex transportation systems in the world, with tens of thousands of stations connected through an intricate web of routes. For a commuter or a developer trying to build travel applications, a core challenge exists: how do you find the most efficient path between two stations, at scale, without existing tools that expose this in an open, queryable, and fast way? Most public interfaces (like IRCTC) are built for ticket booking, not for route computation or ETA-style queries, and don't expose a route-finding API a developer could build on top of. There was no lightweight, self-hosted system that could take raw station-to-station connection data and instantly compute optimal paths — something any transport-tech, logistics, or EdTech project might need as infrastructure.

Uniqueness

What sets this project apart is the scale of real-world data it operates on — Pratap sourced and processed over 411,000 station-route entries from actual Indian Railways data, not a toy dataset. Handling data at this volume required careful attention to how the graph was structured in memory and how queries were served without recomputing everything from scratch each time. Rather than treating this as an academic algorithms exercise, he engineered it as a production-style system: a proper caching layer, a real frontend, and design decisions aimed at response time under real load — the kind of decisions that matter when you're shipping something, not just demonstrating you know Dijkstra's algorithm.

Solution

The core of the system is a graph representation of the Indian rail network, where stations are nodes and routes between them are weighted edges. On top of this graph, Pratap implemented Dijkstra's shortest-path algorithm to compute the most efficient route between any two stations based on distance/cost weighting. Given the graph's size, naive recomputation on every user query would be slow, so he introduced Redis as a caching layer — frequently requested routes and intermediate computations are cached, which significantly cuts down repeated computation and keeps response times low even under repeated or similar queries.

On the frontend, he built a React-based interface where users can select origin and destination stations and get the computed optimal route back interactively, rather than needing to interact with a raw API or CLI tool. This closes the loop from "raw government-scale data" to "usable product" — something a non-technical user could actually operate.

Architecturally, the project demonstrates full-stack systems thinking: data ingestion and cleaning of a massive real-world dataset, graph algorithm implementation at scale, a caching strategy to solve the resulting performance problem, and a user-facing layer to make it accessible. It's a strong signal of someone who can take a classic CS concept (shortest path algorithms) and apply it to a genuinely large, messy, real dataset — and then productionize it with the kind of infrastructure decisions (caching, frontend, API design) that separate "coursework project" from "engineering project."

2. Ubuntu Cache Cleaner & RAM Guardian

Problem Statement

Linux systems, particularly Ubuntu-based desktops and servers, accumulate cache files, orphaned packages, and memory-hogging processes over time — degrading performance without users always realizing why. Existing solutions in this space are largely either overly simplistic shell scripts with no real interface, or heavyweight GUI tools that abstract away control from the user. There wasn't a lightweight, terminal-native tool that gave users both visibility into what's consuming system resources and direct control over cache and memory management — without needing a full desktop environment or sacrificing granularity.

Uniqueness

The standout technical decision here is building a proper Terminal User Interface (TUI) using Python's Textual and Rich libraries, rather than a bare command-line script. This means the tool has real interactivity — navigable menus, live-updating displays, visual feedback — while still being fully terminal-based, making it usable over SSH, on headless servers, or in minimal environments where a GUI isn't available or desired. Beyond cache cleaning, Pratap extended the project with a RAM Guardian module that uses low-level Unix process signals — SIGSTOP and SIGCONT — to pause and resume memory-intensive processes on demand. This is a meaningfully more advanced technique than typical "close the app" resource management; it's closer to how a systems programmer or OS-level engineer would think about process control.

Solution

The tool is architected around two core modules. The cache cleaning module scans and identifies stale package caches, temporary files, and reclaimable disk space, presenting this information through the Textual-based TUI with clear, navigable menus rather than a dense wall of terminal output. Users can review what will be cleaned before committing to it, avoiding the "blind trust" problem common in one-shot cleanup scripts.

The RAM Guardian module monitors system memory usage and identifies processes consuming excessive RAM. Instead of forcibly killing these processes (which risks data loss in the app being paused), it uses SIGSTOP to suspend the process's execution entirely — freeing up CPU scheduling and allowing memory pressure to ease — and SIGCONT to resume it later, either on user command or based on system state. This is a much safer intervention than termination and reflects a real understanding of how the Linux process scheduler and signal handling work.

Beyond the code itself, Pratap treated this as a real open-source release: he authored over 100 pages of documentation covering installation, usage, and internals, and published the project to r/linux, where he directly engaged with technical criticism from the community — a meaningful signal of being able to defend design decisions to a technically demanding audience and iterate based on real feedback, not just ship and walk away.

3. SafeTrack — IoT GPS Tracking Platform

Problem Statement

Real-time location tracking systems — for personal safety, asset tracking, or fleet monitoring — typically require stitching together hardware, backend infrastructure, and a live-updating frontend, and most off-the-shelf trackers are closed, subscription-locked black boxes. For someone wanting an affordable, transparent, and customizable tracking solution, there was a gap: an end-to-end system, built from the hardware layer up, where every part of the pipeline — from GPS signal acquisition to live map rendering — is understood, owned, and controllable.

Uniqueness

SafeTrack is unusual in scope for a solo project because it spans the entire stack in the truest sense: physical hardware, embedded firmware, backend services, real-time communication, and a live frontend. Most software engineering projects stop at the backend/frontend boundary; this one starts at the microcontroller and soldered hardware level. Using an ESP8266 as the tracking hardware meant working within tight memory and processing constraints typical of embedded systems, while still needing to reliably push live location data to a cloud backend — a very different engineering discipline from typical web development.

Solution

At the hardware layer, an ESP8266 microcontroller — a low-cost WiFi-enabled chip — is used to acquire GPS coordinates and transmit them over the network. This required embedded firmware work to interface with GPS modules and manage the constraints of the ESP8266's limited resources, along with reliable connectivity handling for a device that may operate in variable network conditions.

On the backend, Pratap built the system using Django, which handles ingesting location data from the hardware, storing it, and exposing it securely to the frontend. Security is handled through JWT-based authentication, ensuring that location data streams are only accessible to authorized users — a meaningful consideration given the sensitive nature of real-time location data.

For real-time visualization, the frontend is built in React with WebSocket connections, allowing the tracker's location to update live on a map without requiring the user to refresh or poll manually. This WebSocket layer is what gives the platform its "live tracking" feel, as opposed to a system that only shows stale, periodically-refreshed positions.

Taken together, SafeTrack demonstrates Pratap's ability to work fluidly across abstraction layers — from soldering and embedded C/firmware-adjacent work, through backend API and database design, to real-time frontend engineering — and to secure the entire pipeline end to end. It's a strong demonstration of systems thinking beyond typical web development, showing comfort with hardware constraints, network protocols, and full-stack security in a single cohesive project.
"""

Hobbie="""
Seeing nature changes
Implementing my waste idea into real idea
"""
resume_path = Path("resume/PratapChoubey Resume.pdf")

class ExperienceResume(BaseModel):
    company:str|None=None
    role:str|None=None
    duration:str|None=None
    skillUsed:list[str]=Field(default_factory=list)
    whatdone:str|None=None

class Resume(BaseModel):
    name:str|None=None
    email:str|None=None
    phone:str|None=None
    summary:str|None=None
    totalExperienceinYears:float|None=None
    skills:list[str]=Field(default_factory=list)
    experience:list[ExperienceResume]=Field(default_factory=list)
    project:list[str]=Field(default_factory=list)
    certification:list[str]=Field(default_factory=list)

resumeSchema=Resume.model_json_schema()




def parsedresume(resumetext):
    system_prompt=f"""
You are an expert resume parser.
Return the output as valid json only.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    -summary
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

   

    You MUST return json matching EXACTLY this schema. Use these exact key
    names, no others. Do not nest fields inside objects that are not in the
    schema (e.g. do not create a "contact" object - email and phone are
    top-level keys).

    {json.dumps(resumeSchema, indent=2)}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume, flattened into a
       single list of strings (skills is a list, not an object of categories).
    6. "project" is a list of strings - one string per project, combining the
       project name and its description.
    7. totalExperienceinYears must be a number, estimated from the date ranges
       in the experience section.
    """
    user_prompt = f"""
    Parse the following resume and return json only:

    {resumetext}
    """
    message_system={
        "role" : "system",
        "content" : system_prompt
    }
    message_user={
        "role" : "user",
        "content" : user_prompt
    }
    messages=[message_system, message_user]
    response_format={
        "type": "json_object"
    }
    response=client.chat.completions.create(model=model_name, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)

    # Pydantic silently ignores unknown keys, so surface them instead of
    # letting the whole resume vanish into nothing.
    unknown = set(data) - set(Resume.model_fields)
    if unknown:
        print(f"[warn] model returned keys not in Resume schema, dropped: {sorted(unknown)}")

    resume = Resume(**data)
    return resume
##resume read method
from PyPDF2 import PdfReader
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
    for para in reader.paragraphs:
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

# Parsing the resume costs an LLM call, and the resume rarely changes. Cache the
# parsed result and only re-parse when the pdf/docx is newer than the cache.
cache_path = Path(__file__).with_name("resume_cache.json")

def loadParsedResume(filePath, refresh=False):
    if not refresh and cache_path.exists():
        if cache_path.stat().st_mtime >= filePath.stat().st_mtime:
            return Resume(**json.loads(cache_path.read_text()))
        print("[info] resume changed since last parse, re-parsing")

    resume_text = readResume(filePath)
    if not resume_text:
        raise ValueError("Could not read resume text")
    resume = parsedresume(resume_text)
    cache_path.write_text(json.dumps(resume.model_dump(), indent=2))
    print(f"[info] parsed resume cached to {cache_path.name}")
    return resume

# run with --refresh to force a re-parse
import sys
parsed_resume = loadParsedResume(resume_path, refresh="--refresh" in sys.argv)
resume_json = json.dumps(parsed_resume.model_dump(), indent=2)

systemPrompt=f"""
You are an expert HR assistant answering questions about one candidate.

CRITICAL - HOW YOU SPEAK:
The HR person cannot see your source material. They see only your answer.
So NEVER refer to your sources. Never write "According to SECTION 3",
"based on the resume data", "the write-up says", "in section 1", or anything
similar. State every fact directly as a fact about the candidate. Write as if
you simply know these things about him.

Your profile context is made of FOUR labelled sections below. All four are
equally valid sources - the resume is not the only one. Read every section
before answering, and pick the section that actually matches the question.

===== SECTION 1: RESUME DATA (structured) =====
{resume_json}
===== END SECTION 1 =====

===== SECTION 2: CANDIDATE'S OWN SUMMARY =====
{summary}
===== END SECTION 2 =====

===== SECTION 3: DETAILED PROJECT WRITE-UPS =====
{projectdetail}
===== END SECTION 3 =====

===== SECTION 4: HOBBIES AND INTERESTS =====
{Hobbie}
===== END SECTION 4 =====

How to answer:
- Hobbies / interests / "what does he do outside work" -> SECTION 4.
- Work experience, a company name (e.g. Roomhy) -> SECTION 1 "experience".
  Describe completely what he did there, in the resume's own words.
- Contact details, skills, certifications, education -> SECTION 1.
- "Tell me about him" -> a short intro from SECTION 1 + SECTION 2.
- ANY question about projects -> follow the PROJECT ANSWER PROCEDURE below.
  This applies to every project question, casual or deep - "tell me about his
  projects", "what has he built", "what he has done" all count.

PROJECT ANSWER PROCEDURE (follow these steps in order, every time):

STEP 1. Build the project list from SECTION 1 "project" ONLY. That list decides
        how many projects you write about and in what order. SECTION 3 does NOT
        get a vote here - it has write-ups for only some of them.

STEP 2. For each project in that list, find its matching write-up in SECTION 3.
        Match by project name and be generous, the wording differs slightly
        between sections (e.g. "SafeTrack - IoT Real-Time GPS Tracking Platform"
        and "SafeTrack - IoT GPS Tracking Platform" are the SAME project).
        Some projects will have no write-up. That is expected and fine.

STEP 3. Write every project from STEP 1 using this exact structure:

          **<project name>** (<dates, if SECTION 1 has them>)
          <the resume bullets for that project, from SECTION 1>

          Problem: <that project's Problem Statement>
          Approach: <that project's Solution, with the technical specifics>
          What stands out: <that project's Uniqueness>

        The bold line and resume bullets come from SECTION 1 and are REQUIRED -
        write them even when a rich write-up exists. The Problem / Approach /
        What stands out lines come from SECTION 3 - include them whenever that
        project has a write-up, and simply omit those three lines for a project
        that has none. Never invent them.

STEP 4. Check your answer contains every project from STEP 1. If SECTION 1 lists
        four projects, your answer has four projects. A project with no write-up
        still gets its bold heading and its resume bullets - do not silently
        drop it just because SECTION 3 does not mention it.

Keep the real detail: name the actual technologies, numbers, and design
decisions. Do not compress a write-up into a single sentence. Do not end with a
summarising paragraph about his range, versatility, or abilities - stop after
the last project.

Important:
Read the HR question first, then answer only from the sections above.
Never name or reference the sections in your answer (see CRITICAL at the top).
Do not invent anything. Do not add your own creative wording.
A section being short does not mean it is empty - if SECTION 4 has two lines,
those two lines ARE the hobbies, report them.
Only say "I do not have that information" if it is genuinely absent from all
four sections.
Answer only what was asked, then stop until the next question.
"""

messageSystem={
    "role":"system",
    "content":systemPrompt
}
messageHr={
    "role":"user",
    "content":Hrprompt
}
messages=[messageSystem,messageHr]
response = client.chat.completions.create(
    model=model_name,
    messages=messages,
    max_tokens=2000,
)
if response.choices[0].finish_reason == "length":
    print("[warn] answer hit the token limit and was cut off")
answer=response.choices[0].message.content
print(answer)
