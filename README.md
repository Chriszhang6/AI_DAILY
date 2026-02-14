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
pip install requests beautifulsoup4 python-dotenv
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
   - `GMAIL_PASS`
   - `TO_EMAIL`

The workflow runs daily at **8:00 AM UTC** (6:00 PM AEST).

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.

## License

MIT
