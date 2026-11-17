# Frontier Scaler Cluster

We’ll build this project over the remaining weeks: run an API in Kubernetes, process image uploads, then add a gateway and workers that scale under load. Keep everything in one repository.

The project is our final assessment. There is no final exam or showcase.

## Getting started

Extract this ZIP and open `FrontierStudio` in VS Code. You should see `kind.yaml`, `recover/` and `requirements.txt` in the top-level folder. Use your own Git repository. If you already started, keep your work.

You need Git, Docker Desktop (Linux containers), kind, kubectl and Python 3.12. Start Docker Desktop, then run these commands in PowerShell from the project folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/preflight.py
.\.venv\Scripts\Activate.ps1
```

Wait for `HOST_PREFLIGHT_OK`. If activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python` in later commands. Go builds inside Docker. Installation help is in `docs/CS411 Student Setup Checklist.pdf`.

## Today

Follow the slides in order. We’ll pause together after setup, the container test, the cluster deployment and the saved commit.

1. Build and run the API in `recover/`. Check for `APP_READY`.
2. Deploy three Ready Pods in `frontier-studio` and test the Service.
3. Run `python tools/recovery.py --inject`. Read the JSON and CSV in `evidence/`. Copy them before another run overwrites them.
4. Add your working commands and results to this README, then commit your manifests and evidence. The evidence folder is ignored, so use `git add -f` for the required JSON/CSV. Keep credentials, kubeconfig and `.venv` out of Git.

The Milestone 1 handout in `docs/` lists the full submission. Keep failed results so you can explain what you fixed.

## What comes next

- **Nov 18:** Milestone 1 due .
- **Nov 17–19:** Add the image handler in `images/`. Lab 12 is due Nov 25.
- **Nov 24:** Add the gateway, workers and autoscaling. No class Nov 26.
- **Dec 2, 11:59 PM Central:** Project 3 and the individual Cloud Phase Gate are due.
- **Dec 3–4:** Test and refine the project. Fresh verification is due Dec 4 at 11:59 PM Central.

Keep `recover/` when you add the next part. See `docs/Project_3_Scaler_Cluster.pdf` for project requirements and grading.
