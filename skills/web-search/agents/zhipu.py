#!/usr/bin/env python3
"""
智谱 AI 搜索 Agent - web_search API
"""

import asyncio
import json
import aiohttp
from typing import Dict, List, Any


class ZhipuSearch:
    """智谱 AI 搜索 Agent"""
    
    def __init__(self, api_key: str = None, search_engine: str = 'search_pro'):
        self.api_key = api_key or ''
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/web_search"
        self.search_engine = search_engine
        self.timeout = 60
        
    async def search(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        执行智谱搜索
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索结果字典
        """
        if not self.api_key:
            return {'source': 'zhipu', 'error': 'API Key 未配置', 'results': []}
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'search_query': query,
            'search_engine': self.search_engine,
            'search_intent': False,
            'count': max_results
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
                        'source': 'zhipu',
                        'query': query,
                        'results': self._parse_results(result.get('search_result', []))
                    }
        except Exception as e:
            return {'source': 'zhipu', 'error': str(e), 'results': []}
    
    def _parse_results(self, results: List[Dict]) -> List[Dict]:
        """解析搜索结果"""
        parsed = []
        for item in results:
            parsed.append({
                'title': item.get('title', ''),
                'url': item.get('link', ''),
                'summary': item.get('content', ''),
                'media': item.get('media', ''),
                'publish_date': item.get('publish_date', '')
            })
        return parsed
