"""Integration check through the real Functions Framework HTTP endpoint and filesystem."""

import io
import json
import tempfile
import time
import urllib.request
import urllib.error
from pathlib import Path
from urllib.parse import quote_plus
from PIL import Image
from storage import client

store = client()
key = "uploads/check-" + str(time.time_ns()) + ".png"
stream = io.BytesIO()
Image.new("RGB", (500, 400), (50, 80, 140)).save(stream, format="PNG")
store.put_object(Bucket="frontier-media", Key=key, Body=stream.getvalue())


def invoke(key):
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "frontier-media"},
                    "object": {"key": quote_plus(key)},
                }
            }
        ]
    }
    request = urllib.request.Request(
        "http://127.0.0.1:8082",
        data=json.dumps(event).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


code, body = invoke(key)
assert code == 200 and body["token"] == "SCALE_OK"
target = store.path("frontier-media", body["key"])
first = target.read_bytes()
result = Image.open(io.BytesIO(first))
assert max(result.size) <= 128
code, again = invoke(key)
assert code == 200 and again["key"] == body["key"] and target.read_bytes() == first
bad = "uploads/invalid-" + str(time.time_ns()) + ".txt"
store.put_object(Bucket="frontier-media", Key=bad, Body=b"invalid image")
code, error = invoke(bad)
assert (
    code == 422
    and not store.path("frontier-media", "thumbnails/" + bad + ".png").exists()
)
record = {
    "source_key": key,
    "output_key": body["key"],
    "dimensions": list(result.size),
    "http_handler": "PASSED",
    "duplicate_delivery": "PASSED",
    "invalid_image": "PASSED",
    "token": "SCALE_OK",
    "scope": "Local HTTP function runtime and supplied filesystem event adapter; not managed cloud autoscaling or S3 notification verification",
}
(Path(__file__).parent / "local-function.json").write_text(json.dumps(record, indent=2))
print(json.dumps(record, indent=2))
