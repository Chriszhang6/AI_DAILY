# 邮件发送问题诊断与测试指南 (Email Delivery Issue Diagnosis & Testing Guide)

## 问题摘要 (Problem Summary)

### 问题描述 (Issue Description)
在修复了 lxml 依赖问题后，手动运行 GitHub Action 仍然没有收到邮件。

### 根本原因 (Root Cause)
通过分析 GitHub Actions 的工作流运行日志（run ID: 22014183062），发现：

1. **时间线问题**: 
   - 计划任务在 2026-02-14 08:23 UTC 运行
   - 使用的是旧提交 `5db6fd6` (first commit)
   - PR #1 在 21:29 UTC 才合并到 main 分支

2. **工作流文件差异**:
   - 旧提交中的 `.github/workflows/ai_daily_news.yml` 使用了错误的安装命令:
     ```yaml
     run: pip install requests beautifulsoup4  # ❌ 错误：缺少 lxml
     ```
   - 更新后的工作流文件使用正确的命令:
     ```yaml
     run: pip install -r requirements.txt      # ✓ 正确：包含所有依赖
     ```

3. **失败原因**:
   - 由于缺少 lxml，BeautifulSoup 无法解析 XML
   - 所有新闻获取失败（错误信息: "Couldn't find a tree builder with the features you requested: xml"）
   - 没有获取到新闻，因此没有发送邮件

## 解决方案 (Solution)

### 1. 验证修复 (Verify Fix)

主分支现在包含正确的工作流配置：
- ✓ `requirements.txt` 包含 `lxml>=4.9.0`
- ✓ 工作流使用 `pip install -r requirements.txt`
- ✓ `main.py` 包含 lxml 导入检查

### 2. 本地测试 (Local Testing)

运行测试脚本验证所有组件：

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试套件
python test_email_flow.py
```

测试内容：
- ✓ 依赖导入（requests, beautifulsoup4, lxml）
- ✓ XML 解析功能
- ✓ HTML 邮件生成
- ✓ 完整流程模拟（使用模拟数据）
- ⚠ 新闻获取（需要网络访问）
- ⚠ SMTP 连接（需要邮件凭证）

### 3. GitHub Actions 测试 (GitHub Actions Testing)

#### 方式 A: 使用测试工作流（推荐）

1. 进入 GitHub 仓库的 Actions 标签
2. 选择 "Test Email Flow" 工作流
3. 点击 "Run workflow"
4. 选择是否发送真实邮件：
   - `false`: 仅测试组件和逻辑（不需要secrets）
   - `true`: 发送真实邮件（需要配置 secrets）

#### 方式 B: 手动触发生产工作流

1. 进入 GitHub 仓库的 Actions 标签
2. 选择 "AI Daily News" 工作流
3. 点击 "Run workflow" 按钮
4. 选择 `main` 分支
5. 点击 "Run workflow" 确认

### 4. 验证邮件发送 (Verify Email Delivery)

当工作流成功运行时，检查以下内容：

#### 在 GitHub Actions 日志中：
```
🚀 Starting AI Daily News Digest...
📡 Fetching news from sources...
  ✓ Fetched 2 articles for 'OpenAI GPT'
  ✓ Fetched 2 articles for 'Claude AI Anthropic'
  ...
✓ Fetched 10 articles total
📝 Generating email content...
📧 Sending email to your@email.com...
✓ Email sent successfully to your@email.com
✓ Daily news digest completed successfully!
```

#### 在收件箱中：
- 主题: "AI Daily News Digest - YYYY-MM-DD"
- 格式: 报纸风格的 HTML 邮件
- 内容: 10 条 AI 相关新闻

## 测试文件说明 (Test Files)

### `test_email_flow.py`
综合测试脚本，验证所有组件：
- 模块导入测试
- XML 解析器测试
- 新闻获取测试（需要网络）
- HTML 生成测试
- 完整流程测试（使用模拟数据）
- 环境变量检查
- SMTP 连接测试（需要凭证）

### `.github/workflows/test_email_flow.yml`
测试工作流，可以：
- 在 CI 环境中运行测试
- 可选择性发送真实邮件
- 验证依赖安装正确

### `.github/workflows/ai_daily_news.yml`
生产工作流：
- 每天 UTC 8:00 自动运行
- 可以手动触发
- 获取真实新闻并发送邮件

## 常见问题 (FAQ)

### Q: 为什么我还是没收到邮件？

**A:** 检查以下几点：

1. **GitHub Secrets 配置**
   ```
   Settings → Secrets and variables → Actions → Repository secrets
   ```
   需要配置：
   - `GMAIL_USER`: 发送邮件的 Gmail 地址
   - `GMAIL_PASS`: Gmail 应用专用密码（不是账号密码！）
   - `TO_EMAIL`: 接收邮件的地址

2. **Gmail 应用专用密码**
   - 访问: https://myaccount.google.com/apppasswords
   - 创建新的应用专用密码
   - 使用生成的 16 位密码作为 `GMAIL_PASS`

3. **工作流运行状态**
   - 检查 Actions 标签中的工作流运行日志
   - 查找错误消息
   - 确认使用的是 main 分支的最新代码

### Q: 测试脚本显示网络错误？

**A:** 这是正常的。`test_email_flow.py` 会尝试获取真实新闻，但在受限网络环境中会失败。只要其他测试通过，说明代码逻辑正确。在 GitHub Actions 中有完整的网络访问，可以正常获取新闻。

### Q: 如何调试邮件发送问题？

**A:** 查看 GitHub Actions 运行日志：

1. 进入 Actions 标签
2. 点击最近的工作流运行
3. 点击 "build" job
4. 展开 "Run AI Daily News" 步骤
5. 查看详细输出，包括：
   - 新闻获取状态
   - 环境变量检查
   - SMTP 连接和发送状态

## 技术细节 (Technical Details)

### 依赖项 (Dependencies)
- `requests>=2.31.0`: HTTP 请求
- `beautifulsoup4>=4.12.0`: HTML/XML 解析
- `lxml>=4.9.0`: XML 解析器（**关键依赖**）
- `python-dotenv>=1.0.0`: 本地开发环境变量（可选）

### 新闻源 (News Sources)
使用 Google News RSS feeds，搜索以下关键词：
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

### 邮件格式 (Email Format)
- 报纸风格的 HTML 布局
- 响应式设计（支持移动设备）
- 包含以下部分：
  - 头条新闻（大版面）
  - 重点新闻（中等版面）
  - 简讯列表
  - 侧边栏快讯

## 下一步 (Next Steps)

1. ✓ 已创建测试脚本和文档
2. ✓ 已修复工作流配置
3. ⏳ 等待下次计划任务运行 (每天 UTC 8:00)
4. ⏳ 或手动触发工作流验证
5. ⏳ 确认收到邮件

## 参考链接 (References)

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Gmail 应用专用密码](https://support.google.com/accounts/answer/185833)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [lxml 文档](https://lxml.de/)
