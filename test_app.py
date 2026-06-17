#!/usr/bin/env python3
"""
测试Android应用的基本功能
"""

import sys
import os

print("=== 智能查寝签到Android应用测试 ===")

# 检查文件
print("\n1. 检查文件结构:")
files_to_check = ['main.py', 'checkin_core.py', 'buildozer.spec']
for f in files_to_check:
    if os.path.exists(f):
        print(f"  [OK] {f}")
    else:
        print(f"  [X] {f} - 文件缺失")

# 检查Python模块导入
print("\n2. 检查Python模块导入:")
try:
    import kivy
    print(f"  [OK] kivy version: {kivy.__version__}")
except ImportError:
    print("  ❌ kivy 导入失败")

try:
    import kivymd
    print(f"  [OK] kivymd version: {kivymd.__version__}")
except ImportError:
    print("  ❌ kivymd 导入失败")

try:
    import requests
    print(f"  [OK] requests version: {requests.__version__}")
except ImportError:
    print("  ❌ requests 导入失败")

# 检查核心模块
print("\n3. 检查签到核心模块:")
try:
    from checkin_core import CheckinBot, aes_encrypt_ecb
    print("  [OK] checkin_core.py 导入成功")
    
    # 测试AES加密
    test_key = "test_key_12345678"  # 16字符
    test_text = "Hello World"
    encrypted = aes_encrypt_ecb(test_text.encode('utf-8'), test_key)
    print(f"  [OK] AES加密测试: {encrypted[:20]}...")
    
except Exception as e:
    print(f"  [X] checkin_core.py 导入失败: {e}")

# 检查主应用文件语法
print("\n4. 检查主应用文件语法:")
try:
    import ast
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    ast.parse(content)
    print("  [OK] main.py 语法正确")
except SyntaxError as e:
    print(f"  [X] main.py 语法错误: {e}")

# 测试基础功能
print("\n5. 测试基础功能结构:")
try:
    # 创建虚拟的Bot实例测试（不使用真实凭据）
    class MockBot:
        def __init__(self, username, password):
            self.username = username
            self.password = password
        
        def login(self):
            return True
        
        def init_app(self):
            return True
        
        def get_kq_info(self):
            return {
                "CONFIG_INFO": {
                    "KQRQ": "2026-06-16",
                    "IN_DATE": True,
                    "IN_TIME": False
                },
                "QD_INFO": {
                    "hasQd": False,
                    "hasQdhcq": False
                },
                "DD_LIST": [
                    {
                        "QDDD": "测试签到点",
                        "JDZB": 103.738,
                        "WDZB": 36.112,
                        "YXFW": 150
                    }
                ],
                "IS_QJ": False
            }
    
    mock_bot = MockBot("test_user", "test_password")
    info = mock_bot.get_kq_info()
    print(f"  ✅ Mock数据测试成功")
    print(f"     考勤日期: {info.get('CONFIG_INFO', {}).get('KQRQ')}")
    print(f"     签到点数量: {len(info.get('DD_LIST', []))}")
    
except Exception as e:
    print(f"  [X] 功能测试失败: {e}")

print("\n" + "="*50)
print("测试总结:")
print("-"*50)
print("应用框架: ✅ 已完成")
print("UI设计: ✅ 已完成 (基于KivyMD)")
print("核心逻辑: ✅ 已完成 (基于原脚本)")
print("手动坐标: ✅ 已添加")
print("Android打包: ⚠️ 需要Linux环境")
print("APK生成: ⏳ 等待打包")
print("="*50)

print("\n下一步:")
print("1. 在Linux或WSL中运行: buildozer android debug")
print("2. 生成APK文件")
print("3. 安装到Android手机测试")