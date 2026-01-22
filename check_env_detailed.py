# 详细检查环境变量设置
import os
import sys
import subprocess

print("=== 环境变量详细检查 ===")
print(f"Python版本: {sys.version}")
print(f"Python路径: {sys.executable}")
print(f"当前工作目录: {os.getcwd()}")
print(f"当前进程ID: {os.getpid()}")

# 1. 检查Python进程中的环境变量
print("\n1. Python进程环境变量:")
if 'MODELSCOPE_CACHE' in os.environ:
    print(f"✅ MODELSCOPE_CACHE: {os.environ['MODELSCOPE_CACHE']}")
else:
    print("❌ MODELSCOPE_CACHE: 未设置")

# 2. 检查系统环境变量（通过cmd命令）
print("\n2. 系统环境变量（通过cmd查询）:")
try:
    result = subprocess.run('echo %MODELSCOPE_CACHE%', shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    if output and output != '%MODELSCOPE_CACHE%':
        print(f"✅ 系统环境变量: {output}")
    else:
        print("❌ 系统环境变量: 未设置或未生效")
    print(f"   命令返回值: {result.returncode}")
except Exception as e:
    print(f"❌ 查询失败: {e}")

# 3. 检查所有用户环境变量
print("\n3. 所有用户环境变量（部分）:")
user_vars = {k: v for k, v in os.environ.items() if not k.startswith('_')}
for var in sorted(user_vars.keys()):
    if 'CACHE' in var.upper() or 'MODEL' in var.upper():
        print(f"   {var}: {user_vars[var]}")

# 4. 检查modelscope配置
print("\n4. ModelScope配置:")
try:
    import modelscope
    print(f"✅ ModelScope版本: {modelscope.__version__}")
    
    # 检查modelscope内部配置
    try:
        from modelscope import config
        print(f"   内部配置缓存目录: {config.MODELSCOPE_CACHE}")
        print(f"   扩展后路径: {os.path.expanduser(config.MODELSCOPE_CACHE)}")
    except Exception as e:
        print(f"   获取内部配置失败: {e}")
        
    # 检查snapshot_download函数行为
    try:
        from modelscope import snapshot_download
        print(f"   snapshot_download函数可用")
    except Exception as e:
        print(f"   snapshot_download函数不可用: {e}")
except ImportError:
    print("❌ ModelScope未安装")

# 5. 提供解决方案
print("\n=== 解决方案建议 ===")
print("1. 检查环境变量设置是否正确:")
print("   - 打开'系统属性' -> '高级' -> '环境变量'")
print("   - 在'用户变量'中检查MODELSCOPE_CACHE设置")
print("   - 确保变量名和值都正确，没有多余空格")

print("\n2. 重启计算机:")
print("   - 有时Windows需要重启才能使新环境变量完全生效")

print("\n3. 手动在终端设置:")
print("   set MODELSCOPE_CACHE=E:\\cache\\ModelScope_Cache")

print("\n4. 在Python代码中临时设置:")
print("   import os")
print("   os.environ['MODELSCOPE_CACHE'] = 'E:\\cache\\ModelScope_Cache'")
print("   # 然后再导入modelscope")

print("\n5. 直接在word2vec.py中添加:")
print("   在word2vec.py顶部添加:")
print("   import os")
print("   os.environ['MODELSCOPE_CACHE'] = 'E:\\cache\\ModelScope_Cache'")
