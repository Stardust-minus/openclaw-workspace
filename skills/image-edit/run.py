#!/usr/bin/env python3
"""
Image Edit Skill - OpenClaw 入口
当用户请求图像编辑时调用
"""

import sys
import os
import json

# 添加 skill 目录到路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

from edit import edit_image


def main():
    """OpenClaw 调用入口"""
    if len(sys.argv) < 3:
        print(json.dumps({
            "success": False,
            "error": "用法：image-edit <图片路径> <编辑指令>"
        }))
        sys.exit(1)
    
    image_path = sys.argv[1]
    instruction = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else "/tmp/edited_image.png"
    
    # 检查图片是否存在
    if not os.path.exists(image_path):
        print(json.dumps({
            "success": False,
            "error": f"图片不存在：{image_path}"
        }))
        sys.exit(1)
    
    # 执行编辑
    result = edit_image(image_path, instruction, output_path)
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False))
    
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
