# 简单脚本查看ModelScope缓存目录
import os

# ModelScope默认缓存目录
DEFAULT_CACHE_DIR = os.path.expanduser("~/.cache/modelscope")

print("=== ModelScope缓存目录信息 ===")
print(f"默认缓存目录: {DEFAULT_CACHE_DIR}")
print(f"目录是否存在: {os.path.exists(DEFAULT_CACHE_DIR)}")

# 检查环境变量
print("\n=== 环境变量 ===")
if 'MODELSCOPE_CACHE' in os.environ:
    print(f"MODELSCOPE_CACHE环境变量: {os.environ['MODELSCOPE_CACHE']}")
else:
    print("MODELSCOPE_CACHE环境变量未设置")

# 检查Hugging Face缓存目录
print("\n=== Hugging Face缓存目录 ===")
try:
    from huggingface_hub import get_cache_dir
    hf_cache = get_cache_dir()
    print(f"Hugging Face默认缓存: {hf_cache}")
except ImportError:
    print("未安装huggingface_hub")
except Exception as e:
    print(f"获取Hugging Face缓存失败: {e}")

# 模型大小信息
print("\n=== 模型大小参考 ===")
print("finbert-base-chinese模型大小约为: 410-450 MB")
print("bert-base-chinese模型大小约为: 390-430 MB")
print("\n=== 手动下载建议 ===")
print("1. 从Hugging Face下载: https://huggingface.co/nghuyong/finbert-base-chinese")
print("2. 下载后解压到任意目录")
print("3. 运行word2vec.py时使用--local_model_path指定该目录")
print("4. 手动指定路径不会缓存到默认目录")
