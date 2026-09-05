import os
from pathlib import Path

# 定义 classes.txt 的预期路径
CLASSES_FILE_PATH = Path("./YOLOv8/YOLOv8-main/datasets/CatCategory/classes.txt")

# 类别定义 (用于重新生成)
CLASS_NAMES = [
    "Abyssinian", "American Curl", "American Shorthair", "Balinese", "Bengal",
    "Birman", "Bombay", "British Shorthair", "Burmese", "Cornish Rex",
    "Devon Rex", "Egyptian Mau", "Exotic Shorthair", "Extra-Toes Cat - Hemingway Polydactyl",
    "Havana", "Himalayan", "Japanese Bobtail", "Korat", "Maine Coon",
    "Manx", "Nebelung", "Norwegian Forest Cat", "Oriental Short Hair", "Persian",
    "Ragdoll", "Russian Blue", "Scottish Fold", "Selkirk Rex", "Siamese",
    "Siberian", "Snowshoe", "Sphynx", "Tonkinese", "Toyger tiger cat",
    "Turkish Angora"
]

def fix_and_save_classes(filepath: Path, class_list: list):
    """确保 classes.txt 以标准 UTF-8 格式保存，且末尾有空行。"""
    
    # 确保路径存在
    if not filepath.parent.exists():
        print(f"错误：父目录 {filepath.parent} 不存在。请检查路径配置。")
        return

    print(f"--- 正在重新生成 classes.txt 到: {filepath} ---")
    
    # 使用 'w' 模式以 UTF-8 编码写入，确保没有 BOM，并添加末尾换行
    content = "/n".join(class_list) + "/n"
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ classes.txt 已成功使用标准 UTF-8 编码重新保存。")
        print("请尝试重新启动 LabelImg 并打开图像目录。")
    except Exception as e:
        print(f"写入文件失败: {e}")

if __name__ == "__main__":
    # 注意：这里的 CLASSES_FILE_PATH 依赖于你的实际根目录。
    # 我们假设 ./datasets 是你的数据集根目录
    fix_and_save_classes(CLASSES_FILE_PATH, CLASS_NAMES)
