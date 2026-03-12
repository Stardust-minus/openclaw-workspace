# image-edit Skill - ComfyUI 图像编辑

使用 ComfyUI + AI 模型进行图像编辑。

## 触发条件

当用户表达以下意图时触发：
- "编辑这张图片"
- "把图片里的 XXX 改成 XXX"
- "图像编辑"
- "改图"
- "P 图"
- "换个背景"
- "调整颜色"
- 其他图像编辑相关请求

## 使用方法

### 1. 用户发送图片 + 编辑指令

```
[图片] 把背景换成 sunset
[图片] 把电话从绿色变成红色
```

### 2. Skill 自动执行

1. 下载用户发送的图片
2. 上传到 ComfyUI `/input/` 目录
3. 调用 AI 图像编辑节点
4. 等待处理完成
5. 返回编辑后的图片

## 配置

在 `openclaw.json` 中添加：

```json
{
  "skills": {
    "image-edit": {
      "enabled": true,
      "comfyUI": "http://your-comfyui-server:8188",
      "defaultModel": "HunyuanImage-3.0-Instruct",
      "defaultBotTask": "image"
    }
  }
}
```

**环境变量配置：**
```bash
COMFYUI_URL=http://your-comfyui-server:8188
DEFAULT_MODEL=HunyuanImage-3.0-Instruct
DEFAULT_BOT_TASK=image
```

## 支持的模型

| 模型 | 说明 |
|------|------|
| **HunyuanInstruct** | 腾讯混元图像编辑模型 |
| **Qwen Image** | 通义千问图像编辑模型 |

## 实现

📁 `/home/firefly/.openclaw/workspace/skills/image-edit/edit.py`

## 注意事项

- 图片上传必须指定 `type=input`，否则 LoadImage 无法访问
- AI 图像编辑节点需要以下参数：
  - `model`: 模型加载器输出的模型
  - `image`: LoadImage 输出的图片
  - `instruction`: 编辑指令（中文或英文）
  - `bot_task`: "image"（直接编辑）或 "recaption" 或 "think_recaption"
- 处理时间约 30-60 秒，需要告知用户等待

## 依赖

- ComfyUI 实例（带 AI 图像编辑节点）
- requests 库
- Python 3.8+

---

_最后更新：2026-03-12_
