import os
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer


load_dotenv()

# Retrieve API key
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key missing")

# Initialize the client
client = Groq(api_key=my_api_key)

model = SentenceTransformer('all-MiniLM-L6-v2')
model_name = "llama-3.3-70b-versatile"
def consineSimilar(a,b):
  return np.dot(a,b)/( np.linalg.norm(a)*np.linalg.norm(b))

KnowledgeBaseDocument=["""
   ChatGPT said:
Nexora Technologies — Internship Knowledge Base
1. Company Information
Company Name: Nexora Technologies Pvt. Ltd.
Industry: Software Development, Artificial Intelligence, and Data Engineering
Location: Bengaluru, India
Company Type: Private Technology Company

Nexora Technologies develops software products and AI-based solutions for businesses. The company has software engineering, AI/ML, data engineering, product, design, sales, and HR teams.

2. Internship Program
The Nexora Technologies Internship Program is designed for students and recent graduates who want practical industry experience.

Internships are generally available for:

Software Development
Web Development
Backend Development
AI/ML
Data Science
Data Engineering
DevOps
UI/UX Design
Internship duration can be between 3 and 6 months depending on the offer letter.

Each intern is assigned a mentor who provides guidance and reviews the intern's work.

3. Working Hours
Normal working days are Monday to Friday.

Working hours are:

9:30 AM to 6:30 PM

Interns are expected to work approximately 8 hours per day, excluding the lunch break.

Lunch break:

1:00 PM to 2:00 PM

Saturday and Sunday are normally non-working days.

Interns are expected to be available during working hours for meetings, communication, and assigned tasks.

4. Attendance Policy
Interns should maintain at least 90% attendance during their internship.

Attendance is recorded through the company's attendance system.

Interns should arrive on time and be available during their scheduled working hours.

Repeated late arrival or unexplained absence may negatively affect the intern's performance evaluation.

If an intern cannot attend work, they should inform their mentor or manager as soon as possible.

5. Leave Policy
Interns receive 1 paid leave day per month.

For example:

3-month internship = up to 3 paid leave days.

6-month internship = up to 6 paid leave days.

Planned leave should normally be requested at least 2 working days in advance.

Emergency or sick leave should be communicated to the mentor or manager as soon as possible.

Unused monthly leave does not automatically carry forward to the next month.

Additional leave may be approved by the manager in special circumstances.

6. Sick Leave
If an intern becomes sick and cannot work, they should inform their mentor or manager.

For short-term illness, the intern should provide a basic explanation of the absence.

For extended illness, HR may request appropriate documentation.

Sick leave is subject to the company's leave policy and approval process.

7. Academic Leave
Interns may request leave for:

University examinations
College presentations
Mandatory academic activities
University projects
Other important academic requirements
Academic leave must be requested in advance whenever possible.

The mentor or manager must approve the request.

8. Work From Home Policy
Interns may work from home when approved by their mentor or manager.

Work from home is not an automatic right.

WFH may be approved for situations such as:

Temporary illness
Personal emergencies
University requirements
Transportation problems
Other special circumstances
While working from home, interns must remain available during normal working hours and attend scheduled meetings.

9. Internship Stipend
The standard internship stipend at Nexora Technologies is ₹15,000 per month.

The actual stipend may vary depending on the internship role, candidate experience, and offer letter.

The stipend is normally paid during the first week of the following month.

For example, the stipend for January is normally paid during the first week of February.

The offer letter is the final authority for the stipend amount applicable to an individual intern.

10. Working From Office
Interns assigned to office-based or hybrid roles are expected to work from the designated company office according to their team's schedule.

Interns must carry their company ID or other required identification when visiting the office.

Company equipment should be handled responsibly.

11. Intern Responsibilities
Interns are expected to:

Complete assigned tasks on time.
Attend required meetings.
Communicate with their mentor regularly.
Follow company policies.
Maintain confidentiality.
Protect company information.
Follow security guidelines.
Document their work.
Submit progress updates when required.
Collaborate with team members.
Ask questions when they are blocked.
Maintain professional behavior.
Interns should inform their mentor early if they are unable to complete a task by the expected deadline.

12. Mentor
Every intern is assigned a mentor.

The mentor helps the intern understand:

Assigned projects
Technical requirements
Development processes
Company tools
Team procedures
Project deadlines
The mentor also provides feedback on the intern's performance.

The mentor is generally the first person an intern should contact for questions related to their daily work.

13. Reporting Structure
The normal reporting structure is:

Intern → Mentor → Team Lead → Engineering Manager

For technical or project-related questions, interns should contact their mentor first.

For HR, stipend, certificate, or administrative questions, interns should contact HR.

14. Performance Evaluation
Intern performance is evaluated based on:

Technical ability
Quality of work
Problem-solving ability
Learning ability
Communication
Teamwork
Attendance
Punctuality
Meeting deadlines
Professional behavior
Initiative
The mentor and team lead may provide feedback throughout the internship.

A final evaluation is generally conducted near the end of the internship.

15. Internship Certificate
Interns who successfully complete their internship may receive an Internship Completion Certificate.

The certificate generally contains:

Intern's name
Internship role
Internship duration
Company name
Completion date
Authorized company representative
Interns should contact HR if they have questions about their certificate.

16. Full-Time Employment
Successfully completing an internship does not guarantee a full-time job.

Outstanding interns may be considered for full-time employment depending on:

Performance
Technical skills
Team requirements
Available positions
Business requirements
Any full-time employment offer will be provided separately.

17. Company Holidays
The company observes public and company holidays according to its annual holiday calendar.

Common holidays may include:

Republic Day
Holi
Independence Day
Gandhi Jayanti
Diwali
Christmas
The official holiday calendar published by HR is the final authority.

18. Confidentiality
Interns may have access to confidential company information.

Confidential information may include:

Source code
Customer information
Business plans
Internal documents
Product information
Passwords and credentials
Financial information
Internal databases
Company strategies
Interns must not share confidential information with people outside the company.

Interns must continue to respect confidentiality after completing their internship.

19. Company Equipment
If an intern receives company equipment such as a laptop, monitor, access card, or other equipment, the intern is responsible for taking reasonable care of it.

Company equipment must be returned when requested or when the internship ends.

Loss or damage should be reported to the appropriate manager or IT department.

20. Security Policy
Interns must:

Keep passwords confidential.
Never share company credentials.
Use approved software and services.
Lock their computer when away.
Avoid downloading suspicious files.
Report security incidents immediately.
Never share internal data publicly.
Company data should not be uploaded to personal cloud storage or unauthorized AI tools without approval.

21. Daily Work
A typical intern's day may include:

9:30 AM — Start work
10:00 AM — Team communication or stand-up meeting
10:30 AM — Development/research/task work
1:00 PM — Lunch break
2:00 PM — Continue assigned work
4:00 PM — Mentor discussion or project meeting
5:30 PM — Documentation and progress update
6:30 PM — End of working day

The exact schedule may differ depending on the team and project.

22. Weekly Progress
Interns may be required to provide a weekly progress update.

A progress update can contain:

Tasks completed
Tasks currently in progress
Problems encountered
New things learned
Tasks planned for the following week
The mentor may use these updates to track the intern's progress.

23. Resignation or Early Termination
An intern who wants to leave the internship early should inform their mentor and HR.

The intern should provide reasonable notice according to the terms mentioned in their internship offer letter.

The company may terminate an internship for reasons including:

Serious misconduct
Repeated absence
Poor performance
Violation of company policies
Security violations
Breach of confidentiality
The terms of the internship agreement and offer letter apply in such situations.

24. Frequently Asked Questions
How many hours do interns work?

Interns normally work 8 hours per day, Monday to Friday, from 9:30 AM to 6:30 PM, with a one-hour lunch break.

How many leaves does an intern get?

Interns receive 1 paid leave day per month.

Can I take leave for college exams?

Yes. Academic leave can be requested with prior approval from the mentor or manager.

Can interns work from home?

Yes, but work from home requires approval from the mentor or manager.

What is the internship stipend?

The standard stipend is ₹15,000 per month. The intern's offer letter determines the final applicable amount.

Are Saturday and Sunday working days?

Normally, no. Saturday and Sunday are non-working days.

What should I do if I am sick?

Inform your mentor or manager as soon as possible.

Who should I contact about my stipend?

HR should be contacted for stipend-related questions.

Who should I contact about my technical work?

The assigned mentor is normally the first point of contact.

Will I receive an internship certificate?

Interns who successfully complete the internship may receive an Internship Completion Certificate.

Does an internship guarantee a full-time job?

No. Full-time employment depends on performance and available positions.

What happens if I am late frequently?

Repeated lateness may negatively affect attendance records and the final performance evaluation.

Can unused leave be carried forward?

Unused monthly leave does not automatically carry forward unless specifically approved.

Can I work from home without informing my manager?

No. Work from home requires prior approval except in emergency situations where the manager should be informed as soon as possible
"""]

InternshipEmbedding=model.encode(KnowledgeBaseDocument)

def retrive(qembed):
   score=[]
   for i ,doc in enumerate(InternshipEmbedding):
      scores=consineSimilar(qembed,doc)
      score.append((scores,KnowledgeBaseDocument[i]))
   score.sort(reverse=True)
   return score[0]


def askllm(queryy):
   context=retrive(queryy)   
   systemprompt=f"""
answer in one line answer should be based on the context donot halucinate or anything else {context}
   """
   systemMessgae={
      "role":"system",
      "content":systemprompt
   }
   message={
    "role":"user",
    "content":queryy
   }
   messages=[systemMessgae,message]
   response=client.chat.completions.create(
               model=model_name,
               messages=message
           )
   answer=response.choices[0].message.content
   print(answer)






prompt="what is the name of the company and i want to know that timing of the company is in afternoon or morning or evening and company location"
queryEmbed=model.encode(prompt)
score,context=retrive(queryEmbed)
