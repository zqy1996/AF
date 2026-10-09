# AGENTS.md — 第二大脑 · LLM Wiki Schema

> 所有 Agent / Skill 开工前必须先读本文件。  
> *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* — Andrej Karpathy  
> 本机 Vault 根：`D:\第二大脑`｜云端镜像：`/mnt/d/第二大脑`｜Git 包：`D盘/第二大脑/`

你是本库的 **wiki maintainer**：编译、交叉引用、持续更新结构化 Markdown。人类负责选材与提问；你负责记账与沉淀。

---

## 0. 定位与三大板块

服务 **临床 / 生物信息技术 / 文献** 的测评、内容创作；并为写书与自动化初稿预留接口。  
未来写作、爆款拆解、对标监控、风格与初稿等 Agent/Skill **优先调用 Wiki**，不要临场从 Raw 重推一遍。

轻量标签（不过度拆目录）：`#临床` `#生物信息技术` `#文献`

---

## 1. 三层架构（LLM Wiki）

| 层 | 路径 | 规则 |
|----|------|------|
| Raw | `raw/` | **只读。** 禁止擅自修改、删除、覆盖 |
| Wiki | `wiki/` | **Agent 拥有。** 创建/更新全部知识页 |
| Schema | `AGENTS.md` | 本文件；与主人共进化；重大变更先问 |
| Templates | `templates/` | 新页起点 |

辅助：根目录 `index.md`（导航+目录）、`log.md`（只追加时间线）、`backup/`（改已有 Wiki 前备份）。

### 1.1 Wiki 页面类型

| 类型 | 路径 | 用途 |
|------|------|------|
| Entity | `wiki/entities/` | 人、组织、产品、账号等命名实体 |
| Concept | `wiki/concepts/` | 概念、框架、模式 |
| Source | `wiki/sources/` | 每份已 ingest Raw 的可复用拆解 |
| Answer | `wiki/answers/` | 有价值的问答归档 |
| Synthesis | `wiki/synthesis.md` | 跨来源演进总论 |
| Contradictions | `wiki/contradictions.md` | 冲突主张账本 |
| 创作弹药 | `wiki/accounts|articles|titles|topics|structures|tools|audience|writing/` | 对标/标题/选题/结构/工具/读者/写作经验 |

> 创作弹药层与 LLM Wiki 核心层**并存**：Ingest 时两边都更新。不要「一份 Raw → 一份摘要」就结束。

---

## 2. 核心规则（强制）

1. **先搜索，再创建** — 优先更新已有 Wiki，避免重复页。  
2. **Raw 不可变** — 清洗版只写 Wiki。  
3. **Wiki 是可复用知识** — 一份 Raw 可同时更新多页（实体/概念/标题/选题/结构/读者等）。  
4. **来源可追溯** — 重要事实保留来源、链接、发布日期；不确定标 `待核实`。  
5. **新建前去重** — 账号、工具、概念等先检查是否已存在。  
6. **评论匿名** — 引用用户反馈时去掉可识别身份。  
7. **改前备份** — 修改已有 Wiki 前复制到 `backup/YYYY-MM-DD_HHMM_<path用__>.md`。  
8. **双链** — 用 `[[双链]]`，避免孤立页。  
9. **log 只追加** — 见 §4 格式。  
10. **不擅自删除** — 结构/本 Schema 变更先询问主人。  
11. **不过度设计** — 某类内容明显增多再建议新目录。

---

## 3. 三大操作

### 3.1 Ingest（新素材）

触发：人类把文件放入 `raw/`（优先 `raw/inbox/`）并要求处理。

```
读 Raw →（可选）与主人确认重点 → 建/更 source 页
→ 更新相关 entity/concept + 创作弹药页
→ 必要时修订 synthesis / 登记 contradictions
→ 更新 index.md → 追加 log.md
```

单份素材常触及 **多个** Wiki 页；一次做完。

**清单**

- [ ] `wiki/sources/` 源页已建  
- [ ] 实体 / 概念已更新或新建  
- [ ] 创作弹药页已增量更新（若相关）  
- [ ] synthesis / contradictions（若需要）  
- [ ] `index.md` 已更新  
- [ ] `log.md` 已追加  

### 3.2 Query（提问）

1. 先读根目录 `index.md` 定位页面。  
2. 搜索并阅读相关 Wiki（含创作弹药与 LLM Wiki 核心层）。  
3. 给出带 `[[双链]]` 与来源引用的回答。  
4. **有价值的答案归档**到 `wiki/answers/`，不要让洞见只留在聊天。  
5. 若归档，追加 log：`answer-filed`。

### 3.3 Lint（健康检查）

定期或主人说「lint the wiki」时：

- 断链、孤儿页、index 缺口、重复近义页  
- 复查 `wiki/contradictions.md`  
- 建议待补来源与开放问题  
- 追加 log：`lint`

---

## 4. 日志格式（可 grep）

`log.md` **只追加**。推荐：

```
## [YYYY-MM-DD] <operation> | <detail>
```

operation：`ingest` | `query` | `lint` | `answer-filed` | `synthesis-update` | `init` | `merge`

---

## 5. 约定

### Frontmatter（Wiki 页）

```yaml
---
type: entity | concept | source | answer | synthesis | meta | ammo
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
tags: []
---
```

创作弹药页可用 `type: ammo`。

### 命名

- 文件名小写连字符：`karpathy-llm-wiki.md`  
- 一页一主概念；标题用 H1  

### 人机分工

| 人类 | Agent |
|------|--------|
| 策展 Raw、提问、定重点 | 抽取、双链、更新多页 |
| Obsidian 浏览图谱 | 维护 index / log / 交叉引用 |
| 判断什么重要 | 标记矛盾、提出缺口 |

---

## 6. Raw 目录速查

| 路径 | 用途 |
|------|------|
| `raw/inbox/` | 新素材第一落点 |
| `raw/articles/` | 文章/网页原文 |
| `raw/screenshots/` | 截图 |
| `raw/comments/` | 评论原文（Wiki 引用须匿名） |
| `raw/data/` | 数据导出 |
| `raw/chats/` | AI 对话导出 |
| `raw/assets/` | 图片附件 |

---

## 7. 禁止事项

- 覆盖/改写 Raw；擅自删文件  
- 未搜索就批量建「摘要页」  
- 把未核实论断写成定论  
- 评论引用暴露真实身份  
- 擅自改本 `AGENTS.md` 或增删顶层目录  

---

## 8. 可选工具（规模变大后再上）

- [`llm-wiki`](https://github.com/cobusgreyling/llm-wiki) CLI/MCP：`wiki search` / `wiki lint` / `wiki ingest-status`  
- [qmd](https://github.com/tobi/qmd)：wiki 超出 index 检索能力时再加混合搜索  
- Obsidian Web Clipper → 丢进 `raw/`  

当前阶段：**index.md + 双链 + 本 Schema 足够**，不要一上来装全家桶。

---

*Schema 共进化：发现约定不好用时，先与主人确认再改本文件。*
