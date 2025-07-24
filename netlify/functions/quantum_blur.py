import json, base64, io
import numpy as np
import cv2
from PIL import Image

# replace this with your real algorithm!
def quantum_blur(img: np.ndarray) -> np.ndarray:
    return cv2.GaussianBlur(img, (31, 31), 0)

def handler(event, context):
    # handle CORS preflight
    if event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "https://qatalive.art",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        }

    body = json.loads(event["body"] or "{}")
    img_b64 = body.get("image", "").split(",", 1)[-1]
    img_data = base64.b64decode(img_b64)

    # load into OpenCV via NumPy
    arr = np.frombuffer(img_data, dtype=np.uint8)
    img  = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)

    # run your blur
    out  = quantum_blur(img)

    # re‑encode as PNG→base64
    _, buf     = cv2.imencode('.png', out)
    out_b64str = base64.b64encode(buf).decode('utf-8')
    payload    = {"image": f"data:image/png;base64,{out_b64str}"}

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://qatalive.art",
        },
        "body": json.dumps(payload)
    }
