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

    
    


    
