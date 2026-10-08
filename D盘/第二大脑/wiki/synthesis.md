---
type: synthesis
created: 2026-10-08
updated: 2026-10-08
source_count: 2
tags: [core]
---

# Synthesis · 第二大脑总论

## 当前论题

本 Vault 采用 **LLM Wiki 自生长**：Raw 只增不改；Wiki 由 Agent 编译维护；Schema 在 [[AGENTS]]。  
在通用 LLM Wiki 核心（entities/concepts/sources/answers）之上，叠加**创作弹药层**（账号/标题/选题/结构/工具/读者/写作），服务临床、生物信息技术、文献的测评与内容生产，并为写书与自动初稿留接口。

## 关键判断

1. 知识必须在 Ingest 时**编译进 Wiki**，Query 读 Wiki 而非每次重读 Raw。  
2. 好答案要归档到 `wiki/answers/`，探索本身也要复利。  
3. 工具链（CLI/MCP/qmd）按规模渐进；早期靠 index + 双链即可。  

## 演进记录

- 2026-10-08：接入 Karpathy gist + cobusgreyling 参考实现要点；建立核心页型与创作弹药并存结构。

## 相关

- [[LLM-Wiki模式]]
- [[RAG对比]]
- [[sources/karpathy-llm-wiki-gist]]
- [[sources/cobusgreyling-llm-wiki-readme]]
- [[wiki/contradictions|Contradictions]]
