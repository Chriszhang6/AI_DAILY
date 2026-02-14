# AI DAILY | AI 日报

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### 📰 Overview

**AI DAILY** is an automated news aggregation system that delivers a daily digest of AI-related news directly to your inbox. It fetches the latest articles from multiple sources, compiles them into a beautifully formatted newspaper-style HTML email, and sends it automatically via GitHub Actions.

### ✨ Features

- 📰 **Professional Layout**: Newspaper-style HTML email with responsive design
- 🤖 **Comprehensive Coverage**: Aggregates news from 12 AI-related keywords including OpenAI, Claude, DeepMind, Qwen, Kimi, GLM, DeepSeek, and more
- ⏰ **Automated Delivery**: Runs 3 times daily via GitHub Actions (8am, 12pm, 5pm AEST)
- 🌏 **Global Perspective**: Covers both international and Chinese AI companies and research
- 🎨 **Responsive Design**: Looks great on both desktop and mobile devices
- 🔒 **Secure**: Uses GitHub Secrets to protect your credentials

### 🚀 Quick Start

#### Prerequisites

- Python 3.9 or higher
- A Gmail account with [App Password](https://myaccount.google.com/apppasswords) enabled
- A GitHub account (for automated deployment)

#### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Chriszhang6/AI_DAILY.git
   cd AI_DAILY
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file based on `.env.template`:
   ```bash
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASS=your_app_password
   TO_EMAIL=recipient@example.com
   ```

4. **Run the script**
   ```bash
   python main.py
   ```

#### GitHub Actions Setup (Recommended)

For automated daily emails, set up GitHub Actions:

1. **Fork or push this repository to your GitHub account**

2. **Configure GitHub Secrets**
   
   Go to your repository → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   
   Add three secrets:
   - `GMAIL_USER`: Your Gmail address (e.g., `your_email@gmail.com`)
   - `GMAIL_PASS`: Your Gmail App Password ([how to generate](https://myaccount.google.com/apppasswords))
   - `TO_EMAIL`: Recipient email address

3. **Enable GitHub Actions**
   
   Go to **Actions** tab and enable workflows if prompted.

4. **Test the workflow**
   
   - Go to **Actions** tab
   - Select **"AI Daily News"** workflow
   - Click **"Run workflow"** → select `main` branch → **"Run workflow"**
   - Check your inbox in 1-2 minutes!

### 📋 How It Works

1. **News Fetching**: Queries Google News RSS feeds with 12 AI-related keywords
2. **Aggregation**: Collects articles and removes duplicates by title
3. **HTML Generation**: Creates a newspaper-style HTML email with different layout sections:
   - Hero article (featured story)
   - Featured articles (highlighted news)
   - Standard list (brief updates)
   - Sidebar (quick reads)
4. **Email Delivery**: Sends the formatted email via Gmail SMTP

### 🔧 Configuration

#### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GMAIL_USER` | Gmail address for sending emails | `your_email@gmail.com` |
| `GMAIL_PASS` | Gmail App Password (not account password!) | `abcd efgh ijkl mnop` |
| `TO_EMAIL` | Recipient email address | `recipient@example.com` |

#### News Sources

The system searches for news using these keywords:
- OpenAI GPT
- Claude AI Anthropic
- Google DeepMind
- Qwen Alibaba
- Kimi AI Moonshot
- GLM Zhipu
- DeepSeek AI
- Artificial Intelligence breakthrough
- LLM large language model
- Machine Learning news
- AI technology latest
- Deep learning research

#### Schedule

The GitHub Actions workflow runs automatically 3 times daily:
- **22:00 UTC** (8am AEST)
- **02:00 UTC** (12pm AEST)
- **07:00 UTC** (5pm AEST)

You can also manually trigger the workflow anytime from the Actions tab.

### 📦 Dependencies

- `requests>=2.31.0` - HTTP requests
- `beautifulsoup4>=4.12.0` - HTML/XML parsing
- `lxml>=4.9.0` - XML parser backend (required)
- `python-dotenv>=1.0.0` - Environment variable management (optional for local dev)

### 🐛 Troubleshooting

**Not receiving emails?**

1. ✅ Verify GitHub Secrets are correctly set (no extra spaces)
2. ✅ Ensure `GMAIL_PASS` is an App Password, not your account password
3. ✅ Check if 2-Factor Authentication is enabled on your Google account
4. ✅ Review GitHub Actions logs for error messages
5. ✅ Check your spam/junk folder

**How to generate Gmail App Password:**

1. Go to https://myaccount.google.com/apppasswords
2. Enable 2-Factor Authentication if not already enabled
3. Create a new app password for "Mail"
4. Copy the 16-character password (remove spaces)
5. Use this as `GMAIL_PASS` in GitHub Secrets

### 📝 License

MIT License - Feel free to use and modify for your own needs!

---

<a name="中文"></a>
## 中文

### 📰 项目简介

**AI DAILY (AI 日报)** 是一个自动化的新闻聚合系统，每天自动将 AI 相关的最新新闻整理成精美的报纸风格 HTML 邮件，直接发送到您的邮箱。通过 GitHub Actions 实现完全自动化，无需服务器。

### ✨ 功能特点

- 📰 **专业排版**：报纸风格的 HTML 邮件，响应式设计
- 🤖 **全面覆盖**：聚合 12 个 AI 相关关键词的新闻，包括 OpenAI、Claude、DeepMind、通义千问、Kimi、智谱、DeepSeek 等
- ⏰ **自动推送**：通过 GitHub Actions 每天自动运行 3 次（澳东时间上午 8 点、中午 12 点、下午 5 点）
- 🌏 **国际视野**：涵盖国际和中国的 AI 公司及研究
- 🎨 **响应式设计**：在桌面和移动设备上都有很好的显示效果
- 🔒 **安全可靠**：使用 GitHub Secrets 保护您的凭证信息

### 🚀 快速开始

#### 前置要求

- Python 3.9 或更高版本
- 一个启用了[应用专用密码](https://myaccount.google.com/apppasswords)的 Gmail 账号
- 一个 GitHub 账号（用于自动化部署）

#### 本地设置

1. **克隆仓库**
   ```bash
   git clone https://github.com/Chriszhang6/AI_DAILY.git
   cd AI_DAILY
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境变量**
   
   基于 `.env.template` 创建 `.env` 文件：
   ```bash
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASS=your_app_password
   TO_EMAIL=recipient@example.com
   ```

4. **运行脚本**
   ```bash
   python main.py
   ```

#### GitHub Actions 设置（推荐）

设置 GitHub Actions 以实现每日自动邮件推送：

1. **Fork 或推送此仓库到您的 GitHub 账号**

2. **配置 GitHub Secrets**
   
   进入仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
   
   添加三个密钥：
   - `GMAIL_USER`：您的 Gmail 地址（如 `your_email@gmail.com`）
   - `GMAIL_PASS`：您的 Gmail 应用专用密码（[如何生成](https://myaccount.google.com/apppasswords)）
   - `TO_EMAIL`：接收邮件的地址

3. **启用 GitHub Actions**
   
   进入 **Actions** 标签页，如提示则启用工作流。

4. **测试工作流**
   
   - 进入 **Actions** 标签页
   - 选择 **"AI Daily News"** 工作流
   - 点击 **"Run workflow"** → 选择 `main` 分支 → **"Run workflow"**
   - 1-2 分钟后检查您的收件箱！

### 📋 工作原理

1. **新闻获取**：使用 12 个 AI 相关关键词查询 Google News RSS 源
2. **聚合处理**：收集文章并按标题去重
3. **HTML 生成**：创建包含多个布局区域的报纸风格 HTML 邮件：
   - 头条文章（主要故事）
   - 精选文章（重点新闻）
   - 标准列表（简讯）
   - 侧边栏（快速阅读）
4. **邮件发送**：通过 Gmail SMTP 发送格式化的邮件

### 🔧 配置说明

#### 环境变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `GMAIL_USER` | 用于发送邮件的 Gmail 地址 | `your_email@gmail.com` |
| `GMAIL_PASS` | Gmail 应用专用密码（不是账号密码！） | `abcd efgh ijkl mnop` |
| `TO_EMAIL` | 接收邮件的地址 | `recipient@example.com` |

#### 新闻来源

系统使用以下关键词搜索新闻：
- OpenAI GPT
- Claude AI Anthropic
- Google DeepMind
- Qwen Alibaba（通义千问）
- Kimi AI Moonshot
- GLM Zhipu（智谱）
- DeepSeek AI
- Artificial Intelligence breakthrough
- LLM large language model
- Machine Learning news
- AI technology latest
- Deep learning research

#### 运行时间表

GitHub Actions 工作流每天自动运行 3 次：
- **22:00 UTC**（澳东时间上午 8 点）
- **02:00 UTC**（澳东时间中午 12 点）
- **07:00 UTC**（澳东时间下午 5 点）

您也可以随时从 Actions 标签页手动触发工作流。

### 📦 依赖项

- `requests>=2.31.0` - HTTP 请求
- `beautifulsoup4>=4.12.0` - HTML/XML 解析
- `lxml>=4.9.0` - XML 解析器后端（必需）
- `python-dotenv>=1.0.0` - 环境变量管理（本地开发可选）

### 🐛 故障排除

**收不到邮件？**

1. ✅ 验证 GitHub Secrets 设置正确（无多余空格）
2. ✅ 确保 `GMAIL_PASS` 是应用专用密码，而不是账号密码
3. ✅ 检查 Google 账号是否已启用两步验证
4. ✅ 查看 GitHub Actions 日志中的错误信息
5. ✅ 检查垃圾邮件/垃圾箱文件夹

**如何生成 Gmail 应用专用密码：**

1. 访问 https://myaccount.google.com/apppasswords
2. 如果尚未启用，请先启用两步验证
3. 为"邮件"创建新的应用专用密码
4. 复制 16 位密码（去掉空格）
5. 将其作为 `GMAIL_PASS` 用于 GitHub Secrets

### 📝 许可证

MIT 许可证 - 欢迎自由使用和修改！
