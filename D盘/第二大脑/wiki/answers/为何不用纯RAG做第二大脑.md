---
type: answer
created: 2026-10-08
updated: 2026-10-08
question: "为什么第二大脑要用 LLM Wiki 而不是纯 RAG？"
sources: ["sources/karpathy-llm-wiki-gist"]
tags: [llm-wiki]
---

# 为何不用纯 RAG 做第二大脑？

## 结论

纯 RAG 每次提问都重新拼片段，**没有复利**。第二大脑需要跨文献/案例/工具的持续综合——这正是 [[LLM-Wiki模式]] 的 Ingest 编译 + Wiki 维护所解决的。

## 依据

- [[RAG对比]]
- [[sources/karpathy-llm-wiki-gist]]
- [[wiki/synthesis|Synthesis]]

## 可复用弹药（写作/测评）

- 标题钩子：从「搜得到」到「越用越懂」  
- 结构：痛点（重推知识）→ 机制（编译 Wiki）→ 人机分工 → 案例（临床/生信/文献）
