#!/usr/bin/env python3
"""
页面抓取器 - 深入访问搜索结果页面
"""

import asyncio
import aiohttp
from typing import Optional


class PageCrawler:
    """页面抓取器"""
    
    def __init__(self):
        self.timeout = 30
        self.user_agent = (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
        
    async def fetch(self, url: str, timeout: int = None) -> str:
        """
        抓取页面内容
        
        Args:
            url: 页面 URL
            timeout: 超时时间（秒）
            
        Returns:
            页面文本内容
        """
        timeout = timeout or self.timeout
        
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout),
                    allow_redirects=True
                ) as resp:
                    html = await resp.text()
                    return self._extract_text(html)
        except Exception as e:
            raise Exception(f"抓取失败：{e}")
    
    def _extract_text(self, html: str) -> str:
        """从 HTML 提取正文内容"""
        # 简化版本：移除 HTML 标签
        import re
        text = re.sub(r'<[^>]+>', '', html)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()[:5000]  # 限制长度
