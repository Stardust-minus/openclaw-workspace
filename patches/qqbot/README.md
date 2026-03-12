# QQ Bot 图片视觉分析补丁

本文件夹包含 QQ Bot 插件的图片视觉分析功能修改文件。

## 文件说明

| 文件 | 说明 | 使用方式 |
|------|------|----------|
| **vision-analyze.ts** | 图片视觉分析工具（完整源码） | 复制到 `src/utils/` |
| **gateway.ts** | QQ Bot 网关修改（完整源码） | 复制到 `src/` |
| **.env.example** | 环境变量配置模板 | 复制为 `.env` |
| **.gitignore** | Git 忽略配置 | 自动忽略敏感文件 |

---

## 功能特性

- 📸 **图片自动分析** - 调用 Qwen3.5-397B 多模态 API
- 💬 **结果注入** - 分析结果自动注入到 AI 上下文
- 🏷️ **标签支持** - 支持 `<qqimg>` 标签格式
- 🔒 **安全配置** - 环境变量存储敏感信息

---

## 使用方法

### 方案一：直接覆盖（快速）

```bash
cd /path/to/openclaw-qqbot

# 复制文件
cp patches/qqbot/vision-analyze.ts src/utils/
cp patches/qqbot/gateway.ts src/

# 重启 QQ Bot 插件
openclaw gateway restart
```

### 方案二：Git 集成（推荐，永久）

```bash
cd /path/to/openclaw-qqbot

# 复制文件
cp patches/qqbot/vision-analyze.ts src/utils/
cp patches/qqbot/gateway.ts src/

# 提交到 openclaw-qqbot 仓库
git add src/utils/vision-analyze.ts src/gateway.ts
git commit -m "feat: add image vision analysis"
git push
```

---

## 配置环境变量

**创建 `.env` 文件：**

```bash
cp patches/qqbot/.env.example .env
```

**填写真实值：**

```bash
# vLLM API 端点
VISION_API_URL=http://your-vllm-endpoint:19000/v1/chat/completions

# API 密钥
VISION_API_KEY=sk-your-api-key

# 模型名称
VISION_MODEL=Qwen/Qwen3.5-397B-A17B-FP8
```

**推荐存储位置：**
- `~/.openclaw/openclaw.json` 的 `env` 字段
- 或 `.env` 文件（加入 `.gitignore`）

---

## 功能流程

```
用户发送图片
    ↓
QQ Bot 下载图片
    ↓
调用 vision-analyze.ts
    ↓
Qwen3.5 多模态 API 分析
    ↓
返回图片描述文本
    ↓
注入到 agentBody
    ↓
AI 看到图片描述
```

---

## 依赖项

- Node.js >= 18
- Qwen3.5-397B 多模态模型
- openclaw-qqbot >= 1.5.7

---

## 安全说明

⚠️ **重要：**
- 不要将包含敏感信息的文件提交到 Git
- 使用环境变量或 `openclaw.json` 存储 API Key
- `vision-analyze.ts` 和 `gateway.ts` 不包含硬编码的敏感信息

---

_最后更新：2026-03-13_
