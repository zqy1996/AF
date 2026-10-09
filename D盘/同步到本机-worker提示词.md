# 在 My Machines 上运行（把 Vault 写入 D:\第二大脑）

当前云端对话 **看不到你的物理磁盘**（`usePrivateWorker=false`）。  
worker `LAPTOP-JGEBOIUJ` 已连接，请新开一个跑在该机器上的 Agent：

1. 打开 https://cursor.com/agents  
2. 运行位置选 **My Machines → LAPTOP-JGEBOIUJ**  
3. 粘贴下方整段提示词并发送  

---

## 提示词（复制全部）

```
在本机 Windows 把第二大脑 Vault 完整写入 D:\第二大脑（覆盖同步，保留目录结构）。

执行 PowerShell：

$ErrorActionPreference='Stop'
$tmp = Join-Path $env:TEMP 'AF-second-brain'
if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
git clone --depth 1 -b cursor/obsidian-second-brain-f64a https://github.com/zqy1996/AF.git $tmp
New-Item -ItemType Directory -Force -Path 'D:\第二大脑' | Out-Null
robocopy (Join-Path $tmp 'D盘\第二大脑') 'D:\第二大脑' /E /XD .git /XF '第二大脑-Vault.zip' 'Obsidian.AppImage' /NFL /NDL /NJH /NJS /nc /ns /np
if (-not (Test-Path 'D:\第二大脑\AGENTS.md')) { throw 'AGENTS.md missing' }
Add-Content -Path 'D:\第二大脑\log.md' -Value "`n## [2026-10-09] init | 本机 My Machines worker 同步完成 → D:\第二大脑`n" -Encoding UTF8
Write-Output "AGENTS=$(Test-Path 'D:\第二大脑\AGENTS.md')"
Write-Output "OBSIDIAN=$(Test-Path 'D:\第二大脑\.obsidian\app.json')"
Write-Output "INBOX=$(Test-Path 'D:\第二大脑\raw\inbox')"
Write-Output "SYNTHESIS=$(Test-Path 'D:\第二大脑\wiki\synthesis.md')"
Get-ChildItem 'D:\第二大脑' -Force | ForEach-Object Name
Get-ChildItem 'D:\第二大脑\wiki' | ForEach-Object Name

完成后回报验证结果与目录列表。然后用 Obsidian Open folder as vault 打开 D:\第二大脑。
```

---

## 或：在本机已打开的 worker 终端直接跑

若你已在 `D:\第二大脑` 目录启动了 `agent worker start`，也可在 **另一个 PowerShell 窗口**直接执行上面脚本（不经过 Agent）。
