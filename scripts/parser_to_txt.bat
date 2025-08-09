@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 正在搜索 Python 文件...
for /r %%i in (*.py) do (
    echo 发现: %%i
)

set /p confirm=是否继续转换为纯文本文件(.txt)？(Y/N)
if /i not "%confirm%"=="Y" goto :end

:: 执行转换
for /r %%i in (*.py) do (
    rename "%%i" "%%~ni.txt"
)

echo.
echo 转换完成！

:end
pause