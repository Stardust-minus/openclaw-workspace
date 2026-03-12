#!/usr/bin/env python3
"""
ComfyUI 图像编辑工具
支持 HunyuanInstruct 和 Qwen Image 模型
"""

import requests
import time
import sys
import os

# 配置（从环境变量读取）
COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://localhost:8188")
DEFAULT_MODEL = os.environ.get("DEFAULT_MODEL", "HunyuanImage-3.0-Instruct")
DEFAULT_BOT_TASK = os.environ.get("DEFAULT_BOT_TASK", "image")

# 支持的模型列表
SUPPORTED_MODELS = {
    "hunyuan": {
        "name": "HunyuanImage-3.0-Instruct",
        "loader_node": "HunyuanInstructLoader",
        "edit_node": "HunyuanInstructImageEdit",
        "description": "腾讯混元图像编辑模型"
    },
    "qwen": {
        "name": "Qwen-Image-Edit",
        "loader_node": "QwenImageLoader",
        "edit_node": "QwenImageEdit",
        "description": "通义千问图像编辑模型"
    }
}


def upload_image(image_path: str) -> dict:
    """上传图片到 ComfyUI /input/ 目录"""
    print(f"上传图片：{image_path}")
    
    with open(image_path, "rb") as f:
        files = {"image": f}
        data = {"overwrite": "false", "type": "input"}
        response = requests.post(f"{COMFYUI_URL}/api/upload/image", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"上传成功：{result['name']}")
        return result
    else:
        print(f"上传失败：{response.text}")
        return None


def get_model_prompt(model_type: str, image_name: str, instruction: str, seed: int = 42) -> dict:
    """根据模型类型生成对应的 prompt"""
    
    if model_type == "qwen":
        # Qwen Image 编辑 prompt
        return {
            "prompt": {
                "10": {
                    "class_type": "LoadImage",
                    "inputs": {
                        "image": image_name
                    }
                },
                "8": {
                    "class_type": "QwenImageLoader",
                    "inputs": {
                        "model_name": "Qwen-Image-Edit",
                        "force_reload": False
                    }
                },
                "9": {
                    "class_type": "QwenImageEdit",
                    "inputs": {
                        "model": ["8", 0],
                        "image": ["10", 0],
                        "instruction": instruction,
                        "seed": seed
                    }
                },
                "17": {
                    "class_type": "PreviewImage",
                    "inputs": {
                        "images": ["9", 0]
                    }
                }
            },
            "client_id": "image-edit-skill"
        }
    else:
        # Hunyuan Image 编辑 prompt（默认）
        return {
            "prompt": {
                "10": {
                    "class_type": "LoadImage",
                    "inputs": {
                        "image": image_name
                    }
                },
                "8": {
                    "class_type": "HunyuanInstructLoader",
                    "inputs": {
                        "model_name": DEFAULT_MODEL,
                        "force_reload": False
                    }
                },
                "9": {
                    "class_type": "HunyuanInstructImageEdit",
                    "inputs": {
                        "model": ["8", 0],
                        "image": ["10", 0],
                        "instruction": instruction,
                        "bot_task": DEFAULT_BOT_TASK,
                        "seed": seed
                    }
                },
                "17": {
                    "class_type": "PreviewImage",
                    "inputs": {
                        "images": ["9", 0]
                    }
                }
            },
            "client_id": "image-edit-skill"
        }


def submit_prompt(image_name: str, instruction: str, model_type: str = "hunyuan", seed: int = 42) -> dict:
    """提交图像编辑任务"""
    print(f"提交编辑任务：{instruction} (模型：{model_type})")
    
    prompt = get_model_prompt(model_type, image_name, instruction, seed)
    
    response = requests.post(f"{COMFYUI_URL}/prompt", json=prompt)
    
    if response.status_code == 200:
        result = response.json()
        if "prompt_id" in result:
            print(f"任务提交成功：{result['prompt_id']}")
            return result
        else:
            print(f"提交失败：{result}")
            return None
    else:
        print(f"HTTP 错误：{response.status_code} - {response.text}")
        return None


def wait_for_result(prompt_id: str, timeout: int = 120) -> dict:
    """等待任务完成"""
    print(f"等待处理完成...（最多 {timeout} 秒）")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(5)
        
        response = requests.get(f"{COMFYUI_URL}/history/{prompt_id}")
        if response.status_code == 200:
            data = response.json()
            if prompt_id in data and data[prompt_id]:
                print("任务完成！")
                return data[prompt_id]
    
    print("超时")
    return None


def get_output_image(result: dict) -> dict:
    """获取输出图片信息"""
    outputs = result.get("outputs", {})
    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for img in node_output["images"]:
                return img
    return None


def download_image(image_info: dict, save_path: str) -> str:
    """下载编辑后的图片"""
    filename = image_info.get("filename", "")
    subfolder = image_info.get("subfolder", "")
    img_type = image_info.get("type", "temp")
    
    url = f"{COMFYUI_URL}/view?filename={filename}&subfolder={subfolder}&type={img_type}"
    print(f"下载图片：{url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"图片已保存：{save_path}")
        return save_path
    else:
        print(f"下载失败：{response.text}")
        return None


def edit_image(image_path: str, instruction: str, output_path: str = "/tmp/edited_image.png", 
               model_type: str = "hunyuan", seed: int = 42) -> dict:
    """
    完整的图像编辑流程
    
    Args:
        image_path: 输入图片路径
        instruction: 编辑指令
        output_path: 输出图片路径
        model_type: 模型类型 (hunyuan | qwen)
        seed: 随机种子
    
    Returns:
        {
            "success": bool,
            "output_path": str,
            "message": str
        }
    """
    print("=" * 60)
    print("ComfyUI 图像编辑")
    print("=" * 60)
    
    # 验证模型类型
    if model_type not in SUPPORTED_MODELS:
        available = ", ".join(SUPPORTED_MODELS.keys())
        return {"success": False, "message": f"不支持的模型类型：{model_type}。可用：{available}"}
    
    model_info = SUPPORTED_MODELS[model_type]
    print(f"使用模型：{model_info['name']} ({model_info['description']})")
    
    # 1. 上传图片
    upload_result = upload_image(image_path)
    if not upload_result:
        return {"success": False, "message": "图片上传失败"}
    
    image_name = upload_result["name"]
    
    # 2. 提交任务
    prompt_result = submit_prompt(image_name, instruction, model_type, seed)
    if not prompt_result:
        return {"success": False, "message": "任务提交失败"}
    
    prompt_id = prompt_result["prompt_id"]
    
    # 3. 等待完成
    history_result = wait_for_result(prompt_id)
    if not history_result:
        return {"success": False, "message": "任务超时或失败"}
    
    # 4. 获取输出图片
    output_image = get_output_image(history_result)
    if not output_image:
        return {"success": False, "message": "未找到输出图片"}
    
    # 5. 下载图片
    downloaded_path = download_image(output_image, output_path)
    if not downloaded_path:
        return {"success": False, "message": "图片下载失败"}
    
    print("=" * 60)
    print("图像编辑完成！")
    print("=" * 60)
    
    return {
        "success": True,
        "output_path": downloaded_path,
        "message": f"编辑完成：{instruction}"
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法：python edit.py <图片路径> <编辑指令> [输出路径] [模型类型]")
        print("示例：python edit.py input.jpg '把背景换成日落' output.png hunyuan")
        print(f"支持的模型：{', '.join(SUPPORTED_MODELS.keys())}")
        sys.exit(1)
    
    image_path = sys.argv[1]
    instruction = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "/tmp/edited_image.png"
    model_type = sys.argv[4] if len(sys.argv) > 4 else "hunyuan"
    
    result = edit_image(image_path, instruction, output_path, model_type)
    
    if result["success"]:
        print(f"\n{result['message']}")
        print(f"输出：{result['output_path']}")
        sys.exit(0)
    else:
        print(f"\n{result['message']}")
        sys.exit(1)
