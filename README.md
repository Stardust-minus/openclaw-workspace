# OpenClaw Workspace

<div align="center">

**OpenClaw AI 助手专用工作空间**

[中文](#-中文) | [English](#-english)

</div>

---

## 📁 目录结构 / Directory Structure

```
openclaw-workspace/
├── skills/                  # AI 技能目录 / AI Skills
│   ├── web-search/         # 五子并行搜索技能
│   ├── scc-tunnel/         # SCC 内网穿透技能
│   ├── image-edit/         # ComfyUI 图像编辑技能
│   └── ...
├── .gitignore              # Git 忽略配置
└── README.md               # 本文件
```

---

## 🌏 中文

### 简介

这是 OpenClaw AI 助手的工作空间仓库，用于存储 AI 技能、项目代码和自动化脚本。

### 🔧 可用技能

| 技能 | 描述 | 详细文档 |
|------|------|----------|
| **[web-search](skills/web-search/)** | 五子并行搜索机制，覆盖中文、英文、官方源 | [查看文档](skills/web-search/README.md) |
| **[scc-tunnel](skills/scc-tunnel/)** | SCC 内网穿透工具，HTTP/TCP 隧道 | [查看文档](skills/scc-tunnel/README.md) |

> 更多技能正在添加中...

### 💡 技能说明

每个技能都是独立的模块，包含：
- ✅ 完整的中英双语文档
- ✅ 安装和配置说明
- ✅ 使用示例
- ✅ 安全注意事项

**使用流程：**
1. 克隆仓库
2. 进入技能目录
3. 按照 README 安装依赖
4. 配置环境变量（如需）
5. 开始使用

### 快速开始

**1. 克隆仓库**
```bash
git clone https://github.com/Stardust-minus/openclaw-workspace.git
cd openclaw-workspace
```

**2. 浏览技能**
```bash
ls skills/
```

**3. 使用技能**
每个技能都有独立的 README 文档，包含详细的配置和使用说明。

### ⚠️ 安全注意事项

- **不要提交 `.env` 文件** - 已添加到 `.gitignore`
- **Token 定期更新** - 建议 90 天更换一次
- **权限最小化** - 只给必要的 API 权限

---

## 🌍 English

### Introduction

This is the dedicated workspace repository for OpenClaw AI Assistant, used to store AI skills, project code, and automation scripts.

### 🔧 Available Skills

| Skill | Description | Documentation |
|-------|-------------|---------------|
| **[web-search](skills/web-search/)** | Five-agent parallel search mechanism | [View Docs](skills/web-search/README.md) |
| **[scc-tunnel](skills/scc-tunnel/)** | SCC tunnel tool to expose local services to public internet | [View Docs](skills/scc-tunnel/README.md) |
| **[image-edit](skills/image-edit/)** | ComfyUI Hunyuan image editing skill | [View Docs](skills/image-edit/README.md) |

### Quick Start

**1. Clone repository**
```bash
git clone https://github.com/Stardust-minus/openclaw-workspace.git
cd openclaw-workspace
```

**2. Browse skills**
```bash
ls skills/
```

**3. Use skills**
Each skill has its own README with detailed configuration and usage instructions.

### ⚠️ Security Notes

- **Do not commit `.env` files** - Already added to `.gitignore`
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
