# 📄 PDF AI Summarizer

A Streamlit app that summarizes PDF documents with **Google Gemini** (via LangChain).
Upload a PDF, pick a style, and get a summary, a structure analysis and optional key quotes.

## What it does

- Extracts and cleans text from a PDF, then splits it into token-limited chunks
- Summarizes each chunk, then combines them into one final summary
- Four summary types:
  - **brief**: 2-3 sentence overview
  - **detailed**: key points, arguments and conclusions
  - **bullet_points**: scannable bullet list
  - **executive**: business-focused insights and recommendations
- Analyzes document structure and extracts key quotes (both optional)
- Exports the summary as text and per-chunk statistics as CSV

## Setup

Requires Python 3.10+.

```
python -m venv .venv
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
copy .env.example .env           # then put your key in .env
```

Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and set
`GEMINI_API_KEY` in `.env`. `GEMINI_MODEL` sets the default model (it can also be changed in the sidebar).

## Run

```
streamlit run app.py
```

## Project structure

```
app.py            Streamlit UI (settings, upload, results, downloads)
pdf_processor.py  PDF text extraction, cleaning, token counting, chunking
summarizer.py     Gemini calls: chunk summaries, combine, analysis, quotes
prompts.py        All ChatPromptTemplates
utils.py          Display, export, statistics and API key helpers
.env.example      Environment variable template
```

## How it works

```
PDF -> extract text -> clean -> chunk (by tokens)
                                  |
                  +---------------+---------------+
                  v               v               v
             summary 1       summary 2   ...  summary N      (map)
                  +---------------+---------------+
                                  v
                        combine -> final summary             (reduce)
```
