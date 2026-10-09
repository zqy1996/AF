# D 盘第二大脑

## 状态

- Vault 已按 **Karpathy LLM Wiki** 完善（Ingest / Query / Lint + entities/concepts/sources/answers）
- Git 包：`D盘/第二大脑/`
- 安装包：`第二大脑-Vault.zip` + `安装到D盘-第二大脑.bat`
- 云端镜像：`/mnt/d/第二大脑`

## 同步到本机 `D:\第二大脑`

云端仍看不到 worker 时，任选：

```powershell
# 推荐：常驻 worker（窗口不要关）
cd D:\第二大脑
agent worker start --name "second-brain" --worker-dir "D:\第二大脑"
```

或解压/运行本目录安装脚本写入文件后，用 Obsidian 打开 `D:\第二大脑`。
