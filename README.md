# AI DAILY

Automated daily AI news digest delivered to your inbox via email.

## Features

- 📰 Newspaper-style HTML email layout
- 🤖 Aggregates news from multiple AI/LLM sources
- ⏰ Scheduled daily delivery at 6 PM AEST
- 🌏 Covers both international and Chinese AI companies (OpenAI, Anthropic, Alibaba, Moonshot, Zhipu, DeepSeek, etc.)

## Setup

### 1. Clone and Install Dependencies

```bash
pip install -r requirements.txt
# Or manually:
# pip install requests beautifulsoup4 lxml python-dotenv
```

### 2. Configure Gmail

1. Create a `.env` file (use `.env.template` as reference)
2. Enable 2-Factor Authentication on your Google Account
3. Generate an [App Password](https://myaccount.google.com/apppasswords)
4. Add your credentials to `.env`:

```
GMAIL_USER=your_email@gmail.com
GMAIL_PASS=your_app_password_here
TO_EMAIL=recipient@example.com
```

### 3. Run Locally

```bash
python main.py
```

## GitHub Actions Setup

To enable automated daily emails via GitHub Actions:

1. Fork/Clone this repository to your GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:
   - `GMAIL_USER`
   - `GMAIL_PASS` (use [App Password](https://myaccount.google.com/apppasswords), not your account password)
   - `TO_EMAIL`

The workflow runs daily at **8:00 AM UTC** (6:00 PM AEST).

### Testing Your Setup

Before waiting for the scheduled run, test your configuration:

1. Go to **Actions** tab in your GitHub repository
2. Select **"AI Daily News"** workflow
3. Click **"Run workflow"** → select `main` branch → **"Run workflow"**
4. Check the logs and your inbox for the test email

For detailed testing and troubleshooting, see [TESTING.md](TESTING.md).

## Troubleshooting

If you don't receive emails:
1. Verify GitHub Secrets are correctly set
2. Check GitHub Actions logs for errors
3. Ensure you're using a Gmail App Password (not your account password)
4. Run the test script locally: `python test_email_flow.py`
5. See [TESTING.md](TESTING.md) for comprehensive debugging guide

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.

## License

MIT
