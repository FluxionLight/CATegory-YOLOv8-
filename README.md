# CATegory —— 基于 YOLOv8 的猫咪品种检测与识别

「科研实践」课程项目:输入一张猫咪照片,系统可对图中的猫进行**目标检测 + 分割 + 品种识别**,
既支持 35 个国际常见品种,也额外扩充了 4 种中国本土猫(狸花猫、橘猫、奶牛猫、三花猫),
并提供 Web 前端与后端服务在线演示。

> 数据以图片为主,仓库体积较大(约 3 GB),克隆前请注意。

## 系统组成

```
├── CatCategoryData/                  # 35 品种分类图片集(train/test,每品种一类文件夹)
│
├── YOLOv8/
│   ├── YOLOv8-main/                  # YOLOv8 实验目录
│   │   ├── datasets/                 #   各版本检测/分割数据集(见下)
│   │   └── runs/                     #   历次训练产物(权重/args/结果图)
│   ├── SERVER/                       # 检测识别 Web 服务(FastAPI + 2 个已训练权重)
│   └── test/                         # 推理测试图片
│
├── MeowIDAPI-deploy/                 # 分类 API(Flask + ResNet-50,35 品种 Top-4)
├── MeowID-main/                      # Vue3 分类 Web 前端
├── runs/                             # 分割训练记录(部分运行)
│
├── auto_labeling.py                  # 自动标注:VOC 猫检测器 + SAM 预标注(多边形)
├── prepare_yolo_dataset.py           # 分类集 → YOLO 检测集重组(images/train|val)
├── prepare_yaml_chinese.py           # 生成中文标签 data.yaml
├── label_trans.py                    # 自动标注类别 ID(COCO cat 15) → 品种 ID
├── txtlabel_to_json.py               # YOLO txt → LabelMe JSON(人工精修用)
├── fix_classes.py                    # 修复 classes.txt(UTF-8 标准格式)
├── requirements.txt                  # Python 依赖
└── README.md
```

### 数据集版本演进(均在 `YOLOv8/YOLOv8-main/datasets/`)

| 目录 | 内容 |
|---|---|
| `CatCategory/` | 初始 YOLO 结构:由 35 品种分类集复制并按 `品种_原图名` 重命名;`CATimages_auto_annotate_labels/` 为 SAM 自动标注结果,`json_label/` 为 LabelMe 格式 |
| `CATegory/` | 35 类国际品种数据集(约 7,229 张图 / 7,214 份多边形标注),`data.yaml` 为中文标签,检测与分割训练均使用 |
| `CATegoryInternational/` | 英文标签版精修标注集:7,229 张原图,自动标注 6,190 份,人工精修 6,190 份 |
| `CATegoryChinese/` | 中国本土猫(4 类)实验小集:396 张图,自动/精修标注各 362 份 |
| `FinalTrain/` | 最终训练划分:`Chinese/`(4 本土猫,396 张)与 `International/`(35 类,7,229 张),含 `split_data.py` 划分脚本 |

35 类国际品种 + 4 类中国本土猫合计 39 个类别标签。

## 训练产物(`runs/`)

| 权重 | 用途 |
|---|---|
| `runs/detect/train_VOC/weights/best.pt` | VOC 猫检测器(供 `auto_labeling.py` 自动标注) |
| `runs/segment/cat_segmentation_model/…/best.pt` | 35 类分割模型 |
| `runs/segment/{Chinese,International}/…/best.pt` | 中国本土 / 国际品种最终分割模型 |

对外服务的两个最终权重位于 `YOLOv8/SERVER/weights/`: `chinese.pt`(本土 4 类)、`international.pt`(35 类)。

## 数据生产流程

1. `prepare_yolo_dataset.py`:把分类图片集(按品种分目录)复制重组为 YOLO 格式;
2. `labelimg` 等工具人工初标注(数据标签见各数据集 `labels/`);
3. `auto_labeling.py`:用 VOC 猫检测器 + SAM(`sam_b.pt`)批量预标注生成精细轮廓;
   `label_trans.py` 将类别 ID(COCO cat)映射回 35 品种 ID;
4. `txtlabel_to_json.py` → LabelMe 人工修正 `json_label/`;`fix_classes.py` 修复类别表;
5. 训练 YOLOv8 检测 / 分割模型,效果好的版本沉淀为 `FinalTrain/` 最终划分并产出服务权重。

## 使用方法

### 检测识别服务(`YOLOv8/SERVER/`)

```bash
pip install -r requirements.txt   # 或按需安装 ultralytics fastapi uvicorn python-multipart
cd YOLOv8/SERVER
python COMMUNICATE.py             # 监听 0.0.0.0:8000
```

浏览器打开 `http://localhost:8000/` 即可上传图片识别(页面同源调用 `/predict`、`/feedback`)。
对外发布时请自行配置反向代理 / HTTPS / 内网穿透,仓库内不含任何个人公网地址与端口配置。

### 分类 API(`MeowIDAPI-deploy/`)

```bash
cd MeowIDAPI-deploy
python app/app.py                 # Flask,默认 http://localhost:5000
# 重新训练:
python CatBreedClassifier.py      # 默认使用仓库根 CatCategoryData/cat dataset
```

详见其目录内 `ReadMe.md`。前端(`MeowID-main/`,Vue3)通过 `VITE_API_URL` 指定后端地址:

```bash
cd MeowID-main
npm install
npm run dev                       # 默认同源,或设置环境变量 VITE_API_URL
```

### 模型 / 数据来源

- 35 品种分类图片集:`CatCategoryData/README.md` 所列开源数据源(含
  [Aml-Hassan/datasets](https://github.com/Aml-Hassan-Abd-El-hamid) 等)及 Google Images 补充;
- VOC 猫检测器训练数据为 Pascal VOC(公开可下载,仓库未包含);
- 分类模型/API/前端改编自开源项目 [terenzzzz/MeowID](https://github.com/terenzzzz/MeowID)(MIT);
- YOLOv8 部署框架参考 [DataXujing/YOLOv8](https://github.com/DataXujing/YOLOv8);
- 预训练权重(`yolov8n.pt`、`yolov8n-seg.pt`、SAM `sam_b.pt` 等)均可公开下载,仓库未包含,
  运行 `auto_labeling.py` 前请先自行下载。

### 说明

- 仓库已移除本机绝对路径与个人信息;根目录脚本默认在**仓库根目录**下运行。
- 数据集较大且含大量中间版本,请按需克隆。
