#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

# Check for required lxml dependency for XML parsing
try:
    import lxml
except ImportError:
    print("✗ ERROR: lxml package is required for XML parsing", file=sys.stderr)
    print("  Install it with: pip install lxml", file=sys.stderr)
    sys.exit(1)

# Load .env file for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

def get_aest_time():
    """Get current time in Australian Eastern Time (AEST/AEDT)"""
    return datetime.now(ZoneInfo('Australia/Sydney'))

def fetch_google_news(keyword, max_items=2, retries=3):
    """从Google News RSS获取新闻"""
    last_error = None

    for attempt in range(retries):
        try:
            # Google News RSS格式
            url = f'https://news.google.com/rss/search?q={keyword}'
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, timeout=10, headers=headers)
            resp.raise_for_status()  # Raise an exception for bad status codes

            soup = BeautifulSoup(resp.text, 'xml')
            articles = []

            for item in soup.select('item')[:max_items]:
                title_elem = item.select_one('title')
                link_elem = item.select_one('link')
                source_elem = item.select_one('source')

                if title_elem and link_elem:
                    source = source_elem.text if source_elem else 'News'
                    articles.append({
                        'title': title_elem.text.strip(),
                        'link': link_elem.text.strip(),
                        'source': source
                    })

            if articles:
                print(f"  ✓ Fetched {len(articles)} articles for '{keyword}'")
            else:
                print(f"  ⚠ No articles found for '{keyword}'", file=sys.stderr)

            return articles

        except Exception as e:
            last_error = e
            if attempt < retries - 1:
                print(f"  ⚠ Attempt {attempt + 1}/{retries} failed for '{keyword}': {e}", file=sys.stderr)
                time.sleep(2)  # Wait before retrying
            else:
                print(f"  ✗ All {retries} attempts failed for '{keyword}': {e}", file=sys.stderr)

    return []

def fetch_all_news():
    """从多个关键词聚合AI新闻"""
    keywords = [
        # AI 公司和产品
        'OpenAI GPT',
        'Claude AI Anthropic',
        'Google DeepMind',
        'Qwen Alibaba',
        'Kimi AI Moonshot',
        'GLM Zhipu',
        'DeepSeek AI',
        # AI 创始人/CEO
        'Sam Altman OpenAI',
        'Dario Amodei Anthropic',
        'Demis Hassabis DeepMind',
        'AI founder CEO',
        # AI 人事变动
        'OpenAI hiring',
        'AI executive',
        'AI leadership',
        # AI 创投/融资
        'AI startup funding',
        'AI investment',
        'AI venture capital',
        # AI 行业动态/政策
        'AI regulation',
        'AI safety',
        'AI competition',
        # AI 开源框架和工具
        'Hugging Face transformers',
        'LangChain framework',
        'Stable Diffusion',
        'Meta Llama open source',
        'Mistral AI open source',
        'Ollama AI',
        'vLLM inference',
        # AI 开源社区
        'AI open source tools',
        'GitHub AI Copilot',
        'AI framework release',
        'Gradio ML',
        'Streamlit AI',
        'AutoGPT autonomous agent',
        'AI development tools',
        # 通用 AI 新闻
        'Artificial Intelligence breakthrough',
        'LLM large language model',
        'Machine Learning news',
        'AI technology latest',
        'Deep learning research'
    ]

    news = []
    for keyword in keywords:
        articles = fetch_google_news(keyword, max_items=2)
        news.extend(articles)
        if len(news) >= 20:
            break

    # 去重（按title）和返回前20条
    seen_titles = set()
    unique_news = []
    for item in news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_news.append(item)
            if len(unique_news) >= 20:
                break

    return unique_news

def fetch_layoff_news():
    """从多个关键词聚合AI相关的裁员新闻"""
    keywords = [
        # AI导致的裁员关键词
        'AI layoffs 2025',
        'AI automation job cuts',
        'AI replacing workers',
        'AI job displacement',
        'company AI layoffs',
        'tech automation jobs',
        'AI workforce reduction',
        'AI efficiency layoffs',
        'automation replacing jobs',
        'AI job cuts 2025'
    ]

    news = []
    for keyword in keywords:
        articles = fetch_google_news(keyword, max_items=2)
        news.extend(articles)
        if len(news) >= 10:
            break

    # 去重（按title）和返回前10条
    seen_titles = set()
    unique_news = []
    for item in news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            unique_news.append(item)
            if len(unique_news) >= 10:
                break

    return unique_news

def generate_html_content(ai_news, layoff_news=None):
    """生成 HTML 内容"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Times New Roman', Georgia, serif;
            background: #f5f5f5;
            padding: 15px;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .masthead {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 25px 20px;
            text-align: center;
            border-bottom: 4px solid #e94560;
        }
        .masthead h1 {
            font-size: 56px;
            font-weight: 900;
            letter-spacing: 8px;
            margin-bottom: 8px;
            font-family: 'Arial Black', sans-serif;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .masthead .tagline {
            font-size: 11px;
            letter-spacing: 3px;
            opacity: 0.9;
            text-transform: uppercase;
        }
        .subheader {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            border-bottom: 2px solid #000;
            background: #fff;
        }
        .subheader .date {
            font-weight: bold;
            font-size: 13px;
        }
        .subheader .issue {
            font-size: 11px;
            color: #666;
        }

        /* 版块分隔标题 */
        .section-title {
            background: #1a1a2e;
            color: white;
            padding: 15px 20px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 3px;
            margin: 30px 0 20px 0;
            border-top: 3px solid #e94560;
            border-bottom: 3px solid #e94560;
        }

        /* 新闻网格布局 */
        .news-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            padding: 20px;
        }

        .news-card {
            border: 1px solid #e0e0e0;
            padding: 15px;
            background: white;
            transition: box-shadow 0.2s;
        }
        .news-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .news-card .source-tag {
            font-size: 9px;
            color: #e94560;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
        }
        .news-card h3 {
            font-size: 15px;
            font-weight: 600;
            line-height: 1.3;
            margin: 10px 0;
            font-family: 'Georgia', serif;
        }
        .news-card .read-more {
            font-size: 11px;
            color: #1a1a2e;
            text-decoration: none;
            font-weight: bold;
        }
        .news-card .read-more:hover {
            color: #e94560;
        }

        .footer {
            background: #1a1a2e;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 11px;
        }
        .footer p {
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="masthead">
            <h1>AI DAILY</h1>
            <div class="tagline">Your Source for Artificial Intelligence News</div>
        </div>
        <div class="subheader">
            <div class="date">""" + get_aest_time().strftime('%A, %B %d, %Y').upper() + """</div>
            <div class="issue">Vol. """ + get_aest_time().strftime('%Y%m%d') + """ • AI News + Layoff Tracker</div>
        </div>
    """

    # AI 新闻版块 - 使用简洁的两列网格布局
    html += '<div class="news-grid">'
    for item in ai_news:
        html += f"""
            <div class="news-card">
                <span class="source-tag">{item['source']}</span>
                <h3>{item['title']}</h3>
                <a href="{item['link']}" class="read-more" target="_blank">READ MORE →</a>
            </div>
        """
    html += '</div>'

    # 裁员新闻版块
    if layoff_news and len(layoff_news) > 0:
        html += '<div class="section-title">AI LAYOFF TRACKER</div>'
        html += '<div class="news-grid">'
        for item in layoff_news:
            html += f"""
                <div class="news-card">
                    <span class="source-tag">{item['source']}</span>
                    <h3>{item['title']}</h3>
                    <a href="{item['link']}" class="read-more" target="_blank">READ MORE →</a>
                </div>
            """
        html += '</div>'

    html += """
        <div class="footer">
            <p>AI DAILY DIGEST • AUTOMATED DELIVERY • """ + get_aest_time().strftime('%I:%M %p').upper() + """ AEST</p>
        </div>
    </div>
</body>
</html>
    """
    return html

def send_email(subject, html_content, to_email, gmail_user, gmail_pass):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = to_email

        part = MIMEText(html_content, 'html', _charset='UTF-8')
        msg.attach(part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_pass)
            server.sendmail(gmail_user, to_email, msg.as_string())

        print(f"✓ Email sent successfully to {to_email}")
        return True
    except Exception as e:
        print(f"✗ Error sending email: {e}", file=sys.stderr)
        return False

def save_html_file(html_content, output_path='docs/index.html'):
    """Save HTML content to a file for GitHub Pages"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ HTML file saved to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error saving HTML file: {e}", file=sys.stderr)
        return False

def main():
    print("🚀 Starting AI Daily News Digest...")

    # Fetch AI news
    print("📡 Fetching AI news from sources...")
    ai_news = fetch_all_news()
    print(f"✓ Fetched {len(ai_news)} AI articles")

    if not ai_news:
        print("✗ ERROR: No AI news found. Cannot send email.", file=sys.stderr)
        sys.exit(1)

    # Fetch layoff news
    print("📡 Fetching layoff news from sources...")
    layoff_news = fetch_layoff_news()
    print(f"✓ Fetched {len(layoff_news)} layoff articles")

    # Generate HTML
    print("📝 Generating email content...")
    html_content = generate_html_content(ai_news, layoff_news)

    # Send email
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    to_email = os.environ.get('TO_EMAIL')

    if not all([gmail_user, gmail_pass, to_email]):
        print("✗ ERROR: Missing required environment variables:", file=sys.stderr)
        print(f"  GMAIL_USER: {'✓' if gmail_user else '✗'}", file=sys.stderr)
        print(f"  GMAIL_PASS: {'✓' if gmail_pass else '✗'}", file=sys.stderr)
        print(f"  TO_EMAIL: {'✓' if to_email else '✗'}", file=sys.stderr)
        sys.exit(1)

    print(f"📧 Sending email to {to_email}...")
    subject = f"AI Daily News Digest - {get_aest_time().strftime('%Y-%m-%d')}"
    success = send_email(subject, html_content, to_email, gmail_user, gmail_pass)

    if not success:
        print("✗ ERROR: Failed to send email", file=sys.stderr)
        sys.exit(1)

    # Save HTML file for GitHub Pages
    print("💾 Saving HTML file for GitHub Pages...")
    html_saved = save_html_file(html_content)
    if not html_saved:
        print("⚠ Warning: Failed to save HTML file, but email was sent successfully")

    print("✓ Daily news digest completed successfully!")
    sys.exit(0)

if __name__ == '__main__':
    main()
