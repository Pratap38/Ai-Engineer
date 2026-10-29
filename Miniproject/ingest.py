import re
from collections import Counter
from pypdf import PdfReader
import config

class ScannedPdfError(Exception):
    def LowerCaseCoversion(line:str)->str:
        return re.sub(r"\d+","#",line.strip().lower())
    @staticmethod
    def Outline(reader,items,level=1,out=None):
        if out is None:
            out=[]
        for i in items:
            if isinstance(i,list):
                ScannedPdfError.Outline(reader,i,level+1,out)
            else:
                try:
                    page=reader.get_destination_page_number(i)+1
                except Exception:
                    continue
                out.append({
                    "level":level,
                    "title":str(i.title).strip(),
                    "page":page
                })
        return out


# split outline and pages and return
    def ExtractRawPage(pdfPath:str):
        pdfread=PdfReader(pdfPath)

        pages=[]
        for i,j in enumerate(pdfread.pages,start=1):
            try:
                textextract=j.extract_text() or ""
            except Exception:
                text=""
            pages.append({
                "pageNumber":i,
                "text":textextract
            })
        try:
            outlineExtract=ScannedPdfError.Outline(pdfread,pdfread.outline)
        except Exception:
            outlineExtract=[]
        return pages,outlineExtract
#scan karega ki ab koyi character page me

    def EndOFCharpage(pages)->None:
        TotalChar=0
        for i in pages:
            TotalChar+=len(i["text"])
        AvgChar=TotalChar/max(len(pages),1)

        if AvgChar<config.MinCharPerPage:
            raise ScannedPdfError(
                f"Only -{AvgChar:.Of} character per page found "

            )
# apan header and footer determine karenge

    def EdgeIndices(lines):

        NonEmpty=[]
        for i ,l in enumerate(lines):
            if l.strip():
                NonEmpty.append(i)

        n=config.EdgeLine
        return set(NonEmpty[:n]+NonEmpty[-n:])


    def RepeatedLine(pages)->set:
        count=Counter()
        for i in pages:
            lines=i["text"].splitlines()
            keys=set()
            for i in ScannedPdfError.EdgeIndices(lines):
                keys.add(ScannedPdfError.LowerCaseCoversion(lines[i]))
            count.update(keys)
            threshold = max(3, int(len(pages) * config.REPEAT_RATIO))

            result = set()
            for key, countt in count.items():
                if countt >= threshold and key:
                    result.add(key)

            return result
    def CleanPage(text:str,repeated:set)->str:
        lines=text.splitlines()
        edges=ScannedPdfError.EdgeIndices(lines)
        kept=[]
        for i,line in enumerate(lines):
            if not (i in edges and ScannedPdfError.LowerCaseCoversion(line)in repeated):
                kept.append(line)
        text = "\n".join(kept)
        text = re.sub(r"-\n(\w)", r"\1", text)    # join words split by hyphen at line end
        text = re.sub(r"\n{3,}", "\n\n", text)    # collapse many blank lines
        return text.strip()


    def pdfentry(pdfPath:str)->dict:
        pages,outline=ScannedPdfError.ExtractRawPage(pdfPath)
        if not pages:
            raise ValueError("pdf has no pages")
        ScannedPdfError.EndOFCharpage(pages)

        repeatcheck=ScannedPdfError.RepeatedLine(pages)
        for  i in pages:
            i["text"]=ScannedPdfError.CleanPage(i["text"],repeatcheck)
            i["word"]=len(i["text"].split())
        return{
            "pages":pages,
            "outline":outline,
            "TotalPages":len(pages),
           "TotalWordpresent": sum(i["word"] for i in pages),
           "removedLines":sorted(repeatcheck)
        }





