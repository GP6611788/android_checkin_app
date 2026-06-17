#!/usr/bin/env python3
"""
生成应用图标和启动画面
在Linux/WSL中运行，需要imagemagick依赖
"""

import sys
import os
import subprocess

def check_imagemagick():
    """检查imagemagick是否安装"""
    try:
        subprocess.run(['convert', '-version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_icon():
    """创建应用图标"""
    print("生成应用图标 (512x512)...")
    cmd = [
        'convert',
        '-size', '512x512',
        'xc:#1a237e',  # 背景色: 靛蓝色
        '-fill', 'white',
        '-pointsize', '50',
        '-gravity', 'center',
        '-draw', 'text 0,0 "签到"',
        '-font', 'arial',
        'data/icon.png'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 图标生成成功: data/icon.png")
    except subprocess.CalledProcessError as e:
        print(f"❌ 图标生成失败: {e}")
        return False
    return True

def create_presplash():
    """创建启动画面"""
    print("生成启动画面 (1024x768)...")
    cmd = [
        'convert',
        '-size', '1024x768',
        'xc:#1a237e',  # 背景色: 靛蓝色
        '-fill', 'white',
        '-pointsize', '60',
        '-gravity', 'center',
        '-draw', 'text 0,0 "智能查寝签到\nv1.0.0"',
        '-font', 'arial',
        'data/presplash.png'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ 启动画面生成成功: data/presplash.png")
    except subprocess.CalledProcessError as e:
        print(f"❌ 启动画面生成失败: {e}")
        return False
    return True

def create_test_images():
    """创建测试用的图像文件"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print("需要imagemagick来生成图像文件...")
    if not check_imagemagick():
        print("安装imagemagick:")
        print("  Ubuntu/Debian: sudo apt install imagemagick")
        print("  macOS: brew install imagemagick")
        print("  CentOS/RHEL: sudo yum install ImageMagick")
        return False
    
    success = True
    if not os.path.exists('data/icon.png'):
        success = success and create_icon()
    
    if not os.path.exists('data/presplash.png'):
        success = success and create_presplash()
    
    return success

def check_files():
    """检查文件结构"""
    print("📁 检查项目文件结构...")
    
    required_files = [
        'main.py',
        'checkin_core.py', 
        'buildozer.spec',
        'quick_start.sh'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (缺失)")
            all_ok = False
    
    print("\n📱 检查图标文件...")
    if not os.path.exists('data'):
        print("  ❌ data目录不存在")
        all_ok = False
    else:
        icon_files = ['icon.png', 'presplash.png']
        for icon in icon_files:
            icon_path = os.path.join('data', icon)
            if os.path.exists(icon_path):
                print(f"  ✅ {icon_path}")
            else:
                print(f"  ❌ {icon_path} (缺失)")
                all_ok = False
    
    return all_ok

def main():
    print("=" * 50)
    print("   智能查寝签到 - 图标生成工具")
    print("   龟龟 (您的AI助手) 2026-06-16")
    print("=" * 50)
    print()
    
    # 检查当前操作系统
    if sys.platform != 'linux':
        print("⚠️  建议在Linux/WSL中运行此脚本")
        print("   图标生成需要imagemagick，在Windows上可能无法正常工作")
        print()
    
    # 创建data目录
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📁 创建data目录")
    
    print("请选择操作：")
    print("1. 生成图标和启动画面 (需要imagemagick)")
    print("2. 检查文件完整性")
    print("3. 查看配置摘要")
    print("4. 退出")
    print()
    
    try:
        choice = input("请选择 (1-4): ").strip()
        
        if choice == '1':
            if create_test_images():
                print("\n🎉 图标生成完成！")
                print("现在可以运行打包命令: buildozer android debug")
            else:
                print("\n❌ 图标生成失败，请手动添加图标文件")
                
        elif choice == '2':
            if check_files():
                print("\n✅ 所有文件检查通过，可以开始打包！")
            else:
                print("\n⚠️  部分文件缺失，请补充缺失文件")
                
        elif choice == '3':
            print("\n📋 配置摘要:")
            print("-" * 40)
            if os.path.exists('buildozer.spec'):
                with open('buildozer.spec', 'r') as f:
                    lines = f.readlines()
                    display_lines = []
                    for line in lines:
                        line = line.strip()
                        if line.startswith('#') or not line:
                            continue
                        if any(keyword in line for keyword in ['title', 'package', 'version', 'android']):
                            display_lines.append(line)
                            if len(display_lines) >= 15:
                                break
                    for line in display_lines:
                        print(line)
            else:
                print("buildozer.spec 文件不存在")
            print("-" * 40)
            
        elif choice == '4':
            print("退出程序")
            
        else:
            print("无效的选择")
            
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    
    print("\n详细打包指南请查看:")
    print("  - 打包指南.md (详细的打包步骤)")
    print("  - quick_start.sh (快速打包脚本，在Linux中运行)")
    print("  - prepare_for_linux.bat (Windows准备脚本)")

if __name__ == '__main__':
    main()