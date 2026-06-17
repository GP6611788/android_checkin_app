#!/bin/bash
# 智能查寝签到 - 快速打包脚本
# 在Linux/WSL中运行

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  智能查寝签到 APK 快速打包脚本"
echo "  作者：龟龟 (您的AI助手)"
echo "=========================================="

# 配置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在Linux/WSL中
if [[ "$(uname -s)" != "Linux" ]]; then
    log_error "本脚本需要在Linux或WSL环境中运行！"
    log_warn "请在Windows上安装WSL2："
    log_warn "  1. 以管理员身份打开PowerShell"
    log_warn "  2. 运行: wsl --install Ubuntu"
    log_warn "  3. 重新启动电脑"
    exit 1
fi

# 检查Python3
if ! command -v python3 &> /dev/null; then
    log_error "Python3未安装！"
    sudo apt update
    sudo apt install -y python3 python3-pip
fi

# 检查Java
if ! command -v java &> /dev/null; then
    log_warn "Java未安装，正在安装OpenJDK 11..."
    sudo apt install -y openjdk-11-jdk
fi

# 安装必要依赖
log_info "正在安装系统依赖..."
sudo apt update
sudo apt install -y \
    git zip unzip \
    autoconf libtool pkg-config \
    zlib1g-dev libncurses5-dev libncursesw5-dev \
    libtinfo5 cmake libffi-dev libssl-dev \
    ninja-build python3-venv cython3

# 创建项目目录
PROJECT_DIR="$HOME/android_checkin_project"
log_info "创建项目目录: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"

# 复制项目文件（假设文件在当前目录）
log_info "复制项目文件..."
cp_main="main.py checkin_core.py buildozer.spec README.md 打包指南.md 2>/dev/null || true"
eval cp -v $cp_main "$PROJECT_DIR/"

# 创建data目录和图标文件
log_info "创建图标文件..."
mkdir -p "$PROJECT_DIR/data"
if [ ! -f "$PROJECT_DIR/data/icon.png" ]; then
    echo -e "${YELLOW}[注意]${NC} 没有找到icon.png，使用默认图标"
    # 这里应该添加真正的PNG图标文件
    # 暂时创建占位符
    convert -size 512x512 xc:#1a237e -fill white -pointsize 50 -gravity center -draw "text 0,0 '签到'" "$PROJECT_DIR/data/icon.png" 2>/dev/null || \
    echo "需要安装imagemagick来生成图标，或手动添加icon.png文件到data目录"
fi

if [ ! -f "$PROJECT_DIR/data/presplash.png" ]; then
    echo -e "${YELLOW}[注意]${NC} 没有找到presplash.png，使用默认启动画面"
    convert -size 1024x768 xc:#1a237e -fill white -pointsize 60 -gravity center -draw "text 0,0 '智能查寝签到\nv1.0.0'" "$PROJECT_DIR/data/presplash.png" 2>/dev/null || \
    echo "需要安装imagemagick来生成启动画面，或手动添加presplash.png文件到data目录"
fi

# 进入项目目录
cd "$PROJECT_DIR"
log_info "当前目录: $(pwd)"

# 设置环境变量
log_info "设置环境变量..."
export ANDROID_HOME="$HOME/android-sdk"
export ANDROID_SDK_ROOT="$ANDROID_HOME"
export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools"

# 检查Android SDK
if [ ! -d "$ANDROID_HOME" ]; then
    log_warn "Android SDK未安装，准备安装..."
    
    # 下载Android Command Line Tools
    log_info "下载Android Command Line Tools..."
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip
    
    # 解压
    mkdir -p "$ANDROID_HOME/cmdline-tools"
    unzip -q cmdline-tools.zip -d "$ANDROID_HOME/cmdline-tools"
    mv "$ANDROID_HOME/cmdline-tools/cmdline-tools" "$ANDROID_HOME/cmdline-tools/latest"
    rm cmdline-tools.zip
    
    # 接受许可证
    log_info "接受Android SDK许可证..."
    yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --licenses > /dev/null 2>&1 || true
    
    # 安装必要组件
    log_info "安装Android SDK组件（这可能需要一些时间）..."
    "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" \
        "platform-tools" \
        "platforms;android-34" \
        "build-tools;34.0.0" \
        "ndk;23.2.8568313" > /dev/null 2>&1 &
    
    SDK_PID=$!
    echo -n "正在安装Android SDK组件，请稍候"
    while kill -0 $SDK_PID 2>/dev/null; do
        echo -n "."
        sleep 5
    done
    echo " 完成！"
else
    log_info "Android SDK已安装: $ANDROID_HOME"
fi

# 安装Buildozer和Python依赖
log_info "安装Buildozer和Python依赖..."
pip3 install --upgrade pip wheel setuptools > /dev/null 2>&1
pip3 install buildozer cython python-for-android > /dev/null 2>&1

# 初始化Buildozer
if [ ! -f "buildozer.spec" ]; then
    log_info "初始化Buildozer配置..."
    buildozer init
else
    log_info "使用现有的buildozer.spec配置文件"
fi

# 显示配置摘要
log_info "配置摘要:"
echo "------------------------------------------"
grep -E "^(title|package\.name|version|android\.)" buildozer.spec | head -10
echo "------------------------------------------"

# 询问是否继续构建
read -p "是否继续构建APK？(y/N): " continue_build
if [[ ! "$continue_build" =~ ^[Yy]$ ]]; then
    log_info "已停止构建。您可以在 $PROJECT_DIR 目录中手动运行："
    log_info "  buildozer android debug"
    exit 0
fi

# 清理旧构建
log_info "清理旧构建..."
buildozer android clean

# 开始构建
log_info "开始构建APK（第一次构建需要较长时间，请耐心等待）..."
log_warn "构建过程可能需要30-60分钟，取决于网络和系统性能"
log_warn "您可以在另一个终端中运行以下命令查看进度："
log_warn "  tail -f $PROJECT_DIR/.buildozer/android/platform/build-*/build-output.txt"

# 运行构建
start_time=$(date +%s)
buildozer android debug
end_time=$(date +%s)

# 计算构建时间
build_time=$((end_time - start_time))
build_minutes=$((build_time / 60))
build_seconds=$((build_time % 60))

# 查找生成的APK文件
if find .buildozer -name "*.apk" 2>/dev/null | grep -q .; then
    APK_FILE=$(find .buildozer -name "*.apk" | head -1)
    log_info "🎉 APK构建成功！"
    log_info "构建时间: ${build_minutes}分${build_seconds}秒"
    log_info "APK文件: $APK_FILE"
    
    # 复制到当前目录
    cp "$APK_FILE" ./checkin_app.apk
    file_size=$(du -h checkin_app.apk | cut -f1)
    log_info "已复制到: $(pwd)/checkin_app.apk (大小: $file_size)"
    
    echo ""
    echo "=========================================="
    echo "📱 如何安装和使用："
    echo "=========================================="
    echo ""
    echo "1. 安装到手机:"
    echo "   adb install checkin_app.apk"
    echo ""
    echo "2. 手动安装："
    echo "   - 将APK文件复制到手机"
    echo "   - 在手机上打开文件管理器"
    echo "   - 点击APK文件安装"
    echo "   - 允许'安装未知来源应用'"
    echo ""
    echo "3. 应用信息："
    echo "   - 名称: 智能查寝签到"
    echo "   - 包名: com.gsupl.checkin"
    echo "   - 版本: 1.0.0"
    echo "   - 目标Android: 7.0 - 14+"
    echo ""
    echo "4. 测试功能："
    echo "   - 登录界面 (支持仅查看模式)"
    echo "   - 考勤状态查看"
    echo "   - 手动坐标签到"
    echo "   - 签到历史记录"
    echo ""
    echo "=========================================="
else
    log_error "APK构建失败！"
    log_warn "请查看构建日志："
    log_warn "  tail -100 .buildozer/android/platform/build-arm64-v8a/build-output.txt"
    log_warn "常见问题："
    log_warn "  1. 内存不足 - 检查系统内存"
    log_warn "  2. 网络问题 - 检查网络连接"
    log_warn "  3. 依赖缺失 - 重新运行脚本"
    log_warn "  4. SDK问题 - 检查Android SDK安装"
fi

echo ""
log_info "项目文件位置: $PROJECT_DIR"
log_info "详细指南: $PROJECT_DIR/打包指南.md"
log_info "如有问题，请截图错误信息发给我！"