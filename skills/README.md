# Skills - AI 技能集合

<div align="center">

**AI Skills Collection**

[中文](#-中文) | [English](#-english)

</div>

---

## 🌏 中文

### 简介

本目录包含 OpenClaw AI 助手的各种技能，每个技能都是独立的功能模块。

### 📁 当前技能

| 技能 | 描述 | 状态 |
|------|------|------|
| **[web-search](web-search/)** | 五子并行搜索技能 | ✅ 已完成 |

### 🔧 web-search 技能

五子 agent 并行搜索机制，覆盖中文、英文、官方源和结构化数据。

#### 五子架构

| 序号 | 类型 | 搜索方式 | 覆盖范围 |
|------|------|----------|----------|
| 1 | 浏览器 | 百度搜索 | 中文信息 |
| 2 | 浏览器 | Bing 中国搜索 | 海外/官方源 |
| 3 | API | 智谱 API | 国内 + 海外 |
| 4 | API | Brave API | 英文/海外 |
| 5 | 抓取 | 定向网站 | 结构化数据 |

#### 快速开始

**1. 安装依赖**
```bash
cd web-search
pip install aiohttp playwright python-dotenv
playwright install chromium firefox
```

**2. 配置环境变量**
```bash
cp .env.example .env
nano .env
```

**3. 填写 API Keys**
```bash
# 智谱 API Key（申请地址：https://open.bigmodel.cn）
ZHIPU_API_KEY=your_key_here

# Brave API Key（申请地址：https://brave.com/search/api）
BRAVE_API_KEY=your_key_here
```

**4. 使用示例**
```python
import asyncio
from search import search

async def main():
    results = await search(
        query="vLLM DeepGEMM Qwen3.5 支持",
        max_results=5,
        deep_crawl=True
    )
    print(results['summary'])

asyncio.run(main())
```

#### 配置选项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SEARCH_TIMEOUT` | 300 | 搜索超时（秒） |
| `CRAWL_TIMEOUT` | 30 | 页面抓取超时（秒） |
| `PROGRESS_INTERVAL` | 60 | 进度汇报间隔（秒） |
| `MAX_RESULTS_PER_AGENT` | 5 | 每个 agent 最大结果数 |
| `DEEP_CRAWL_ENABLED` | true | 是否深入抓取页面 |
| `MAX_PAGES_PER_AGENT` | 3 | 每个 agent 抓取页面数 |

#### ⚠️ 安全注意事项

- **不要提交 `.env` 文件** - 已添加到 `.gitignore`
- **Token 定期更新** - 建议 90 天更换一次
- **权限最小化** - 只给必要的 API 权限

---

## 🌍 English

### Introduction

This directory contains various skills for OpenClaw AI Assistant. Each skill is an independent functional module.

### 📁 Current Skills

| Skill | Description | Status |
|-------|-------------|--------|
| **[web-search](web-search/)** | Five-agent parallel search skill | ✅ Completed |

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

#### Quick Start

**1. Install dependencies**
```bash
cd web-search
pip install aiohttp playwright python-dotenv
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

**4. Usage Example**
```python
import asyncio
from search import search

async def main():
    results = await search(
        query="vLLM DeepGEMM Qwen3.5 support",
        max_results=5,
        deep_crawl=True
    )
    print(results['summary'])

asyncio.run(main())
```

#### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `SEARCH_TIMEOUT` | 300 | Search timeout (seconds) |
| `CRAWL_TIMEOUT` | 30 | Page crawl timeout (seconds) |
| `PROGRESS_INTERVAL` | 60 | Progress report interval (seconds) |
| `MAX_RESULTS_PER_AGENT` | 5 | Max results per agent |
| `DEEP_CRAWL_ENABLED` | true | Enable deep page crawling |
| `MAX_PAGES_PER_AGENT` | 3 | Max pages to crawl per agent |

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
