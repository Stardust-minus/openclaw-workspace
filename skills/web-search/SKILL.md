# Web Search Skill - 三层智能搜索

覆盖中文、英文、官方源和结构化数据的三层搜索体系，按需逐层升级。

## 搜索流程

```
搜索请求
  │
  ▼
【第一层】轻量搜索（web_fetch）
  │ 搜狗 / DuckDuckGo / 百度
  │ 快速、无依赖
  │
  ├─ 成功 → 返回结果
  ├─ 验证码/空结果 → 降级
  │
  ▼
【第二层】浏览器搜索（browser tool）
  │ Bing / Google
  │ Chromium 145 headless
  │
  ├─ 成功 → snapshot/screenshot 读取结果
  ├─ 仍不够 → 升级
  │
  ▼
【第三层】深度搜索（Python 五子并行）
  │ 百度 + Bing + 智谱 API + Brave API + 定向抓取
  │ 并行执行，深度抓取页面内容，结果存 JSON
  │ 适合深度调研、大量结果需求
```

## 第一层：轻量搜索（web_fetch）

快速搜索，无依赖。web_fetch 已配置 Chrome UA。

### 引擎优先级

| 优先级 | 引擎 | URL 模板 | 适用场景 |
|--------|------|----------|----------|
| 1 | 搜狗 | `https://sogou.com/web?query={keyword}` | 中文首选，最稳 |
| 2 | DuckDuckGo | `https://duckduckgo.com/html/?q={keyword}` | 英文首选，最稳 |
| 3 | 百度 | `https://www.baidu.com/s?wd={keyword}` | 中文备用 |
| 4 | 360 | `https://www.so.com/s?q={keyword}` | 中文备用 |
| 5 | 头条 | `https://so.toutiao.com/search?keyword={keyword}` | 新闻资讯 |
| 6 | 微信 | `https://wx.sogou.com/weixin?type=2&query={keyword}` | 公众号文章 |

### 降级判断

web_fetch 结果出现以下内容时触发第二层：
- "Please solve the challenge" / "验证码" / "captcha"
- "unusual traffic" / "异常流量"
- 空内容（rawLength < 100）
- 搜索引擎登录/设置页面

### 示例

```javascript
// 搜狗搜索（中文首选）
web_fetch({"url": "https://sogou.com/web?query=搜索关键词"})

// DuckDuckGo（英文首选）
web_fetch({"url": "https://duckduckgo.com/html/?q=search+keywords"})
```

## 第二层：浏览器搜索（browser tool）

web_fetch 失败时的降级方案。Chromium 145 headless，SSRF 已放开。

### 引擎优先级

| 优先级 | 引擎 | URL 模板 | 说明 |
|--------|------|----------|------|
| 1 | Bing | `https://cn.bing.com/search?q={keyword}&ensearch=0` | 浏览器搜索首选，稳定 |
| 2 | Google | `https://www.google.com/search?q={keyword}` | 最后手段，headless 会触发验证码 |

### 示例

```javascript
// Bing 浏览器搜索
browser({"action": "open", "url": "https://cn.bing.com/search?q=关键词"})
browser({"action": "snapshot", "targetId": "t1"})

// 截图查看结果
browser({"action": "screenshot", "targetId": "t1"})
```

## 第三层：深度搜索（Python 五子并行）

需要大量结果或深度调研时使用。五个 agent 并行搜索，支持深度抓取页面内容。

### 五子架构

| 序号 | 类型 | 子 agent | 工具 | 覆盖范围 |
|------|------|----------|------|----------|
| 1 | 浏览器 | 百度搜索 | Playwright + Chromium | 中文信息 |
| 2 | 浏览器 | Bing 中国搜索 | Playwright + Firefox | 海外/官方源 |
| 3 | API | 智谱 API | search_pro 引擎 | 国内 + 海外 |
| 4 | API | Brave API | Brave Search | 英文/海外 |
| 5 | 抓取 | 定向网站 | Playwright 直接访问 | 结构化数据 |

### 依赖

- Playwright（已安装，Chromium 145 + Firefox）
- 智谱 API Key（已配置在 `.env`）
- Brave API Key（已配置在 `.env`）

### 配置 (.env)

```bash
ZHIPU_API_KEY=***
BRAVE_API_KEY=***
SEARCH_TIMEOUT=300
CRAWL_TIMEOUT=30
MAX_RESULTS_PER_AGENT=5
DEEP_CRAWL_ENABLED=true
MAX_PAGES_PER_AGENT=3
```

### 使用方法

```python
from search import search

# 深度搜索（抓取页面内容）
result = await search(
    query="Qwen3.5-397B FP8 性能",
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

搜索结果自动保存到 `search_results.json`，包含完整的搜索结果（标题、链接、摘要、内容）和去重汇总。

```python
import json

with open('search_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for agent_name, agent_data in data['agents'].items():
    for result in agent_data.get('results', []):
        print(f"标题：{result['title']}")
        print(f"链接：{result['url']}")
```

## 全部搜索引擎一览

### 国内引擎（8）

| 引擎 | URL 模板 | 层级 |
|------|----------|------|
| 搜狗 | `https://sogou.com/web?query={keyword}` | 第一层 |
| 百度 | `https://www.baidu.com/s?wd={keyword}` | 第一层 |
| 360 | `https://www.so.com/s?q={keyword}` | 第一层 |
| 头条 | `https://so.toutiao.com/search?keyword={keyword}` | 第一层 |
| 微信 | `https://wx.sogou.com/weixin?type=2&query={keyword}` | 第一层 |
| Bing CN | `https://cn.bing.com/search?q={keyword}&ensearch=0` | 第二层 |
| Bing INT | `https://cn.bing.com/search?q={keyword}&ensearch=1` | 第二层 |
| 集思录 | `https://www.jisilu.cn/explore/?keyword={keyword}` | 第一层 |

### 国际引擎（9）

| 引擎 | URL 模板 | 层级 |
|------|----------|------|
| DuckDuckGo | `https://duckduckgo.com/html/?q={keyword}` | 第一层 |
| Google | `https://www.google.com/search?q={keyword}` | 第二层 |
| Google HK | `https://www.google.com.hk/search?q={keyword}` | 第二层 |
| Yahoo | `https://search.yahoo.com/search?p={keyword}` | 第一层 |
| Startpage | `https://www.startpage.com/sp/search?query={keyword}` | 第一层 |
| Brave | `https://search.brave.com/search?q={keyword}` | 第一层 |
| Ecosia | `https://www.ecosia.org/search?q={keyword}` | 第一层 |
| Qwant | `https://www.qwant.com/?q={keyword}` | 第一层 |
| WolframAlpha | `https://www.wolframalpha.com/input?i={keyword}` | 第一层 |

## 高级搜索

### 运算符

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

1. **日常搜索** — 第一层搜狗/DuckDuckGo，覆盖 90% 场景
2. **验证码挡住** — 第二层浏览器 Bing
3. **深度调研** — 第三层五子并行，结果存 JSON
4. **抓页面内容** — web_fetch 或 Jina.ai 中转
5. **web_fetch UA** — 已配置 Chrome UA，减少验证码
6. **浏览器** — Chromium 145 已修复，SSRF 已放开
