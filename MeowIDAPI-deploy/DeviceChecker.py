# -*- coding: utf-8 -*-
"""
PyTorch GPU / CPU 环境检测脚本
改编自开源项目: https://github.com/terenzzzz/MeowID
"""

import torch

# 检查 PyTorch 是否能够识别到 GPU
print(f"Cuda可用: {torch.cuda.is_available()}")  # 如果是 True，说明 GPU 可用
print(f"GPU 设备编号: {torch.cuda.current_device()}")  # 查看当前 GPU 设备编号

# 查看当前 GPU 的详细信息
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"GPU 型号: {torch.cuda.get_device_name(device)}")
print(f"GPU总内存: {torch.cuda.get_device_properties(device).total_memory / 1024**3} GB")
