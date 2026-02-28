# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI DAILY is an automated news aggregation system that:
1. Fetches AI-related news from Google News RSS using multiple keywords
2. Generates a newspaper-style HTML email with two sections:
   - **AI News**: 20 articles in a clean 2-column grid layout
   - **AI Layoff Tracker**: Up to 10 articles about AI-related layoffs
3. Sends the email via Gmail SMTP
4. Saves HTML to `docs/index.html` for GitHub Pages

The system runs daily via GitHub Actions at 22:00 UTC (8am AEST / 9am AEDT).

## Development Commands

### Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (requires .env file with GMAIL_USER, GMAIL_PASS, TO_EMAIL)
python main.py
```

### GitHub Actions
- **Manual trigger**: Go to Actions tab → "AI Daily News" → "Run workflow"
- **Schedule**: `cron: '0 22 * * *'` (fixed UTC time, does not auto-adjust for DST)

## Architecture

### Single-File Structure (`main.py`)

All logic is contained in `main.py` (~440 lines):

| Function | Purpose |
|----------|---------|
| `get_aest_time()` | Returns current AEST/AEDT time using ZoneInfo |
| `fetch_google_news(keyword, max_items, retries)` | Fetches articles from Google News RSS for a single keyword |
| `fetch_all_news()` | Aggregates AI news using 38 keywords, returns 20 deduplicated articles |
| `fetch_layoff_news()` | Aggregates layoff news using 10 keywords, returns up to 10 deduplicated articles |
| `generate_html_content(ai_news, layoff_news)` | Generates HTML with 2-column grid layout for both sections |
| `send_email(subject, html_content, ...)` | Sends email via Gmail SMTP |
| `save_html_file(html_content)` | Saves HTML to `docs/index.html` |
| `main()` | Orchestrates the entire pipeline |

### News Keywords

Keywords are organized in categories within `fetch_all_news()`:
- AI companies/products (OpenAI, Claude, DeepMind, Qwen, Kimi, GLM, DeepSeek)
- Founders/CEOs (Sam Altman, Dario Amodei, Demis Hassabis)
- Hiring/executive moves
- VC/funding
- Regulation/safety/competition
- Open source tools (Hugging Face, LangChain, Stable Diffusion, Llama, Mistral, Ollama, vLLM, Gradio, Streamlit)
- General AI news

Layoff keywords in `fetch_layoff_news()`:
- AI layoffs, automation job cuts, AI replacing workers, job displacement, workforce reduction

### HTML Generation

The `generate_html_content()` function:
- Takes `ai_news` and `layoff_news` as separate parameters
- Uses CSS Grid for 2-column layout (`.news-grid`)
- Each news card has: source tag, title, "READ MORE" link
- No JavaScript, no pagination - all content on one page
- Section divider: "AI LAYOFF TRACKER" with distinct styling

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GMAIL_USER` | Yes | Gmail address for sending |
| `GMAIL_PASS` | Yes | Gmail App Password (NOT account password) |
| `TO_EMAIL` | Yes | Recipient email address |

Local development: create `.env` file (see `.env.template`)
GitHub Actions: set as repository secrets

## Modifying Keywords

When adding news keywords:
1. Add to the appropriate section in `fetch_all_news()` (line 79-127)
2. Keep descriptive comments for organization
3. Use English keywords for global coverage

When adding layoff keywords:
1. Add to `fetch_layoff_news()` (line 150-162)
2. Focus on AI-driven automation/displacement themes

## Testing Changes

1. **Local test**: Run `python main.py` and check output
2. **Manual workflow**: Trigger from GitHub Actions tab
3. **View result**: Check `docs/index.html` on GitHub Pages after commit

## Important Notes

- The workflow auto-commits `docs/index.html` with message "Update daily news - YYYY-MM-DD"
- Google News RSS rate limiting: each keyword fetches max 2 items
- lxml is **required** for XML parsing - script exits without it
- Time zone handling uses Python's `zoneinfo` (built-in since 3.9)
- The schedule is fixed UTC; during Australian DST it runs at 9am local instead of 8am
