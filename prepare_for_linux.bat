@echo off
REM ========================================
REM 智能查寝签到 - Linux打包准备脚本
REM 龟龟 (您的AI助手) 2026-06-16
REM ========================================

echo.
echo ========================================
echo   智能查寝签到 Android APK 准备脚本
echo ========================================
echo.

REM 检查是否在Windows中
wmic os get caption | findstr /i windows >nul 2>&1
if errorlevel 1 (
    echo [错误] 本脚本需要在Windows环境中运行！
    goto end
)

REM 设置颜色（可选的）
color 0A

echo [信息] 正在检查目录和文件...
echo.

REM 检查必需的文件
set "missing_files="

if not exist "main.py" (
    echo [错误] main.py 文件不存在！
    set "missing_files=1"
)

if not exist "checkin_core.py" (
    echo [错误] checkin_core.py 文件不存在！
    set "missing_files=1"
)

if not exist "buildozer.spec" (
    echo [错误] buildozer.spec 文件不存在！
    set "missing_files=1"
)

if defined missing_files (
    echo.
    echo [错误] 必需文件缺失，无法继续！
    goto end
)

echo [成功] 所有必需文件检查通过！
echo.
echo ========================================
echo   文件清单
echo ========================================

echo 1. 主应用程序文件:
echo    - main.py
echo.
echo 2. 核心逻辑文件:
echo    - checkin_core.py
echo.
echo 3. 配置文件:
echo    - buildozer.spec
echo    - buildozer.local.spec (如果存在)
echo.
echo 4. 文档文件:
echo    - README.md
echo    - 打包指南.md
echo    - quick_start.sh (Linux打包脚本)
echo.
echo 5. 图标文件 (data目录):
if exist "data" (
    echo    - data\icon.png (必需)
    echo    - data\presplash.png (必需)
) else (
    echo    - data目录不存在！
    echo    [警告] 需要创建data目录和图标文件
)

echo.
echo ========================================
echo   下一步操作指南
echo ========================================
echo.

echo 步骤1: 安装WSL2 (如果尚未安装)
echo   1. 以管理员身份打开PowerShell
echo   2. 运行: wsl --install Ubuntu
echo   3. 按照提示完成安装
echo   4. 重新启动电脑
echo.
echo 步骤2: 将项目文件复制到WSL
echo   方法A: 使用WSL访问Windows文件
echo     在Ubuntu终端中:
echo     cd /mnt/c/Users/【您的用户名】/【项目路径】
echo.
echo   方法B: 复制到Ubuntu主目录
echo     mkdir -p ~/android_project
echo     cp -r /mnt/c/【项目路径】/* ~/android_project/
echo.
echo 步骤3: 在WSL中运行打包脚本
echo     1. 启动Ubuntu终端
echo     2. cd ~/android_project
echo     3. chmod +x quick_start.sh
echo     4. ./quick_start.sh
echo.
echo 或者手动运行:
echo     buildozer android debug
echo.
echo ========================================
echo   重要提醒
echo ========================================
echo.
echo [重要] 图标文件要求:
echo   - icon.png: 512x512像素，PNG格式
echo   - presplash.png: 1024x768像素，PNG格式
echo.
echo [重要] 如果没有图标文件，可以在Linux中:
echo   sudo apt install imagemagick
echo   convert -size 512x512 xc:#1a237e -fill white -pointsize 50 ^
echo     -gravity center -draw "text 0,0 '签到'" data/icon.png
echo.
echo [重要] 打包环境要求:
echo   - 至少8GB内存
echo   - 至少20GB磁盘空间
echo   - 稳定的网络连接
echo.
echo ========================================
echo   技术支持
echo ========================================
echo.
echo 如果遇到问题:
echo   1. 检查网络连接
echo   2. 确保有足够的内存和磁盘空间
echo   3. 查看构建日志
echo   4. 截图错误信息发给我
echo.
echo 联系方式:
echo   龟龟 - 您的AI助手
echo   创建时间: %date% %time%
echo.

:end
echo.
echo 按任意键退出...
pause >nul