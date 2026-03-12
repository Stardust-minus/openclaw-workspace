# Skills - AI 技能集合

<div align="center">

**AI Skills Collection**

[中文](#-中文) | [English](#-english)

</div>

---

## 中文

### 简介

本目录包含 OpenClaw AI 助手的各种技能，每个技能都是独立的功能模块。

### 当前技能

| 技能 | 描述 | 详细文档 |
|------|------|----------|
| **[web-search](web-search/)** | 五子并行搜索机制，覆盖中文、英文、官方源 | [查看文档](web-search/README.md) |
| **[scc-tunnel](scc-tunnel/)** | SCC 内网穿透工具，HTTP/TCP 隧道 | [查看文档](scc-tunnel/README.md) |

> 更多技能正在添加中...

### 使用方式

每个技能都是独立的模块，包含完整的安装和使用说明。

**快速开始：**
```bash
# 1. 进入技能目录
cd skills/<skill-name>

# 2. 安装依赖
pip install -r requirements.txt  # 如果有

# 3. 配置环境变量
cp .env.example .env
nano .env

# 4. 使用技能
# 参考各技能的 README.md
```

### 安全注意事项

- **不要提交 `.env` 文件** - 已添加到 `.gitignore`
- **Token 定期更新** - 建议 90 天更换一次
- **权限最小化** - 只给必要的 API 权限

---

## English

### Introduction

This directory contains various skills for OpenClaw AI Assistant. Each skill is an independent functional module.

### Current Skills

| Skill | Description | Documentation |
|-------|-------------|---------------|
| **[web-search](web-search/)** | Five-agent parallel search mechanism | [View Docs](web-search/README.md) |
| **[scc-tunnel](scc-tunnel/)** | SCC tunnel tool for HTTP/TCP tunnels | [View Docs](scc-tunnel/README.md) |

> More skills coming soon...

### Usage

Each skill is an independent module with complete installation and usage instructions.

**Quick Start:**
```bash
# 1. Enter skill directory
cd skills/<skill-name>

# 2. Install dependencies
pip install -r requirements.txt  # if available

# 3. Configure environment variables
cp .env.example .env
nano .env

# 4. Use the skill
# Refer to each skill's README.md
```

### Security Notes

- **Do not commit `.env` files** - Already added to `.gitignore`
- **Rotate Token regularly** - Recommended every 90 days
- **Minimal permissions** - Only grant necessary API permissions

---

## 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
