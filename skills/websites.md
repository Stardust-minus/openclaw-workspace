# 定向访问网站知识库

> 根据搜索内容智能匹配相关网站
> 格式：`| 网站名 | 关键词 (逗号分隔) | URL 模板 | 说明 |`

---

## 游戏/二次元

| 网站 | 关键词 | URL 模板 | 说明 |
|------|--------|---------|------|
| PRTS Wiki | 明日方舟，arknights, 舟游，ark | `https://prts.wiki/w/{query}` | 明日方舟中文 Wiki |
| 萌娘百科 | 萌百，二次元，游戏，动漫，角色，舰娘，原神，崩坏，明日 | `https://zh.moegirl.org.cn/{query}` | 二次元百科 |
| BWIKI | 游戏，攻略，手游 | `https://wiki.biligame.com/{query}` | B 站游戏 Wiki |
| 官方官网 | 官网，official | `https://ak.hypergryph.com/` | 鹰角网络官网 |
| NGA | 论坛，攻略，玩家 | `https://bbs.nga.cn/thread.php?stid={query}` | 玩家社区 |

---

## AI/技术

| 网站 | 关键词 | URL 模板 | 说明 |
|------|--------|---------|------|
| GitHub | 代码，开源，项目，repo, 库，源码 | `https://github.com/search?q={query}` | 代码托管平台 |
| HuggingFace | 模型，AI, ML, transformer, diffusers, LLM | `https://huggingface.co/{query}` | AI 模型平台 |
| vLLM 文档 | vllm, 推理，部署，PagedAttention | `https://docs.vllm.ai/en/latest/search.html?q={query}` | vLLM 官方文档 |
| Papers With Code | 论文，SOTA, benchmark, 论文代码 | `https://paperswithcode.com/search?q={query}` | 论文 + 代码 |
| PyPI | python, pip, 包，库，package | `https://pypi.org/search/?q={query}` | Python 包索引 |
| StackOverflow | 报错，exception, error, how to | `https://stackoverflow.com/search?q={query}` | 技术问答 |
| 知乎 | 教程，详解，入门，是什么 | `https://www.zhihu.com/search?q={query}` | 中文技术社区 |

---

## 通用

| 网站 | 关键词 | URL 模板 | 说明 |
|------|--------|---------|------|
| Wikipedia | 百科，历史，人物，国家，城市 | `https://en.wikipedia.org/wiki/{query}` | 维基百科 |
| 百度百科 | 百科，中文，人物，事件 | `https://baike.baidu.com/item/{query}` | 中文百科 |
| Google | 通用搜索 | `https://www.google.com/search?q={query}` | 搜索引擎 |
| Bing | 通用搜索 | `https://cn.bing.com/search?q={query}` | 必应搜索 |
| Reddit | 讨论，community, subreddit | `https://www.reddit.com/search/?q={query}` | 社区讨论 |
| Twitter/X | 新闻，官方，announcement | `https://twitter.com/search?q={query}` | 社交媒体 |

---

## 新闻/媒体

| 网站 | 关键词 | URL 模板 | 说明 |
|------|--------|---------|------|
| IT 之家 | 科技，数码，手机，电脑 | `https://www.ithome.com/search/{query}` | 科技媒体 |
| 36 氪 | 创业，投资，科技 | `https://36kr.com/search/{query}` | 科技媒体 |
| 腾讯新闻 | 新闻，热点 | `https://news.qq.com/search?query={query}` | 新闻媒体 |

---

## 使用说明

### 1. 自动匹配

```python
from agents.direct import DirectCrawl

agent = DirectCrawl()
results = await agent.search("明日方舟")
# 自动选择：PRTS Wiki + 萌娘百科 + BWIKI
```

### 2. 添加新网站

在对应分类下添加一行：

```markdown
| 网站名 | 关键词 1，关键词 2 | URL 模板 | 说明 |
```

### 3. 关键词匹配规则

- 不区分大小写
- 逗号分隔多个关键词
- 匹配任意一个关键词即可
- 按顺序返回前 5 个匹配网站

---

## 更新日志

- 2026-03-11: 初始版本，基于搜索结果整理
