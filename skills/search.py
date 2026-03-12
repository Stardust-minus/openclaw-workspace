#!/usr/bin/env python3
"""
Web Search Skill - 五子并行搜索主入口
"""

import asyncio
import json
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from dotenv import load_dotenv

# 加载 .env 文件
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)

from agents.baidu import BaiduSearch
from agents.bing import BingSearch
from agents.zhipu import ZhipuSearch
from agents.brave import BraveSearch
from agents.direct import DirectCrawl
from crawler import PageCrawler
from summarizer import ResultSummarizer


class WebSearch:
    """五子并行搜索主类"""
    
    def __init__(self):
        # 从环境变量加载配置
        self.timeout = int(os.getenv('SEARCH_TIMEOUT', 180))
        self.progress_interval = int(os.getenv('PROGRESS_INTERVAL', 0))  # 0=禁用进度推送
        self.progress_threshold = self.timeout  # 只在超时时提示
        self.max_results = int(os.getenv('MAX_RESULTS_PER_AGENT', 3))
        self.deep_crawl_enabled = os.getenv('DEEP_CRAWL_ENABLED', 'false').lower() == 'true'
        self.max_pages_per_agent = int(os.getenv('MAX_PAGES_PER_AGENT', 1))
        self.enable_progress_push = os.getenv('ENABLE_PROGRESS_PUSH', 'false').lower() == 'true'
        
        # 初始化五个子 agent
        self.agents = {
            'baidu': BaiduSearch(),
            'bing': BingSearch(),
            'zhipu': ZhipuSearch(
                api_key=os.getenv('ZHIPU_API_KEY'),
                search_engine='search_pro'
            ),
            'brave': BraveSearch(
                api_key=os.getenv('BRAVE_API_KEY')
            ),
            'direct': DirectCrawl()
        }
        
        self.crawler = PageCrawler()
        self.summarizer = ResultSummarizer()
        self.last_progress_time = 0
    
    async def _report_progress(self, start_time: float, stage: str, completed: int = 0, total: int = 0):
        """定时进度汇报（默认禁用）"""
        # 只有在 ENABLE_PROGRESS_PUSH=true 时才推送进度
        if not self.enable_progress_push:
            return
        
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        
        # 每 60 秒汇报一次
        if int(elapsed) - self.last_progress_time >= self.progress_interval and self.progress_interval > 0:
            progress_info = f"({completed}/{total})" if total > 0 else ""
            print(f"\n[{self._now()}] ⏱️  进度汇报：已运行 {minutes}分{seconds}秒 {progress_info}")
            print(f"           阶段：{stage}")
            self.last_progress_time = int(elapsed)
        
        # 超时前主动提示
        if int(elapsed) == self.progress_threshold:
            print(f"\n[{self._now()}] ⚠️  即将超时，已运行 {self.timeout} 秒...")
        
    async def search(
        self,
        query: str,
        max_results: int = 5,
        deep_crawl: bool = True,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        执行五子并行搜索
        
        Args:
            query: 搜索关键词
            max_results: 每个 agent 返回的最大结果数
            deep_crawl: 是否深入抓取页面内容
            progress_callback: 进度回调函数
            
        Returns:
            搜索结果字典
        """
        start_time = time.time()
        self.last_progress_time = 0
        results = {'query': query, 'agents': {}, 'summary': ''}
        
        # 并行启动五个子 agent
        print(f"[{self._now()}] 🚀 开始五子并行搜索：{query}")
        print(f"           超时：{self.timeout}秒 | 推送间隔：{self.progress_interval}秒 | 推送开关：{self.enable_progress_push}")
        
        agent_tasks = {
            name: agent.search(query, max_results)
            for name, agent in self.agents.items()
        }
        
        # 等待所有 agent 完成（带超时）+ 定时进度推送
        try:
            # 创建定时进度推送任务
            progress_task = None
            if self.enable_progress_push and self.progress_interval > 0:
                progress_task = asyncio.create_task(
                    self._periodic_progress_report(start_time, agent_tasks)
                )
            
            completed = await asyncio.wait_for(
                asyncio.gather(*agent_tasks.values(), return_exceptions=True),
                timeout=self.timeout
            )
            
            # 取消定时推送任务
            if progress_task:
                progress_task.cancel()
                try:
                    await progress_task
                except asyncio.CancelledError:
                    pass
            
            # 汇报最终进度
            await self._report_progress(start_time, "搜索完成", len([r for r in completed if not isinstance(r, Exception)]), 5)
            
            for (name, _), result in zip(agent_tasks.items(), completed):
                if isinstance(result, Exception):
                    print(f"[{self._now()}] ❌ {name} 失败：{str(result)}")
                    results['agents'][name] = {'error': str(result)}
                else:
                    result_count = len(result.get('results', []))
                    print(f"[{self._now()}] ✅ {name} 完成：{result_count} 条结果")
                    results['agents'][name] = result
                    
        except asyncio.TimeoutError:
            print(f"[{self._now()}] ⚠️  搜索超时（{self.timeout}秒）")
            results['error'] = '搜索超时'
        
        # 深入抓取页面内容
        if deep_crawl and self.deep_crawl_enabled and 'error' not in results:
            print(f"\n[{self._now()}] 🔍 开始深入抓取页面...")
        
        # 定时进度推送（在搜索过程中）
        async def _periodic_progress_report():
            while True:
                await asyncio.sleep(self.progress_interval)
            elapsed = time.time() - start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            print(f"\n[{self._now()}] ⏱️  进度汇报：已运行 {minutes}分{seconds}秒")
            print(f"           阶段：搜索中...")
        
        # 深入抓取页面内容
        if deep_crawl and self.deep_crawl_enabled and 'error' not in results:
            print(f"\n[{self._now()}] 🔍 开始深入抓取页面...")
            await self._deep_crawl(results, start_time, progress_callback)
        
        # 汇总结果
        print(f"\n[{self._now()}] 📝 汇总搜索结果...")
        results['summary'] = self.summarizer.summarize(results)
        
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        print(f"\n[{self._now()}] ✅ 搜索完成，总耗时：{minutes}分{seconds}秒")
        
        # 保存结果到文件
        output_file = Path(__file__).parent / 'search_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"[{self._now()}] 💾 结果已保存：{output_file}")
        
        # 只返回文件路径和统计信息（不返回完整结果）
        summary_info = {
            'status': 'success',
            'file': str(output_file),
            'query': query,
            'agents_completed': 5,
            'total_results': sum(
                len(agent_result.get('results', []))
                for agent_result in results.get('agents', {}).values()
                if 'results' in agent_result
            ),
            'elapsed_seconds': round(elapsed, 2)
        }
        print(f"[{self._now()}] 📦 返回：{summary_info}")
        
        return summary_info
    
    async def _deep_crawl(
        self,
        results: Dict[str, Any],
        start_time: float,
        progress_callback: Optional[callable] = None
    ):
        """深入抓取页面内容"""
        all_urls = []
        for agent_name, agent_result in results['agents'].items():
            if 'results' in agent_result:
                for item in agent_result['results'][:self.max_pages_per_agent]:
                    if 'url' in item and item['url'] not in all_urls:
                        all_urls.append(item['url'])
        
        if not all_urls:
            print(f"[{self._now()}] 无页面需要抓取")
            return
        
        print(f"[{self._now()}] 待抓取页面：{len(all_urls)} 个")
        
        # 批量抓取
        for i, url in enumerate(all_urls):
            try:
                content = await self.crawler.fetch(url, timeout=self.crawler.timeout)
                # 更新对应结果
                for agent_result in results['agents'].values():
                    for item in agent_result.get('results', []):
                        if item.get('url') == url:
                            item['content'] = content
                            break
            except Exception as e:
                print(f"[{self._now()}] 抓取失败 {url}: {e}")
            
            # 进度汇报
            await self._report_progress(start_time, "页面抓取", i + 1, len(all_urls))
            
            # 进度回调
            if progress_callback and (i + 1) % 5 == 0:
                await progress_callback(i + 1, len(all_urls))
    
    def _now(self) -> str:
        return datetime.now().strftime('%H:%M:%S')


# 便捷函数
async def search(
    query: str,
    max_results: int = 5,
    deep_crawl: bool = True
) -> Dict[str, Any]:
    """快速搜索函数"""
    engine = WebSearch()
    return await engine.search(query, max_results, deep_crawl)
