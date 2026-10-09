# 变更日志（只追加）

> 格式：`## [YYYY-MM-DD] <operation> | <detail>`  
> operation：`ingest` | `query` | `lint` | `answer-filed` | `synthesis-update` | `init` | `merge`

---

## [2026-10-08] init | 初始化第二大脑 Vault（Raw/Wiki/Schema）

- 建立目录树与 `AGENTS.md`；保留 AF 仓库 `immune` 不纳入 Vault
- 目标本机路径 `D:\第二大脑`；云端镜像 `/mnt/d/第二大脑`

## [2026-10-08] merge | 迁入 D 盘布局 `D盘/第二大脑/`

## [2026-10-08] ingest | Karpathy LLM Wiki Gist

- Raw：`raw/articles/karpathy-llm-wiki-gist.md`
- 新建：`wiki/sources/karpathy-llm-wiki-gist`、`wiki/concepts/{LLM-Wiki模式,RAG对比,Memex}`、`wiki/entities/Andrej-Karpathy`
- 更新：`wiki/synthesis.md`、`wiki/contradictions.md`、根 `index.md`、`AGENTS.md`（接入 Ingest/Query/Lint）

## [2026-10-08] ingest | cobusgreyling/llm-wiki 参考实现要点

- Source：`wiki/sources/cobusgreyling-llm-wiki-readme`
- 采纳页型 entities/concepts/sources/answers + templates；创作弹药目录保留并存

## [2026-10-08] answer-filed | 为何不用纯 RAG 做第二大脑

- `wiki/answers/为何不用纯RAG做第二大脑.md`

## [2026-10-08] synthesis-update | 确立「LLM Wiki 核心 + 创作弹药层」双层并存

## [2026-10-08] init | 待本机 worker：`agent worker start --worker-dir D:\第二大脑` 后同步落盘

## [2026-10-09] init | 检测到 worker LAPTOP-JGEBOIUJ；本会话 usePrivateWorker=false，需 My Machines 新 Agent 落盘（见 D盘/同步到本机-worker提示词.md）
