---
name: "web-search"
description: "智能搜索技能：web_fetch 优先，遇到验证码自动降级到浏览器。支持搜狗、DuckDuckGo、Bing、百度等引擎。"
---

# Web Search Skill v3.0

智能搜索策略：web_fetch 优先，验证码失败自动上浏览器。

## 搜索策略

### 第一优先级：web_fetch（快速、轻量）

按以下优先级依次尝试：

| 优先级 | 引擎 | URL 模板 | 说明 |
|--------|------|----------|------|
| 1 | 搜狗 | `https://sogou.com/web?query={keyword}` | 中文搜索最稳，不易触发验证码 |
| 2 | DuckDuckGo | `https://duckduckgo.com/html/?q={keyword}` | 英文搜索最稳，支持 Bangs |
| 3 | 百度 | `https://www.baidu.com/s?wd={keyword}` | 中文覆盖广，偶尔空结果 |
| 4 | 360 | `https://www.so.com/s?q={keyword}` | 备用中文引擎 |
| 5 | 头条 | `https://so.toutiao.com/search?keyword={keyword}` | 备用中文引擎 |

### 第二优先级：浏览器搜索（web_fetch 失败时）

当 web_fetch 返回验证码页面或空结果时，使用 browser tool：

| 引擎 | URL 模板 | 说明 |
|------|----------|------|
| Bing | `https://cn.bing.com/search?q={keyword}&ensearch=0` | 浏览器搜索最可靠 |
| Google | `https://www.google.com/search?q={keyword}` | 会触发验证码，最后手段 |

### 降级判断

web_fetch 结果出现以下内容时触发降级：
- "Please solve the challenge" / "验证码" / "captcha"
- "unusual traffic" / "异常流量"
- 空内容（rawLength < 100）
- 搜索引擎登录/设置页面

## 使用方法

### 基本搜索（web_fetch）

```javascript
// 搜狗搜索（推荐首选）
web_fetch({"url": "https://sogou.com/web?query=搜索关键词"})

// DuckDuckGo（英文推荐）
web_fetch({"url": "https://duckduckgo.com/html/?q=search+keywords"})

// 百度搜索
web_fetch({"url": "https://www.baidu.com/s?wd=搜索关键词"})
```

### 浏览器搜索（降级方案）

```javascript
// Bing 浏览器搜索
browser({"action": "open", "url": "https://cn.bing.com/search?q=搜索关键词"})
browser({"action": "snapshot", "targetId": "t1"})

// 截图查看结果
browser({"action": "screenshot", "targetId": "t1"})
```

### 内容抓取

```javascript
// 抓取具体页面内容
web_fetch({"url": "https://example.com/article", "maxChars": 10000})

// Jina.ai 中转（绕过反爬）
web_fetch({"url": "https://r.jina.ai/https://example.com/article"})
```

## 搜索引擎选择指南

### 按语言选择
- **中文内容**：搜狗 > 百度 > 360 > 头条
- **英文内容**：DuckDuckGo > Bing（浏览器）> Google（浏览器）
- **技术内容**：DuckDuckGo > 搜狗 > Bing

### 按类型选择
- **新闻资讯**：搜狗 > 头条 > 百度
- **技术文档**：DuckDuckGo > Google
- **中文论坛/社区**：搜狗 > 百度
- **GitHub/开源项目**：DuckDuckGo > `site:github.com` 搜索

## 高级搜索技巧

### 搜索运算符

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

## 注意事项

- **web_fetch UA 已配置为 Chrome**，减少验证码触发
- **浏览器已修复**（Chromium 145 via Playwright），可正常使用
- **SSRF 策略已放开**，浏览器可访问外部网站
- **Google 浏览器搜索会触发验证码**，headless 指纹问题，最后手段
- **Bing 浏览器搜索稳定可用**，推荐作为浏览器搜索首选

## 变更日志

- v3.0 (2026-06-21): 重构为智能降级策略，web_fetch 优先 + 浏览器降级
- v2.0 (2026-02-06): Playwright 五子并行搜索（已弃用，依赖过重）
- v1.0: 初版浏览器搜索
