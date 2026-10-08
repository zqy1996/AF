---
type: concept
created: 2026-10-08
updated: 2026-10-08
sources: ["sources/karpathy-llm-wiki-gist"]
tags: [llm-wiki]
---

# RAG 对比

## 定义

经典 RAG：查询时检索 Raw 片段再生成答案——**不积累**。  
LLM Wiki：Ingest 时编译进 Wiki，Query 读的是已交叉引用的持久页。

| | RAG | LLM Wiki |
|---|-----|----------|
| 知识是否积累 | 否 | 是 |
| 跨文档综合 | 临场拼装 | 预编译在 synthesis/实体页 |
| Agent 角色 | 检索+回答 | 维护 Wiki |
| 人类角色 | 策展语料 | 策展 Raw + 提问 |

## 实践要点

本库默认走 LLM Wiki；仅在「实体精确查找」等场景可并行考虑检索增强（参见社区讨论，待核实具体阈值）。

## 相关

- [[LLM-Wiki模式]]
- [[sources/karpathy-llm-wiki-gist]]
