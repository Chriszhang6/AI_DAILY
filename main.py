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

def generate_html_content(news_items):
    # 报纸风格：每个新闻项指定其布局类型
    # layout types: 'hero' (头条大图), 'featured' (重要新闻), 'sidebar' (侧边栏小方块), 'standard' (标准)
    layouts = ['hero', 'featured', 'sidebar', 'sidebar', 'featured', 'standard', 'standard', 'sidebar', 'sidebar', 'standard']

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

        /* 主布局：左侧主内容区 + 右侧边栏 */
        .main-layout {
            display: flex;
            gap: 0;
        }
        .content-area {
            flex: 1;
            padding: 20px;
            border-right: 1px solid #ddd;
        }
        .sidebar {
            width: 280px;
            background: #f9f9f9;
            padding: 20px 15px;
        }
        .sidebar-title {
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 2px solid #e94560;
            padding-bottom: 8px;
            margin-bottom: 15px;
            color: #1a1a2e;
        }

        /* 英雄头条样式 */
        .hero-article {
            margin-bottom: 25px;
            padding-bottom: 25px;
            border-bottom: 3px double #000;
        }
        .hero-article .hero-badge {
            display: inline-block;
            background: #e94560;
            color: white;
            font-size: 10px;
            font-weight: bold;
            padding: 4px 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
        }
        .hero-article h2 {
            font-size: 32px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 15px;
            font-family: 'Georgia', serif;
        }
        .hero-article .meta {
            font-size: 11px;
            color: #666;
            margin-bottom: 12px;
            font-style: italic;
        }
        .hero-article .hero-link {
            display: inline-block;
            background: #1a1a2e;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* 重点新闻样式 */
        .featured-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }
        .featured-article {
            border: 1px solid #e0e0e0;
            padding: 18px;
            background: white;
            transition: box-shadow 0.2s;
        }
        .featured-article:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .featured-article .source-tag {
            font-size: 9px;
            color: #e94560;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: bold;
        }
        .featured-article h3 {
            font-size: 16px;
            font-weight: 600;
            line-height: 1.3;
            margin: 10px 0;
            font-family: 'Georgia', serif;
        }
        .featured-article .read-more {
            font-size: 11px;
            color: #1a1a2e;
            text-decoration: none;
            font-weight: bold;
        }

        /* 标准新闻列表 */
        .standard-list {
            border-top: 2px solid #000;
            padding-top: 20px;
        }
        .standard-list h4 {
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 15px;
            color: #1a1a2e;
        }
        .standard-item {
            padding: 12px 0;
            border-bottom: 1px solid #eee;
        }
        .standard-item:last-child {
            border-bottom: none;
        }
        .standard-item .number {
            display: inline-block;
            width: 24px;
            height: 24px;
            background: #1a1a2e;
            color: white;
            font-size: 12px;
            font-weight: bold;
            text-align: center;
            line-height: 24px;
            margin-right: 10px;
        }
        .standard-item h3 {
            display: inline;
            font-size: 14px;
            font-weight: 500;
            line-height: 1.4;
        }
        .standard-item .source {
            display: block;
            font-size: 10px;
            color: #999;
            margin-top: 5px;
            margin-left: 34px;
            text-transform: uppercase;
        }
        .standard-item .read-more {
            display: block;
            font-size: 11px;
            color: #1a1a2e;
            text-decoration: none;
            font-weight: bold;
            margin-top: 5px;
            margin-left: 34px;
        }
        .standard-item .read-more:hover {
            color: #e94560;
        }

        /* 侧边栏小方块 */
        .sidebar-item {
            background: white;
            border: 1px solid #e0e0e0;
            padding: 12px;
            margin-bottom: 12px;
        }
        .sidebar-item h3 {
            font-size: 12px;
            font-weight: 600;
            line-height: 1.4;
            margin: 8px 0;
        }
        .sidebar-item .source {
            font-size: 9px;
            color: #999;
            text-transform: uppercase;
        }
        .sidebar-item .link {
            font-size: 10px;
            color: #e94560;
            text-decoration: none;
            font-weight: bold;
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
            <div class="issue">Vol. """ + get_aest_time().strftime('%Y%m%d') + """ • """ + str(len(news_items)) + """ Stories</div>
        </div>
        <div class="main-layout">
            <div class="content-area">
    """

    # 分配新闻到不同区域
    hero_items = []
    featured_items = []
    standard_items = []
    sidebar_items = []

    for i, item in enumerate(news_items):
        layout = layouts[i] if i < len(layouts) else 'standard'
        item_with_layout = {**item, 'index': i + 1}

        if layout == 'hero':
            hero_items.append(item_with_layout)
        elif layout == 'featured':
            featured_items.append(item_with_layout)
        elif layout == 'sidebar':
            sidebar_items.append(item_with_layout)
        else:
            standard_items.append(item_with_layout)

    # 英雄头条
    if hero_items:
        item = hero_items[0]
        html += f"""
                <article class="hero-article">
                    <h2>{item['title']}</h2>
                    <div class="meta">From {item['source']} • Full story inside</div>
                    <a href="{item['link']}" class="hero-link" target="_blank">Read Full Story →</a>
                </article>
        """

    # 重点新闻网格
    if featured_items:
        html += '<div class="featured-grid">'
        for item in featured_items:
            html += f"""
                    <article class="featured-article">
                        <span class="source-tag">{item['source']}</span>
                        <h3>{item['title']}</h3>
                        <a href="{item['link']}" class="read-more" target="_blank">READ MORE →</a>
                    </article>
            """
        html += '</div>'

    # 标准新闻列表
    if standard_items:
        html += '<div class="standard-list"><h4>In Brief</h4>'
        for item in standard_items:
            html += f"""
                    <div class="standard-item">
                        <span class="number">{item['index']}</span>
                        <h3>{item['title']}</h3>
                        <span class="source">{item['source']}</span>
                        <a href="{item['link']}" class="read-more" target="_blank">READ MORE →</a>
                    </div>
            """
        html += '</div>'

    html += """
            </div>
            <div class="sidebar">
                <div class="sidebar-title">Quick Reads</div>
        """

    # 侧边栏
    for item in sidebar_items:
        html += f"""
                <div class="sidebar-item">
                    <div class="source">{item['source']}</div>
                    <h3>{item['title']}</h3>
                    <a href="{item['link']}" class="link" target="_blank">Read →</a>
                </div>
        """

    html += """
            </div>
        </div>
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
    
    # Fetch news
    print("📡 Fetching news from sources...")
    news = fetch_all_news()
    print(f"✓ Fetched {len(news)} articles total")
    
    if not news:
        print("✗ ERROR: No news found. Cannot send email.", file=sys.stderr)
        sys.exit(1)  # Exit with error code
    
    # Generate HTML
    print("📝 Generating email content...")
    html_content = generate_html_content(news)
    
    # Send email
    gmail_user = os.environ.get('GMAIL_USER')
    gmail_pass = os.environ.get('GMAIL_PASS')
    to_email = os.environ.get('TO_EMAIL')
    
    if not all([gmail_user, gmail_pass, to_email]):
        print("✗ ERROR: Missing required environment variables:", file=sys.stderr)
        print(f"  GMAIL_USER: {'✓' if gmail_user else '✗'}", file=sys.stderr)
        print(f"  GMAIL_PASS: {'✓' if gmail_pass else '✗'}", file=sys.stderr)
        print(f"  TO_EMAIL: {'✓' if to_email else '✗'}", file=sys.stderr)
        sys.exit(1)  # Exit with error code
    
    print(f"📧 Sending email to {to_email}...")
    subject = f"AI Daily News Digest - {get_aest_time().strftime('%Y-%m-%d')}"
    success = send_email(subject, html_content, to_email, gmail_user, gmail_pass)

    if not success:
        print("✗ ERROR: Failed to send email", file=sys.stderr)
        sys.exit(1)  # Exit with error code

    # Save HTML file for GitHub Pages
    print("💾 Saving HTML file for GitHub Pages...")
    html_saved = save_html_file(html_content)
    if not html_saved:
        print("⚠ Warning: Failed to save HTML file, but email was sent successfully")

    print("✓ Daily news digest completed successfully!")
    sys.exit(0)

if __name__ == '__main__':
    main()
