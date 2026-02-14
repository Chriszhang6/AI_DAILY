# Solution Architecture | 解决方案架构

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### 📐 Solution Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GitHub Repository                                 │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        GitHub Actions Workflow                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  Scheduled Triggers (3x daily):                                 │  │  │
│  │  │  • 22:00 UTC (8am AEST)  • 02:00 UTC (12pm AEST)               │  │  │
│  │  │  • 07:00 UTC (5pm AEST)                                         │  │  │
│  │  │  • Manual trigger available anytime                             │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                              ↓                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  1. Setup Environment                                           │  │  │
│  │  │     • Checkout code                                             │  │  │
│  │  │     • Setup Python 3.10                                         │  │  │
│  │  │     • Install dependencies (requests, beautifulsoup4, lxml)    │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                              ↓                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  2. Load Secrets from GitHub                                    │  │  │
│  │  │     • GMAIL_USER (sender email)                                 │  │  │
│  │  │     • GMAIL_PASS (app-specific password)                        │  │  │
│  │  │     • TO_EMAIL (recipient email)                                │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                              ↓                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  3. Execute main.py                                             │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Main Python Script (main.py)                        │
│                                                                               │
│  Step 1: Fetch News from Multiple Sources                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Keywords searched (12 total):                                         │ │
│  │  • OpenAI GPT             • Claude AI Anthropic                        │ │
│  │  • Google DeepMind        • Qwen Alibaba                               │ │
│  │  • Kimi AI Moonshot       • GLM Zhipu                                  │ │
│  │  • DeepSeek AI            • Artificial Intelligence breakthrough       │ │
│  │  • LLM large language model  • Machine Learning news                   │ │
│  │  • AI technology latest   • Deep learning research                     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  For each keyword:                                                     │ │
│  │  1. Query Google News RSS feed                                         │ │
│  │     URL: https://news.google.com/rss/search?q={keyword}                │ │
│  │  2. Parse XML response with BeautifulSoup + lxml                       │ │
│  │  3. Extract: title, link, source                                       │ │
│  │  4. Retry up to 3 times on failure (2-second delay)                    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  Step 2: Aggregate and Deduplicate                                           │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  • Collect all articles from different keywords                        │ │
│  │  • Remove duplicates by title                                          │ │
│  │  • Keep top 10 unique articles                                         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  Step 3: Generate Newspaper-Style HTML Email                                 │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  Layout Structure:                                                     │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  Masthead: "AI DAILY" - Professional newspaper header            │ │ │
│  │  ├──────────────────────────────────────────────────────────────────┤ │ │
│  │  │  Hero Article (Item 1): Large featured story with badge         │ │ │
│  │  ├─────────────────────────────────────┬────────────────────────────┤ │ │
│  │  │  Content Area                       │  Sidebar                   │ │ │
│  │  │  • Featured Articles (Items 2, 5)   │  • Quick Reads (Items 3,  │ │ │
│  │  │  • Standard List (Items 6, 7, 10)   │    4, 8, 9) - Compact     │ │ │
│  │  │    "In Brief" section               │    news boxes             │ │ │
│  │  └─────────────────────────────────────┴────────────────────────────┘ │ │
│  │  Responsive CSS: Desktop & Mobile optimized                            │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  Step 4: Send Email via Gmail SMTP                                           │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  • Connect to smtp.gmail.com:587 (TLS)                                 │ │
│  │  • Authenticate with GMAIL_USER and GMAIL_PASS                         │ │
│  │  • Create MIME multipart message (HTML format)                         │ │
│  │  • Send to TO_EMAIL recipient                                          │ │
│  │  • Subject: "AI Daily News | AI 日报 - {date}"                         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                              📧 User's Inbox                                 │
│  Beautiful newspaper-style HTML email with latest AI news                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🔍 How It Works: Detailed Explanation

#### For People Unfamiliar with GitHub Actions

**What is GitHub Actions?**
- GitHub Actions is a free automation service provided by GitHub
- It allows you to run code automatically on a schedule or when events occur
- No server needed! GitHub runs your code on their cloud infrastructure
- Perfect for automated tasks like sending daily emails

**Why use GitHub Actions for this project?**
- ✅ **Free**: Up to 2,000 minutes/month for free accounts
- ✅ **No Server Required**: No need to maintain your own server
- ✅ **Reliable**: GitHub's infrastructure ensures high availability
- ✅ **Easy to Configure**: Simple YAML file configuration
- ✅ **Secure**: Secrets are encrypted and never exposed

#### For People Unfamiliar with RSS

**What is RSS?**
- RSS (Really Simple Syndication) is a standard format for publishing frequently updated content
- It's like a news feed that websites publish for others to read
- Instead of visiting multiple websites, you query RSS feeds to get all news in one place

**How does Google News RSS work?**
- Google News aggregates news from thousands of sources worldwide
- You can search Google News by keyword and get an RSS feed
- Format: `https://news.google.com/rss/search?q={keyword}`
- Returns XML with articles: title, link, source, publication date
- No API key required - it's publicly accessible!

**Why use RSS for this project?**
- ✅ **Free Access**: No API keys or authentication needed
- ✅ **Comprehensive**: Google aggregates from thousands of sources
- ✅ **Reliable**: Google's infrastructure ensures uptime
- ✅ **Structured**: XML format is easy to parse
- ✅ **Fresh Content**: Updated in real-time

### 🔄 Complete Workflow: Step by Step

#### Phase 1: Scheduled Trigger
```
1. GitHub Actions timer reaches scheduled time (e.g., 22:00 UTC)
2. GitHub automatically starts a virtual machine (Ubuntu Linux)
3. Workflow file (.github/workflows/ai_daily_news.yml) is read
4. Execution begins...
```

#### Phase 2: Environment Setup
```
1. Code is checked out from the repository
2. Python 3.10 is installed on the virtual machine
3. Dependencies are installed:
   - requests: For making HTTP requests
   - beautifulsoup4: For parsing HTML/XML
   - lxml: XML parser backend (required by BeautifulSoup)
```

#### Phase 3: Fetch News
```
For each of 12 AI-related keywords:
  1. Construct Google News RSS URL with keyword
  2. Send HTTP GET request to Google News
  3. Receive XML response with news articles
  4. Parse XML using BeautifulSoup + lxml
  5. Extract article data (title, link, source)
  6. Retry up to 3 times if request fails
  7. Add articles to collection
  
Stop when we have at least 10 articles
```

#### Phase 4: Process and Deduplicate
```
1. Review all collected articles
2. Remove duplicates (same title = duplicate)
3. Keep only the top 10 unique articles
4. Prepare for HTML generation
```

#### Phase 5: Generate HTML Email
```
1. Create HTML document structure
2. Add masthead with "AI DAILY" branding
3. Assign each article to a layout slot:
   - Article 1 → Hero (large featured story)
   - Articles 2, 5 → Featured (highlighted news)
   - Articles 3, 4, 8, 9 → Sidebar (quick reads)
   - Articles 6, 7, 10 → Standard list ("In Brief")
4. Apply newspaper-style CSS
5. Make it responsive for mobile devices
```

#### Phase 6: Send Email
```
1. Connect to Gmail SMTP server (smtp.gmail.com:587)
2. Authenticate with credentials from GitHub Secrets
3. Create email message:
   - From: GMAIL_USER
   - To: TO_EMAIL
   - Subject: "AI Daily News | AI 日报 - {date}"
   - Body: HTML content (multipart MIME)
4. Send email
5. Close connection
```

#### Phase 7: Cleanup
```
1. GitHub Actions logs the result (success/failure)
2. Virtual machine is destroyed
3. Wait for next scheduled time
```

### 🔐 Security Features

1. **GitHub Secrets**: Credentials never appear in code or logs
2. **App-Specific Password**: Not your actual Gmail password
3. **TLS Encryption**: Email sent over secure connection
4. **No Data Storage**: News is fetched fresh each time, nothing stored
5. **Read-Only RSS**: Only reading public RSS feeds, no data sent to Google

### 🎯 Key Technologies

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Automation** | GitHub Actions | Schedule and run workflow automatically |
| **Language** | Python 3.10 | Main programming language |
| **HTTP Requests** | requests library | Fetch RSS feeds from Google News |
| **XML Parsing** | BeautifulSoup + lxml | Parse RSS XML responses |
| **Email Sending** | smtplib + email.mime | Send formatted emails via SMTP |
| **Data Source** | Google News RSS | Aggregate news from multiple sources |
| **Email Provider** | Gmail SMTP | Deliver emails to inbox |

### 💡 Why This Solution is Elegant

1. **Serverless**: No server costs, no maintenance, no downtime worries
2. **Free**: All components are free (GitHub Actions, Google RSS, Gmail)
3. **Reliable**: Built on enterprise-grade infrastructure (GitHub + Google)
4. **Simple**: Single-file Python implementation (~500 lines), easy to understand
5. **Flexible**: Easy to modify keywords, schedule, or HTML layout
6. **Scalable**: Can handle thousands of recipients with minor changes
7. **Secure**: Industry-standard security practices
8. **Professional**: Newspaper-quality HTML email design

### 🔧 Customization Points

Users can easily customize:
- **Keywords**: Change which AI topics to follow (main.py line 74-87)
- **Schedule**: Modify when emails are sent (.github/workflows/ai_daily_news.yml line 9-11)
- **Layout**: Adjust HTML template and CSS (main.py line 113-460)
- **Recipient**: Send to different email or multiple recipients
- **Language**: Add more languages to email content
- **Number of Articles**: Change from 10 to any number

---

<a name="中文"></a>
## 中文

### 📐 解决方案架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            GitHub 代码仓库                                    │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        GitHub Actions 工作流                           │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  定时触发器（每天3次）：                                          │  │  │
│  │  │  • 22:00 UTC (澳东时间上午8点)  • 02:00 UTC (中午12点)            │  │  │
│  │  │  • 07:00 UTC (下午5点)                                            │  │  │
│  │  │  • 支持随时手动触发                                               │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                              ↓                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  1. 搭建环境                                                     │  │  │
│  │  │     • 检出代码                                                   │  │  │
│  │  │     • 安装 Python 3.10                                           │  │  │
│  │  │     • 安装依赖包 (requests, beautifulsoup4, lxml)               │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                              ↓                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  2. 从 GitHub 加载密钥                                           │  │  │
│  │  │     • GMAIL_USER (发件人邮箱)                                    │  │  │
│  │  │     • GMAIL_PASS (应用专用密码)                                  │  │  │
│  │  │     • TO_EMAIL (收件人邮箱)                                      │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  │                              ↓                                         │  │
│  │  ┌─────────────────────────────────────────────────────────────────┐  │  │
│  │  │  3. 执行 main.py                                                 │  │  │
│  │  └─────────────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                          主 Python 脚本 (main.py)                            │
│                                                                               │
│  步骤 1: 从多个来源获取新闻                                                    │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  搜索关键词（共12个）：                                                 │ │
│  │  • OpenAI GPT             • Claude AI Anthropic                        │ │
│  │  • Google DeepMind        • Qwen Alibaba（通义千问）                   │ │
│  │  • Kimi AI Moonshot       • GLM Zhipu（智谱）                          │ │
│  │  • DeepSeek AI            • Artificial Intelligence breakthrough       │ │
│  │  • LLM large language model  • Machine Learning news                   │ │
│  │  • AI technology latest   • Deep learning research                     │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  对每个关键词：                                                         │ │
│  │  1. 查询 Google News RSS 源                                            │ │
│  │     URL: https://news.google.com/rss/search?q={keyword}                │ │
│  │  2. 使用 BeautifulSoup + lxml 解析 XML 响应                            │ │
│  │  3. 提取数据：标题、链接、来源                                          │ │
│  │  4. 失败时最多重试 3 次（间隔 2 秒）                                    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  步骤 2: 聚合和去重                                                           │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  • 收集所有来自不同关键词的文章                                         │ │
│  │  • 按标题去除重复项                                                     │ │
│  │  • 保留前 10 篇独特的文章                                               │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  步骤 3: 生成报纸风格的 HTML 邮件                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  布局结构：                                                             │ │
│  │  ┌──────────────────────────────────────────────────────────────────┐ │ │
│  │  │  报头：「AI DAILY」- 专业报纸风格的头部                          │ │ │
│  │  ├──────────────────────────────────────────────────────────────────┤ │ │
│  │  │  头条文章（文章 1）：大型特写故事，带徽章                        │ │ │
│  │  ├─────────────────────────────────────┬────────────────────────────┤ │ │
│  │  │  内容区域                           │  侧边栏                    │ │ │
│  │  │  • 精选文章（文章 2, 5）            │  • 快速阅读（文章 3, 4,   │ │ │
│  │  │  • 标准列表（文章 6, 7, 10）        │    8, 9）- 紧凑型新闻框   │ │ │
│  │  │    "简讯"部分                       │                            │ │ │
│  │  └─────────────────────────────────────┴────────────────────────────┘ │ │
│  │  响应式 CSS：桌面和移动端优化                                          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    ↓                                          │
│  步骤 4: 通过 Gmail SMTP 发送邮件                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │  • 连接到 smtp.gmail.com:587 (TLS)                                     │ │
│  │  • 使用 GMAIL_USER 和 GMAIL_PASS 进行身份验证                          │ │
│  │  • 创建 MIME 多部分消息（HTML 格式）                                    │ │
│  │  • 发送到 TO_EMAIL 收件人                                              │ │
│  │  • 主题：「AI Daily News | AI 日报 - {日期}」                         │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                              📧 用户收件箱                                    │
│  精美的报纸风格 HTML 邮件，包含最新 AI 新闻                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 🔍 工作原理：详细说明

#### 给不熟悉 GitHub Actions 的人

**什么是 GitHub Actions？**
- GitHub Actions 是 GitHub 提供的免费自动化服务
- 它允许您按计划或在事件发生时自动运行代码
- 无需服务器！GitHub 在其云基础设施上运行您的代码
- 非常适合自动化任务，如发送每日邮件

**为什么在这个项目中使用 GitHub Actions？**
- ✅ **免费**：免费账户每月可使用 2,000 分钟
- ✅ **无需服务器**：无需维护自己的服务器
- ✅ **可靠**：GitHub 的基础设施确保高可用性
- ✅ **易于配置**：简单的 YAML 文件配置
- ✅ **安全**：密钥经过加密，永不暴露

#### 给不熟悉 RSS 的人

**什么是 RSS？**
- RSS（Really Simple Syndication，真正简单的聚合）是一种发布频繁更新内容的标准格式
- 它就像网站发布的新闻源，供他人阅读
- 无需访问多个网站，您可以查询 RSS 源在一个地方获取所有新闻

**Google News RSS 如何工作？**
- Google News 聚合来自全球数千个来源的新闻
- 您可以按关键词搜索 Google News 并获得 RSS 源
- 格式：`https://news.google.com/rss/search?q={关键词}`
- 返回包含文章的 XML：标题、链接、来源、发布日期
- 无需 API 密钥 - 它是公开可访问的！

**为什么在这个项目中使用 RSS？**
- ✅ **免费访问**：无需 API 密钥或身份验证
- ✅ **全面**：Google 聚合来自数千个来源
- ✅ **可靠**：Google 的基础设施确保正常运行时间
- ✅ **结构化**：XML 格式易于解析
- ✅ **新鲜内容**：实时更新

### 🔄 完整工作流程：一步一步

#### 阶段 1：定时触发
```
1. GitHub Actions 计时器到达计划时间（例如，22:00 UTC）
2. GitHub 自动启动虚拟机（Ubuntu Linux）
3. 读取工作流文件 (.github/workflows/ai_daily_news.yml)
4. 开始执行...
```

#### 阶段 2：环境设置
```
1. 从仓库检出代码
2. 在虚拟机上安装 Python 3.10
3. 安装依赖项：
   - requests：用于发送 HTTP 请求
   - beautifulsoup4：用于解析 HTML/XML
   - lxml：XML 解析器后端（BeautifulSoup 必需）
```

#### 阶段 3：获取新闻
```
对于 12 个 AI 相关关键词中的每一个：
  1. 使用关键词构造 Google News RSS URL
  2. 向 Google News 发送 HTTP GET 请求
  3. 接收包含新闻文章的 XML 响应
  4. 使用 BeautifulSoup + lxml 解析 XML
  5. 提取文章数据（标题、链接、来源）
  6. 如果请求失败，最多重试 3 次
  7. 将文章添加到集合中
  
当我们至少有 10 篇文章时停止
```

#### 阶段 4：处理和去重
```
1. 查看所有收集的文章
2. 删除重复项（相同标题 = 重复）
3. 仅保留前 10 篇独特文章
4. 准备生成 HTML
```

#### 阶段 5：生成 HTML 邮件
```
1. 创建 HTML 文档结构
2. 添加带有「AI DAILY」品牌的报头
3. 将每篇文章分配到布局位置：
   - 文章 1 → 头条（大型特写故事）
   - 文章 2, 5 → 精选（重点新闻）
   - 文章 3, 4, 8, 9 → 侧边栏（快速阅读）
   - 文章 6, 7, 10 → 标准列表（「简讯」）
4. 应用报纸风格的 CSS
5. 使其适配移动设备
```

#### 阶段 6：发送邮件
```
1. 连接到 Gmail SMTP 服务器 (smtp.gmail.com:587)
2. 使用 GitHub Secrets 中的凭证进行身份验证
3. 创建邮件消息：
   - 发件人：GMAIL_USER
   - 收件人：TO_EMAIL
   - 主题：「AI Daily News | AI 日报 - {日期}」
   - 正文：HTML 内容（多部分 MIME）
4. 发送邮件
5. 关闭连接
```

#### 阶段 7：清理
```
1. GitHub Actions 记录结果（成功/失败）
2. 销毁虚拟机
3. 等待下一个计划时间
```

### 🔐 安全功能

1. **GitHub Secrets**：凭证永不出现在代码或日志中
2. **应用专用密码**：不是您的实际 Gmail 密码
3. **TLS 加密**：通过安全连接发送邮件
4. **无数据存储**：每次都新鲜获取新闻，不存储任何内容
5. **只读 RSS**：只读取公共 RSS 源，不向 Google 发送数据

### 🎯 关键技术

| 组件 | 技术 | 用途 |
|------|------|------|
| **自动化** | GitHub Actions | 自动安排和运行工作流 |
| **编程语言** | Python 3.10 | 主要编程语言 |
| **HTTP 请求** | requests 库 | 从 Google News 获取 RSS 源 |
| **XML 解析** | BeautifulSoup + lxml | 解析 RSS XML 响应 |
| **邮件发送** | smtplib + email.mime | 通过 SMTP 发送格式化邮件 |
| **数据源** | Google News RSS | 从多个来源聚合新闻 |
| **邮件提供商** | Gmail SMTP | 将邮件传递到收件箱 |

### 💡 为什么这个解决方案很优雅

1. **无服务器**：无服务器成本、无维护、无停机时间担忧
2. **免费**：所有组件都是免费的（GitHub Actions、Google RSS、Gmail）
3. **可靠**：构建在企业级基础设施上（GitHub + Google）
4. **简单**：单文件 Python 实现（约 500 行代码），易于理解
5. **灵活**：易于修改关键词、时间表或 HTML 布局
6. **可扩展**：稍作更改即可处理数千个收件人
7. **安全**：采用行业标准的安全实践
8. **专业**：报纸级别的 HTML 邮件设计

### 🔧 自定义点

用户可以轻松自定义：
- **关键词**：更改要关注的 AI 主题（main.py 第 74-87 行）
- **时间表**：修改邮件发送时间（.github/workflows/ai_daily_news.yml 第 9-11 行）
- **布局**：调整 HTML 模板和 CSS（main.py 第 113-460 行）
- **收件人**：发送到不同的邮箱或多个收件人
- **语言**：向邮件内容添加更多语言
- **文章数量**：从 10 篇更改为任意数量
