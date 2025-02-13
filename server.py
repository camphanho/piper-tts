import os
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", "vi/model2.onnx")
CONFIG_PATH = os.getenv("CONFIG_PATH", "vi/config2.json")
PORT = int(os.getenv("PORT", 5000))

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return {"error": "No text provided"}, 400

    output_path = "output.wav"

    # Gọi Piper đúng cách
    try:
        with open(output_path, "wb") as out_wav:
            process = subprocess.run(
                ["piper", "--model", MODEL_PATH, "--config", CONFIG_PATH, "--output_file", output_path],
                input=text.encode("utf-8"),
                stdout=out_wav,
                stderr=subprocess.PIPE,
                check=True
            )
    except subprocess.CalledProcessError as e:
        return {"error": "Piper failed", "details": e.stderr.decode()}, 500

    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

