import re
from dataclasses import dataclass
import config

@dataclass
class Chapter:
    title:str
    startPage:str
    endPage:str

@dataclass
class Paragraph:
    page:int
    text:str
    token:int

@dataclass
class Section:
    index:str
    chapter:str
    startPage:str
    endPage:str
    text:str
    token:int
    words:int
    budgetWord:int


charPerTokens=4
ChapterPattern= re.compile(
    r"^\s*(chapter|part|unit)\s+(\d+|[ivxlc]+)\b[:.\- ]*(.*)$",
    re.IGNORECASE,
)

def TokenCounter(text:str)->int:
    return max(1,len(text)//charPerTokens)


def ChapterBuilder(starts:list[tuple[str,int]],totalPage:int )->list[Chapter]:
    starts=sorted(starts,key=lambda item:item[1])
    starts=dropDuplicatepage(starts)
    chapters=[]
    FirstPage=starts[0][1]
    if FirstPage>1:
        chapters.append(Chapter("front matter"),1,FirstPage-1)

    for pageindex,(title,startPage) in enumerate(starts):
        IsLast=pageindex==len(starts)-1
        if IsLast:
            EndPage=totalPage
        else:
            EndPage=starts[pageindex+1][1]-1
        chapters.append(Chapter(title,startPage,EndPage))
    return chapters


# there might be chance ki two chapter migh start at the same page
def dropDuplicatepage(starts:list[tuple[str:int]])->list[tuple[str,int]]:
    visitPage=set()
    unique=[]
    for title ,page in starts:
        if page in visitPage:
            continue
        visitPage.add(page)
        unique.append((title,page))
    return unique


def OutlineChapter(outline:list[dict],totalPage:int)->list[Chapter]:
    starts=[]
    for i in outline:
        if i["level"]==1:
            starts.append(i["tite"],i["pages"])    ## thsi basically use to store te title and the page
    if len(starts)<2:
        return[]
    return ChapterBuilder(starts,totalPage)


##function to determine the heading in an pdf this will help to  reducee the token consumption

def FindHeading(text:str):
    firstLine=text.split()[:3]
    for i in firstLine:
        match=ChapterPattern.match(i)
        if match:
            key=(match.group(1).lower(),match.group(2).lower())
            return i.strip(),key
    return None