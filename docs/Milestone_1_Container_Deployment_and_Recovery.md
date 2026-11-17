# Project Milestone 1: Container Deployment and Recovery
CS411 Fall 2026

100 points in Weekly Assessments, 50 for each part
Due Wednesday November 18 at 11:59 PM Central

Run three copies of the supplied app, delete one Pod and measure its replacement while requests continue. Work in `recover/` in your own repository. This gives you a recovery test to reuse in Project 3. Allow about 4–6 hours, including class time.

## Part B Build and check 50 points
Start at the repository root with Docker running in Linux-container mode. Use the supplied local cluster configuration.
1. Build the app. Create the cluster only if it does not already exist, then load the image:
```sh
docker build -t frontier-recover:studio recover
kind create cluster --name frontier-studio --config kind.yaml
kind load docker-image frontier-recover:studio --name frontier-studio
kubectl apply -f namespace.yaml
```
Reuse an existing course cluster after checking its context. Keep other clusters intact.
2. Finish `recover/deployment.yaml`: name `api-deployment`, three replicas, matching labels, `frontier-recover:studio`, `imagePullPolicy: IfNotPresent`, readiness/liveness probes on `/healthz` port 8080, and CPU/memory requests. The app waits six seconds before opening its port. Choose and explain probe timings that allow it to start. Keep `timeoutSeconds` inside the probe. In `recover/service.yaml`, keep `api-service`, matching selectors and `targetPort: 8080`.
3. Check, apply and wait:
```sh
python tools/check_manifests.py recover
kubectl -n frontier-studio apply -f recover/
kubectl -n frontier-studio rollout status deployment/api-deployment --timeout=120s
```
Wait until exactly three Pods are Ready and the old rollout Pods are gone. Then request `http://localhost:18080/healthz`. The app returns `APP_READY`. Use the supplied NodePort Service so a deleted Pod does not take a Pod-specific port-forward with it.
4. Run `python tools/recovery.py --inject`. It deletes one Pod and samples requests about every 200 ms. Check the deleted name, before/after UIDs, replacement owner/event, elapsed time, request count and failures. Regain three Ready Pods within 30 seconds with zero failed sampled requests. If a check fails, keep the failed run, explain it briefly, repair the setup and collect a fresh run.
5. Repeat the check independently. `SELF_HEALED` appears only when the verifier's measured checks pass. `APP_READY` by itself shows neither recovery nor uninterrupted traffic.

---PAGE---
## Part A Short questions 50 points
Submit `Milestone1_Questions.md` or PDF. Each question is worth 12.5 points. Use a trace table or about 3–6 sentences per answer.

1. Desired state. Start with three desired and three Ready Pods. Delete two. Trace the API observation, ReplicaSet controller, scheduler and kubelet. Which controller creates replacement Pods? If each replacement needs a hypothetical three-second pull and two-second start, what is the earliest plausible Ready time when they start concurrently? Which scheduling and probe delays can make it longer?
2. Health probes. The app opens its port after six seconds. A readiness probe checks `/healthz:8080` with `initialDelaySeconds=0`, `periodSeconds=5`, `failureThreshold=1`, `timeoutSeconds=1`. Trace checks near 0, 5 and 10 seconds. When can it receive traffic? Does failed readiness restart it? Why can the rollout still succeed? Propose and justify timings that allow startup.
3. Rolling update. With `replicas=4`, `maxUnavailable=1` and `maxSurge=1`, give a valid sequence of old/new Ready counts from 4/0 to 0/4. State the minimum available replicas and maximum Pods. Give your assumptions, including how terminating Pods can affect observed totals. The controller may interleave steps differently.
4. Node failure. How does losing a node differ from deleting a known Pod? Discuss detection, unreachable-node handling, capacity and scheduling. Why must the replacement have a suitable healthy node? Why does this case have no universal five-second or 30-second recovery guarantee?

## Grading and submission
Part B: Deployment/probes/resources 20 points; Service routing 10; repeatable deletion and recovery evidence 15; interpretation and repeatable commands 5. Part A is 50 points.

In Blackboard, submit your repository URL, exact commit SHA, `Milestone1_Questions.md` or PDF, `recover/deployment.yaml`, `recover/service.yaml`, `evidence/recovery.json` and `evidence/requests.csv`. Include the `SELF_HEALED` output when the check passes. Keep earlier lab work in the repository. Report failed attempts honestly. Leave out kubeconfig, credentials, binaries and instructor files.

Our class example traces desired=3 and observed=1 before you build this version. Your run tests one targeted Pod replacement with sampled requests. It does not establish node-failure tolerance or a general zero-downtime guarantee.

## References
https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/
https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
