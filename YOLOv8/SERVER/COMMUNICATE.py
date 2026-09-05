from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import uvicorn
import os
import shutil
import time

app = FastAPI()

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models = {
    "domestic": YOLO("weights/chinese.pt"),
    "international": YOLO("weights/international.pt")
}


# --- 2. 接口：图片识别 (带 NMS 极大值抑制) ---
@app.post("/predict")
async def predict(file: UploadFile = File(...), model_type: str = Form("domestic")):
    current_model = models.get(model_type, models["domestic"])

    temp_file = f"temp_{int(time.time())}_{file.filename}"
    with open(temp_file, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # conf=0.25: 基本门槛; iou=0.45: 极大值抑制，过滤重叠率超过45%的框
    results = current_model.predict(source=temp_file, conf=0.2, iou=0.9)

    predictions = []
    for r in results:
        # 按置信度从高到低排序，确保 ID #1 是最准的那只
        boxes = sorted(r.boxes, key=lambda x: x.conf.item(), reverse=True)
        for i, box in enumerate(boxes):
            predictions.append({
                "id": i + 1,
                "box": [int(x) for x in box.xyxy[0].tolist()],
                "label": r.names[int(box.cls.item())],
                "confidence": float(box.conf.item())
            })

    if os.path.exists(temp_file):
        os.remove(temp_file)
    return {"status": "success", "results": predictions}


# --- 3. 接口：用户纠正反馈 ---
@app.post("/feedback")
async def save_feedback(file: UploadFile = File(...), correct_label: str = Form(...)):
    feedback_dir = "feedback_data"
    os.makedirs(feedback_dir, exist_ok=True)

    timestamp = int(time.time())
    file_ext = os.path.splitext(file.filename)[1]
    image_name = f"{timestamp}_{correct_label}{file_ext}"

    with open(os.path.join(feedback_dir, image_name), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(os.path.join(feedback_dir, f"{timestamp}_{correct_label}.txt"), "w", encoding="utf-8") as f:
        f.write(f"User Correction: {correct_label}")

    return {"status": "success"}


# --- 4. 静态文件与首页 (放在最后防止路由冲突) ---
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("web_v2.html", "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)