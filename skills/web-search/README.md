# Web Search Skill - 五子并行搜索

<div align="center">

**Five-Agent Parallel Search Mechanism**

[中文](#-中文) | [English](#-english)

</div>

---

## 中文

### 简介

五子 agent 并行搜索机制，覆盖中文、英文、官方源和结构化数据。搜索结果自动保存到 JSON 文件，避免大数据量返回被截断。

### 五子架构

| 序号 | 类型 | 搜索方式 | 工具 | 覆盖范围 |
|------|------|----------|------|----------|
| 1 | 浏览器 | 百度搜索 | Playwright + Chromium | 中文信息 |
| 2 | 浏览器 | Bing 中国搜索 | Playwright + Firefox | 海外/官方源 |
| 3 | API | 智谱 API | search_pro 引擎 | 国内 + 海外 |
| 4 | API | Brave API | Brave Search | 英文/海外 |
| 5 | 抓取 | 定向网站 | Playwright 直接访问 | 结构化数据 |

### 安装

**1. 安装依赖**
```bash
cd skills/web-search
pip install playwright python-dotenv aiohttp
playwright install chromium firefox
```

**2. 配置环境变量**
```bash
cp .env.example .env
```

**3. 填写 API Keys**

编辑 `.env` 文件，填入真实的 API Keys：
```bash
# 智谱 API Key（申请地址：https://open.bigmodel.cn）
ZHIPU_API_KEY=your_key_here

# Brave API Key（申请地址：https://brave.com/search/api）
BRAVE_API_KEY=your_key_here
```

### 使用方法

**在子 agent 中调用：**
```python
from search import search

result = await search(
    query="搜索关键词",
    max_results=5,
    deep_crawl=True
)
```

**输出格式：**
```json
{
  "status": "success",
  "file": "/path/to/search_results.json",
  "query": "搜索关键词",
  "agents_completed": 5,
  "total_results": 19,
  "elapsed_seconds": 35.09
}
```

### 配置选项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SEARCH_TIMEOUT` | 300 | 搜索超时（秒） |
| `CRAWL_TIMEOUT` | 30 | 页面抓取超时（秒） |
| `PROGRESS_INTERVAL` | 60 | 进度汇报间隔（秒） |
| `MAX_RESULTS_PER_AGENT` | 5 | 每个 agent 最大结果数 |
| `DEEP_CRAWL_ENABLED` | true | 是否深入抓取页面 |
| `MAX_PAGES_PER_AGENT` | 3 | 每个 agent 抓取页面数 |

### 目录结构

```
web-search/
├── search.py           # 主入口
├── crawler.py          # 页面抓取器
├── summarizer.py       # 结果摘要
├── agents/             # 5 个搜索 agent
│   ├── baidu.py       # 百度搜索
│   ├── bing.py        # Bing 搜索
│   ├── zhipu.py       # 智谱 API
│   ├── brave.py       # Brave API
│   └── direct.py      # 定向抓取
├── websites.md         # 定向网站配置
├── .env.example        # 环境变量模板
└── .gitignore          # Git 忽略
```

---

## English

### Introduction

Five-agent parallel search mechanism, covering Chinese, English, official sources, and structured data. Search results are automatically saved to JSON files to avoid truncation.

### Five-Agent Architecture

| # | Type | Search Method | Tool | Coverage |
|---|------|---------------|------|----------|
| 1 | Browser | Baidu Search | Playwright + Chromium | Chinese content |
| 2 | Browser | Bing China Search | Playwright + Firefox | Overseas/Official sources |
| 3 | API | Zhipu API | search_pro engine | Domestic + Overseas |
| 4 | API | Brave API | Brave Search | English/Overseas |
| 5 | Crawler | Direct Website | Playwright direct access | Structured data |

### Installation

**1. Install dependencies**
```bash
cd skills/web-search
pip install playwright python-dotenv aiohttp
playwright install chromium firefox
```

**2. Configure environment variables**
```bash
cp .env.example .env
nano .env
```

**3. Fill in API Keys**
```bash
# Zhipu API Key (Apply at: https://open.bigmodel.cn)
ZHIPU_API_KEY=your_key_here

# Brave API Key (Apply at: https://brave.com/search/api)
BRAVE_API_KEY=your_key_here
```

### Usage

**Call in sub-agent:**
```python
from search import search

result = await search(
    query="search keyword",
    max_results=5,
    deep_crawl=True
)
```

**Output format:**
```json
{
  "status": "success",
  "file": "/path/to/search_results.json",
  "query": "search keyword",
  "agents_completed": 5,
  "total_results": 19,
  "elapsed_seconds": 35.09
}
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `SEARCH_TIMEOUT` | 300 | Search timeout (seconds) |
| `CRAWL_TIMEOUT` | 30 | Page crawl timeout (seconds) |
| `PROGRESS_INTERVAL` | 60 | Progress report interval (seconds) |
| `MAX_RESULTS_PER_AGENT` | 5 | Max results per agent |
| `DEEP_CRAWL_ENABLED` | true | Enable deep page crawling |
| `MAX_PAGES_PER_AGENT` | 3 | Max pages to crawl per agent |

### Directory Structure

```
web-search/
├── search.py           # Main entry
├── crawler.py          # Page crawler
├── summarizer.py       # Result summarizer
├── agents/             # 5 search agents
│   ├── baidu.py       # Baidu Search
│   ├── bing.py        # Bing Search
│   ├── zhipu.py       # Zhipu API
│   ├── brave.py       # Brave API
│   └── direct.py      # Direct Crawler
├── websites.md         # Website configuration
├── .env.example        # Environment template
└── .gitignore          # Git ignore
```

---

## 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
