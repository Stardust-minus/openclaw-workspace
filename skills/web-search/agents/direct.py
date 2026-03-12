#!/usr/bin/env python3
"""
定向网站抓取 Agent - 读取 websites.md 配置
"""

import re
from pathlib import Path
from typing import Dict, List, Any
from playwright.async_api import async_playwright


class DirectCrawl:
    """定向网站抓取 Agent"""
    
    def __init__(self, config_path: str = None):
        self.timeout = 300
        self.headless = True
        
        # 加载配置文件
        if config_path is None:
            config_path = Path(__file__).parent.parent / 'websites.md'
        self.websites = self._load_config(config_path)
    
    def _load_config(self, config_path: Path) -> List[Dict]:
        """加载 websites.md 配置"""
        websites = []
        current_category = ''
        
        if not config_path.exists():
            print(f"警告：配置文件不存在 {config_path}")
            return self._get_default_websites()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 Markdown 表格
        for line in content.split('\n'):
            # 检测分类标题
            if line.startswith('## '):
                current_category = line.replace('## ', '').strip()
                continue
            
            # 解析表格行（跳过表头）
            if line.startswith('|') and '网站' not in line and '---' not in line:
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 4:
                    # 支持中英文逗号分隔
                    keywords_str = parts[1]
                    # 使用 Unicode 编码替换全角逗号 (U+FF0C)
                    keywords_str = keywords_str.replace('\uFF0C', ',')
                    # 分割并清理
                    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]
                    websites.append({
                        'category': current_category,
                        'name': parts[0],
                        'keywords': keywords,
                        'url_template': parts[2].strip('`'),
                        'description': parts[3]
                    })
        
        return websites
    
    def _get_default_websites(self) -> List[Dict]:
        """默认网站配置"""
        return [
            {'name': 'GitHub', 'keywords': ['代码', 'github'], 'url_template': 'https://github.com/search?q={query}'},
            {'name': 'Wikipedia', 'keywords': ['百科', 'wiki'], 'url_template': 'https://en.wikipedia.org/wiki/{query}'},
        ]
    
    def select_websites(self, query: str) -> List[Dict]:
        """根据 query 智能选择网站"""
        query_lower = query.lower()
        matched = []
        
        for site in self.websites:
            # 关键词匹配
            for keyword in site['keywords']:
                if keyword.lower() in query_lower:
                    matched.append(site)
                    break
        
        # 返回匹配的网站（最多 5 个）
        return matched[:5]
    
    async def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        执行定向抓取
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
            
        Returns:
            搜索结果字典
        """
        # 1. 智能选择网站
        targets = self.select_websites(query)
        
        if not targets:
            return {
                'source': 'direct',
                'query': query,
                'message': '未找到相关网站，使用默认网站',
                'selected_sites': [],
                'results': []
            }
        
        # 2. 并行抓取
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            
            for site in targets:
                url = site['url_template'].format(query=query.replace(' ', '_'))
                try:
                    content = await self._fetch_page(p, browser, url, site['name'])
                    results.append({
                        'title': f"{site['name']}: {query}",
                        'url': url,
                        'summary': content[:500] + '...' if len(content) > 500 else content,
                        'category': site['category']
                    })
                except Exception as e:
                    results.append({
                        'title': f"抓取失败：{site['name']}",
                        'url': url,
                        'summary': str(e)
                    })
            
            await browser.close()
        
        return {
            'source': 'direct',
            'query': query,
            'selected_sites': [s['name'] for s in targets],
            'results': results[:max_results]
        }
    
    async def _fetch_page(self, playwright, browser, url: str, site_name: str = '') -> str:
        """抓取页面内容"""
        try:
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = await context.new_page()
            await page.goto(url, timeout=30000)
            await page.wait_for_timeout(3000)
            
            # 提取正文内容
            content = await page.evaluate('''() => {
                // 尝试多种选择器
                const selectors = [
                    'article',
                    '.content',
                    '#content',
                    '.main',
                    '#main',
                    'p',
                    'body'
                ];
                
                for (const selector of selectors) {
                    const el = document.querySelector(selector);
                    if (el && el.innerText.trim().length > 50) {
                        return el.innerText.trim();
                    }
                }
                return document.body.innerText;
            }''')
            
            await context.close()
            return content[:2000]  # 限制长度
            
        except Exception as e:
            return f"抓取失败：{e}"
