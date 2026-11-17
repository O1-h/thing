# Project 3 Scaler Cluster
CS411 Fall 2026, Systems Projects
Project 3 and Cloud Phase Gate due Wednesday December 2 at 11:59 PM Central
Project refinement Thursday December 3, final verification Friday December 4 at 11:59 PM Central

Build one continuing Frontier Scaler Cluster project, starting with the container and recovery milestone on November 12. Deploy the supplied gateway and worker in your local Kubernetes cluster. Show how the system handles load, rate limits and one worker failure. Keep `recover/` and `images/` in the same repository, with a diagram explaining their roles. The image function can run independently; connecting it to the gateway is optional. Allow about 5–7 hours, including class time and reuse of your earlier work.

## Build the system
1. Package both services. Use minimal multi-stage Dockerfiles for `gateway/` and `worker/`, applying Lab 10's cache ordering. The starter Dockerfiles work as a baseline. Inspect and explain what they contain, then adapt them as needed. Build images named `frontier-gateway:studio` and `frontier-worker:studio` and load both into the course kind cluster.
2. Connect them. Complete the files in `k8s/`. Match Deployment labels and Service selectors so the gateway reaches the worker at `worker-service/work`. The supplied NodePort exposes the gateway at `http://localhost:18081/work`. No ingress controller is required.
3. Add health and resources. Set readiness/liveness probes and CPU/memory requests and limits for both services. Explain your choices using startup and light-load observations. Requests affect scheduling and HPA CPU percentages; limits bound use. Get healthy Pods and a successful request before adding load.
4. Set up scaling. Use an `autoscaling/v2` HorizontalPodAutoscaler targeting `worker-deployment`. Choose minimum and maximum replicas and a positive CPU-utilization target. Keep the maximum at ten or fewer workers and within your computer's capacity. Explain the values using measurements. Install metrics-server with the supplied helper in your local kind context. `kubectl top pods -n frontier-studio` must work before you interpret HPA percentages. Note the helper's local certificate exception in your README.

Use these checks from the repository root:
```sh
python tools/check_manifests.py cluster
kubectl -n frontier-studio apply -f k8s/
kubectl -n frontier-studio get hpa -w
```
Wait for both deployments to finish rolling out and request `/work`. The README must include your exact build, image-load, apply, wait and request commands.

## Test load and recovery
Use the supplied `tools/load.py`, hey or k6 for a bounded load test. Record baseline, load, scale-up and eventual scale-down with timestamps. Record both desired replicas and Ready Pods: they change at different times. Capture the full scale-down window before the project submission; default stabilization can take several minutes.

---PAGE---
Test rate limiting separately. Count accepted HTTP 200, limited HTTP 429 and unexpected failures. The supplied limiter is per client IP, per gateway process. It does not share a quota between replicas, and a proxy can combine client addresses. Do not trust arbitrary forwarded headers. Send enough accepted work to raise worker CPU. Explain what happens to a legitimate client as well as an excessive one; rejections alone do not show scaling.

Use the Milestone 1 method to replace one worker Pod while the Service is available. Record its identities, recovery and subsequent readiness. Keep failed requests and CrashLoopBackOff observations, diagnose them, repair the setup and repeat. Report resources, replica counts, throughput and errors. Explain what the run establishes. One Pod replacement does not establish node-failure tolerance.

## Grading
- Manifests and Service networking, 20%: selectors, routing and useful probes.
- Autoscaling, 30%: working metrics, justified settings, observed scale-up and scale-down.
- Recovery and rate limiting, 20%: controlled replacement, useful admission limit and continuing legitimate traffic.
- Load evidence, 15%: timestamps, desired/Ready counts, accepted/limited/failed requests and a comparable baseline.
- Documentation and code quality, 15%: reproduction commands, architecture, reasons for settings and an evidence index.

These are the existing Project 3 weights. The earlier labs keep their own grades. The Cloud Phase Gate is part of these project criteria, not another project or exam.

## What to submit
In Blackboard, submit your own repository URL and exact project commit SHA. Include:
- Gateway/worker source and Dockerfiles, plus all Kubernetes manifests.
- An architecture diagram and an index linking the earlier lab evidence.
- A README with clean deployment/load commands and reasons for the settings.
- Selected results: baseline/load/limiter counts, timestamped HPA and Ready-Pod observations, full scale-up/scale-down output and the recovery trace.

Keep the `recover/` and `images/` source. A fresh cluster must be reproducible from the README without hidden GUI steps. Leave out credentials, kubeconfig, binaries, build caches and instructor files. Submit raw results, not a token or an assumed outcome.

## Dates
November 24: integration, metrics and load testing. No class November 26. December 1: clean reproduction practice and an individual run/explanation check. Each student must run the deployment, explain a load or failure observation, identify a health signal and defend one setting.

Project 3 and that Cloud Phase Gate are due December 2 at 11:59 PM Central. December 3 is project testing and refinement. Submit fresh verification and feedback revisions December 4 at 11:59 PM Central. December 4 does not extend the project deadline or add a separate grade. The project is the final assessment. There is no final exam or showcase.

## References
https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
https://github.com/kubernetes-sigs/metrics-server
