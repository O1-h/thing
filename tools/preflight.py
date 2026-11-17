"""Host checks for the local Frontier Scaler Cluster; Go builds inside Docker."""
import importlib
import subprocess
import sys

failed = []
if sys.version_info < (3, 12):
    failed.append("Python 3.12+")
for tool, args in [
    ("docker", ["info"]),
    ("kubectl", ["version", "--client"]),
    ("kind", ["version"]),
]:
    try:
        subprocess.run([tool, *args], check=True, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=20)
    except Exception:
        failed.append(tool)
for module in ["PIL", "functions_framework", "yaml"]:
    try:
        importlib.import_module(module)
    except ImportError:
        failed.append(module)
if failed:
    print("Missing or unavailable: " + ", ".join(failed))
else:
    print("HOST_PREFLIGHT_OK")
print("Go compiles inside Docker. Check cluster context/readiness separately; add metrics-server during the HPA milestone.")
if failed:
    sys.exit(1)
sys.exit(0)
