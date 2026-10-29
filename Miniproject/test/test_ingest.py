import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so `ingest` is found from test/

from pypdf import PdfReader
import config
from ingest import ScannedPdfError


# ---------------------------------------------------------------------------
# Workarounds for bugs in ingest.py. ingest.py itself is NOT modified;
# the fixes are applied here, in memory, only while this test runs.
# ---------------------------------------------------------------------------

# Bug 1: ingest.py uses config.REPEAT_RATIO, but config.py calls it RepeatRatio.
config.REPEAT_RATIO = config.RepeatRatio


# Bug 2: RepeatedLine returned inside the page loop, so only the first page was checked.
def _repeated_line(pages) -> set:
    count = Counter()
    for page in pages:
        lines = page["text"].splitlines()
        keys = set()
        for i in ScannedPdfError.EdgeIndices(lines):
            keys.add(ScannedPdfError.LowerCaseCoversion(lines[i]))
        count.update(keys)
    threshold = max(3, int(len(pages) * config.REPEAT_RATIO))
    return {key for key, c in count.items() if c >= threshold and key}


# Bug 3: the error message used `.Of` (letter O) instead of `.0f` (zero), which crashes.
def _end_of_char_page(pages) -> None:
    total_chars = sum(len(p["text"]) for p in pages)
    avg_chars = total_chars / max(len(pages), 1)
    if avg_chars < config.MinCharPerPage:
        raise ScannedPdfError(f"Only {avg_chars:.0f} characters per page found; looks like a scanned PDF")


# Bug 4: when a page failed to read, the fallback set `text` but the code used `textextract`.
def _extract_raw_page(pdf_path: str):
    reader = PdfReader(pdf_path)
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        try:
            textextract = page.extract_text() or ""
        except Exception:
            textextract = ""
        pages.append({"pageNumber": number, "text": textextract})
    try:
        outline = ScannedPdfError.Outline(reader, reader.outline)
    except Exception:
        outline = []
    return pages, outline


ScannedPdfError.RepeatedLine = _repeated_line
ScannedPdfError.EndOFCharpage = _end_of_char_page
ScannedPdfError.ExtractRawPage = _extract_raw_page


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_ingest.py <pdf_path>")
        sys.exit(1)

    try:
        result = ScannedPdfError.pdfentry(sys.argv[1])
    except ScannedPdfError as e:
        print(f"STOPPED: {e}")
        sys.exit(1)

    print(f"Pages        : {result['TotalPages']}")
    print(f"Total words  : {result['TotalWordpresent']}")
    print(f"Outline items: {len(result['outline'])}")

    print("\n--- Removed header/footer patterns ---")
    for line in result["removedLines"][:10] or ["(none found)"]:
        print(f"  {line!r}")

    print("\n--- Outline (first 10) ---")
    for item in result["outline"][:10] or [{"level": 1, "title": "(no bookmarks)", "page": 0}]:
        print(f"  {'  ' * (item['level'] - 1)}{item['title']}  (p.{item['page']})")

    mid = min(5, result["TotalPages"]) - 1
    page = result["pages"][mid]
    print(f"\n--- Page {page['pageNumber']} preview ({page['word']} words) ---")
    print(page["text"][:500])


if __name__ == "__main__":
    main()
