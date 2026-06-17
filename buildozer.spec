[app]

# 应用信息
title = 智能查寝签到
package.name = com.gsupl.checkin
package.domain = com.gsupl
version = 1.0.0

# 源文件
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,bmp
source.exclude_exts = spec
source.exclude_dirs = tests, bin, .buildozer

# Android配置
android.ndk = 23c
android.sdk = 30
android.arch = arm64-v8a
android.archs = arm64-v8a, armeabi-v7a
android.minapi = 24  # Android 7.0
android.targetapi = 34  # Android 14
android.gradle_dependencies = 
android.enable_androidx = True
android.permissions = INTERNET, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE, WAKE_LOCK
android.entrypoint = org.kivy.android.PythonActivity
android.accept_sdk_license = True

# 图标和启动画面
icon.filename = %(source.dir)s/data/icon.png
presplash.filename = %(source.dir)s/data/presplash.png

# 编译配置
osx.python_version = 3
osx.kivy_version = 2.0.0
p4a.branch = develop
p4a.bootstrap = sdl2
p4a.local_recipes = 

# Kivy配置
requirements = python3==3.12.2, kivy==2.3.0, kivymd==1.2.0, requests, pillow, certifi, urllib3, charset-normalizer, idna

# 构建选项
build.pattern = ignore
blacklist = dist, __pycache__, *.pyc, cover, .git, .github
log_level = 2
warn_on_root = 1

# 打包选项
fullscreen = 0
orientation = portrait
window.maximum = 0

# Cython编译选项
android.add_src = 
android.add_resources = 
android.add_assets = 
android.add_jars = 
android.add_aars = 

# 日志配置
log_level = 0
log_format = %(color)s[%(levelname)s]%(color_normal)s %(message)s
log_filters = INFO:python, INFO:kivy

# 测试配置
android.testrunner = 
android.test_package = 

# 自定义参数
android.api = 34
android.ndk_api = 24
android.minapi = 24
android.gradle_dependencies = 

[buildozer]
# 构建目录
log_dir = %(source.dir)s/.buildozer/log
bin_dir = %(source.dir)s/.buildozer/bin
build_dir = %(source.dir)s/.buildozer/build
dist_dir = %(source.dir)s/.buildozer/dist
platform_dir = %(source.dir)s/.buildozer/platform
global_cache_dir = %(source.dir)s/.buildozer/.cache

# 构建缓存
cache = True
cache_mode = all
cache_size = 1024

# 网络配置
http_proxy = 
https_proxy = 
no_proxy = 

# 调试选项
wifi_ssid = 
wifi_password = 
android.release = 0
android.private_storage = True
android.library_references =