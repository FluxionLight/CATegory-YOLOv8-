import os
from pathlib import Path

# --- 配置区域 ---
classes_file = './CATegoryChinese/classes.txt'  # 类别定义文件
labels_src = './CATegoryChinese\CATimages_auto_annotate_labels'  # 原始标签文件夹
labels_dest = './CATegoryChinese\labels_final'  # 转换后的文件夹

# 创建输出目录
os.makedirs(labels_dest, exist_ok=True)

# 1. 构建类别映射表 (Name -> Index)
class_to_idx = {}
try:
    with open(classes_file, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            name = line.strip()
            if name:
                class_to_idx[name] = str(idx)
    print(f"✅ 成功加载类别表，共 {len(class_to_idx)} 类。")
except FileNotFoundError:
    print(f"❌ 错误：找不到 {classes_file}")
    exit()

# 2. 遍历执行：清洗（仅保留7）+ 转换（映射新ID）
processed_count = 0

for file_name in os.listdir(labels_src):
    if not file_name.endswith('.txt') or file_name == 'classes.txt':
        continue

    # --- 核心逻辑修改：单纯以下划线前作为名称 ---
    # 示例: "Abyssinian_109.txt" -> "Abyssinian"
    breed_name = file_name.split('_')[0]

    if breed_name in class_to_idx:
        target_idx = class_to_idx[breed_name]
        src_path = os.path.join(labels_src, file_name)
        dest_path = os.path.join(labels_dest, file_name)

        with open(src_path, 'r') as f_in, open(dest_path, 'w') as f_out:
            for line in f_in:
                parts = line.strip().split()
                if not parts:
                    continue

                # 只有当原始标号为 '7' 时才进行转换并写入
                if parts[0] == '7':
                    parts[0] = target_idx
                    f_out.write(" ".join(parts) + "\n")

        processed_count += 1
    else:
        # 如果下划线前的内容在 classes.txt 里找不到，会在这里提示
        print(f"⚠️ 跳过文件: {file_name} (提取到的品种 '{breed_name}' 不在列表中)")

print(f"---")
print(f"🚀 处理完成！")
print(f"已处理并保存到: {labels_dest}")
print(f"总计成功转换: {processed_count} 个文件")
print(f"结果已存入: {labels_dest}")