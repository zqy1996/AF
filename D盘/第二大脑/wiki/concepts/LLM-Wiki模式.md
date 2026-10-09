---
type: concept
created: 2026-10-08
updated: 2026-10-08
sources: ["sources/karpathy-llm-wiki-gist", "sources/cobusgreyling-llm-wiki-readme"]
tags: [llm-wiki, core]
---

# LLM Wiki 模式

## 定义

由 LLM **增量编译**的持久知识层：结构化、互链的 Markdown，夹在人类与 Raw 之间。知识在 Ingest 时编译一次并持续更新，而不是每次 Query 从片段重推。

## 关键机制

1. **Ingest**：读 Raw → 更新 source/entity/concept/synthesis → 记 log  
2. **Query**：先读 index → 读相关页 → 回答并可选归档到 answers  
3. **Lint**：断链、孤儿、矛盾、缺口  

## 实践要点（本库）

- Schema 在根目录 [[AGENTS]]  
- 创作弹药目录与 LLM Wiki 核心目录**并存**，Ingest 时双侧更新  
- 规模小时只靠 `index.md` + 双链；需要时再加 [cobusgreyling/llm-wiki](https://github.com/cobusgreyling/llm-wiki) / qmd  

## 相关

- [[RAG对比]]
- [[Memex]]
- [[Andrej-Karpathy]]
- [[wiki/synthesis|Synthesis]]
- [[sources/karpathy-llm-wiki-gist]]
