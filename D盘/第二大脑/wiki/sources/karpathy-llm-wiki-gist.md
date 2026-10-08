---
type: source
created: 2026-10-08
updated: 2026-10-08
raw: "raw/articles/karpathy-llm-wiki-gist.md"
url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
published: "2026-04-04"
tags: [llm-wiki, schema]
---

# Karpathy · LLM Wiki（Gist）

## 一句话摘要

用 LLM **编译并维护**持久化、可双链的 Markdown Wiki，替代「每次提问都从 Raw 重新拼装」的纯 RAG。

## 关键信息 / 弹药

- 三层：Raw（不可变）→ Wiki（Agent 写）→ Schema（`AGENTS.md`）
- 三大操作：**Ingest / Query / Lint**
- 一份素材应更新多页（实体、概念、综合），不是一份摘要
- 好的 Query 答案要**归档回 Wiki**（`answers/`）
- `index.md` 内容导向；`log.md` 时间导向、只追加
- Obsidian = IDE；LLM = 程序员；Wiki = 代码库

## 实体与概念

- 实体：[[Andrej-Karpathy]]
- 概念：[[LLM-Wiki模式]] [[Memex]] [[RAG对比]]

## 对三大板块的启示

- #临床 — 病例/指南/共识可 ingest 后沉淀为实体（病种、指标）与概念（路径、证据等级）
- #生物信息技术 — 工具/流水线做成 entity；方法学做成 concept；论文原文留 Raw
- #文献 — 每篇论文一个 source 页；矛盾证据进 contradictions；synthesis 演进总论

## 开放问题

- 创作弹药目录（titles/topics…）与 entities/concepts 的边界如何在实践中收束？
- 何时引入 `llm-wiki` CLI / qmd？（待规模上来再定）

## 来源

- Raw：`raw/articles/karpathy-llm-wiki-gist.md`
- URL：https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- 日期：2026-04-04（gist created）
