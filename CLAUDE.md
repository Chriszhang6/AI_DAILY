# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI DAILY is a Python-based automated news aggregation system that fetches AI-related news from multiple sources, compiles them into a newspaper-style HTML email digest, and delivers it daily via Gmail SMTP.

## Common Commands

### Running the Application
```bash
# Run the main news digest pipeline (fetch → generate HTML → send email)
python3 main.py

# Test the news fetcher module independently
python3 ai_news_fetcher.py
```

### Dependencies
```bash
pip install requests beautifulsoup4
```

### Required Environment Variables
The application requires three environment variables to be set for email delivery:
- `GMAIL_USER` - Gmail address for sending
- `GMAIL_PASS` - Gmail app password (not account password)
- `TO_EMAIL` - Recipient email address

## Architecture

### Entry Points

- **`main.py`** - Primary orchestrator. Fetches from Google News RSS with 8 AI-related keywords, deduplicates by title, generates newspaper-style HTML, and sends via Gmail SMTP. This is the script run in production.

- **`ai_news_fetcher.py`** - Modular news fetching. Currently implements only MarkTechPost scraper; contains placeholders for AITimeJournal, HuggingFace, ArXiv, OpenAI, and DeepMind.

- **`ai_news_mailer.py`** - Email delivery utility
- **`ai_news_translate.py`** - Translation stub (returns "[ZH]" prefix)

### Key Design Decisions

1. **Google News RSS vs. Web Scraping** - `main.py` uses Google News RSS feeds for aggregation, while `ai_news_fetcher.py` was designed for direct web scraping. The RSS approach in `main.py` is the currently active implementation.

2. **HTML Email Template** - The newspaper-style layout uses CSS Grid with specific span rules:
   - First item spans 2 columns, 2 rows (featured story)
   - Items 5 and 8 span 2 columns
   - Responsive: collapses to 2-column grid on mobile

3. **Deduplication Strategy** - News articles are deduplicated by title after fetching from multiple keyword sources.

## Known Issues

### GitHub Actions Workflow Mismatch
The `.github/workflows/ai_daily_news.yml` workflow references paths that don't exist:
```yaml
python ai_completion/ai_news_fetcher.py > news.json
python ai_completion/ai_news_translate.py < news.json > news_zh.json
python ai_completion/ai_news_mailer.py
```

These should reference the root-level scripts:
```yaml
python main.py
```

The workflow also expects a JSON pipeline that the current implementation doesn't produce.

### Incomplete Modules
- Only MarkTechPost scraper is functional in `ai_news_fetcher.py`
- Translation module is a stub returning pseudo-translations
- Other news sources (HuggingFace, ArXiv, OpenAI, DeepMind) are not implemented

## GitHub Actions

The workflow runs daily at 9 AM UTC via cron and supports manual triggers via `workflow_dispatch`. Uses Python 3.10 in CI (main.py tested with 3.9.6).
