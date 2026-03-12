# OpenClaw Workspace

<div align="center">

**OpenClaw AI 助手专用工作空间**

[中文](#-中文) | [English](#-english)

</div>

---

## 目录结构 / Directory Structure

```
openclaw-workspace/
├── skills/                  # AI 技能目录 / AI Skills
│   ├── web-search/         # 五子并行搜索技能
│   ├── scc-tunnel/         # SCC 内网穿透技能
│   └── image-edit/         # ComfyUI 图像编辑（WIP）
├── docs/                    # 文档目录 / Documentation
│   └── personality/        # AI 人格配置文档
├── .gitignore              # Git 忽略配置
└── README.md               # 本文件
```

---

## 中文

### 简介

这是 OpenClaw AI 助手的工作空间仓库，用于存储 AI 技能、项目代码和自动化脚本。

### 可用技能

| 技能 | 描述 | 详细文档 | 状态 |
|------|------|----------|------|
| **[web-search](skills/web-search/)** | 五子并行搜索机制，覆盖中文、英文、官方源 | [查看文档](skills/web-search/README.md) | ✅ |
| **[scc-tunnel](skills/scc-tunnel/)** | SCC 内网穿透工具，HTTP/TCP 隧道 | [查看文档](skills/scc-tunnel/README.md) | ✅ |
| **[image-edit](skills/image-edit/)** | ComfyUI AI 图像编辑（Hunyuan/Qwen） | [查看文档](skills/image-edit/README.md) | ⏳ WIP |

> **WIP** = Work In Progress（进行中，Qwen 模型尚未测试）

### 文档

| 文档 | 说明 |
|------|------|
| **[人格配置](docs/personality/)** | AI 助手的角色设定和行为准则 |

### 技能说明

每个技能都是独立的模块，包含：
- 完整的中英双语文档
- 安装和配置说明
- 使用示例
- 安全注意事项

**使用流程：**
1. 克隆仓库
2. 进入技能目录
3. 按照 README 安装依赖
4. 配置环境变量（如需）
5. 开始使用

---

## English

### Introduction

This is the dedicated workspace repository for OpenClaw AI Assistant, used to store AI skills, project code, and automation scripts.

### Available Skills

| Skill | Description | Documentation | Status |
|-------|-------------|---------------|--------|
| **[web-search](skills/web-search/)** | Five-agent parallel search mechanism | [View Docs](skills/web-search/README.md) | ✅ |
| **[scc-tunnel](skills/scc-tunnel/)** | SCC tunnel tool to expose local services to public internet | [View Docs](skills/scc-tunnel/README.md) | ✅ |
| **[image-edit](skills/image-edit/)** | ComfyUI AI image editing (Hunyuan/Qwen) | [View Docs](skills/image-edit/README.md) | ⏳ WIP |

> **WIP** = Work In Progress (Qwen model not yet tested)

### Documentation

| Document | Description |
|----------|-------------|
| **[Personality](docs/personality/)** | AI assistant character settings and behavioral guidelines |

### Skill Structure

Each skill is an independent module containing:
- Complete bilingual documentation (Chinese/English)
- Installation and configuration instructions
- Usage examples
- Security notes

**Usage Flow:**
1. Clone repository
2. Enter skill directory
3. Install dependencies per README
4. Configure environment variables (if needed)
5. Start using

---

## 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
