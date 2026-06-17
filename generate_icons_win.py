#!/usr/bin/env python3
"""
Windows兼容版图标生成工具
使用纯Python生成基础图标（无imagemagick依赖）
"""

import os
from PIL import Image, ImageDraw, ImageFont
import sys

def create_simple_icon():
    """创建简单的应用图标"""
    try:
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # 创建512x512图标
        img = Image.new('RGB', (512, 512), color='#1a237e')
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试加载字体
            font = ImageFont.truetype('arial.ttf', 80)
        except:
            # 如果字体不存在，使用默认字体
            font = ImageFont.load_default()
        
        # 绘制文字
        text = "签到"
        # 获取文字大小
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 居中绘制
        position = ((512 - text_width) // 2, (512 - text_height) // 2)
        draw.text(position, text, fill='white', font=font)
        
        # 保存图标
        img.save('data/icon.png', 'PNG')
        print(f"✅ 图标生成成功: data/icon.png ({img.size})")
        return True
        
    except Exception as e:
        print(f"❌ 图标生成失败: {e}")
        return False

def create_simple_presplash():
    """创建简单的启动画面"""
    try:
        # 创建1024x768启动画面
        img = Image.new('RGB', (1024, 768), color='#1a237e')
        draw = ImageDraw.Draw(img)
        
        try:
            # 尝试加载字体
            font_large = ImageFont.truetype('arial.ttf', 60)
            font_small = ImageFont.truetype('arial.ttf', 30)
        except:
            # 如果字体不存在，使用默认字体
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 绘制标题
        title = "智能查寝签到"
        ver_text = "v1.0.0"
        
        # 获取标题大小
        title_bbox = draw.textbbox((0, 0), title, font=font_large)
        title_width = title_bbox[2] - title_bbox[0]
        
        # 居中绘制标题
        title_position = ((1024 - title_width) // 2, 300)
        draw.text(title_position, title, fill='white', font=font_large)
        
        # 获取版本号大小
        ver_bbox = draw.textbbox((0, 0), ver_text, font=font_small)
        ver_width = ver_bbox[2] - ver_bbox[0]
        
        # 居中绘制版本号
        ver_position = ((1024 - ver_width) // 2, 380)
        draw.text(ver_position, ver_text, fill='#bbdefb', font=font_small)
        
        # 保存启动画面
        img.save('data/presplash.png', 'PNG')
        print(f"✅ 启动画面生成成功: data/presplash.png ({img.size})")
        return True
        
    except Exception as e:
        print(f"❌ 启动画面生成失败: {e}")
        return False

def check_pillow():
    """检查PIL/Pillow是否安装"""
    try:
        from PIL import Image, ImageDraw
        return True
    except ImportError:
        return False

def install_pillow():
    """安装Pillow库"""
    import subprocess
    print("正在安装Pillow库...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
        print("✅ Pillow安装成功")
        return True
    except Exception as e:
        print(f"❌ Pillow安装失败: {e}")
        return False

def create_alternate_icons():
    """创建替代图标（不使用PIL）"""
    # 如果没有PIL，创建简单的文本说明
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # 创建说明文件
    with open('data/README.txt', 'w', encoding='utf-8') as f:
        f.write("应用图标说明\n")
        f.write("=" * 30 + "\n\n")
        f.write("打包APK需要以下图标文件:\n\n")
        f.write("1. icon.png (512x512)\n")
        f.write("   - 应用图标\n")
        f.write("   - 背景色: #1a237e (靛蓝色)\n")
        f.write("   - 文字: 签到 (白色)\n\n")
        f.write("2. presplash.png (1024x768)\n")
        f.write("   - 启动画面\n")
        f.write("   - 背景色: #1a237e (靛蓝色)\n")
        f.write("   - 文字: 智能查寝签到\\nv1.0.0\n\n")
        f.write("您可以使用以下方法创建图标:\n")
        f.write("- 使用在线图标生成网站\n")
        f.write("- 使用Photoshop/GIMP等图像编辑软件\n")
        f.write("- 使用简单的截图+编辑\n\n")
        f.write("图标生成步骤:\n")
        f.write("1. 创建512x512画布，填充靛蓝色(#1a237e)\n")
        f.write("2. 添加白色文字'签到'\n")
        f.write("3. 保存为icon.png\n")
        f.write("4. 重复步骤创建presplash.png (1024x768)\n")
    
    print("📝 已创建图标说明文件: data/README.txt")
    print("请按照说明文件手动创建图标，或安装Pillow库后重新运行此脚本")
    
    return True

def check_files():
    """检查文件结构"""
    print("📁 检查项目文件结构...")
    
    required_files = [
        'main.py',
        'checkin_core.py', 
        'buildozer.spec',
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
    print("   智能查寝签到 - Windows图标生成工具")
    print("   龟龟 (您的AI助手) 2026-06-17")
    print("=" * 50)
    print()
    
    # 检查PIL/Pillow
    has_pillow = check_pillow()
    
    if not has_pillow:
        print("❌ Pillow库未安装")
        print("要自动生成图标，需要安装Pillow图像处理库")
        print()
        install_pillow = input("是否安装Pillow? (y/n): ").strip().lower()
        
        if install_pillow in ['y', 'yes']:
            if not install_pillow():
                print("\n将使用替代方法...\n")
                has_pillow = False
            else:
                has_pillow = True
        else:
            has_pillow = False
    
    print("\n请选择操作：")
    print("1. 自动生成图标 (需要Pillow)")
    print("2. 创建图标说明文件")
    print("3. 检查文件完整性")
    print("4. 查看当前配置")
    print("5. 退出")
    print()
    
    try:
        choice = input("请选择 (1-5): ").strip()
        
        if choice == '1':
            if has_pillow:
                print("\n正在生成图标...")
                # 确保data目录存在
                if not os.path.exists('data'):
                    os.makedirs('data')
                
                success = True
                success = success and create_simple_icon()
                success = success and create_simple_presplash()
                
                if success:
                    print("\n🎉 图标生成完成！")
                    print("现在可以运行打包命令: buildozer android debug")
                    print("或者使用prepare_for_linux.bat准备打包环境")
                else:
                    print("\n⚠️  图标生成遇到问题，请检查错误信息")
            else:
                print("\n❌ 无法生成图标，Pillow库未安装")
                print("请选择选项2创建说明文件，然后手动创建图标")
                print("或重新运行脚本并选择安装Pillow")
                
        elif choice == '2':
            create_alternate_icons()
            print("\n✅ 图标说明文件已创建")
            print("请查看data/README.txt获取详细说明")
            
        elif choice == '3':
            if check_files():
                print("\n✅ 所有必要文件检查通过")
            else:
                print("\n⚠️  部分文件缺失，请补充缺失文件")
                
        elif choice == '4':
            print("\n📋 当前配置:")
            print("-" * 40)
            if os.path.exists('buildozer.spec'):
                try:
                    with open('buildozer.spec', 'r', encoding='utf-8') as f:
                        config_lines = []
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and not line.startswith('['):
                                if '=' in line:
                                    config_lines.append(line)
                                    
                        for config in config_lines[:15]:  # 显示前15行配置
                            print(config)
                except:
                    print("读取配置文件失败")
            else:
                print("❌ buildozer.spec文件不存在")
            print("-" * 40)
            
            # 显示图标配置
            print("\n📱 图标配置:")
            print(f"  Icon: {(os.path.exists('data/icon.png') if os.path.exists('data') else False)}")
            print(f"  Presplash: {(os.path.exists('data/presplash.png') if os.path.exists('data') else False)}")
            print("-" * 40)
            
        elif choice == '5':
            print("\n再见！祝您打包顺利！🐢")
            
        else:
            print("无效的选择")
            
    except KeyboardInterrupt:
        print("\n\n程序已中断")
    
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
    
    finally:
        print()
        print("💡 提示:")
        print("- 要生成APK，需要在Linux/WSL环境中运行")
        print("- Windows用户可以使用：prepare_for_linux.bat")
        print("- 或查看：打包指南.md 获取详细步骤")

if __name__ == '__main__':
    main()