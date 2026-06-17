@echo off
chcp 65001 >nul
echo.
echo ===========================================
echo     智能查寝签到 - Windows桌面运行器
echo ===========================================
echo.
echo [%date% %time%]
echo.

:menu
cls
echo ===========================================
echo            主菜单 - 选择操作
echo ===========================================
echo.
echo 1. 安装依赖包 (首次运行需要)
echo 2. 运行桌面版应用程序
echo 3. 运行功能测试脚本
echo 4. 生成应用图标
echo 5. 清理__pycache__缓存
echo 6. 查看项目文件
echo 7. 打开项目浏览器界面
echo 8. 退出
echo.
set /p choice=请输入选择 (1-8): 

if "%choice%"=="1" goto install
if "%choice%"=="2" goto run_app
if "%choice%"=="3" goto run_test
if "%choice%"=="4" goto generate_icons
if "%choice%"=="5" goto clean_cache
if "%choice%"=="6" goto view_files
if "%choice%"=="7" goto open_browser
if "%choice%"=="8" goto exit
echo 无效选择，请重试
pause >nul
goto menu

:install
cls
echo.
echo ===========================================
echo           安装Python依赖包
echo ===========================================
echo.
echo 正在检查Python版本...
python --version
echo.
echo 正在安装依赖包...
echo.
echo 安装 Kivy 和 KivyMD...
pip install kivy[base] kivy[full] --prefer-binary
echo.
echo 安装 KivyMD...
pip install kivymd
echo.
echo 安装网络请求库...
pip install requests pillow certifi
echo.
echo 依赖包安装完成！
pause >nul
goto menu

:run_app
cls
echo.
echo ===========================================
echo         运行桌面版应用程序
echo ===========================================
echo.
echo 启动智能查寝签到应用程序...
echo.
echo 如果出现错误，请确保：
echo 1. Python已安装
echo 2. 已安装必要依赖 (选项1)
echo 3. 网络连接正常
echo.
echo 按Ctrl+C可退出应用程序
echo.
echo ===========================================
echo.
pause >nul
python main.py
if %errorlevel% neq 0 (
    echo.
    echo 应用程序运行失败，请检查错误信息。
    pause >nul
)
goto menu

:run_test
cls
echo.
echo ===========================================
echo           运行功能测试脚本
echo ===========================================
echo.
echo 运行签到核心功能测试...
python test_app.py
echo.
echo 测试完成！
pause >nul
goto menu

:generate_icons
cls
echo.
echo ===========================================
echo           生成应用图标
echo ===========================================
echo.
echo 生成应用程序图标...
python generate_icons.py
echo.
echo 图标生成完成！
echo 已创建文件:
echo   - data/icon.png (应用图标)
echo   - data/presplash.png (启动画面)
echo.
pause >nul
goto menu

:clean_cache
cls
echo.
echo ===========================================
echo           清理Python缓存
echo ===========================================
echo.
echo 清理__pycache__目录...
if exist __pycache__ (
    rmdir /s /q __pycache__
    echo 已清理缓存文件
) else (
    echo 未找到缓存目录
)
echo.
echo 清理完成！
pause >nul
goto menu

:view_files
cls
echo.
echo ===========================================
echo           项目文件列表
echo ===========================================
echo.
echo 项目目录: %cd%
echo 总文件数: 13个文件
echo.
echo Python源代码文件:
echo   - main.py (24.3 KB) - 主程序
echo   - checkin_core.py (13.2 KB) - 签到核心
echo   - test_app.py (3.5 KB) - 测试脚本
echo   - generate_icons.py (6.0 KB) - 图标生成器
echo.
echo 配置和脚本文件:
echo   - buildozer.spec (2.2 KB) - 打包配置
echo   - quick_start.sh (7.7 KB) - Linux启动脚本
echo   - run_windows.bat (1.4 KB) - Windows运行脚本
echo   - prepare_for_linux.bat (3.7 KB) - Linux准备脚本
echo.
echo 文档文件:
echo   - README.md (2.3 KB) - 项目说明
echo   - 打包指南.md (6.9 KB) - 打包指南
echo   - 项目总结报告.md (7.3 KB) - 项目总结
echo.
echo 编译缓存:
echo   - __pycache__/ (包含编译字节码)
echo.
dir /B
echo.
pause >nul
goto menu

:open_browser
cls
echo.
echo ===========================================
echo         打开项目浏览器界面
echo ===========================================
echo.
echo 正在打开HTMl项目浏览器...
echo 请稍候...
start "" "android_checkin_app.html"
echo.
echo 浏览器窗口已打开！
echo 您可以在浏览器中：
echo 1. 查看所有项目文件
echo 2. 预览文件内容
echo 3. 快速运行脚本
echo.
pause >nul
goto menu

:exit
cls
echo.
echo ===========================================
echo             再见!
echo ===========================================
echo.
echo 感谢使用智能查寝签到项目
echo 开发者: 龟龟 (您的AI助手)
echo 创建时间: 2026-06-16
echo.
echo 祝您打包成功！🐢
echo.
pause >nul
exit