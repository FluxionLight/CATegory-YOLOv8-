import os
import shutil
import random
from sklearn.model_selection import train_test_split

# --- 🎯 配置区域 ---
# 数据集根目录
DATASET_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Chinese")

# 原始文件所在的目录（即您当前的文件位置）
# 假设您已经将所有图片和标签移动到各自的根目录（images/ 和 labels/）
IMAGES_SOURCE = os.path.join(DATASET_ROOT, 'images')
LABELS_SOURCE = os.path.join(DATASET_ROOT, 'labels')

# 划分比例 (80% 训练集, 20% 验证集)
SPLIT_RATIO = 0.2


# --- 核心逻辑 ---

def split_dataset(images_dir, labels_dir, split_ratio):
    # 1. 获取所有图片文件名 (不带扩展名)
    all_images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    all_filenames = [os.path.splitext(f)[0] for f in all_images]

    if not all_filenames:
        print("❌ 错误：images 目录中没有找到任何图片文件。")
        return

    # 2. 划分文件名列表
    train_names, val_names = train_test_split(
        all_filenames,
        test_size=split_ratio,
        random_state=42  # 确保每次划分结果一致
    )

    print(f"✅ 数据集划分完成：训练集 {len(train_names)} 张，验证集 {len(val_names)} 张。")

    # 3. 创建目标目录
    for subset in ['train', 'val']:
        os.makedirs(os.path.join(images_dir, subset), exist_ok=True)
        os.makedirs(os.path.join(labels_dir, subset), exist_ok=True)

    # 4. 移动文件
    for names, subset in zip([train_names, val_names], ['train', 'val']):
        for name in names:
            # 移动图片
            image_src = os.path.join(images_dir, name + os.path.splitext(all_images[all_filenames.index(name)])[1])
            image_dst = os.path.join(images_dir, subset, os.path.basename(image_src))
            shutil.move(image_src, image_dst)

            # 移动标签
            label_src = os.path.join(labels_dir, name + '.txt')
            label_dst = os.path.join(labels_dir, subset, name + '.txt')
            if os.path.exists(label_src):
                shutil.move(label_src, label_dst)
            else:
                print(f"⚠️ 警告：标签文件 {name}.txt 未找到，跳过移动。")

    print("\n✨ 文件移动和数据集划分完成！")


if __name__ == "__main__":
    # 需要先安装 scikit-learn
    # pip install scikit-learn

    # 假设您的所有图片在 images/ 下，标签在 labels/ 下（即运行前的状态）
    split_dataset(IMAGES_SOURCE, LABELS_SOURCE, SPLIT_RATIO)