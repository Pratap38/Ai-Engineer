import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # so `ingest` is found from test/

from ingest import ScannedPdfError


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
