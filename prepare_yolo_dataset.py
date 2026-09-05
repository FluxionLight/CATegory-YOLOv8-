import os
import shutil
from pathlib import Path

# --- 1. 配置路径 ---
# 你的原始分类数据集的根目录
SOURCE_DATA_ROOT = Path("./CatCategoryData/cat dataset")

# YOLOv8 项目中，新数据集的目标根目录
# 目标结构: F:/YOLOv8/YOLOv8-main/datasets/cat_species
YOLO_PROJECT_ROOT = Path("./YOLOv8/YOLOv8-main/datasets/CatCategory")

# --- 2. 类别定义 (来自前一步的输出) ---
# 严格按照字母顺序或你的自定义顺序
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

def prepare_yolo_structure(source_root: Path, target_root: Path, class_names: list):
    """
    创建 YOLO 目标结构，移动图像文件，并生成配置文件。
    """
    print(f"--- 目标根目录: {target_root} ---")
    
    # 1. 创建所有必要的目录
    for sub_dir in ['images/train', 'images/val', 'labels/train', 'labels/val']:
        (target_root / sub_dir).mkdir(parents=True, exist_ok=True)

    # 2. 复制图像文件
    print("\n--- 正在复制图像文件并重命名以避免冲突 ---")
    
    # 映射：原始文件夹名 -> YOLO 目标文件夹名
    # 用户的 'test' 对应 YOLO 标准的 'val'
    phase_mapping = {
        'train': 'train',
        'test': 'val'
    }

    total_files_moved = 0
    
    for phase_folder, yolo_phase in phase_mapping.items():
        source_phase_dir = source_root / phase_folder
        target_image_dir = target_root / 'images' / yolo_phase
        
        print(f"处理阶段: {phase_folder} -> {yolo_phase}")
        
        # 遍历每个类别文件夹
        for class_name in class_names:
            source_class_dir = source_phase_dir / class_name
            
            if not source_class_dir.exists():
                print(f"警告: 未找到目录 {source_class_dir}，跳过。")
                continue
            
            file_count = 0
            # 遍历类别目录下的所有文件
            for file_name in os.listdir(source_class_dir):
                # 仅处理图片文件
                if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    # 创建新的文件名: 类别名_原文件名
                    new_file_name = f"{class_name}_{file_name}"
                    
                    source_path = source_class_dir / file_name
                    target_path = target_image_dir / new_file_name
                    
                    try:
                        shutil.copy2(source_path, target_path) # copy2 保留元数据
                        file_count += 1
                        total_files_moved += 1
                    except Exception as e:
                        print(f"复制文件失败 {source_path}: {e}")
            
            print(f"  -> {class_name}: 复制 {file_count} 张图片")

    print(f"\n--- 图像复制完成。总共复制 {total_files_moved} 张图片 ---")

    # 3. 生成 classes.txt 文件
    classes_path = target_root / 'classes.txt'
    with open(classes_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(class_names) + '\n')
    print(f"\n--- 生成 classes.txt ({len(class_names)} 个类别) 到 {classes_path} ---")

    # 4. 生成 data.yaml 配置文件
    yaml_content = f"""
# YOLO Datasets Configuration for Cat Species Detection
path: {target_root.as_posix()}  # 数据集根目录 (使用正斜杠以确保跨平台兼容性)

# 训练集和验证集的相对路径 (相对于上面的 path)
train: images/train
val: images/val
# test: images/val # (通常在没有单独测试集时，val 也用作测试集)

# 类别数
nc: {len(class_names)}

# 类别名称
names:
"""
    for i, name in enumerate(class_names):
        yaml_content += f"  {i}: {name}\n"

    yaml_path = target_root / 'data.yaml'
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    print(f"--- 生成 data.yaml 配置文件到 {yaml_path} ---")


if __name__ == "__main__":
    # 检查根路径是否存在
    if not SOURCE_DATA_ROOT.exists():
        print(f"错误：未找到原始数据集根目录: {SOURCE_DATA_ROOT}")
        print("请检查 SOURCE_DATA_ROOT 变量是否配置正确。")
    elif not YOLO_PROJECT_ROOT.parent.exists():
        print(f"错误：未找到 YOLO 目标父目录: {YOLO_PROJECT_ROOT.parent}")
        print("请检查 YOLO_PROJECT_ROOT 变量是否配置正确。")
    else:
        prepare_yolo_structure(SOURCE_DATA_ROOT, YOLO_PROJECT_ROOT, CLASS_NAMES)
        print("\n🎉 所有文件已重组并准备就绪，可以开始标注了！")
        print("\n下一步：使用 LabelImg 等工具，以 'YOLO' 格式为 images/train 和 images/val 中的图片进行标注，并将 .txt 文件保存在对应的 labels/train 和 labels/val 文件夹中。")