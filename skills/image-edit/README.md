# Image Edit Skill - ComfyUI 图像编辑

<div align="center">

**AI-Powered Image Editing with ComfyUI**

> ⚠ **WIP (Work In Progress)** - Qwen 模型支持尚未测试

[中文](#-中文) | [English](#-english)

</div>

---

## 中文

### 简介

使用 ComfyUI 进行 AI 图像编辑，支持多种模型：
- **HunyuanInstruct** - 腾讯混元图像编辑模型
- **Qwen Image** - 通义千问图像编辑模型

### 功能特性

- ✅ 文本指令驱动编辑
- ✅ 支持多种 AI 模型
- ✅ 自动上传/下载图片
- ✅ 任务状态监控
- ✅ 可配置 ComfyUI 实例

### 安装

**1. 克隆仓库**
```bash
cd skills/image-edit
```

**2. 安装依赖**
```bash
pip install requests
```

**3. 配置环境变量**
```bash
cp .env.example .env
nano .env
```

**4. 填写配置**
```bash
# ComfyUI 实例地址
COMFYUI_URL=http://your-comfyui-server:8188

# 默认模型 (hunyuan | qwen)
DEFAULT_MODEL=HunyuanImage-3.0-Instruct

# 默认任务类型 (image | recaption | think_recaption)
DEFAULT_BOT_TASK=image
```

### 使用方法

**命令行使用：**
```bash
# 使用默认模型（Hunyuan）
python edit.py input.jpg "把背景换成日落" output.png

# 指定模型类型
python edit.py input.jpg "把电话变成红色" output.png qwen

# 简短指令
python edit.py input.jpg "换个背景"
```

**Python 调用：**
```python
from edit import edit_image

result = edit_image(
    image_path="input.jpg",
    instruction="把背景换成海滩",
    output_path="output.png",
    model_type="hunyuan",  # 或 "qwen"
    seed=42
)

if result["success"]:
    print(f"编辑完成：{result['output_path']}")
else:
    print(f"失败：{result['message']}")
```

### 支持的模型

| 模型 | 类型 | 说明 | 状态 |
|------|------|------|------|
| **hunyuan** | HunyuanImage-3.0-Instruct | 腾讯混元，支持复杂指令 | ✅ 已测试 |
| **qwen** | Qwen-Image-Edit | 通义千问，编辑精度高 | ⏳ WIP |

> **注意**：Qwen 模型支持尚未测试，目前推荐使用 Hunyuan 模型。

### 编辑指令示例

- "把背景换成日落"
- "把衣服颜色改成蓝色"
- "添加一副眼镜"
- "让表情更开心"
- "换成雪景"
- "添加彩虹"

### 配置选项

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `COMFYUI_URL` | `http://localhost:8188` | ComfyUI 实例地址 |
| `DEFAULT_MODEL` | `HunyuanImage-3.0-Instruct` | 默认模型名称 |
| `DEFAULT_BOT_TASK` | `image` | 任务类型 (image/recaption) |

### 注意事项

- **图片上传**：必须指定 `type=input`，否则 LoadImage 无法访问
- **处理时间**：约 30-60 秒，取决于模型和指令复杂度
- **ComfyUI 节点**：需要安装对应的模型节点（HunyuanInstructLoader 或 QwenImageLoader）
- **环境变量**：不要将 `.env` 文件提交到 Git

### 工作流程

```
1. 用户发送图片 + 编辑指令
        ↓
2. 上传图片到 ComfyUI /input/ 目录
        ↓
3. 构建 prompt（根据模型类型）
        ↓
4. 提交任务到 ComfyUI
        ↓
5. 轮询任务状态（最多 120 秒）
        ↓
6. 下载编辑后的图片
        ↓
7. 返回结果
```

### 故障排除

**问题：图片上传失败**
- 检查 ComfyUI 服务是否运行
- 确认 `COMFYUI_URL` 配置正确
- 验证图片路径是否存在

**问题：任务超时**
- 增加 `timeout` 参数（默认 120 秒）
- 检查 ComfyUI 服务器负载
- 简化编辑指令

**问题：模型加载失败**
- 确认 ComfyUI 已安装对应节点
- 检查模型名称是否正确
- 查看 ComfyUI 日志

---

## English

### Introduction

AI-powered image editing using ComfyUI, supporting multiple models:
- **HunyuanInstruct** - Tencent Hunyuan image editing model
- **Qwen Image** - Alibaba Qwen image editing model

### Features

- ✅ Text-driven editing
- ✅ Multiple AI models support
- ✅ Automatic image upload/download
- ✅ Task status monitoring
- ✅ Configurable ComfyUI instance

### Installation

**1. Clone repository**
```bash
cd skills/image-edit
```

**2. Install dependencies**
```bash
pip install requests
```

**3. Configure environment variables**
```bash
cp .env.example .env
nano .env
```

**4. Fill in configuration**
```bash
# ComfyUI instance URL
COMFYUI_URL=http://your-comfyui-server:8188

# Default model (hunyuan | qwen)
DEFAULT_MODEL=HunyuanImage-3.0-Instruct

# Default task type (image | recaption | think_recaption)
DEFAULT_BOT_TASK=image
```

### Usage

**Command line:**
```bash
# Use default model (Hunyuan)
python edit.py input.jpg "change background to sunset" output.png

# Specify model type
python edit.py input.jpg "make the phone red" output.png qwen

# Short instruction
python edit.py input.jpg "change background"
```

**Python API:**
```python
from edit import edit_image

result = edit_image(
    image_path="input.jpg",
    instruction="change background to beach",
    output_path="output.png",
    model_type="hunyuan",  # or "qwen"
    seed=42
)

if result["success"]:
    print(f"Editing complete: {result['output_path']}")
else:
    print(f"Failed: {result['message']}")
```

### Supported Models

| Model | Type | Description |
|-------|------|-------------|
| **hunyuan** | HunyuanImage-3.0-Instruct | Tencent Hunyuan, supports complex instructions |
| **qwen** | Qwen-Image-Edit | Alibaba Qwen, high editing precision |

### Example Instructions

- "change background to sunset"
- "make the shirt blue"
- "add glasses"
- "make the expression happier"
- "change to snowy scene"
- "add a rainbow"

### Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `COMFYUI_URL` | `http://localhost:8188` | ComfyUI instance URL |
| `DEFAULT_MODEL` | `HunyuanImage-3.0-Instruct` | Default model name |
| `DEFAULT_BOT_TASK` | `image` | Task type (image/recaption) |

### Notes

- **Image Upload**: Must specify `type=input`, otherwise LoadImage cannot access
- **Processing Time**: ~30-60 seconds, depends on model and instruction complexity
- **ComfyUI Nodes**: Requires corresponding model nodes (HunyuanInstructLoader or QwenImageLoader)
- **Environment Variables**: Do not commit `.env` file to Git

### Workflow

```
1. User sends image + editing instruction
        ↓
2. Upload image to ComfyUI /input/ directory
        ↓
3. Build prompt (based on model type)
        ↓
4. Submit task to ComfyUI
        ↓
5. Poll task status (max 120 seconds)
        ↓
6. Download edited image
        ↓
7. Return result
```

### Troubleshooting

**Issue: Image upload failed**
- Check if ComfyUI service is running
- Verify `COMFYUI_URL` configuration
- Confirm image path exists

**Issue: Task timeout**
- Increase `timeout` parameter (default 120 seconds)
- Check ComfyUI server load
- Simplify editing instruction

**Issue: Model loading failed**
- Confirm ComfyUI has corresponding nodes installed
- Check model name is correct
- Review ComfyUI logs

---

## 许可证 / License

MIT License

---

<div align="center">

_最后更新 / Last Updated: 2026-03-12_

**OpenClaw AI Assistant** | [OpenClaw](https://openclaw.ai)

</div>
