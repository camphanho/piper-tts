from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)

MODEL_PATH = "vi/model.onnx"  # Đường dẫn tới model Piper
CONFIG_PATH = "vi/config.json"  # Đường dẫn tới file cấu hình

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.json
    text = data.get("text", "")

    if not text:
        return {"error": "No text provided"}, 400

    output_path = "output.wav"
    
    # Chạy Piper TTS để tạo file âm thanh
    command = f'piper --model {MODEL_PATH} --config {CONFIG_PATH} --output_file {output_path} --text "{text}"'
    subprocess.run(command, shell=True)

    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

