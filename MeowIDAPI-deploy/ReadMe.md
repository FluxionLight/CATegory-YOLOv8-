# MeowIDAPI-deploy —— 猫咪品种分类 API(ResNet-50)

基于开源项目 [terenzzzz/MeowID](https://github.com/terenzzzz/MeowID)(MIT,见 `LICENSE`)改编的猫咪品种分类服务:
上传猫咪图片 → 识别其所属的 35 个国际品种之一,并返回 Top-4 概率。

## 目录结构

| 文件 | 说明 |
|---|---|
| `app/app.py` | Flask API 入口(默认监听本机 `5000` 端口,路由 `/predictBreed`) |
| `app/predict.py` | 推理封装与 35 品种中英文名称映射 |
| `app/model.pt` | 已训练模型权重(ResNet-50 微调,约 90 MB) |
| `CatBreedClassifier.py` | 训练/评估脚本(ResNet-50 微调,50 epochs) |
| `DeviceChecker.py` | PyTorch CUDA/CPU 环境自检脚本 |

## 快速开始

```bash
# 1. 安装依赖(或直接使用仓库根目录 requirements.txt)
pip install Flask Flask-Cors Pillow numpy tqdm torch torchvision

# 2. 启动 API(默认 http://localhost:5000)
python app/app.py
```

### 调用示例

以表单字段 `file` 上传图片(`.jpg/.jpeg/.png`):

```bash
curl -F "file=@cat.jpg" http://localhost:5000/predictBreed
```

返回 JSON:

```json
{
  "message": "File successfully uploaded and processed",
  "prediction": [
    { "en": "Ragdoll",  "probability": 0.9496, "zh": "布偶猫" },
    { "en": "Birman",   "probability": 0.0346, "zh": "缅甸猫" },
    { "en": "Balinese", "probability": 0.0040, "zh": "巴厘猫" }
  ]
}
```

### 重新训练

```bash
python CatBreedClassifier.py
```

脚本默认使用**仓库根目录** `CatCategoryData/cat dataset`(35 品种分类图片集,train/test 划分)进行训练,
训练过程自动保存最优权重到 `app/model.pt`。

### 部署提示

对外提供服务时请将 API 置于 Nginx/Caddy 等反向代理之后并自行配置 HTTPS 与公网地址,
本仓库不包含任何个人服务器地址、域名或端口配置。

## 致谢

- 原项目: [terenzzzz/MeowID](https://github.com/terenzzzz/MeowID)
- 35 品种图片数据集整理与开源: 见 `../CatCategoryData/README.md`
