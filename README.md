# GOD'S EYE — Surveillance Analytics System
**Created by Zakhwan Padikkal · Class 10 R**  
The Indian High School Dubai • “Knowledge is Power”

## Run on Windows
1. Install Python 3.11 or 3.12 from https://www.python.org/downloads/. Tick **Add Python to PATH**.
2. Extract this ZIP.
3. Open Command Prompt in the extracted `Gods_Eye_AI_Project` folder.
4. Run:

```bat
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser. First use may need internet to download the YOLO model weights.

## Features
- Dark red/charcoal school-branded dashboard
- Image object detection
- Short video frame analysis
- Training guide for a custom security-camera object detector
- Project credits across the interface

## Train a custom camera detector
The default YOLO model detects common object classes; it does **not** include security camera as a dedicated class. Label authorized images in CVAT or Label Studio, export to YOLO format, and create:

```text
camera_dataset/
  images/train/
  images/val/
  labels/train/
  labels/val/
```

Copy `camera_dataset_example.yaml` to `camera_dataset.yaml` and adjust its path. Then run:

```bat
yolo detect train model=yolov8n.pt data=camera_dataset.yaml epochs=30 imgsz=640
```

Use `runs/detect/train/weights/best.pt` as the weights path in the app.

## Responsible-use note
Use only footage you own or have permission to analyze. This project analyzes uploaded files; it does not connect to private camera networks, identify people, or track them across cameras.
