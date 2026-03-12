# Web Search Skill - 五子并行搜索

## 概述

五子 agent 并行搜索机制，覆盖中文、英文、官方源和结构化数据。搜索结果自动保存到 JSON 文件，避免大数据量返回。

## 五子架构

| 序号 | 类型 | 子 agent | 工具 | 覆盖范围 |
|------|------|----------|------|----------|
| 1 | 浏览器 | 百度搜索 | Playwright + Chromium | 中文信息 |
| 2 | 浏览器 | Bing 中国搜索 | Playwright + Firefox | 海外/官方源 |
| 3 | API | 智谱 API | search_pro 引擎 | 国内 + 海外 |
| 4 | API | Brave API | Brave Search | 英文/海外 |
| 5 | 抓取 | 定向网站 | Playwright 直接访问 | 结构化数据 |

## 配置 (.env)

```bash
# API Keys
ZHIPU_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here

# 超时配置
SEARCH_TIMEOUT=300        # 搜索超时（秒）
CRAWL_TIMEOUT=30          # 页面抓取超时（秒）
PROGRESS_INTERVAL=60      # 进度汇报间隔（秒），0=禁用

# 搜索配置
MAX_RESULTS_PER_AGENT=5   # 每个 agent 返回的最大结果数
DEEP_CRAWL_ENABLED=true   # 是否启用深度抓取
MAX_PAGES_PER_AGENT=3     # 每个 agent 最多抓取页面数
ENABLE_PROGRESS_PUSH=false # 是否启用进度推送
```

## 使用方法

### 在子 agent 中使用

```python
from search import search

# 执行搜索
result = await search(
    query="搜索关键词",
    max_results=5,
    deep_crawl=True
)

# result 包含：
# - status: "success"
# - file: 结果文件路径
# - query: 搜索关键词
# - agents_completed: 完成的 agent 数
# - total_results: 总结果数
# - elapsed_seconds: 耗时
```

### 结果文件

搜索结果自动保存到 `search_results.json`，包含：
- 完整的搜索结果（标题、链接、摘要、内容）
- 每个 agent 的结果
- 去重后的汇总报告

### 读取结果文件

```python
import json

with open('search_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 访问结果
for agent_name, agent_data in data['agents'].items():
    for result in agent_data.get('results', []):
        print(f"标题：{result['title']}")
        print(f"链接：{result['url']}")
```

## 输出格式

### 子 agent 返回（简洁版）

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

### 结果文件（完整版）

```json
{
  "query": "搜索关键词",
  "agents": {
    "baidu": {
      "results": [
        {
          "title": "标题",
          "url": "链接",
          "summary": "摘要",
          "content": "详细内容（如果启用了深度抓取）"
        }
      ]
    },
    "bing": { ... },
    "zhipu": { ... },
    "brave": { ... },
    "direct": { ... }
  }
}
```

## 最佳实践

1. **搜索结果较大时** - 让子 agent 保存文件，只返回文件路径
2. **需要详细数据时** - 读取 JSON 文件，手动整理
3. **进度推送** - 默认关闭，需要时设置 `ENABLE_PROGRESS_PUSH=true`
4. **深度抓取** - 耗时较长，简单搜索可设置 `DEEP_CRAWL_ENABLED=false`

## 示例

```python
# 简单搜索（不抓取页面内容）
result = await search(
    query="明日方舟",
    max_results=5,
    deep_crawl=False
)

# 深度搜索（抓取页面内容）
result = await search(
    query="Qwen3.5-397B FP8 性能",
    max_results=5,
    deep_crawl=True
)
```
