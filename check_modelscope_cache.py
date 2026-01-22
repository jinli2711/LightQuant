import modelscope
from modelscope import snapshot_download
import os

# 查看ModelScope配置信息
print("=== ModelScope配置信息 ===")
print(f"ModelScope版本: {modelscope.__version__}")

# 获取缓存目录
cache_dir = os.path.expanduser(modelscope.config.MODELSCOPE_CACHE)
print(f"默认缓存目录: {cache_dir}")

# 查看环境变量
print("\n=== 相关环境变量 ===")
if 'MODELSCOPE_CACHE' in os.environ:
    print(f"MODELSCOPE_CACHE环境变量: {os.environ['MODELSCOPE_CACHE']}")
else:
    print("MODELSCOPE_CACHE环境变量未设置，使用默认值")

# 尝试获取finbert-base-chinese模型信息
print("\n=== 模型信息 ===")
try:
    # 只下载配置文件来获取模型信息，不下载完整模型
    model_dir = snapshot_download('nghuyong/finbert-base-chinese', cache_dir=cache_dir, revision='master', ignore_file_pattern=['*.bin', '*.pt', '*.model'])
    print(f"模型配置目录: {model_dir}")
    print("模型文件列表:")
    for file in os.listdir(model_dir):
        file_path = os.path.join(model_dir, file)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  {file}: {file_size:.2f} MB")
except Exception as e:
    print(f"获取模型信息失败: {e}")
    print("可能需要完整下载模型才能获取准确大小")

# 查看Hugging Face缓存目录（如果ModelScope使用了Hugging Face后端）
print("\n=== Hugging Face缓存信息 ===")
try:
    from huggingface_hub import get_cache_dir
    hf_cache_dir = get_cache_dir()
    print(f"Hugging Face默认缓存目录: {hf_cache_dir}")
except ImportError:
    print("未安装huggingface_hub库")
