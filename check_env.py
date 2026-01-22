# 检查MODELSCOPE_CACHE环境变量是否生效
import os
import sys

print("=== 检查环境变量 ===")
print(f"Python版本: {sys.version}")
print(f"当前进程ID: {os.getpid()}")

# 检查环境变量
if 'MODELSCOPE_CACHE' in os.environ:
    cache_dir = os.environ['MODELSCOPE_CACHE']
    print(f"✅ MODELSCOPE_CACHE环境变量已设置: {cache_dir}")
    print(f"目录是否存在: {os.path.exists(cache_dir)}")
    # 尝试创建目录
    try:
        os.makedirs(cache_dir, exist_ok=True)
        print(f"✅ 目录已创建或已存在")
    except Exception as e:
        print(f"❌ 创建目录失败: {e}")
else:
    print("❌ MODELSCOPE_CACHE环境变量未设置")
    print("使用默认缓存目录: ~/.cache/modelscope")

# 检查modelscope是否已安装
try:
    import modelscope
    print(f"✅ modelscope已安装，版本: {modelscope.__version__}")
except ImportError:
    print("❌ modelscope未安装")
