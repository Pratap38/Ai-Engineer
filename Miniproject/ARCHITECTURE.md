# Hinglish Book Summarizer Agent: System Architecture

Scope: a plain Python AI agent run from the CLI. No backend, no frontend, no LangGraph.
Input is a PDF path. Output is a Hinglish summary file.
Built only from what we already learned: Groq tool calling, a single `ask_llm`, manager + worker agents, a notes file, token counting, retry loops, LLM-as-judge evaluation, Qdrant (optional).

---

## 1. Requirements

**Functional**
| # | Requirement |
|---|---|
| F1 | User gives a PDF path (CLI). Agent returns a summary file, nothing else to do. |
| F2 | 300 pages in, about 70-100 pages out (compression about 25-33%). |
| F3 | Tone is Hinglish: Hindi + English in **Roman script**, casual, engaging. Technical terms stay in English. |
| F4 | Output is structured: chapter headings, key points, short explanation, takeaways/action items. |
| F5 | Faithful: no invented facts, numbers or names. |
| F6 | Resumable: a crash or rate-limit at chapter 9 must not restart from chapter 1. |
| F7 | Progress is printed step by step (same style as the Day 17 agent). |
| F8 | Token usage is reported per stage (same as Day 15). |

**Non-functional**
- Works within Groq free-tier limits. We already hit `429` in Day 15, so pacing and backoff are required, not optional.
- Max 2 retries per section when the reviewer rejects it (same rule as Day 17).
- Deterministic where possible: page and chunk math is done in Python, not by the LLM.

**Out of scope for v1**: scanned PDFs (OCR), images, charts, tables as tables, web UI, multi-user, translating to Devanagari.

---

## 2. Architecture

```
                         CLI:  python summarizer.py book.pdf
                                        |
        +-------------------------------v--------------------------------+
        |  1. INGEST (pure Python, no LLM)                                |
        |     pypdf/PyMuPDF -> text per page -> strip headers/footers     |
        |     -> detect scanned PDF (no text) -> stop with clear message  |
        +-------------------------------+--------------------------------+
                                        |
        +-------------------------------v--------------------------------+
        |  2. STRUCTURE (pure Python)                                     |
        |     PDF bookmarks -> else heading regex -> else ~10-page windows|
        |     -> sections of <= ~3k tokens, each with page range          |
        +-------------------------------+--------------------------------+
                                        |
        +-------------------------------v--------------------------------+
        |  3. MANAGER LLM  (decides, never writes the summary)            |
        |     reads outline + notes file                                  |
        |     -> length budget per chapter (python checks the sum)        |
        |     -> picks next action: summarize / review / retry / assemble |
        +--------+---------------------+---------------------+-----------+
                 |                     |                     |
        +--------v-------+   +---------v--------+   +--------v---------+
        | SUMMARIZER LLM |   |  REVIEWER LLM    |   |  EDITOR LLM      |
        | section ->     |   |  judge: faithful?|   |  book-level TL;DR|
        | Hinglish       |   |  covers key pts? |   |  + chapter flow  |
        | summary        |   |  Hinglish ok?    |   |  at the end      |
        | (no tools)     |   |  length ok?      |   |                  |
        +--------+-------+   +---------+--------+   +--------+---------+
                 |   reject (max 2x)   |                     |
                 +<--------------------+                     |
                 | accept                                    |
        +--------v-------------------------------------------v-----------+
        |  4. STATE (files on disk)                                       |
        |     notes.md          manager's running log (like Day 15)       |
        |     state.json        section status + budgets (resume)         |
        |     sections/NN.md    accepted summaries                        |
        |     glossary.json     term -> how we write it (consistency)     |
        +-------------------------------+--------------------------------+
                                        |
        +-------------------------------v--------------------------------+
        |  5. ASSEMBLE (pure Python)                                      |
        |     TL;DR + chapters in order -> summary.md (optional PDF)      |
        |     + report: pages, compression %, tokens per stage, retries   |
        +-----------------------------------------------------------------+

   Cross-cutting: ask_llm (one entry point) | TokenCounter | rate limiter + 429 backoff
```

---

## 3. Components

| Component | Type | Job | Tools it may use |
|---|---|---|---|
| Ingest | Python | Extract and clean text per page | pypdf / PyMuPDF |
| Structure | Python | Find chapters, build sections with page ranges and token counts | PDF outline, regex, tokenizer count |
| Manager | LLM (JSON output) | Reads outline and notes, assigns the length budget, chooses the next step. Same pattern as the Day 15 manager. | `read_notes`, `write_note` |
| Summarizer | LLM | One section -> Hinglish summary in the required format. Gets: the section text, the style guide, the glossary, and a 3-line recap of the previous section. | none (pure generation) |
| Reviewer | LLM judge | Compares the summary against the source section. Returns JSON: `faithful`, `coverage`, `hinglish_ok`, `length_ok` and the issues found. | none |
| Editor | LLM | Writes the book-level TL;DR and cross-chapter takeaways from the accepted summaries only (not the full book). | none |
| Assembler | Python | Joins everything, computes final page count and compression | none |

Why LLMs get few tools: the Day 15 and Day 17 lessons were that more tools mean more invalid tool calls and wasted tokens. Here, deterministic work (parse, count, split, join) is plain Python. The LLMs only do language work.

---

## 4. Core design decisions

1. **Map-reduce, not "send the whole book".** 300 pages is about 200k tokens in. We summarize section by section (map), then assemble and write a TL;DR from the summaries (reduce).
2. **Length is controlled in words, not pages.** LLMs cannot count pages. Python converts: about 450 words per page, so 70-100 pages is about 32k-45k words. Each section gets a word budget proportional to its source length (+/- weight for importance), and the Reviewer checks it.
3. **One Hinglish style guide in the system prompt** (the "expert prompt engineer" prompt, as in Day 15). It states: Roman script, simple Hindi connectors, keep technical terms in English, a few analogies, no slang overload. The glossary keeps term spelling consistent across 300 pages.
4. **Reviewer is a separate LLM call, ideally a different or larger model.** A model grading its own output is weak. This is the same idea as the RAG evaluation work.
5. **Resume by design.** `state.json` marks each section `pending / accepted / failed`. Re-running the command skips accepted sections.
6. **Qdrant is not in v1.** The summarizer already has the exact source text in hand, so retrieval adds cost with no benefit. It becomes useful in v2: "ask questions about the book", or fact-checking the final TL;DR against the source.

---

## 5. Data flow for one section

```
section text --> Summarizer --> draft
                                  |
                          Reviewer(draft, section text)
                           /                 \
                      accept                reject (issues listed)
                        |                        |
             save sections/NN.md       retry < 2 ? --yes--> Summarizer(draft + issues)
             update glossary, notes                |
                                                  no --> keep best draft, mark "needs review" in the report
```

---

## 6. Requirements and tools to set up

**Python packages** (add to the root `requirements.txt`)
| Package | Used for |
|---|---|
| `groq` | LLM calls (already have) |
| `python-dotenv` | keys (already have) |
| `pypdf` or `pymupdf` | PDF text and outline extraction |
| `tiktoken` (or a char/4 estimate) | token counting for chunking and budgets |
| `tenacity` (optional) | retry with backoff on 429 |
| `qdrant-client`, an embedding model | **v2 only** |

**Config** (`config.py`): model names, chunk size, compression target, words per page, max retries, delay between calls.

**Proposed layout**
```
Miniproject/
  prompt.md
  ARCHITECTURE.md
  summarizer.py      CLI entry, orchestrates the stages
  ingest.py          PDF -> pages
  structure.py       pages -> sections
  agents.py          manager / summarizer / reviewer / editor prompts + ask_llm
  state.py           notes.md, state.json, glossary.json helpers
  assemble.py        final file + report
  output/<book>/     notes.md, state.json, sections/, summary.md
```

---

## 7. Evaluation (how we know it works)

| Metric | How |
|---|---|
| Faithfulness | Reviewer score per section, plus a spot check of 10 random sentences by hand |
| Coverage | Reviewer lists key points from the source and checks each appears in the summary |
| Length | `pages_out / pages_in` must land in 23-33%; Python computes it |
| Hinglish quality | Rubric (Roman script only, English technical terms, readable), judged by the Reviewer, then 1-2 human reads |
| Cost | `TokenCounter` per stage, compared against the budget |
| Test set | Start with a 20-30 page PDF, then a 300-page one |

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Groq free-tier 429 / token-per-minute limits | Small sections, a delay between calls, backoff, resumable state |
| Hallucinated facts or numbers | Reviewer compares against the source; rule "do not add facts not in the section" |
| Output too long or too short | Word budget per section, checked in Python |
| Tone drifts (too formal, or too much slang, or Devanagari) | One fixed style guide plus the Reviewer rubric |
| Terms spelled differently in different chapters | `glossary.json` passed into every summarizer call |
| Scanned PDF or messy layout | Detect and stop with a clear message in v1 |
| Model emits invalid tool/JSON output | Reuse the Day 15/17 fallback pattern: catch the error, retry once, then degrade gracefully |
| Chapters lose connection to each other | Pass a short recap of the previous section; the Editor smooths the whole at the end |

---

## 9. Build order (when you say go)

1. `ingest.py` + `structure.py` with a test PDF. No LLM yet, just print the sections.
2. Summarizer on one section, tune the Hinglish style guide.
3. Reviewer + retry loop (max 2) on one section.
4. Manager, notes and state, so the whole book runs and resumes.
5. Editor TL;DR, assembler and the token report.
6. Evaluation run on a small PDF, then the 300-page one.

---

## 10. Open points to decide before building

1. **Reading-time claim:** at the stated "1 page = 1 minute", 70-100 pages is 70-100 minutes, not 1 hour. For a true 1 hour the target is about 60 pages (20% compression). Proposal: make the ratio configurable and default to 25-30%.
2. **Model limits:** which Groq model do we use for the summarizer and for the reviewer? Context and rate limits decide the section size.
3. **Output format:** Markdown only, or also PDF/DOCX?
4. **Scanned PDFs:** is text-only PDF enough for v1?
