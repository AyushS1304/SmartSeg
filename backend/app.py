from flask import Flask, request, jsonify, send_from_directory
import torch
from ultralytics import YOLO
from PIL import Image
import pathlib
import os
import pandas as pd
import time
from flask_cors import CORS
from google import genai
import base64
import json
import cv2
import re
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore")
os.environ["GEMINI_API_KEY"] = os.getenv("Gemini_API_key")

# -----------------------------
# 1) Gemini Setup
# -----------------------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# 2) Windows Compatibility
# -----------------------------
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# -----------------------------
# 3) Flask Initialization
# -----------------------------
app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# -----------------------------
# 4) Load Models
# -----------------------------
YOLOV8_MODEL_PATH = r"C:\Users\Ayush Sharma\OneDrive\Desktop\SmartSeg\backend\model\best_e.pt"
model_ewaste = YOLO(YOLOV8_MODEL_PATH)

YOLOV5_MODEL_DIR = r"C:\Users\Ayush Sharma\OneDrive\Documents\yolov5"
YOLOV5_MODEL_PATH = r"C:\Users\Ayush Sharma\OneDrive\Desktop\SmartSeg\backend\model\best.pt"
model_waste = torch.hub.load(YOLOV5_MODEL_DIR, 'custom', source='local',
                             path=YOLOV5_MODEL_PATH, force_reload=False)

# NEW → Mixed waste model (both e-waste + waste)
MIXED_MODEL_PATH = r"C:\Users\Ayush Sharma\OneDrive\Desktop\SmartSeg\backend\model\bestmix.pt"
model_mixed = YOLO(MIXED_MODEL_PATH)

print("Models loaded successfully.")

# -----------------------------
# 5) Gemini Waste Classification
# -----------------------------
def gemini_analyze_image(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()

    image_base64 = base64.b64encode(image_data).decode("utf-8")

    prompt = (
        "Analyze the image and RETURN STRICT JSON ONLY.\n"
        "NO Markdown. NO ``` blocks. NO text outside JSON.\n"
        "Format:\n"
        "{\n"
        "  \"is_waste\": true/false,\n"
        "  \"waste_type\": \"E-waste\", \"BioDegradable Waste\", \"Non-Biodegradable Waste\", \"Mixed Waste\", or \"Not Waste\",\n"
        "  \"description\": \"reason\",\n"
        "  \"disposal_advice\": \"advice\"\n"
        "}"
    )

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }
            ]
        )

        raw = response.text.strip()
        print("\n--- RAW GEMINI RESPONSE ---\n", raw, "\n---------------------------")

        # Extract first JSON block
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("No JSON found in Gemini response.")

        json_str = match.group(0).replace("'", "\"")
        return json.loads(json_str)

    except Exception as e:
        print("Gemini parsing error:", e)
        return {
            "is_waste": None,
            "waste_type": None,
            "description": f"Parsing error: {str(e)}",
            "disposal_advice": "N/A"
        }

# -----------------------------
# 6) Detection Route
# -----------------------------
@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save image
        uploaded_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(uploaded_image_path)

        # Gemini classification
        gemini_result = gemini_analyze_image(uploaded_image_path)
        waste_type = (gemini_result.get("waste_type") or "").lower()

        # If not waste
        if gemini_result.get("is_waste") is False:
            return jsonify({
                "gemini_result": gemini_result,
                "uploaded_image_url": f"http://127.0.0.1:5000/static/uploads/{file.filename}",
                "output_image_url": None,
                "message": "The object is not waste.",
                "detected_objects": [],
                "model_used": None,
                "final_advice": gemini_result.get("disposal_advice", "")
            })

        # MODEL SELECTION LOGIC (UPDATED)
        if "mixed" in waste_type or ("e-waste" in waste_type and "non-biodegradable" in waste_type):
            model = model_mixed
            model_type = "YOLOv8 (Mixed Waste)"
        elif "e-waste" in waste_type:
            model = model_ewaste
            model_type = "YOLOv8 (E-waste)"
        else:
            model = model_waste
            model_type = "YOLOv5 (Waste)"

        # Run model inference
        timestamp = int(time.time())
        output_filename = f"output_{timestamp}.jpg"
        output_image_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        detected_objects = []

        if "YOLOv8" in model_type:
            results = model.predict(uploaded_image_path, conf=0.25, iou=0.35)
            result_image = results[0].plot()
            result_image_bgr = cv2.cvtColor(result_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_image_path, result_image_bgr)

            boxes = results[0].boxes
            if boxes is not None and len(boxes) > 0:
                detected_objects = [model.names[int(c)] for c in boxes.cls.cpu().numpy().tolist()]

        else:
            img = Image.open(uploaded_image_path)
            if img.mode != "RGB":
                img = img.convert("RGB")
            results = model(img)
            result_img = Image.fromarray(results.render()[0])
            result_img.save(output_image_path)

            if len(results.xywh[0]) > 0:
                detected_objects = [model.names[int(cls)] for cls in results.xywh[0][:, -1].tolist()]

        # Response
        return jsonify({
            "gemini_result": gemini_result,
            "uploaded_image_url": f"http://127.0.0.1:5000/static/uploads/{file.filename}",
            "output_image_url": f"http://127.0.0.1:5000/static/output/{output_filename}",
            "detected_objects": detected_objects,
            "model_used": model_type,
            "final_advice": gemini_result.get("disposal_advice", "")
        })

    except Exception as e:
        print("Server error:", e)
        return jsonify({"error": str(e)}), 500



# -----------------------------
# Run Flask
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True)

