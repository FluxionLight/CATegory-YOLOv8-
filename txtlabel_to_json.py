import os
import json
from PIL import Image


# 假设您的数据结构如下：
# images/
#   img1.jpg
# labels/
#   img1.txt

def yolo_to_labelme(img_folder, label_folder, output_folder):
    """
    将 YOLO 分割标注文件 (.txt) 转换为 Labelme 格式 (.json)
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for txt_file in os.listdir(label_folder):
        if not txt_file.endswith('.txt'):
            continue

        base_name = os.path.splitext(txt_file)[0]
        img_path = os.path.join(img_folder, base_name + '.jpg')
        txt_path = os.path.join(label_folder, txt_file)
        json_path = os.path.join(output_folder, base_name + '.json')

        if not os.path.exists(img_path):
            print(f"Warning: Image not found for {txt_file}")
            continue

        try:
            # 1. 获取图像尺寸
            img = Image.open(img_path)
            img_w, img_h = img.size
        except Exception as e:
            print(f"Error opening image {img_path}: {e}")
            continue

        labelme_data = {
            "version": "5.0.1",  # Labelme 版本号
            "flags": {},
            "shapes": [],
            "imagePath": os.path.join("..", img_folder, base_name + ".jpg"),  # 相对路径
            "imageData": None,
            "imageHeight": img_h,
            "imageWidth": img_w
        }

        # 2. 读取 YOLO TXT 文件
        with open(txt_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            parts = list(map(float, line.strip().split()))
            if not parts:
                continue

            # 假设类别 ID 0 对应标签 'cat'
            class_id = int(parts[0])
            # YOLO 坐标是归一化的 (0到1)，需要转换回像素坐标
            normalized_points = parts[1:]

            points = []
            for i in range(0, len(normalized_points), 2):
                x_normalized = normalized_points[i]
                y_normalized = normalized_points[i + 1]

                # 转换为像素坐标
                x_pixel = round(x_normalized * img_w)
                y_pixel = round(y_normalized * img_h)
                points.append([x_pixel, y_pixel])

            shape = {
                "label": f"class_{class_id}",  # 您需要根据您的 data.yaml 映射实际的类别名称
                "points": points,
                "group_id": None,
                "shape_type": "polygon",
                "flags": {}
            }
            labelme_data["shapes"].append(shape)

        # 3. 写入 Labelme JSON 文件
        with open(json_path, 'w') as out_f:
            json.dump(labelme_data, out_f, indent=4)

        print(f"Converted {txt_file} to {base_name}.json")


# --- 运行配置 ---
# 确保路径与您的实际数据集结构一致！
# 您的 cat_segmentation_model 数据集结构可能如下:
IMG_DIR = './YOLOv8/YOLOv8-main/datasets/CatCategory/CATimages'
LABEL_DIR = './YOLOv8/YOLOv8-main/datasets/CatCategory/CATimages_auto_annotate_labels'
OUTPUT_DIR = './YOLOv8/YOLOv8-main/datasets/CatCategory/json_label'

# 运行转换函数
yolo_to_labelme(IMG_DIR, LABEL_DIR, OUTPUT_DIR)