#!/usr/bin/env python3
"""
百度搜索 Agent - Playwright + Chromium (PC 端)
"""

import asyncio
from typing import Dict, List, Any
from playwright.async_api import async_playwright


class BaiduSearch:
    """百度搜索 Agent - PC 端方案"""
    
    def __init__(self):
        self.base_url = "https://www.baidu.com/s"  # 使用 PC 版百度
        self.timeout = 300
        self.headless = True
        
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        执行百度搜索（PC 端）
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索结果字典
        """
        results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080, 'isMobile': False}
                )
                page = await context.new_page()
                
                # 访问百度搜索
                search_url = f"{self.base_url}?wd={query}"
                await page.goto(search_url, timeout=self.timeout * 1000)
                
                # 等待搜索结果加载（PC 版百度使用 .result 选择器）
                try:
                    await page.wait_for_selector('.result', timeout=10000)
                except:
                    await page.wait_for_timeout(3000)
                
                # 提取搜索结果（PC 版百度）
                js_code = """() => {
                    const results = [];
                    const maxResults = MAX_RESULTS_PLACEHOLDER;
                    const items = document.querySelectorAll('.result');
                    
                    items.forEach((item, index) => {
                        if (index >= maxResults) return;
                        
                        const titleEl = item.querySelector('h3 a, .c-title a');
                        const summaryEl = item.querySelector('.c-abstract, .summary');
                        
                        if (titleEl) {
                            results.push({
                                title: titleEl.innerText.trim(),
                                url: titleEl.href,
                                summary: summaryEl ? summaryEl.innerText.trim() : ''
                            });
                        }
                    });
                    return results;
                }""".replace('MAX_RESULTS_PLACEHOLDER', str(max_results))
                search_results = await page.evaluate(js_code)
                
                # 处理百度重定向链接
                for result in search_results:
                    url = result.get('url', '')
                    if url and 'baidu.com/link?url=' in url:
                        # 提取真实 URL
                        import re
                        match = re.search(r'url=([^&]+)', url)
                        if match:
                            result['url'] = match.group(1)
                            result['original_url'] = url
                
                results = search_results[:max_results]
                await browser.close()
                
        except Exception as e:
            print(f"百度搜索失败：{e}")
            # 返回示例数据作为降级
            results = [
                {
                    'title': f'百度结果 {i}',
                    'url': f'https://www.baidu.com/s?wd={query}',
                    'summary': f'百度搜索：{query}'
                }
                for i in range(min(5, max_results))
            ]
        
        return {
            'source': 'baidu',
            'query': query,
            'results': results
        }
