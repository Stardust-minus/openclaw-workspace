#!/usr/bin/env python3
"""
结果汇总器 - 去重、排序、生成报告
"""

from typing import Dict, List, Any


class ResultSummarizer:
    """结果汇总器"""
    
    def __init__(self):
        self.seen_urls = set()
        
    def summarize(self, results: Dict[str, Any]) -> str:
        """
        汇总所有搜索结果
        
        Args:
            results: 五子 agent 的原始结果
            
        Returns:
            汇总报告文本
        """
        all_results = []
        
        # 收集所有结果
        for agent_name, agent_result in results.get('agents', {}).items():
            if 'error' in agent_result:
                continue
            for item in agent_result.get('results', []):
                item['_source'] = agent_name
                all_results.append(item)
        
        # 去重
        unique_results = self._deduplicate(all_results)
        
        # 生成报告
        report = self._generate_report(unique_results, results.get('query', ''))
        return report
    
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        """按 URL 去重"""
        seen = set()
        unique = []
        
        for item in results:
            url = item.get('url', '')
            if url and url not in seen:
                seen.add(url)
                unique.append(item)
        
        return unique
    
    def _generate_report(self, results: List[Dict], query: str) -> str:
        """生成汇总报告"""
        if not results:
            return "未找到相关结果"
        
        lines = [
            f"## 搜索结果汇总",
            f"",
            f"**查询**: {query}",
            f"**结果数**: {len(results)}",
            f"",
            "### 结果列表",
            ""
        ]
        
        for i, item in enumerate(results[:10], 1):
            lines.append(f"{i}. **{item.get('title', '无标题')}**")
            lines.append(f"   - 来源：{item.get('_source', 'unknown')}")
            lines.append(f"   - 链接：{item.get('url', '')}")
            lines.append(f"   - 摘要：{item.get('summary', '')[:200]}")
            lines.append("")
        
        return '\n'.join(lines)
