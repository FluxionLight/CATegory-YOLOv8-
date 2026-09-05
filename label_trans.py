import os
import re

# --- 🎯 配置区域：请根据您的实际路径和数据进行修改 ---

# 1. 您的标签文件所在的目录
LABELS_DIR = os.path.expanduser("./YOLOv8/YOLOv8-main/datasets/CatCategory/CATimages_auto_annotate_labels")

# 2. 您的类别文件路径（包含所有猫咪品种名称，每行一个）
CLASSES_FILE_PATH = os.path.expanduser("./YOLOv8/YOLOv8-main/datasets/CatCategory/classes.txt")

# 3. 预标注中的原始猫咪 ID (COCO 的猫 ID)
OLD_CAT_ID = "15"


# --- 辅助函数：提取文件名中的类别名称 ---
def extract_class_name_from_filename(filename):
    """
    从文件名中提取第一个下划线分隔的名称字段。
    示例: 'Abyssinian_Abyssinian_109.txt' -> 'Abyssinian'
    """
    # 移除文件扩展名 .txt
    base_name = os.path.splitext(filename)[0]

    # 尝试根据第一个下划线分割
    parts = base_name.split('_')

    # 我们假设第一个字段就是品种名称
    if parts:
        return parts[0]
    return None


# --- 核心转换逻辑 ---
def batch_convert_class_ids():
    # 1. 加载类别映射表
    try:
        with open(CLASSES_FILE_PATH, 'r', encoding='utf-8') as f:
            # 去除空白行和首尾空格
            class_names = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ 错误：未找到类别文件在路径: {CLASSES_FILE_PATH}")
        return

    # 创建 名称 -> ID 索引 的映射字典
    name_to_id = {name: str(i) for i, name in enumerate(class_names)}
    print("✅ 类别映射表已创建:")
    for name, idx in name_to_id.items():
        print(f"   {name} -> {idx}")
    print("-" * 30)

    # 2. 遍历标签文件并执行替换
    files_processed = 0
    ids_changed_count = 0

    for filename in os.listdir(LABELS_DIR):
        if filename.endswith(".txt"):

            # 从文件名中获取目标类别名称
            class_name = extract_class_name_from_filename(filename)

            if class_name not in name_to_id:
                # 警告：如果文件名中的名称不在 classes.txt 中
                print(f"⚠️ 警告：文件名 '{filename}' 中的类别 '{class_name}' 未在 classes.txt 中找到，跳过。")
                continue

            # 获取新的类别 ID (字符串类型)
            new_id = name_to_id[class_name]
            filepath = os.path.join(LABELS_DIR, filename)

            with open(filepath, 'r') as f:
                lines = f.readlines()

            new_lines = []
            file_modified = False

            for line in lines:
                parts = line.split()
                if parts and parts[0] == OLD_CAT_ID:
                    # 替换类别 ID
                    parts[0] = new_id
                    new_lines.append(" ".join(parts) + "\n")
                    file_modified = True
                    ids_changed_count += 1
                else:
                    new_lines.append(line)

            # 3. 写回文件
            if file_modified:
                with open(filepath, 'w') as f:
                    f.writelines(new_lines)
                files_processed += 1
                # print(f"  → 修正 {filename}: ID {OLD_CAT_ID} -> {new_id} ({class_name})")

    print("\n" + "=" * 40)
    print(f"✨ 转换完成！共处理 {files_processed} 个标签文件。")
    print(f"总计替换了 {ids_changed_count} 个类别 ID。")
    print("请检查您的标签文件是否已成功转换为新的品种 ID。")


if __name__ == "__main__":
    batch_convert_class_ids()