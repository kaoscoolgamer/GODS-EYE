import os, tempfile
from pathlib import Path
import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="GOD'S EYE | Surveillance Analytics", page_icon="👁", layout="wide")

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
.stApp { background: radial-gradient(ellipse at 50% 0%, #151923 0%, #080b10 52%, #05070a 100%); color:#e9edf4; }
html, body, [class*="css"] { font-family: Inter, sans-serif; }
h1,h2,h3 { font-family:'Barlow Condensed',sans-serif !important; letter-spacing:1px; }
h1 { color:#f1f3f8; font-size:2.8rem !important; }
h2,h3 { color:#f4f5fa !important; }
[data-testid="stMetric"] { background:#0d121a; border:1px solid #34313a; border-radius:8px; padding:12px; }
[data-testid="stSidebar"] { background:#080b10; border-right:1px solid #4b171b; }
.stButton>button { background:#8d171f; color:white; border:1px solid #e13a45; border-radius:5px; }
.stButton>button:hover { background:#ad202a; color:white; border-color:#ff515c; }
div[data-testid="stFileUploader"] { background:#0d121a; border:1px dashed #6b3035; border-radius:8px; padding:10px; }
div[data-testid="stDataFrame"] { border:1px solid #34313a; }
hr { border-color:#4b171b; }
.smallcaps { color:#ff535d; text-transform:uppercase; letter-spacing:2px; font-size:11px; }
.panel { background:#0b1017; border:1px solid #4a2429; border-radius:8px; padding:15px; }
.muted { color:#a9b1c0; }
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent
CREST = ROOT / "assets" / "school_crest.png"

def branding():
    left, right = st.columns([1, 7])
    with left:
        if CREST.exists():
            st.image(str(CREST), width=95)
        else:
            st.markdown("## 👁")
    with right:
        st.markdown("<div class='smallcaps'>The Indian High School Dubai</div>", unsafe_allow_html=True)
        st.title("GOD'S EYE")
        st.markdown("**SURVEILLANCE ANALYTICS SYSTEM**")
        st.markdown("<span class='smallcaps'>Created by Zakhwan Padikkal · 10 R</span>", unsafe_allow_html=True)
    st.divider()

branding()

with st.sidebar:
    if CREST.exists():
        st.image(str(CREST), width=125)
    st.markdown("### GOD'S EYE")
    st.caption("Surveillance Analytics System")
    st.markdown("**Created by Zakhwan Padikkal**")
    st.markdown("**Class: 10 R**")
    page = st.radio("NAVIGATION", ["Dashboard", "Image Scan", "Video Scan", "Camera Detector Guide", "About & Credits"])
    st.divider()
    st.markdown("<span class='smallcaps'>Knowledge is Power</span>", unsafe_allow_html=True)
    st.caption("AI Week project • Local demo")

def get_model(weights):
    from ultralytics import YOLO
    return YOLO(weights)

def detect(model, image, confidence):
    result = model.predict(source=image, conf=confidence, verbose=False)[0]
    plotted = result.plot()[:, :, ::-1]
    items = []
    if result.boxes is not None:
        for box in result.boxes:
            cls = int(box.cls[0].item())
            score = float(box.conf[0].item())
            coords = [round(float(x), 1) for x in box.xyxy[0].tolist()]
            items.append({"Object": result.names.get(cls, str(cls)),
                          "Confidence": f"{score:.1%}",
                          "Bounding box": str(coords)})
    return plotted, items

if page == "Dashboard":
    st.markdown("### SYSTEM OVERVIEW")
    st.caption("Local demonstration interface — upload authorized footage to run detections.")
    a,b,c,d = st.columns(4)
    a.metric("SYSTEM", "READY")
    b.metric("ANALYSIS MODE", "UPLOAD")
    c.metric("MODEL", "YOLOv8")
    d.metric("NETWORK ACCESS", "OFF")
    st.markdown("### MODULES")
    cols = st.columns(3)
    modules = [
        ("01 / IMAGE SCAN", "Detects common objects in a still image."),
        ("02 / VIDEO SCAN", "Samples frames from a short uploaded video."),
        ("03 / CAMERA DETECTOR", "Guide to training a custom camera-object model.")
    ]
    for col, (title, desc) in zip(cols, modules):
        with col:
            st.markdown(f"<div class='panel'><div class='smallcaps'>{title}</div><p>{desc}</p></div>", unsafe_allow_html=True)
    st.info("The default model detects common objects. It does not have a dedicated security-camera class until you train a custom model.")
    st.markdown("### PROJECT CREDITS")
    st.markdown("**Created by Zakhwan Padikkal · Class 10 R**")
    st.caption("The Indian High School Dubai • “Knowledge is Power”")

elif page == "Image Scan":
    st.markdown("### IMAGE ANALYSIS")
    st.caption("Upload a photo you own or have permission to analyze.")
    weights = st.text_input("Model weights", "yolov8n.pt")
    confidence = st.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
    file = st.file_uploader("Choose image", type=["jpg","jpeg","png"])
    if file and st.button("ANALYZE IMAGE"):
        try:
            model = get_model(weights)
            image = Image.open(file).convert("RGB")
            annotated, rows = detect(model, np.array(image), confidence)
            x,y = st.columns([1.5,1])
            with x: st.image(annotated, caption="Detection overlay", use_container_width=True)
            with y:
                st.metric("OBJECTS DETECTED", len(rows))
                if rows: st.dataframe(rows, use_container_width=True, hide_index=True)
                else: st.warning("No objects detected above the selected threshold.")
        except Exception as e:
            st.error(f"Could not run detection: {e}")
            st.caption("Install requirements and check the model path. First use may download model weights.")

elif page == "Video Scan":
    st.markdown("### VIDEO ANALYSIS")
    st.caption("Scans selected frames from an uploaded clip; it does not connect to camera networks.")
    weights = st.text_input("Model weights", "yolov8n.pt")
    confidence = st.slider("Detection confidence", 0.10, 0.90, 0.35, 0.05)
    file = st.file_uploader("Choose video", type=["mp4","mov","avi"])
    if file and st.button("ANALYZE VIDEO"):
        temp_path = None
        try:
            import cv2
            model = get_model(weights)
            suffix = Path(file.name).suffix or ".mp4"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(file.getbuffer()); temp_path = tmp.name
            cap = cv2.VideoCapture(temp_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 24
            total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
            stride = max(1, int(fps * 2))
            frames, counts = [], {}
            progress = st.progress(0)
            i = 0
            while cap.isOpened():
                ok, frame = cap.read()
                if not ok: break
                if i % stride == 0:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    result = model.predict(source=rgb, conf=confidence, verbose=False)[0]
                    frames.append(result.plot()[:, :, ::-1])
                    if result.boxes is not None:
                        for box in result.boxes:
                            label = result.names.get(int(box.cls[0].item()), "unknown")
                            counts[label] = counts.get(label, 0) + 1
                i += 1
                if i % 25 == 0: progress.progress(min(1.0, i/total))
            cap.release()
            progress.progress(1.0)
            if frames:
                st.image(frames[:8], caption=[f"Sample {n+1}" for n in range(min(8,len(frames)))], width=320)
            st.markdown("### DETECTION COUNTS")
            if counts: st.bar_chart(counts)
            else: st.info("No detections found in sampled frames.")
        except Exception as e:
            st.error(f"Could not analyze video: {e}")
        finally:
            if temp_path and os.path.exists(temp_path): os.unlink(temp_path)

elif page == "Camera Detector Guide":
    st.markdown("### CUSTOM CAMERA-OBJECT DETECTOR")
    st.warning("The default model does not recognize security cameras as a dedicated category. Train a custom model using labeled images.")
    st.markdown("""
1. Gather images of visible cameras from sources you are allowed to use.
2. Draw bounding boxes around cameras using CVAT or Label Studio.
3. Export annotations in YOLO detection format.
4. Create a dataset with `images/train`, `images/val`, `labels/train`, and `labels/val`.
5. Edit `camera_dataset.yaml` to point to that dataset.
6. Run the training command below.
""")
    st.code("yolo detect train model=yolov8n.pt data=camera_dataset.yaml epochs=30 imgsz=640", language="bash")
    st.markdown("Then set the model weights field in Image Scan or Video Scan to `runs/detect/train/weights/best.pt`.")
    st.caption("This identifies visible camera-shaped objects in authorized footage. It does not locate hidden devices or access private camera systems.")

else:
    st.markdown("### ABOUT THIS PROJECT")
    st.markdown("**GOD'S EYE — Surveillance Analytics System**")
    st.markdown("Created by **Zakhwan Padikkal · 10 R**")
    st.markdown("The Indian High School Dubai")
    st.markdown("“Knowledge is Power”")
    st.divider()
    st.markdown("#### TECH STACK")
    st.markdown("- Python\n- Streamlit dashboard\n- Ultralytics YOLO object detection\n- OpenCV video frame processing")
    st.markdown("#### LIMITATIONS")
    st.markdown("This is a student demonstration, not a real surveillance network. It processes uploaded files only and does not identify or track people.")
