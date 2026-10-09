$ErrorActionPreference = "Stop"
$target = "D:\第二大脑"
$src = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not (Test-Path "D:\")) { throw "未检测到 D 盘" }
New-Item -ItemType Directory -Force -Path $target | Out-Null
Get-ChildItem -Force $src | Where-Object {
  $_.Name -notin @("一键安装到D盘.bat","一键安装到D盘.ps1","第二大脑-Vault.zip")
} | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $target $_.Name) -Recurse -Force
}
Write-Host "完成：$target"
Write-Host "请用 Obsidian 打开该文件夹。素材入口：D:\第二大脑\raw\inbox\"
