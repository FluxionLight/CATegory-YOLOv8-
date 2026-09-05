import yaml
from pathlib import Path

# --- 1. 配置路径 ---
# YOLOv8 项目中，新数据集的目标根目录
YOLO_DATASET_ROOT = Path("./YOLOv8/YOLOv8-main/datasets/CatCategory")
YAML_OUTPUT_PATH = YOLO_DATASET_ROOT / 'data.yaml'

# --- 2. 类别定义 (中英对照) ---
# 严格按照英文类名的顺序 (索引 0-34) 进行中文翻译
# 注意：YOLO 模型只认索引 (0, 1, 2...)，不认名字
CHINESE_CLASS_NAMES = [
    "阿比西尼亚猫", "美国卷耳猫", "美国短毛猫", "巴厘猫", "孟加拉猫",
    "伯曼猫", "孟买猫", "英国短毛猫", "缅甸猫", "柯尼斯雷克斯猫",
    "德文雷克斯猫", "埃及猫", "异国短毛猫", "多趾猫-海明威多趾猫",
    "哈瓦那猫", "喜马拉雅猫", "日本短尾猫", "科拉特猫", "缅因猫",
    "曼岛猫", "内华达森林猫", "挪威森林猫", "东方短毛猫", "波斯猫",
    "布偶猫", "俄罗斯蓝猫", "苏格兰折耳猫", "塞尔凯克卷毛猫", "暹罗猫",
    "西伯利亚猫", "雪鞋猫", "斯芬克斯猫 (无毛猫)", "东奇尼猫", "虎斑猫",
    "土耳其安哥拉猫"
]

def generate_yaml_config(names_list: list, output_path: Path):
    """生成符合 YOLO 格式的 data.yaml 文件。"""
    
    # 类别字典 (索引: 名称)
    names_dict = {i: name for i, name in enumerate(names_list)}
    
    # YOLO 配置文件内容
    data_config = {
        'path': YOLO_DATASET_ROOT.as_posix(),
        'train': 'images/train',
        'val': 'images/val',
        'nc': len(names_list),
        'names': names_dict
    }

    print(f"--- 类别数 nc: {data_config['nc']} ---")
    
    # 使用 YAML 库写入文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data_config, f, allow_unicode=True, sort_keys=False)
        print(f"🎉 成功生成 data.yaml (含中文标签) 到: {output_path}")
        print("/n您可以使用此文件启动 YOLO 训练。训练结果和预测显示将使用中文标签。")
    except Exception as e:
        print(f"写入 YAML 文件失败: {e}")
        print("请确保已安装 PyYAML 库: pip install pyyaml")


if __name__ == "__main__":
    if not YOLO_DATASET_ROOT.exists():
        print(f"错误：数据集根目录 {YOLO_DATASET_ROOT} 不存在。请检查路径。")
    else:
        generate_yaml_config(CHINESE_CLASS_NAMES, YAML_OUTPUT_PATH)
