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

## 轻量搜索（web_fetch 直抓）

当 Playwright 不可用或不需要深度搜索时，可直接用 web_fetch 抓取搜索引擎结果页。

### 搜索引擎 URL 列表

#### 国内引擎（8）

| 引擎 | URL 模板 | 说明 |
|------|----------|------|
| 百度 | `https://www.baidu.com/s?wd={keyword}` | 中文覆盖广，偶尔空结果 |
| Bing CN | `https://cn.bing.com/search?q={keyword}&ensearch=0` | 国内版 Bing |
| Bing INT | `https://cn.bing.com/search?q={keyword}&ensearch=1` | 国际版 Bing |
| 360 | `https://www.so.com/s?q={keyword}` | 备用中文引擎 |
| 搜狗 | `https://sogou.com/web?query={keyword}` | 中文最稳，不易触发验证码 |
| 微信 | `https://wx.sogou.com/weixin?type=2&query={keyword}` | 搜公众号文章 |
| 头条 | `https://so.toutiao.com/search?keyword={keyword}` | 备用中文引擎 |
| 集思录 | `https://www.jisilu.cn/explore/?keyword={keyword}` | 投资理财 |

#### 国际引擎（9）

| 引擎 | URL 模板 | 说明 |
|------|----------|------|
| Google | `https://www.google.com/search?q={keyword}` | JS challenge，web_fetch 抓不到 |
| Google HK | `https://www.google.com.hk/search?q={keyword}` | 同上 |
| DuckDuckGo | `https://duckduckgo.com/html/?q={keyword}` | 英文最稳，支持 Bangs |
| Yahoo | `https://search.yahoo.com/search?p={keyword}` | 备用英文引擎 |
| Startpage | `https://www.startpage.com/sp/search?query={keyword}` | Google 结果 + 隐私 |
| Brave | `https://search.brave.com/search?q={keyword}` | 独立索引 |
| Ecosia | `https://www.ecosia.org/search?q={keyword}` | 易触发验证码 |
| Qwant | `https://www.qwant.com/?q={keyword}` | 欧盟 GDPR |
| WolframAlpha | `https://www.wolframalpha.com/input?i={keyword}` | 知识计算 |

### 轻量搜索优先级

1. **搜狗**（中文首选，最稳）
2. **DuckDuckGo**（英文首选，最稳）
3. **百度**（中文备用）
4. **360 / 头条**（中文备用）
5. **Bing**（浏览器降级时首选）
6. **Google**（最后手段，headless 会触发验证码）

### 浏览器降级策略

当 web_fetch 返回以下内容时，自动降级到 browser tool：
- "Please solve the challenge" / "验证码" / "captcha"
- "unusual traffic" / "异常流量"
- 空内容（rawLength < 100）
- 搜索引擎登录/设置页面

```javascript
// 浏览器搜索 Bing（降级首选）
browser({"action": "open", "url": "https://cn.bing.com/search?q=关键词"})
browser({"action": "snapshot", "targetId": "t1"})

// 浏览器搜索 Google（最后手段）
browser({"action": "open", "url": "https://www.google.com/search?q=关键词"})
```

### 高级搜索运算符

| 运算符 | 示例 | 说明 |
|--------|------|------|
| `site:` | `site:github.com python` | 限定网站 |
| `filetype:` | `filetype:pdf report` | 限定文件类型 |
| `""` | `"machine learning"` | 精确匹配 |
| `-` | `python -snake` | 排除词 |
| `OR` | `cat OR dog` | 或逻辑 |

### 时间过滤（Google/Bing）

| 参数 | 说明 |
|------|------|
| `tbs=qdr:h` | 过去一小时 |
| `tbs=qdr:d` | 过去一天 |
| `tbs=qdr:w` | 过去一周 |
| `tbs=qdr:m` | 过去一个月 |
| `tbs=qdr:y` | 过去一年 |

### DuckDuckGo Bangs

| Bang | 目标 |
|------|------|
| `!g` | Google |
| `!gh` | GitHub |
| `!so` | Stack Overflow |
| `!w` | Wikipedia |
| `!yt` | YouTube |

### Jina.ai 内容中转

抓取具体页面内容时，如遇反爬可用 Jina.ai 中转：

```javascript
web_fetch({"url": "https://r.jina.ai/https://example.com/article"})
```

## 最佳实践

1. **搜索结果较大时** - 让子 agent 保存文件，只返回文件路径
2. **需要详细数据时** - 读取 JSON 文件，手动整理
3. **进度推送** - 默认关闭，需要时设置 `ENABLE_PROGRESS_PUSH=true`
4. **深度抓取** - 耗时较长，简单搜索可设置 `DEEP_CRAWL_ENABLED=false`
5. **轻量搜索** - 不需要 Playwright 时直接用 web_fetch，搜狗 + DuckDuckGo 最稳
6. **浏览器降级** - web_fetch 触发验证码时，用 browser tool 搜 Bing
7. **web_fetch UA** - 已配置为 Chrome UA，减少验证码触发

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
