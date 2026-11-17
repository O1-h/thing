"""Delete one lab Pod and record its replacement while sampling requests."""

import argparse
import csv
import datetime
import json
import subprocess
import threading
import time
import urllib.request
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--inject", action="store_true")
parser.add_argument("--url")
parser.add_argument("--app", choices=["api-service", "worker"], default="api-service")
options = parser.parse_args()
options.url = options.url or (
    "http://127.0.0.1:18080/healthz"
    if options.app == "api-service"
    else "http://127.0.0.1:18081/work"
)
expected_replicas = 3 if options.app == "api-service" else 2
deployment = "api-deployment" if options.app == "api-service" else "worker-deployment"
assert options.inject, "Pass --inject to authorize deleting one Pod in frontier-studio"
assert options.url.startswith(("http://127.0.0.1:", "http://localhost:"))


def kubectl(*args):
    return subprocess.run(
        ["kubectl", "-n", "frontier-studio", *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def get(*args):
    return json.loads(kubectl("get", *args, "-o", "json"))


def is_ready(pod):
    # A running container is not necessarily ready for Service traffic.
    conditions = pod["status"].get("conditions", [])
    for condition in conditions:
        if condition["type"] == "Ready":
            return condition["status"] == "True"
    return False


def has_replica_set_owner(pod):
    owners = pod["metadata"].get("ownerReferences", [])
    for owner in owners:
        if owner["kind"] == "ReplicaSet":
            return True
    return False


# 1. Check the starting Pods before changing anything.
before = get("pods", "-l", "app=" + options.app)["items"]
assert len(before) == expected_replicas, "Start with the expected Pod count"
for pod in before:
    assert is_ready(pod), "Start with every Pod Ready"
    assert has_replica_set_owner(pod), "Each Pod must belong to a ReplicaSet"
original_uids = {pod["metadata"]["uid"] for pod in before}
deleted_pod = before[0]["metadata"]["name"]
samples = []
stop = threading.Event()



# 2. Sample HTTP requests while the main thread watches the Pods.
def sample():
    while not stop.is_set():
        stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            with urllib.request.urlopen(options.url, timeout=2) as response:
                ok = response.status == 200
        except OSError:
            ok = False
        samples.append([stamp, ok])
        stop.wait(0.2)



# 3. Delete one Pod and wait up to 30 seconds for its replacement.
thread = threading.Thread(target=sample)
thread.start()
time.sleep(1)
start = time.monotonic()
try:
    kubectl("delete", "pod", deleted_pod, "--wait=false")
    recovered = False
    after = []
    while time.monotonic() - start < 30:
        after = get("pods", "-l", "app=" + options.app)["items"]
        active = [pod for pod in after if not pod["metadata"].get("deletionTimestamp")]
        # Check the count, identity and readiness separately.
        correct_count = len(active) == expected_replicas
        current_uids = {pod["metadata"]["uid"] for pod in active}
        identity_changed = current_uids != original_uids
        all_ready = all(is_ready(pod) for pod in active)
        if correct_count and identity_changed and all_ready:
            recovered = True
            break
        time.sleep(0.5)
    elapsed = time.monotonic() - start
    time.sleep(1)
finally:
    stop.set()
    thread.join()

# 4. Save the observed results, including failures.
events = get("events")["items"]
created = [
    e
    for e in events
    if e.get("reason") == "SuccessfulCreate"
    and e.get("involvedObject", {}).get("kind") == "ReplicaSet"
    and deployment in e.get("involvedObject", {}).get("name", "")
]
failed = sum(not row[1] for row in samples)
record = {
    "app": options.app,
    "expected_replicas": expected_replicas,
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "deleted_pod": deleted_pod,
    "before_uids": sorted(original_uids),
    "after_uids": [
        pod["metadata"]["uid"]
        for pod in after
        if not pod["metadata"].get("deletionTimestamp")
    ],
    "recovery_seconds": round(elapsed, 2),
    "recovered_within_30s": recovered,
    "requests": len(samples),
    "failed_requests": failed,
    "replicaset_creation_event_seen": bool(created),
    "event_note": "Events corroborate ownership; API timestamps and UIDs establish this replacement.",
    "token": "SELF_HEALED" if recovered and failed == 0 and created else None,
    "scope": "One targeted Pod deletion and sampled traffic; not node-failure proof or a universal zero-downtime guarantee.",
}
out = Path(__file__).resolve().parents[1] / "evidence"
out.mkdir(exist_ok=True)
(out / "recovery.json").write_text(json.dumps(record, indent=2))
with (out / "requests.csv").open("w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["utc", "http_200"])
    writer.writerows(samples)
print(json.dumps(record, indent=2))
raise SystemExit(0 if record["token"] else 1)
