import os
from ultralytics.data.annotator import auto_annotate

# --- 配置参数 ---

# 1. 设置您的图像文件夹路径
IMAGE_DIR = os.path.expanduser("./YOLOv8/YOLOv8-main/datasets/CATegoryChinese/CATimages")

# 2. 设置您的自定义检测模型路径（替换为您自己的路径）
# 将 'path/to/your/best.pt' 替换为您的实际权重文件路径
DET_MODEL = "./YOLOv8/YOLOv8-main/runs/detect/train_VOC/weights/best.pt"

# 3. 设置 SAM 分割模型（用于精修边界，保持稳定版本）
SAM_MODEL = "sam_b.pt"

# --- 关键：设置严格的置信度阈值 ---
# 从 0.25 开始测试，如果仍然有噪声，请提高到 0.4 或 0.5。
CONFIDENCE_THRESHOLD = 0.25

# --- 执行自动标注 ---
print(f"🚀 正在使用自定义 VOC 模型 ({DET_MODEL}) 进行预标注...")

try:
    auto_annotate(
        data=IMAGE_DIR,
        det_model=DET_MODEL,
        sam_model=SAM_MODEL,
        output_dir=None,
        conf=CONFIDENCE_THRESHOLD,
        # 如果您的 VOC 模型只识别一个类别，可以省略 names 参数
        # 否则，您可能需要提供 names= [ 'cat', 'dog', ... ] 列表
    )

    print("✅ 预标注完成！请检查生成的标签文件。")

except Exception as e:
    print(f"❌ 自动标注过程中发生错误: {e}")