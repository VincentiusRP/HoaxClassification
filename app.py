from flask import Flask, render_template, request, jsonify
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, BertTokenizer
import os
import gdown
import zipfile

app = Flask(__name__)

MAX_LEN = 64
LABELS = {0: "Non-Hoax (Valid)", 1: "Hoax"}

FILE_ID = "1kjney3SOWxFzgpCQWs4Nec1Foks0XBID"
ZIP_PATH = "model.zip"
MODEL_DIR = "model"

def download_model():
    if not os.path.exists(MODEL_DIR) or not os.listdir(MODEL_DIR):
        os.makedirs(MODEL_DIR, exist_ok=True)

        url = f"https://drive.google.com/uc?id={FILE_ID}"
        gdown.download(url, ZIP_PATH, quiet=False)

        with zipfile.ZipFile(ZIP_PATH, 'r') as z:
            z.extractall(MODEL_DIR)

        os.remove(ZIP_PATH)

def get_model_path():
    if os.path.exists(os.path.join(MODEL_DIR, "config.json")):
        return MODEL_DIR
    for root, dirs, files in os.walk(MODEL_DIR):
        if "config.json" in files:
            return root
    raise FileNotFoundError("config.json tidak ditemukan di dalam model dir")


download_model()
MODEL_PATH = get_model_path()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained(MODEL_PATH, use_fast=False, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, local_files_only=True)
model.to(device)
model.eval()

def predict(text):
    encoding = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=MAX_LEN,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**encoding)
        probs = torch.softmax(outputs.logits, dim=1)[0]
        pred_id = int(torch.argmax(probs).item())

    return {
        "label": LABELS[pred_id],
        "label_id": pred_id,
        "confidence": round(float(probs[pred_id]) * 100, 2),
        "probabilities": {
            "Non-Hoax (Valid)": round(float(probs[0]) * 100, 2),
            "Hoax": round(float(probs[1]) * 100, 2)
        }
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict_route():
    data = request.get_json()
    title = data.get("title", "").strip()

    if not title:
        return jsonify({"error": "Judul artikel tidak boleh kosong"}), 400

    result = predict(title)
    return jsonify(result)
#a
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)