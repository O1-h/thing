"""Given local upload adapter. An upload writes a file and delivers its event over HTTP."""

import argparse
import json
import urllib.request
import urllib.error
from urllib.parse import quote_plus
from pathlib import Path
from storage import client

p = argparse.ArgumentParser()
p.add_argument("file")
p.add_argument("--key", default="uploads/sample.png")
p.add_argument("--url", default="http://127.0.0.1:8082")
a = p.parse_args()
assert a.url.startswith(("http://127.0.0.1:", "http://localhost:"))
assert a.key.startswith("uploads/"), "Only uploads/ emits source events"
data = Path(a.file).read_bytes()
assert len(data) <= 8 * 1024 * 1024, "Use a sample below 8 MiB"
client().put_object(Bucket="frontier-media", Key=a.key, Body=data)
event = {
    "Records": [
        {
            "s3": {
                "bucket": {"name": "frontier-media"},
                "object": {"key": quote_plus(a.key)},
            }
        }
    ]
}
request = urllib.request.Request(
    a.url, data=json.dumps(event).encode(), headers={"Content-Type": "application/json"}
)
try:
    with urllib.request.urlopen(request, timeout=15) as response:
        print(response.read().decode())
except urllib.error.HTTPError as error:
    print(
        json.dumps(
            {
                "http_status": error.code,
                "body": error.read().decode(),
                "delivery": "completed with non-success response; no automatic retry for invalid input",
            }
        )
    )
    raise SystemExit(1)
