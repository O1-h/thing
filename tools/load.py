"""Send a short load test and count successful, limited and failed requests."""

import argparse
import concurrent.futures
import time
import json
import urllib.request
import urllib.error

parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("--seconds", type=int, default=30)
parser.add_argument("--clients", type=int, default=4)
parser.add_argument("--interval", type=float, default=0.2)
options = parser.parse_args()
assert options.url.startswith(
    ("http://127.0.0.1:", "http://localhost:")
), "Use your local lab gateway"
assert (
    1 <= options.seconds <= 180 and 1 <= options.clients <= 50 and options.interval >= 0
)
end_time = time.monotonic() + options.seconds


def worker(_):
    counts = {"accepted": 0, "limited": 0, "failed": 0}
    while time.monotonic() < end_time:
        try:
            with urllib.request.urlopen(options.url, timeout=10) as response:
                status_code = response.status
        except urllib.error.HTTPError as error:
            status_code = error.code
        except OSError:
            status_code = 0
        counts[
            (
                "accepted"
                if status_code == 200
                else "limited" if status_code == 429 else "failed"
            )
        ] += 1
        time.sleep(options.interval)
    return counts


with concurrent.futures.ThreadPoolExecutor(max_workers=options.clients) as pool:
    results = list(pool.map(worker, range(options.clients)))
print(
    json.dumps(
        {
            "seconds": options.seconds,
            "clients": options.clients,
            "interval": options.interval,
            **{
                category: sum(result[category] for result in results)
                for category in results[0]
            },
        },
        indent=2,
    )
)
