import json
import base64
import io

import numpy as np
from PIL import Image
from quantumblur import quantum_blur

def handler(event, context):
    # CORS preflight
    if event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin":  "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            }
        }

    body = json.loads(event.get("body", "{}"))
    img_b64 = body.get("image", "").split(",", 1)[-1]
    try:
        img_data = base64.b64decode(img_b64)
    except Exception:
        return { "statusCode": 400, "body": json.dumps({"error": "Invalid base64"}) }

    # Decode, blur, re-encode
    img = Image.open(io.BytesIO(img_data)).convert("RGB")
    arr = np.array(img)
    blurred_arr = quantum_blur(arr)
    out_img = Image.fromarray(blurred_arr, mode="RGB")

    buf = io.BytesIO()
    out_img.save(buf, format="PNG")
    out_b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type":              "application/json",
            "Access-Control-Allow-Origin":  "*",
        },
        "body": json.dumps({
            "image": f"data:image/png;base64,{out_b64}"
        })
    }
