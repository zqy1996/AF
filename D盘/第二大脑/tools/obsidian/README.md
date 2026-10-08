# Obsidian（本机 / 云端）

本 Vault 根目录即 Obsidian 仓库（含 `.obsidian/`）。

## 云端环境

已下载 Linux AppImage（不入库，体积过大）：

- 二进制：`~/Applications/Obsidian-1.14.4.AppImage`
- 符号链接：`tools/obsidian/Obsidian.AppImage`

云端通常无图形界面，**知识库以 Markdown Vault 为准**；Agent 直接读写本仓库即可。

本机打开：

1. 安装 [Obsidian](https://obsidian.md/download)
2. Open folder as vault → 选择本仓库根目录（含 `AGENTS.md` 与 `.obsidian/` 的那一层）
3. 若需同步到 Windows D: 盘：将该目录克隆/同步到 `D:\` 下任意文件夹后，用 Obsidian 打开同一路径

## 与 Agent 协作

所有 Agent 先读根目录 `AGENTS.md`，再按 Raw → Wiki 自生长流程工作。
