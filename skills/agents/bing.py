#!/usr/bin/env python3
"""
Bing 搜索 Agent - Playwright + Firefox
"""

import asyncio
from typing import Dict, List, Any
from playwright.async_api import async_playwright


class BingSearch:
    """Bing 搜索 Agent"""
    
    def __init__(self):
        self.base_url = "https://cn.bing.com/search"
        self.timeout = 300
        self.headless = True
        
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        执行 Bing 搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索结果字典
        """
        results = []
        
        try:
            async with async_playwright() as p:
                browser = await p.firefox.launch(headless=self.headless)
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
                )
                page = await context.new_page()
                
                # 访问 Bing 搜索
                search_url = f"{self.base_url}?q={query}"
                await page.goto(search_url, timeout=self.timeout * 1000)
                
                # 等待搜索结果加载
                try:
                    await page.wait_for_selector('li.b_algo', timeout=10000)
                except:
                    await page.wait_for_timeout(3000)
                
                # 提取搜索结果
                js_code = """() => {
                    const results = [];
                    const maxResults = MAX_RESULTS_PLACEHOLDER;
                    const items = document.querySelectorAll('li.b_algo');
                    
                    items.forEach((item, index) => {
                        if (index >= maxResults) return;
                        
                        const titleEl = item.querySelector('h2 a, .b_title a');
                        const summaryEl = item.querySelector('.b_caption p, .b_snippet');
                        
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
                results = search_results[:max_results]
                await browser.close()
                
        except Exception as e:
            print(f"Bing 搜索失败：{e}")
            results = []
        
        return {
            'source': 'bing',
            'query': query,
            'results': results
        }
