@echo off
echo =========================================
echo   智能查寝签到 - Windows测试启动
echo   龟龟 (您的AI助手) 2026-06-16
echo =========================================
echo.

echo [1/4] 检查Python环境...
python --version
if errorlevel 1 (
    echo [错误] Python未安装或不在PATH中
    echo 请安装Python 3.8+ 并添加到PATH
    pause
    exit /b 1
)

echo.
echo [2/4] 检查Kivy模块...
python -c "import kivy; print('Kivy版本:', kivy.__version__)"
if errorlevel 1 (
    echo [错误] Kivy模块未安装
    echo 请运行: pip install kivy kivymd
    pause
    exit /b 1
)

python -c "import kivymd; print('KivyMD版本:', kivymd.__version__)"
if errorlevel 1 (
    echo [错误] KivyMD模块未安装
    echo 请运行: pip install kivymd
    pause
    exit /b 1
)

echo.
echo [3/4] 检查依赖库...
python -c "import requests; print('requests版本:', requests.__version__)"
python -c "from checkin_core import CheckinBot; print('checkin_core导入成功')"

echo.
echo [4/4] 启动应用...
echo.
echo "现在启动智能查寝签到应用..."
echo "如果窗口正常显示，表示应用工作正常"
echo "按Ctrl+C可关闭应用"
echo.
echo =========================================

:: 设置控制台编码为UTF-8
chcp 65001 >nul

:: 启动主应用
python main.py

:: 如果应用关闭，暂停一下
echo.
echo "应用已关闭"
pause