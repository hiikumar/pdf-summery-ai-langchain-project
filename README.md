# 📄 PDF AI Summarizer

A Streamlit app that summarizes PDF documents with **Google Gemini** (via LangChain). Upload a PDF, pick a style, and get a summary, a structure analysis and optional key quotes.

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

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: Copy-Item .env.example .env
```

Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) and set `GEMINI_API_KEY` in `.env`. `GEMINI_MODEL` sets the default model (it can also be changed in the sidebar).

## Run

```bash
streamlit run app.py
```

## Prompt templates

All prompts live in `prompts.py` as LangChain `ChatPromptTemplate`s (system + human message):

- `STYLES`: dict mapping each summary type to its instruction text (injected as `{style}`)
- `_template(human)`: helper that builds a `ChatPromptTemplate` from the shared system message plus a human message
- `CHUNK_SUMMARY`: per-chunk summary prompt (takes `{style}` and `{text}`)
- `COMBINE`: merges chunk summaries into the final summary
- `ANALYSIS`: document structure analysis
- `QUOTES`: key quote extraction

To add a new style, add an entry to the `STYLES` dict in `prompts.py` with its instruction text, then add its name to the "Summary Type" options in `app.py`.

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
PDF → extract text → clean → chunk (by tokens)
                                  │
                  ┌───────────────┼───────────────┐
                  ▼               ▼               ▼
             summary 1       summary 2   ...  summary N      (map)
                  └───────────────┼───────────────┘
                                  ▼
                        combine → final summary             (reduce)
```

## Deploy to Streamlit Community Cloud

The app reads its settings through `config.get_secret()`, which checks Streamlit secrets first and then the environment. That means the same code runs locally from `.env` and in the cloud from the Secrets manager — no code changes needed.

1. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
2. Pick this repository and branch `main`, with `app.py` as the main file.
3. Open **Advanced settings → Secrets** and paste:

   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   GEMINI_MODEL = "gemini-3.1-flash-lite"
   ```

4. Click **Deploy**.

Never commit real keys. `.env` and `.streamlit/secrets.toml` are both git-ignored; `.env.example` and `.streamlit/secrets.toml.example` are the safe templates.

## Troubleshooting

- **"No extractable text"**: the PDF is probably scanned images. Run OCR on it first.
- **429 / rate limit errors**: wait a minute and retry, use a smaller document, or switch to another model.
- **Model not available / 404**: set `GEMINI_MODEL` in `.env` (or pick another model in the sidebar) to one your key can access.
- **API key not found**: make sure `.env` exists next to `app.py` and contains `GEMINI_API_KEY`.
