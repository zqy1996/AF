@echo off
chcp 65001 >nul
set "TARGET=D:\第二大脑"
set "SRC=%~dp0"

echo [第二大脑] 正在创建 %TARGET% ...
if not exist "D:\" (
  echo 错误：未检测到 D 盘。请确认 D 盘可用后重试。
  pause
  exit /b 1
)
mkdir "%TARGET%" 2>nul

echo [第二大脑] 正在复制 Vault 文件...
xcopy "%SRC%*" "%TARGET%\" /E /I /H /Y /EXCLUDE:%SRC%exclude-install.txt >nul 2>&1
if errorlevel 1 (
  robocopy "%SRC%." "%TARGET%" /E /XD .git /XF "一键安装到D盘.bat" "一键安装到D盘.ps1" /NFL /NDL /NJH /NJS /nc /ns /np
)

echo.
echo 完成。Vault 根目录：%TARGET%
echo 请打开 Obsidian - Open folder as vault - 选择 %TARGET%
echo 第一份素材请放入：%TARGET%\raw\inbox\
pause
