@echo off
chcp 65001 >nul
set "TARGET=D:\第二大脑"
set "ZIP=%~dp0第二大脑-Vault.zip"
set "DIR=%~dp0第二大脑"

echo ======================================
echo   第二大脑 Vault - 安装到 D:\第二大脑
echo ======================================

if not exist "D:\" (
  echo [错误] 未检测到 D 盘。
  pause
  exit /b 1
)

mkdir "%TARGET%" 2>nul

if exist "%ZIP%" (
  echo [1/2] 解压 %ZIP% ...
  powershell -NoProfile -Command "Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%TARGET%' -Force"
) else if exist "%DIR%\AGENTS.md" (
  echo [1/2] 复制文件夹 第二大脑 ...
  robocopy "%DIR%" "%TARGET%" /E /XD .git /XF "第二大脑-Vault.zip" "Obsidian.AppImage" /NFL /NDL /NJH /NJS /nc /ns /np
) else (
  echo [错误] 未找到 第二大脑-Vault.zip 或 第二大脑 文件夹。
  pause
  exit /b 1
)

if not exist "%TARGET%\AGENTS.md" (
  echo [错误] 安装后未找到 AGENTS.md，请检查解压结果。
  pause
  exit /b 1
)

echo [2/2] 完成。
echo.
echo Vault 已创建：%TARGET%
echo 请打开 Obsidian - Open folder as vault - 选择该文件夹
echo 测试素材目录：%TARGET%\raw\inbox\
echo.
pause
