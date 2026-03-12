# OpenClaw Workspace

<div align="center">

**OpenClaw AI 助手专用工作空间**

[中文](#-中文) | [English](#-english)

</div>

---

## 📁 目录结构 / Directory Structure

```
openclaw-workspace/
├── skills/              # AI 技能目录 / AI Skills
│   └── web-search/     # 五子并行搜索技能 / 5-Agent Parallel Search
├── .gitignore          # Git 忽略配置 / Git Ignore Config
└── README.md           # 本文件 / This File
```

---

## 🌏 中文

### 简介

这是 OpenClaw AI 助手的工作空间仓库，用于存储 AI 技能、项目代码和自动化脚本。

### 🔧 web-search Skill

五子 agent 并行搜索机制，覆盖中文、英文、官方源和结构化数据。

#### 五子架构

| 序号 | 类型 | 搜索方式 | 覆盖范围 |
|------|------|----------|----------|
| 1 | 浏览器 | 百度搜索 | 中文信息 |
| 2 | 浏览器 | Bing 中国搜索 | 海外/官方源 |
| 3 | API | 智谱 API | 国内 + 海外 |
| 4 | API | Brave API | 英文/海外 |
| 5 | 抓取 | 定向网站 | 结构化数据 |

#### 配置步骤

**1. 复制配置文件**
```bash
cd skills/web-search
cp .env.example .env
```

**2. 编辑 .env 文件**
```bash
# API Keys（需要自行申请）
ZHIPU_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here

# 超时配置
SEARCH_TIMEOUT=300
CRAWL_TIMEOUT=30
PROGRESS_INTERVAL=60

# 搜索配置
MAX_RESULTS_PER_AGENT=5
DEEP_CRAWL_ENABLED=true
MAX_PAGES_PER_AGENT=3
```

**3. 安装依赖**
```bash
pip install playwright python-dotenv aiohttp
playwright install chromium firefox
```

#### 使用方法

在子 agent 中调用：
```python
from search import search

result = await search(
    query="搜索关键词",
    max_results=5,
    deep_crawl=True
)
```

#### 结果输出

搜索结果自动保存到 `search_results.json` 文件，包含：
- 完整的搜索结果（标题、链接、摘要、内容）
- 每个 agent 的结果
- 去重后的汇总报告

#### ⚠️ 安全注意事项

- **不要提交 `.env` 文件** - 已添加到 `.gitignore`
- **Token 定期更新** - 建议 90 天更换一次
- **权限最小化** - 只给必要的 API 权限

---

## 🌍 English

### Introduction

This is the dedicated workspace repository for OpenClaw AI Assistant, used to store AI skills, project code, and automation scripts.

### 🔧 web-search Skill

Five-agent parallel search mechanism, covering Chinese, English, official sources, and structured data.

#### Five-Agent Architecture

| # | Type | Search Method | Coverage |
|---|------|---------------|----------|
| 1 | Browser | Baidu Search | Chinese content |
| 2 | Browser | Bing China Search | Overseas/Official sources |
| 3 | API | Zhipu API | Domestic + Overseas |
| 4 | API | Brave Search API | English/Overseas |
| 5 | Crawler | Direct Website | Structured data |

#### Configuration Steps

**1. Copy configuration file**
```bash
cd skills/web-search
cp .env.example .env
```

**2. Edit .env file**
```bash
# API Keys (need to apply separately)
ZHIPU_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here

# Timeout configuration
SEARCH_TIMEOUT=300
CRAWL_TIMEOUT=30
PROGRESS_INTERVAL=60

# Search configuration
MAX_RESULTS_PER_AGENT=5
DEEP_CRAWL_ENABLED=true
MAX_PAGES_PER_AGENT=3
```

**3. Install dependencies**
```bash
pip install playwright python-dotenv aiohttp
playwright install chromium firefox
```

#### Usage

Call in sub-agent:
```python
from search import search

result = await search(
    query="search keyword",
    max_results=5,
    deep_crawl=True
)
```

#### Output

Search results are automatically saved to `search_results.json`, including:
- Complete search results (title, link, summary, content)
- Results from each agent
- De-duplicated summary report

#### ⚠️ Security Notes

- **Do not commit `.env` file** - Already added to `.gitignore`
- **Rotate Token regularly** - Recommended every 90 days
- **Minimal permissions** - Only grant necessary API permissions

---

## 📝 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
