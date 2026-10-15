# GOD'S EYE — Vision Intelligence

A futuristic Streamlit computer-vision demo for a CBSE Class 10 AI project. Created by Zakhwan Padikkal · 10 R.

## Features
- Animated intro and modern dark glass interface with cyan/violet accents.
- YOLOv8 model profiles: nano (fast), small (balanced), medium (more detail).
- Image and sampled-video object detection.
- People-focused mode, confidence threshold, and adjustable inference resolution.
- Detection counts, charts, and crowd-scene fine-tuning guide.
- Uses OpenCV headless to avoid common server-side GUI-library issues.

## Run locally (Windows PowerShell)

```powershell
cd path\to\gods_eye_ai
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open `http://localhost:8501`. The first run may download the selected YOLO weights; use a model size appropriate for your hardware.

## Streamlit Community Cloud
- Main file: `app.py`
- Keep `requirements.txt` and `packages.txt` in the repository root.
- `packages.txt` includes `libgl1`; `opencv-python-headless` is used in requirements.

## Improving detection in crowded crosswalks
The pretrained COCO model already has a generic `person` class, but is not specifically trained for Shibuya Crossing. Select `YOLOv8s` or `YOLOv8m` and set inference resolution to 960 or 1280 for a stronger starting point. This can improve small-person detection but is slower and does not guarantee every person will be detected.

Actual fine-tuning requires a representative, permissioned dataset with bounding boxes for visible people. Label with CVAT or Label Studio, then arrange:

```text
shibuya_people_dataset/
  images/train/
  images/val/
  images/test/      # optional
  labels/train/
  labels/val/
  labels/test/      # optional
```

Copy `shibuya_people.yaml.example` to `shibuya_people.yaml` and update paths. Then train on a GPU:

```bash
yolo detect train model=yolov8s.pt data=shibuya_people.yaml epochs=50 imgsz=960 batch=8
```

Review validation precision, recall, and mAP before using the resulting checkpoint. Do not train on random frames without labels and expect improvements; crowded scenes have occlusion and small-object limitations. Counts in the video tab are detections per sampled frame, not unique people. This project does not identify people or track them across cameras.

## Ethical use
Only analyse footage you own or have permission to use, follow applicable privacy rules, and keep a human in the loop for any consequential decisions.
