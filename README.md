# 智能查寝签到 Android App

基于Kivy开发的Android签到应用，将Python签到脚本转换为易用的手机应用。

## 功能特性

- ✅ 用户友好界面
- ✅ 手动坐标输入签到
- ✅ 自动签到（使用默认签到点）
- ✅ 考勤状态查看
- ✅ 签到历史记录
- ✅ Android 15+兼容
- ✅ 纯Python实现，无需额外依赖

## 文件结构

```
android_checkin_app/
├── main.py                    # 主应用程序
├── checkin_core.py            # 签到核心逻辑
├── buildozer.spec             # Buildozer配置文件
├── data/                      # 资源文件
│   ├── icon.png              # 应用图标 (需要添加)
│   └── presplash.png         # 启动画面 (需要添加)
└── README.md                 # 本文件
```

## 如何运行

### 1. 在Windows上测试

```bash
cd android_checkin_app
python main.py
```

### 2. 打包为Android APK

需要Linux或macOS环境：
```bash
# 安装Buildozer依赖
sudo apt update
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 安装Buildozer
pip3 install --user buildozer cython python-for-android

# 打包APK
buildozer android debug
```

### 3. 在手机上安装

1. 将生成的APK文件 (`.buildozer/android/platform/build-arm64-v8a/dists/checkin/checkin-1.0.0-debug.apk`) 复制到手机
2. 在手机上允许安装未知来源的应用
3. 安装并运行

## 配置说明

### buildozer.spec 关键配置：
- `android.minapi = 24`: Android 7.0+支持
- `android.targetapi = 34`: Android 14兼容性
- `android.arch = arm64-v8a`: 支持64位手机
- `android.permissions`: 请求网络权限

## 注意事项

1. **图标需要添加**: 需要添加`data/icon.png` (512x512) 和 `data/presplash.png` (1024x768)
2. **Android打包**: Buildozer需要Linux环境或在WSL2中运行
3. **安全性**: 应用会保存登录凭据在内存中，退出应用后清除
4. **网络要求**: 需要稳定的网络连接执行签到

## 开发日志

- 2026-06-16: 完成Kivy应用框架和UI设计
- 2026-06-16: 适配Python签到脚本核心功能
- 2026-06-16: 添加手动坐标输入功能
- 2026-06-16: 配置Buildozer打包环境

## 作者

龟龟 (为您服务的AI助手)