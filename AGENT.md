---
name: ai-daily-guidance
description: Use when working on the AI DAILY news aggregation system. Provides project overview, architecture, setup instructions, and development guidance.
---

# AI DAILY - Agent Guidance

This is the primary guidance document for Claude Code when working with the AI DAILY project.

## 📋 Project Overview

**AI DAILY** is an automated news aggregation system that:
1. Fetches AI-related news from Google News RSS using 38 carefully selected keywords
2. Fetches AI layoff-related news using 10 keywords
3. Generates a newspaper-style HTML email with two distinct sections:
   - **AI News**: 20 articles in a clean 2-column grid layout
   - **AI Layoff Tracker**: Up to 10 articles about AI-related layoffs
4. Sends the email via Gmail SMTP
5. Saves HTML to `docs/index.html` for GitHub Pages

The system runs **daily via GitHub Actions at 22:00 UTC** (8am AEST / 9am AEDT).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- A Gmail account with [App Password](https://myaccount.google.com/apppasswords) enabled
- A GitHub account (for automated deployment)

### Local Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   
   Create a `.env` file based on `.env.template`:
   ```bash
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASS=your_app_password
   TO_EMAIL=recipient@example.com
   ```

3. **Run the script**
   ```bash
   python main.py
   ```

### GitHub Actions Setup (Recommended)

For automated daily emails:

1. **Fork/push this repository to your GitHub account**

2. **Configure GitHub Secrets** (Settings → Secrets and variables → Actions)
   - `GMAIL_USER`: Your Gmail address
   - `GMAIL_PASS`: Your Gmail App Password (NOT your account password)
   - `TO_EMAIL`: Recipient email address

3. **Enable GitHub Actions** (Actions tab)

4. **Test the workflow**
   - Go to Actions tab
   - Select "AI Daily News" workflow
   - Click "Run workflow"
   - Check inbox in 1-2 minutes!

---

## 🏗️ Architecture

### Single-File Structure (`main.py`)

All logic is contained in `main.py` (~670 lines):

| Function | Purpose |
|----------|---------|
| `get_aest_time()` | Returns current AEST/AEDT time using ZoneInfo |
| `fetch_google_news(keyword, max_items, retries)` | Fetches articles from Google News RSS for a single keyword |
| `fetch_all_news()` | Aggregates AI news using 38 keywords, deduplicates by title + similarity, sorts by media authority |
| `fetch_layoff_news()` | Aggregates layoff news using 10 keywords, deduplicates by title + similarity |
| `generate_html_content(ai_news, layoff_news)` | Generates HTML with 2-column grid layout for both sections |
| `send_email(subject, html_content, ...)` | Sends email via Gmail SMTP |
| `save_html_file(html_content)` | Saves HTML to `docs/index.html` for GitHub Pages |
| `main()` | Orchestrates the entire pipeline |

### News Keywords

**AI News Keywords (38 total):**
- Companies/Products: OpenAI, Claude, DeepMind, Qwen, Kimi, GLM, DeepSeek
- Founders/CEOs: Sam Altman, Dario Amodei, Demis Hassabis
- Topics: AI hiring, VC funding, regulation, safety, competition
- Tools: Hugging Face, LangChain, Llama, Mistral, Ollama, vLLM, Gradio, Streamlit

**Layoff Keywords (10 total):**
- AI layoffs, automation job cuts, AI replacing workers, job displacement, workforce reduction

### SMTP Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `GMAIL_USER` | Yes | Gmail address for sending |
| `GMAIL_PASS` | Yes | Gmail App Password (NOT account password) |
| `TO_EMAIL` | Yes | Recipient email address |

---

## 🔧 Customization

### Modifying Keywords

When adding AI news keywords:
1. Edit `fetch_all_news()` function (around line 79-127 in main.py)
2. Add to the appropriate keyword category
3. Keep descriptive comments for organization
4. Use English keywords for global coverage

When adding layoff keywords:
1. Edit `fetch_layoff_news()` function (around line 150-162 in main.py)
2. Focus on AI-driven automation/displacement themes

### Changing Schedule

Edit `.github/workflows/ai_daily_news.yml`:
- Line 9-11: Modify the cron schedule
- Current: `cron: '0 22 * * *'` (22:00 UTC daily)
- Note: GitHub Actions only supports UTC; schedule does not auto-adjust for DST

### Modifying HTML Layout

The `generate_html_content()` function (~lines 113-460 in main.py):
- Modify inline CSS styles
- Update HTML structure for different layouts
- Change 2-column to single-column or 3-column grid by editing `.news-grid`

---

## ✅ Testing & Deployment

### Local Testing
```bash
python main.py
```
Check:
- Console output for errors
- `docs/index.html` for email preview
- Check your TO_EMAIL inbox for test email

### Manual GitHub Actions Trigger
1. Go to Actions tab
2. Select "AI Daily News" workflow
3. Click "Run workflow"
4. Wait 1-2 minutes and check inbox

### View Deployed Email
- Email in inbox (formatted HTML)
- Web version at GitHub Pages: `https://github.com/yourusername/AI_DAILY/docs/index.html`

---

## 📝 Important Notes

### Technical Details
- **Workflow auto-commits**: Updates `docs/index.html` with message "Update daily news - YYYY-MM-DD"
- **Google News RSS rate limiting**: Each keyword fetches max 2 items to avoid rate limits
- **lxml is REQUIRED**: Script exits without it - ensure installed via `pip install -r requirements.txt`
- **Time zone handling**: Uses Python 3.9+ built-in `zoneinfo` (ZoneInfo)
- **DST Note**: GitHub Actions schedule is fixed UTC; during Australian DST it runs at 9am local instead of 8am

### Security
- GitHub Secrets protect all credentials
- App-Specific Password: Use Gmail app password, NOT your account password
- TLS encryption: Email sent over secure SMTP connection
- Read-only: Only fetches public RSS feeds, no data modifications

### Free & Reliable
- ✅ **GitHub Actions**: Free tier includes 2,000 minutes/month
- ✅ **Google News RSS**: Public, no API key required
- ✅ **Gmail SMTP**: Standard SMTP delivery
- ✅ **GitHub Pages**: Free hosting for `docs/index.html`

---

## 📚 For More Details

- **System Architecture Details**: See `SOLUTION_SUMMARY.md` for detailed diagrams and explanations
- **Project Tracking**: Check `docs/index.html` to see the latest generated email
- **GitHub Workflow**: `.github/workflows/ai_daily_news.yml`

---

## 🔄 Common Workflows

### Add a new keyword to AI News
1. Open `main.py`
2. Find `fetch_all_news()` function
3. Add keyword to appropriate category with comment
4. Test: `python main.py`

### Test changes locally before committing
1. Modify code
2. Run `python main.py`
3. Check `docs/index.html` output
4. Check console for errors
5. Git add/commit/push

### Trigger workflow manually
1. GitHub Actions tab → AI Daily News → Run workflow
2. Select `main` branch
3. Wait 1-2 minutes
4. Check email inbox

---

## 🛠️ Development Commands

```bash
# Install/update dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Check Python version
python --version

# Check installed packages
pip list | grep -E "requests|beautifulsoup4|lxml"
```

---

**Last Updated**: March 2026
**Project Status**: Active, running daily
