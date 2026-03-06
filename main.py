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
import re
from difflib import SequenceMatcher

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

# 权威媒体列表（按优先级排序）
AUTHORITATIVE_SOURCES = [
    'Reuters', 'Bloomberg', 'The New York Times', 'Wall Street Journal',
    'Financial Times', 'The Economist', 'The Verge', 'TechCrunch',
    'Wired', 'Ars Technica', 'MIT Technology Review', 'Nature',
    'Science', 'IEEE Spectrum', 'CNBC', 'BBC News', 'The Guardian',
    'Washington Post', 'AP News', 'AFP'
]

def get_source_priority(source):
    """获取媒体权威性优先级，分数越高越权威"""
    source_upper = source.upper()
    for i, authoritative in enumerate(AUTHORITATIVE_SOURCES):
        if authoritative.upper() in source_upper:
            return len(AUTHORITATIVE_SOURCES) - i  # 权威媒体得高分
    return 0  # 普通媒体得0分

def extract_key_entities(title):
    """从标题中提取关键实体（公司、产品、人名）"""
    entities = set()
    title_upper = title.upper()

    # AI公司列表
    companies = [
        'OPENAI', 'ANTHROPIC', 'CLAUDE', 'DEEPMIND', 'GOOGLE', 'META',
        'ALIBABA', 'QWEN', 'KIMI', 'MOONSHOT', 'GLM', 'ZHIPU', 'DEEPSEEK',
        'MICROSOFT', 'AMAZON', 'NVIDIA', 'APPLE', 'TENCENT', 'BYTEDANCE',
        'BAIDU', 'MISTRAL', 'HUGGING FACE', 'STABILITY AI', 'PERPLEXITY',
        'COHERE', 'AI21', 'INFLECTION', 'CHARACTER.AI', 'AUTODESK',
        'SALESFORCE', 'ORACLE', 'IBM', 'SAP', 'ADOBE', 'SPOTIFY',
        'BLOCK', 'STRIPE', 'PAYPAL', 'INTUIT', 'SERVICENOW'
    ]

    # AI产品和模型
    products = [
        'GPT-4', 'GPT4', 'GPT-5', 'GPT5', 'CHATGPT',
        'LLAMA', 'LLAMA 2', 'LLAMA 3', 'LLAMA2', 'LLAMA3',
        'DALL-E', 'DALLE', 'MIDJOURNEY', 'STABLE DIFFUSION',
        'GEMINI', 'GEMINI PRO', 'GEMINI ULTRA',
        'SORA', 'VOYAGER', 'SPARC', 'JARVIS',
        'ALPHAFOLD', 'ALPHACODE', 'ALPHAGEOMETRY',
        'GROK', 'XAI', 'COPYSCAT', 'JASPER'
    ]

    # AI知名人物
    people = [
        'SAM ALTMAN', 'DARIO AMODEI', 'DEMIS HASSABIS', 'YANN LECUN',
        'ANDREW NG', 'GEOFFREY HINTON', 'ELON MUSK', 'SATYA NADELLA',
        'SUNDAR PICHAI', 'MARK ZUCKERBERG', 'JENNA LYONS'
    ]

    # 提取实体
    for company in companies:
        if company in title_upper:
            entities.add(company)

    for product in products:
        if product.upper() in title_upper:
            entities.add(product.upper())

    for person in people:
        if person in title_upper:
            entities.add(person)

    return entities

def get_event_type(title):
    """获取新闻事件类型"""
    title_lower = title.lower()

    event_patterns = {
        'launch': ['launch', 'release', 'announce', 'unveil', 'introduce', 'debuts', 'rolls out'],
        'funding': ['funding', 'raises', 'investment', 'invest', 'venture', 'series a', 'series b', 'ipo'],
        'layoff': ['layoff', 'lay off', 'layoffs', 'cutting jobs', 'job cuts', 'workforce reduction', 'firing', 'lays off', 'cuts'],
        'hiring': ['hiring', 'recruiting', 'chief', 'executive', 'appointed', 'joins', 'named'],
        'partnership': ['partnership', 'partner', 'collaboration', 'collaborate', 'deal', 'acquisition', 'acquire', 'merger'],
        'regulation': ['regulation', 'regulatory', 'ban', 'lawsuit', 'legal', 'safety', 'concerns', 'investigation'],
        'research': ['research', 'study', 'paper', 'breakthrough', 'develops', 'scientists', 'discovery'],
        'performance': ['beats', 'surpasses', 'outperforms', 'benchmark', 'test', 'evaluation', 'ranking']
    }

    for event_type, patterns in event_patterns.items():
        for pattern in patterns:
            if pattern in title_lower:
                return event_type

    return 'news'  # 默认类型

def title_similarity(title1, title2):
    """计算两个标题的相似度（考虑实体和事件类型）"""
    # 获取实体和事件类型
    entities1 = extract_key_entities(title1)
    entities2 = extract_key_entities(title2)
    event1 = get_event_type(title1)
    event2 = get_event_type(title2)

    # 如果没有实体，使用字符串相似度
    if not entities1 and not entities2:
        return SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

    # 计算实体重叠度
    entity_overlap = len(entities1 & entities2) / max(len(entities1 | entities2), 1)

    # 事件类型相同，增加相似度
    event_bonus = 0.3 if event1 == event2 else 0

    # 字符串相似度作为补充
    text_similarity = SequenceMatcher(None, title1.lower(), title2.lower()).ratio()

    # 综合得分
    similarity = entity_overlap * 0.7 + event_bonus + text_similarity * 0.3

    return min(similarity, 1.0)  # 确保不超过1

def is_same_event(article1, article2, threshold=0.6):
    """判断两篇文章是否报道同一事件"""
    # 标题完全相同
    if article1['title'] == article2['title']:
        return True

    # URL相同（可能是同一来源）
    if article1['link'] == article2['link']:
        return True

    # 计算标题相似度
    similarity = title_similarity(article1['title'], article2['title'])

    return similarity >= threshold

def deduplicate_articles(articles, target_count=10, similarity_threshold=0.6):
    """
    智能去重新闻文章

    Args:
        articles: 原始文章列表
        target_count: 目标保留数量
        similarity_threshold: 相似度阈值

    Returns:
        去重后的文章列表
    """
    if not articles:
        return []

    # 按媒体权威性排序
    sorted_articles = sorted(
        articles,
        key=lambda x: (get_source_priority(x['source']), len(x['title'])),
        reverse=True
    )

    unique_groups = []

    for article in sorted_articles:
        # 检查是否与已有分组中的文章是同一事件
        is_duplicate = False
        for group in unique_groups:
            if is_same_event(article, group[0], similarity_threshold):
                group.append(article)  # 加入同一事件组
                is_duplicate = True
                break

        if not is_duplicate:
            unique_groups.append([article])  # 创建新的事件组

    # 从每个事件组中选择最佳文章（组内第一个，因为已经按权威性排序）
    deduplicated = [group[0] for group in unique_groups]

    return deduplicated[:target_count]

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

    # 收集更多新闻以供去重筛选
    news = []
    for keyword in keywords:
        articles = fetch_google_news(keyword, max_items=3)  # 增加到3条以获得更多候选
        news.extend(articles)
        if len(news) >= 50:  # 收集更多候选新闻
            break

    # 使用智能去重，返回10条不重复的新闻
    unique_news = deduplicate_articles(news, target_count=10)

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

    # 收集更多新闻以供去重筛选
    news = []
    for keyword in keywords:
        articles = fetch_google_news(keyword, max_items=3)  # 增加到3条
        news.extend(articles)
        if len(news) >= 30:
            break

    # 使用智能去重，返回5条不重复的裁员新闻（减少重复）
    unique_news = deduplicate_articles(news, target_count=5)

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
    print(f"✓ Fetched {len(ai_news)} unique AI articles")

    if not ai_news:
        print("✗ ERROR: No AI news found. Cannot send email.", file=sys.stderr)
        sys.exit(1)

    # Fetch layoff news
    print("📡 Fetching layoff news from sources...")
    layoff_news = fetch_layoff_news()
    print(f"✓ Fetched {len(layoff_news)} unique layoff articles")

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
