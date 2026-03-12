/**
 * 图片视觉分析工具
 * 调用 Qwen3.5-397B 多模态 API 分析图片内容
 */

import * as fs from "node:fs";
import path from "node:path";

// 模型配置（从环境变量读取，必须配置）
const API_URL = process.env.VISION_API_URL;
const API_KEY = process.env.VISION_API_KEY;
const MODEL = process.env.VISION_MODEL || "Qwen/Qwen3.5-397B-A17B-FP8";

// 检查必要的环境变量
if (!API_URL || !API_KEY) {
  throw new Error("VISION_API_URL and VISION_API_KEY environment variables are required");
}

/**
 * 将图片文件转为 base64
 */
function imageToBase64(imagePath: string): string {
  const imageBuffer = fs.readFileSync(imagePath);
  return imageBuffer.toString("base64");
}

/**
 * 分析图片内容
 * @param imagePath 图片本地路径
 * @param prompt 分析提示词
 * @returns 分析结果文本
 */
export async function analyzeImageWithVision(
  imagePath: string,
  prompt: string = `请详细分析这张图片，按以下结构描述：

【整体印象】图片类型（插画/照片/表情包等）、艺术风格、整体色调和氛围

【主体内容】
- 人物/角色：数量、性别、年龄特征、发型发色、面部表情、服装细节、配饰、动作姿态
- 物体/场景：主要物体、背景环境、空间布局

【细节描述】
- 颜色：主色调、配色方案、色彩对比
- 光影：光源方向、明暗对比、阴影处理
- 文字：任何可见的文字内容（完整转录）
- 装饰：花纹、图案、特殊元素

【情感表达】画面传达的情绪、角色情感状态、整体氛围

【特殊元素】任何独特的、引人注目的细节

请尽可能详细，不要遗漏任何可见元素。`
): Promise<string | null> {
  try {
    // 检查文件是否存在
    if (!fs.existsSync(imagePath)) {
      console.error(`[vision] 图片文件不存在：${imagePath}`);
      return null;
    }

    // 读取图片转 base64
    const base64Image = imageToBase64(imagePath);
    
    // 检测图片格式
    let mimeType = "image/jpeg";
    if (imagePath.toLowerCase().endsWith(".png")) {
      mimeType = "image/png";
    } else if (imagePath.toLowerCase().endsWith(".webp")) {
      mimeType = "image/webp";
    }
    
    // 构建请求
    const payload = {
      model: MODEL,
      messages: [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: prompt
            },
            {
              type: "image_url",
              image_url: {
                url: `data:${mimeType};base64,${base64Image}`
              }
            }
          ]
        }
      ],
      max_tokens: 4096,
      temperature: 0.6,
      top_p: 0.95
    };

    // 发送 HTTP 请求
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (response.status === 200) {
      const result = await response.json();
      const content = result.choices?.[0]?.message?.content;
      if (content) {
        console.log(`[vision] 图片分析成功：${imagePath}`);
        return content;
      } else {
        console.error(`[vision] API 返回空结果：${imagePath}`);
        return null;
      }
    } else {
      const errorText = await response.text();
      console.error(`[vision] API 调用失败 (${response.status}): ${errorText}`);
      return null;
    }
  } catch (error) {
    console.error(`[vision] 分析出错：${error}`);
    return null;
  }
}

/**
 * 生成图片分析的简短描述（用于消息注入）
 */
export function formatVisionResult(result: string | null, imagePath: string): string {
  if (!result) {
    return `[图片分析失败：${path.basename(imagePath)}]`;
  }
  
  // 截取前 200 字作为简短描述
  const shortDesc = result.length > 200 ? result.slice(0, 200) + "..." : result;
  return `[图片内容] ${shortDesc}`;
}
