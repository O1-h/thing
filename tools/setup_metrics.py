"""Install pinned metrics-server only into the explicitly named local kind context."""

import json
import subprocess
import tempfile
import urllib.request
from pathlib import Path
import yaml

context = subprocess.check_output(
    ["kubectl", "config", "current-context"], text=True
).strip()
if not context.startswith("kind-"):
    raise SystemExit("Select your owned local kind context before running this helper.")
print("Target local context: " + context)
url = "https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.9.1/components.yaml"
documents = list(yaml.safe_load_all(urllib.request.urlopen(url).read()))
for document in documents:
    if document and document["kind"] == "Deployment":
        document["spec"]["template"]["spec"]["containers"][0]["args"].append(
            "--kubelet-insecure-tls"
        )
with tempfile.TemporaryDirectory(prefix="cs411-metrics-") as temp_dir:
    manifest_path = Path(temp_dir) / "metrics.yaml"
    manifest_path.write_text(yaml.safe_dump_all(documents, sort_keys=False))
    # The relative filename avoids kubectl splitting a Windows path that contains commas.
    subprocess.run(
        ["kubectl", "--context", context, "apply", "-f", "metrics.yaml"],
        cwd=temp_dir,
        check=True,
    )
subprocess.run(
    [
        "kubectl",
        "--context",
        context,
        "-n",
        "kube-system",
        "rollout",
        "status",
        "deployment/metrics-server",
        "--timeout=150s",
    ],
    check=True,
)
print(
    "The kubelet TLS exception is limited to this local teaching cluster. Confirm kubectl top pods -n frontier-studio."
)
