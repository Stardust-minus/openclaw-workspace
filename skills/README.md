# Web Search Skill

五子并行搜索机制，覆盖中文、英文、官方源和结构化数据。

## 安装

```bash
cd ~/.openclaw/workspace/skills/web-search
pip install aiohttp playwright python-dotenv
playwright install chromium firefox
```

## 配置

### 1. 复制环境变量模板

```bash
cp .env.example .env
```

### 2. 编辑 `.env` 文件

```bash
nano .env
```

填入真实的 API Key：

```bash
ZHIPU_API_KEY=0f6c3367b642486ebdcf035329567882.cvOthvIrEkKQWr2q
BRAVE_API_KEY=BSAW76m6UwvKotXuOCQ1HuZESW5Jm4_
```

### 3. 可选配置

```bash
SEARCH_TIMEOUT=300          # 搜索超时（秒）
CRAWL_TIMEOUT=30            # 页面抓取超时（秒）
PROGRESS_INTERVAL=60        # 进度汇报间隔（秒）
MAX_RESULTS_PER_AGENT=5     # 每个 agent 最大结果数
DEEP_CRAWL_ENABLED=true     # 是否深入抓取页面
MAX_PAGES_PER_AGENT=3       # 每个 agent 抓取页面数
```

## 使用

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

## 架构

```
search.py (主入口)
    ├── agents/baidu.py (百度搜索 - 浏览器)
    ├── agents/bing.py (Bing 搜索 - 浏览器)
    ├── agents/zhipu.py (智谱 API)
    ├── agents/brave.py (Brave API)
    └── agents/direct.py (定向抓取)
    ├── crawler.py (页面抓取)
    └── summarizer.py (结果汇总)
```

## 超时配置

- 搜索超时：300 秒
- 进度提示：180 秒
- 汇报间隔：60 秒
