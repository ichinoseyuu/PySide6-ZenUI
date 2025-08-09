@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 正在搜索 Python 文件...
for /r %%i in (*.txt) do (
    echo 发现: %%i
)

set /p confirm=是否继续转换为python文件？(Y/N)
if /i not "%confirm%"=="Y" goto :end

:: 执行转换
for /r %%i in (*.txt) do (
    rename "%%i" "%%~ni.py"
)

echo.
echo 转换完成！

:end
pause