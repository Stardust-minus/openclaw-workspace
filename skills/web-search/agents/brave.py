#!/usr/bin/env python3
"""
Brave Search Agent - Brave Search API
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any


class BraveSearch:
    """Brave Search Agent"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or ''
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.timeout = 60
        
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        执行 Brave 搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索结果字典
        """
        if not self.api_key:
            return {'source': 'brave', 'error': 'API Key 未配置', 'results': []}
        
        headers = {
            'x-subscription-token': self.api_key,
            'content-type': 'application/json'
        }
        
        data = {
            'q': query,
            'count': min(max_results, 20)  # Brave 最大 20 条
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as resp:
                    result = await resp.json()
                    
                    return {
                        'source': 'brave',
                        'query': query,
                        'results': self._parse_results(result.get('web', {}).get('results', []))
                    }
        except Exception as e:
            return {'source': 'brave', 'error': str(e), 'results': []}
    
    def _parse_results(self, results: List[Dict]) -> List[Dict]:
        """解析搜索结果"""
        parsed = []
        for item in results:
            parsed.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'summary': item.get('description', ''),
                'age': item.get('age', '')
            })
        return parsed
