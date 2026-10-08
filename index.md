# 第二大脑 · Vault 首页

> LLM 自生长知识库 · 服务 **临床 / 生物信息技术 / 文献**  
> Agent 开工前请先读：[[AGENTS]]

---

## 快速入口

| 层 | 说明 | 入口 |
|----|------|------|
| Schema | Agent 工作规则 | [[AGENTS]] |
| Log | 变更与待确认（只追加） | [[log]] |
| Raw | 原始素材（只读） | [[raw/inbox/README\|Inbox]] |
| Wiki | 可复用知识弹药 | 见下方 |

---

## Wiki 弹药库

- [[wiki/accounts/README|对标账号]] `wiki/accounts/`
- [[wiki/articles/README|文章拆解]] `wiki/articles/`
- [[wiki/titles/README|标题模式]] `wiki/titles/`
- [[wiki/topics/README|选题]] `wiki/topics/`
- [[wiki/structures/README|结构模板]] `wiki/structures/`
- [[wiki/tools/README|工具]] `wiki/tools/`
- [[wiki/audience/README|读者需求]] `wiki/audience/`
- [[wiki/writing/README|写作经验]] `wiki/writing/`

---

## 三大服务板块

本库不按板块硬拆顶层目录（避免过早过度设计）。用标签区分语境：

- `#临床` — 测评要点、诊疗相关科普/专业内容、病例经验沉淀
- `#生物信息技术` — 方法、工具链、可复现分析、教程与对比测评
- `#文献` — 证据链、论文拆解、引用与写书素材

写作 / 测评 / 书稿 Agent 应优先检索对应标签下的 Wiki 页面。

---

## 新素材放哪里？

**第一份测试素材 → `raw/inbox/`**

分类明确后再归入：

- 文章/网页 → `raw/articles/`
- 截图 → `raw/screenshots/`
- 评论 → `raw/comments/`
- 数据 → `raw/data/`
- AI 对话 → `raw/chats/`

然后按 [[AGENTS]] 中的自生长流程更新 Wiki，并追加 [[log]]。

---

## 仓库说明

- 本目录已初始化为 Obsidian Vault（含 `.obsidian/`）。
- 既有文件（如根目录研究脚本）予以**保留**，不纳入 Raw/Wiki 流程，除非主人明确要求迁移。
- `backup/` 用于修改 Wiki 前的版本备份。
